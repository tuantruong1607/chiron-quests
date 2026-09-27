"""Per-day AI budget reservation (in VND) with threshold alerting."""

from collections.abc import Awaitable
from datetime import date
from typing import cast

from app.core.config import settings
from app.core.redis import get_redis
from app.modules.guard.alerts import send_alert

_TTL_SECONDS = 48 * 60 * 60
_ALERT_THRESHOLDS_PCT = (50, 80, 100)

# KEYS: 1=budget key. ARGV: 1=amount, 2=cap, 3=ttl_seconds.
_RESERVE_BUDGET_LUA = """
local used = tonumber(redis.call('GET', KEYS[1]) or '0')
local amount = tonumber(ARGV[1])
local cap = tonumber(ARGV[2])
if used + amount > cap then
  return 0
end
redis.call('INCRBY', KEYS[1], amount)
redis.call('EXPIRE', KEYS[1], ARGV[3])
return 1
"""

# KEYS: 1=budget key. ARGV: 1=delta (actual - reserved, may be negative), 2=ttl_seconds.
_SETTLE_BUDGET_LUA = """
local used = tonumber(redis.call('GET', KEYS[1]) or '0')
local delta = tonumber(ARGV[1])
local new_used = used + delta
if new_used < 0 then
  new_used = 0
end
redis.call('SET', KEYS[1], new_used)
redis.call('EXPIRE', KEYS[1], ARGV[2])
return new_used
"""


def _budget_key(day: date) -> str:
    return f"guard:budget:{day.isoformat()}"


def _alert_key(day: date, threshold_pct: int) -> str:
    return f"guard:budget_alert:{day.isoformat()}:{threshold_pct}"


async def reserve_budget(amount_vnd: int, day: date) -> bool:
    """Atomically reserve `amount_vnd` against `day`'s budget, succeeding
    only if the day's total usage would stay within
    `settings.AI_DAILY_BUDGET_VND`."""
    client = get_redis()
    result = await cast(
        "Awaitable[int]",
        client.eval(
            _RESERVE_BUDGET_LUA,
            1,
            _budget_key(day),
            str(amount_vnd),
            str(settings.AI_DAILY_BUDGET_VND),
            str(_TTL_SECONDS),
        ),
    )
    return bool(result)


async def settle_budget(reserved_vnd: int, actual_vnd: int, day: date) -> None:
    """Adjust `day`'s usage by `actual_vnd - reserved_vnd` (may be
    negative), never letting the day's usage drop below 0."""
    client = get_redis()
    delta = actual_vnd - reserved_vnd
    await cast(
        "Awaitable[str]",
        client.eval(
            _SETTLE_BUDGET_LUA, 1, _budget_key(day), str(delta), str(_TTL_SECONDS)
        ),
    )


async def budget_used(day: date) -> int:
    """Return the amount (VND) reserved/used so far for `day`."""
    client = get_redis()
    value = await client.get(_budget_key(day))
    return int(value) if value is not None else 0


async def maybe_send_budget_alert(day: date) -> None:
    """Send an alert email for each of the 50/80/100% usage thresholds
    crossed for `day`, at most once per threshold per day (tracked via a
    `SET NX` guard key)."""
    cap = settings.AI_DAILY_BUDGET_VND
    if cap <= 0:
        return
    used = await budget_used(day)
    pct = used / cap * 100
    client = get_redis()
    for threshold in _ALERT_THRESHOLDS_PCT:
        if pct < threshold:
            continue
        newly_set = await client.set(
            _alert_key(day, threshold), "1", nx=True, ex=_TTL_SECONDS
        )
        if newly_set:
            send_alert(
                f"AI budget at {threshold}% for {day.isoformat()}",
                f"Used {used} / {cap} VND ({pct:.1f}%) on {day.isoformat()}.",
            )
