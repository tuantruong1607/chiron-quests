import asyncio
from datetime import UTC, date, datetime, timedelta

import pytest

from app.core.time import VIETNAM_TZ
from app.modules.guard.service import (
    block_ip_hash,
    is_blocked,
    record_success,
    reserve_submission,
    submissions_spike,
)

pytestmark = pytest.mark.anyio

D = date(2026, 10, 1)


async def test_third_success_blocked_without_consent(redis) -> None:
    for _ in range(2):
        assert (await reserve_submission("ip", "v", False, D)).allowed
        await record_success("ip", "v", D)
    decision = await reserve_submission("ip", "v", False, D)
    assert (decision.allowed, decision.reason) == (False, "successes")


async def test_consent_allows_third_success(redis) -> None:
    for _ in range(3):
        assert (await reserve_submission("ip", "v", True, D)).allowed
        await record_success("ip", "v", D)
    decision = await reserve_submission("ip", "v", True, D)
    assert (decision.allowed, decision.reason) == (False, "successes")


async def test_sixth_submission_blocked_even_if_failed(redis) -> None:
    for _ in range(5):
        assert (await reserve_submission("ip", "v", False, D)).allowed
    decision = await reserve_submission("ip", "v", False, D)
    assert decision.reason == "submissions"


async def test_limit_by_visitor_even_with_new_ip(redis) -> None:
    for _ in range(5):
        assert (await reserve_submission("ip1", "v", False, D)).allowed
    decision = await reserve_submission("ip2", "v", False, D)
    assert (decision.allowed, decision.reason) == (False, "submissions")


async def test_counters_reset_at_vietnam_midnight(redis) -> None:
    for _ in range(5):
        assert (await reserve_submission("ip", "v", False, D)).allowed
    blocked_today = await reserve_submission("ip", "v", False, D)
    assert not blocked_today.allowed

    next_day = D + timedelta(days=1)
    allowed_tomorrow = await reserve_submission("ip", "v", False, next_day)
    assert allowed_tomorrow.allowed


async def test_blocked_ip_is_refused(redis) -> None:
    await block_ip_hash("ip", D)
    decision = await reserve_submission("ip", "v", False, D)
    assert (decision.allowed, decision.reason) == (False, "blocked")
    assert await is_blocked("ip", D) is True


async def test_not_blocked_ip_reports_false(redis) -> None:
    assert await is_blocked("some-ip", D) is False


async def test_blocked_check_takes_priority_over_submission_count(redis) -> None:
    for _ in range(5):
        assert (await reserve_submission("ip", "v", False, D)).allowed
    await block_ip_hash("ip", D)
    decision = await reserve_submission("ip", "v", False, D)
    assert decision.reason == "blocked"


async def test_resets_at_is_next_vietnam_midnight(redis) -> None:
    decision = await reserve_submission("ip", "v", False, D)
    assert decision.resets_at == datetime(2026, 10, 2, 0, 0, tzinfo=VIETNAM_TZ)
    assert decision.resets_at.tzinfo is not None


async def test_allowed_reservation_increments_current_hour_spike_counter(
    redis,
) -> None:
    now = datetime.now(UTC)
    current_hour = now.astimezone(VIETNAM_TZ).replace(minute=0, second=0, microsecond=0)
    key = f"guard:subs_hour:{current_hour:%Y-%m-%dT%H}"
    assert await redis.get(key) is None

    await reserve_submission("ip", "v", False, D)
    assert await redis.get(key) == b"1"

    await reserve_submission("ip2", "v2", False, D)
    assert await redis.get(key) == b"2"


async def test_concurrent_reservations_respect_limit(redis) -> None:
    results = await asyncio.gather(
        *[reserve_submission("ip", "v", False, D) for _ in range(10)]
    )
    assert sum(r.allowed for r in results) == 5


def _hour_key(hour: datetime) -> str:
    return f"guard:subs_hour:{hour:%Y-%m-%dT%H}"


async def _seed_history(redis, now: datetime, per_hour: int) -> None:
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    for i in range(1, 169):
        await redis.set(_hour_key(current_hour - timedelta(hours=i)), per_hour)


async def test_submissions_spike_true_when_current_hour_much_higher(redis) -> None:
    now = datetime(2026, 10, 8, 10, 30, tzinfo=VIETNAM_TZ)
    # Seed 7 days (168 hours) of history at 2 submissions/hour, then make
    # the current hour's count far exceed 5x that average.
    await _seed_history(redis, now, per_hour=2)
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    await redis.set(_hour_key(current_hour), 50)

    assert await submissions_spike(now) is True


async def test_submissions_spike_false_when_in_line_with_history(redis) -> None:
    now = datetime(2026, 10, 8, 10, 30, tzinfo=VIETNAM_TZ)
    await _seed_history(redis, now, per_hour=10)
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    await redis.set(_hour_key(current_hour), 12)

    assert await submissions_spike(now) is False


async def test_submissions_spike_false_below_floor_with_no_history(redis) -> None:
    now = datetime(2026, 10, 8, 10, 30, tzinfo=VIETNAM_TZ)
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    await redis.set(_hour_key(current_hour), 3)
    assert await submissions_spike(now) is False


async def test_submissions_spike_true_above_floor_with_no_history(redis) -> None:
    now = datetime(2026, 10, 8, 10, 30, tzinfo=VIETNAM_TZ)
    current_hour = now.replace(minute=0, second=0, microsecond=0)
    await redis.set(_hour_key(current_hour), 20)
    assert await submissions_spike(now) is True
