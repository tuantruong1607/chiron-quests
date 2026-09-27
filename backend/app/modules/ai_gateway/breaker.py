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


async def is_open(provider: str) -> bool:
    """True if a call to `provider` should be blocked right now.

    Once `OPEN_COOLDOWN_S` has passed since the breaker opened, exactly one
    caller is let through as a half-open trial: claiming the trial is an
    atomic `SET NX` on a short-lived Redis key, so every other concurrent
    caller still sees the breaker as open (this function keeps returning
    True for them) until the trial's outcome is recorded.
    """
    state = await _load(provider)
    if state.state != "open":
        return False
    if now() - state.opened_at < OPEN_COOLDOWN_S:
        return True
    client = get_redis()
    claimed = await cast(
        "Awaitable[bool | None]",
        client.set(_trial_key(provider), "1", nx=True, ex=int(OPEN_COOLDOWN_S)),
    )
    return not bool(claimed)


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
