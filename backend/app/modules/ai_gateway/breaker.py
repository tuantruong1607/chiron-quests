"""Per-provider circuit breaker, state kept in Redis under `cb:{provider}`.

Rules (spec §4.2): opens after 3 consecutive failures within a 60s window;
after 60s in the open state, exactly one half-open trial call is allowed -
if it succeeds the breaker closes, if it fails the breaker reopens (and its
cooldown restarts). Any failure recorded while the breaker is already open
(whether it's the half-open trial or a straggling concurrent call) keeps it
open rather than falling back through the streak-counting logic.

`record_result` is a single Lua script (read-decide-write in one round
trip), so concurrent callers recording results for the same provider can't
race each other into a lost update.
"""

import json
import time
import uuid
from collections.abc import Awaitable
from dataclasses import dataclass
from typing import cast

from app.core.redis import get_redis

FAILURE_THRESHOLD = 3
FAILURE_WINDOW_S = 60.0
OPEN_COOLDOWN_S = 60.0
_KEY_TTL_S = 600  # tidy up stale keys; well past any window this module cares about

#: Wall-clock source, reassigned by tests so breaker timing doesn't depend on
#: real sleeps.
now = time.time


@dataclass
class _State:
    state: str = "closed"  # "closed" | "open"
    fail_count: int = 0
    streak_start: float = 0.0
    opened_at: float = 0.0


def _key(provider: str) -> str:
    return f"cb:{provider}"


def _trial_key(provider: str) -> str:
    return f"cb:{provider}:trial"


async def _load(provider: str) -> _State:
    client = get_redis()
    raw = await client.get(_key(provider))
    if raw is None:
        return _State()
    return _State(**json.loads(raw))


async def try_claim(
    provider: str, ttl_s: float = OPEN_COOLDOWN_S
) -> tuple[bool, str | None]:
    """Decide whether a call to `provider` should be blocked right now, and
    if the breaker is open past its cooldown, atomically claim the single
    half-open trial slot for the caller.

    Returns `(blocked, token)`:
    - `(False, None)` - the breaker isn't open at all; proceed normally,
      there is no trial claim to release.
    - `(True, None)` - the breaker is open (either still within its
      cooldown, or another caller already holds the trial); this call must
      not proceed.
    - `(False, token)` - this call has just claimed the trial. It must
      either go on to call `record_result` for the attempt it's about to
      make (which always clears the trial, whatever `token` was), or, if it
      aborts before making that attempt, call `release_trial(provider,
      token)` itself - otherwise the claim sits blocking every other caller
      for the rest of `ttl_s`.

    `ttl_s` should exceed the caller's own timeout for the call it's about
    to make (e.g. the gateway's `TIMEOUT_S` plus a margin) - otherwise a
    trial call still in flight near that timeout could outlive its own
    claim and let a second trial start concurrently.
    """
    state = await _load(provider)
    if state.state != "open":
        return False, None
    if now() - state.opened_at < OPEN_COOLDOWN_S:
        return True, None
    token = str(uuid.uuid4())
    client = get_redis()
    claimed = await cast(
        "Awaitable[bool | None]",
        client.set(_trial_key(provider), token, nx=True, ex=int(ttl_s)),
    )
    if not claimed:
        return True, None
    return False, token


async def is_open(provider: str, *, trial_ttl_s: float = OPEN_COOLDOWN_S) -> bool:
    """True if a call to `provider` should be blocked right now.

    A thin wrapper over `try_claim` for callers that have no way to hold
    onto - and later release - a trial's token: **calling this function can
    itself claim the half-open trial** (see `try_claim`), and since the
    token is discarded here, that claim can then only be cleared by a
    matching `record_result`, never by `release_trial`. Callers that might
    abort before reaching `record_result` for their own attempt should call
    `try_claim` directly instead, so they can release what they claimed.
    """
    blocked, _token = await try_claim(provider, trial_ttl_s)
    return blocked


# KEYS: 1=trial key. ARGV: 1=token. Deletes only if the key still holds
# exactly this token - a lost race, a claim already consumed by
# `record_result`, or one released/claimed by someone else in the meantime
# all leave it alone.
_RELEASE_TRIAL_LUA = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
  return redis.call('DEL', KEYS[1])
end
return 0
"""


async def release_trial(provider: str, token: str) -> None:
    """Release `provider`'s half-open trial claim, but only if it's still
    exactly the one identified by `token` (compare-and-delete) - so this
    never deletes a *different* claim, e.g. one made by another worker
    after this one's own claim was already consumed by `record_result`, or
    a claim this call never actually held in the first place. Call this on
    any path that got a `token` back from `try_claim` but never reaches
    `record_result` for that same attempt - budget refused, an adapter
    lookup failure, or a cancellation."""
    client = get_redis()
    await cast(
        "Awaitable[int]",
        client.eval(_RELEASE_TRIAL_LUA, 1, _trial_key(provider), token),
    )


# KEYS: 1=state key, 2=trial key. ARGV: 1=success ("1"/"0"), 2=moment,
# 3=failure_threshold, 4=failure_window_s, 5=key_ttl_s.
#
# On success: always close (reset the streak entirely), whatever the prior
# state - this is what closes a half-open trial.
# On failure while already open: stay open and restart the cooldown - this
# covers both "the half-open trial itself failed" and "a straggling
# concurrent call failed while the breaker was already open".
# On failure while closed: standard consecutive-failures-within-a-window
# counting.
_RECORD_RESULT_LUA = """
local raw = redis.call('GET', KEYS[1])
local state, fail_count, streak_start
if raw then
  local data = cjson.decode(raw)
  state = data['state']
  fail_count = data['fail_count']
  streak_start = data['streak_start']
else
  state = 'closed'
  fail_count = 0
  streak_start = 0
end

local success = tonumber(ARGV[1])
local moment = tonumber(ARGV[2])
local threshold = tonumber(ARGV[3])
local window = tonumber(ARGV[4])
local ttl = tonumber(ARGV[5])

local new_state, new_fail_count, new_streak_start, new_opened_at

if success == 1 then
  new_state = 'closed'
  new_fail_count = 0
  new_streak_start = 0
  new_opened_at = 0
elseif state == 'open' then
  new_state = 'open'
  new_fail_count = fail_count
  new_streak_start = moment
  new_opened_at = moment
else
  if fail_count == 0 or (moment - streak_start) > window then
    new_fail_count = 1
    new_streak_start = moment
  else
    new_fail_count = fail_count + 1
    new_streak_start = streak_start
  end
  if new_fail_count >= threshold then
    new_state = 'open'
    new_opened_at = moment
  else
    new_state = 'closed'
    new_opened_at = 0
  end
end

local encoded = cjson.encode({
  state = new_state,
  fail_count = new_fail_count,
  streak_start = new_streak_start,
  opened_at = new_opened_at,
})
redis.call('SET', KEYS[1], encoded, 'EX', ttl)
redis.call('DEL', KEYS[2])
return encoded
"""


async def record_result(provider: str, *, success: bool) -> None:
    """Feed one call's outcome into `provider`'s breaker, atomically."""
    client = get_redis()
    await cast(
        "Awaitable[str]",
        client.eval(
            _RECORD_RESULT_LUA,
            2,
            _key(provider),
            _trial_key(provider),
            "1" if success else "0",
            str(now()),
            str(FAILURE_THRESHOLD),
            str(FAILURE_WINDOW_S),
            str(_KEY_TTL_S),
        ),
    )
