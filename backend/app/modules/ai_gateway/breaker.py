"""Per-provider circuit breaker, state kept in Redis under `cb:{provider}`.

Rules (spec §4.2): opens after 3 consecutive failures within a 60s window;
after 60s in the open state, one trial call is allowed (half-open) - if it
succeeds the breaker closes, if it fails the breaker reopens.
"""

import json
import time
from dataclasses import asdict, dataclass

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


async def _load(provider: str) -> _State:
    client = get_redis()
    raw = await client.get(_key(provider))
    if raw is None:
        return _State()
    return _State(**json.loads(raw))


async def _save(provider: str, state: _State) -> None:
    client = get_redis()
    await client.set(_key(provider), json.dumps(asdict(state)), ex=_KEY_TTL_S)


async def is_open(provider: str) -> bool:
    """True if calls to `provider` should be blocked right now.

    Once `OPEN_COOLDOWN_S` has passed since the breaker opened, this
    returns False so the caller may make a single half-open trial call -
    the breaker itself only closes once that trial reports success via
    `record_result`.
    """
    state = await _load(provider)
    if state.state != "open":
        return False
    return now() - state.opened_at < OPEN_COOLDOWN_S


async def record_result(provider: str, *, success: bool) -> None:
    """Feed one call's outcome into `provider`'s breaker."""
    state = await _load(provider)
    moment = now()

    if success:
        await _save(provider, _State())
        return

    was_half_open_trial = (
        state.state == "open" and moment - state.opened_at >= OPEN_COOLDOWN_S
    )
    if was_half_open_trial:
        # The half-open trial failed: reopen immediately.
        await _save(
            provider,
            _State(
                state="open",
                fail_count=state.fail_count,
                streak_start=moment,
                opened_at=moment,
            ),
        )
        return

    if state.fail_count == 0 or moment - state.streak_start > FAILURE_WINDOW_S:
        fail_count = 1
        streak_start = moment
    else:
        fail_count = state.fail_count + 1
        streak_start = state.streak_start

    if fail_count >= FAILURE_THRESHOLD:
        await _save(
            provider,
            _State(
                state="open",
                fail_count=fail_count,
                streak_start=streak_start,
                opened_at=moment,
            ),
        )
    else:
        await _save(
            provider,
            _State(
                state="closed",
                fail_count=fail_count,
                streak_start=streak_start,
                opened_at=0.0,
            ),
        )
