"""Per-day submission/success limits, IP blocklist, and hourly spike
detection, all backed by Redis with 48h-TTL keys (the hourly spike counter
is the one exception — see `_HOUR_TTL_SECONDS`)."""

from collections.abc import Awaitable
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Literal, cast

from app.core.redis import get_redis
from app.core.time import VIETNAM_TZ

# Every day-scoped key (blocklist, success/submission counters) is written
# with this TTL, so it self-expires well after the Vietnam-midnight reset
# the day it belongs to has already passed.
_TTL_SECONDS = 48 * 60 * 60

# The hourly spike counter needs 7 days (168 hours) of history to compute
# its rolling average, so it gets a longer TTL than the other guard keys.
_HOUR_TTL_SECONDS = 8 * 24 * 60 * 60

_SUBMISSIONS_CAP = 5
_SPIKE_MULTIPLIER = 5
# With no historical average yet (a brand-new deployment, or the first
# hours after a Redis flush) `avg == 0` would make ANY submission look like
# an infinite-multiple spike. Require this many submissions in the current
# hour before alerting in that case, so a handful of early real users don't
# trigger a false spike alert.
_NO_HISTORY_SPIKE_FLOOR = 20

Reason = Literal["ok", "submissions", "successes", "blocked"]


@dataclass(frozen=True)
class LimitDecision:
    allowed: bool
    reason: Reason
    resets_at: datetime


# KEYS: 1=blocked, 2=succ_ip, 3=succ_visitor, 4=sub_ip, 5=sub_visitor, 6=hour
# ARGV: 1=success_cap, 2=submissions_cap, 3=ttl_seconds, 4=hour_ttl_seconds
_RESERVE_SUBMISSION_LUA = """
if redis.call('EXISTS', KEYS[1]) == 1 then
  return 'blocked'
end

local success_cap = tonumber(ARGV[1])
local succ_ip = tonumber(redis.call('GET', KEYS[2]) or '0')
local succ_visitor = tonumber(redis.call('GET', KEYS[3]) or '0')
if succ_ip >= success_cap or succ_visitor >= success_cap then
  return 'successes'
end

local submissions_cap = tonumber(ARGV[2])
local sub_ip = tonumber(redis.call('GET', KEYS[4]) or '0')
local sub_visitor = tonumber(redis.call('GET', KEYS[5]) or '0')
if sub_ip >= submissions_cap or sub_visitor >= submissions_cap then
  return 'submissions'
end

local ttl = tonumber(ARGV[3])
redis.call('INCR', KEYS[4])
redis.call('EXPIRE', KEYS[4], ttl)
redis.call('INCR', KEYS[5])
redis.call('EXPIRE', KEYS[5], ttl)

local hour_ttl = tonumber(ARGV[4])
redis.call('INCR', KEYS[6])
redis.call('EXPIRE', KEYS[6], hour_ttl)

return 'ok'
"""


def _blocked_key(ip_hash: str, day: date) -> str:
    return f"guard:blocked:{day.isoformat()}:{ip_hash}"


def _success_key(identity_hash: str, day: date) -> str:
    return f"guard:succ:{day.isoformat()}:{identity_hash}"


def _submission_key(identity_hash: str, day: date) -> str:
    return f"guard:sub:{day.isoformat()}:{identity_hash}"


def _hour_floor(now: datetime) -> datetime:
    return now.astimezone(VIETNAM_TZ).replace(minute=0, second=0, microsecond=0)


def _hour_key(hour: datetime) -> str:
    return f"guard:subs_hour:{hour:%Y-%m-%dT%H}"


def _resets_at(day: date) -> datetime:
    """Return the Vietnam-local midnight that starts the day after `day`,
    as a timezone-aware datetime."""
    next_day = day + timedelta(days=1)
    return datetime.combine(next_day, time.min, tzinfo=VIETNAM_TZ)


async def reserve_submission(
    ip_hash: str, visitor_hash: str, consent: bool, day: date
) -> LimitDecision:
    """Atomically check the day's blocklist, success cap, and submission
    cap for both `ip_hash` and `visitor_hash`, and — only when allowed —
    increment both submission counters plus the current hour's spike
    counter. Check order: blocked, successes, submissions."""
    client = get_redis()
    success_cap = 3 if consent else 2
    keys = [
        _blocked_key(ip_hash, day),
        _success_key(ip_hash, day),
        _success_key(visitor_hash, day),
        _submission_key(ip_hash, day),
        _submission_key(visitor_hash, day),
        _hour_key(_hour_floor(datetime.now(UTC))),
    ]
    raw_reason = await cast(
        "Awaitable[str | bytes]",
        client.eval(
            _RESERVE_SUBMISSION_LUA,
            len(keys),
            *keys,
            str(success_cap),
            str(_SUBMISSIONS_CAP),
            str(_TTL_SECONDS),
            str(_HOUR_TTL_SECONDS),
        ),
    )
    reason = cast(
        "Reason", raw_reason.decode() if isinstance(raw_reason, bytes) else raw_reason
    )
    return LimitDecision(
        allowed=reason == "ok", reason=reason, resets_at=_resets_at(day)
    )


async def record_success(ip_hash: str, visitor_hash: str, day: date) -> None:
    """Increment both identities' success counters for `day`."""
    client = get_redis()
    pipe = client.pipeline()
    for key in (_success_key(ip_hash, day), _success_key(visitor_hash, day)):
        pipe.incr(key)
        pipe.expire(key, _TTL_SECONDS)
    await pipe.execute()


async def block_ip_hash(ip_hash: str, day: date) -> None:
    """Add `ip_hash` to `day`'s blocklist."""
    client = get_redis()
    await client.set(_blocked_key(ip_hash, day), "1", ex=_TTL_SECONDS)


async def is_blocked(ip_hash: str, day: date) -> bool:
    """Return whether `ip_hash` is on `day`'s blocklist."""
    client = get_redis()
    return bool(await client.exists(_blocked_key(ip_hash, day)))


async def submissions_spike(now: datetime) -> bool:
    """Return True when the current hour's submission count is more than
    `_SPIKE_MULTIPLIER`x the average of the previous 168 hourly counts.

    When there is no history yet (average of 0), only flag a spike once the
    current hour's count reaches `_NO_HISTORY_SPIKE_FLOOR` (see its
    docstring for why).
    """
    client = get_redis()
    current_hour = _hour_floor(now)
    current_count = int(await client.get(_hour_key(current_hour)) or 0)

    history_keys = [_hour_key(current_hour - timedelta(hours=i)) for i in range(1, 169)]
    history_values = await client.mget(history_keys)
    total = sum(int(value) for value in history_values if value is not None)
    average = total / 168

    if average == 0:
        return current_count >= _NO_HISTORY_SPIKE_FLOOR
    return current_count > _SPIKE_MULTIPLIER * average
