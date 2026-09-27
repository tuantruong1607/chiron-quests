import pytest

from app.modules.ai_gateway import breaker

pytestmark = pytest.mark.anyio


async def test_breaker_closed_initially(redis, clock) -> None:
    assert await breaker.is_open("p") is False


async def test_breaker_opens_after_three_consecutive_failures_within_60s(
    redis, clock
) -> None:
    await breaker.record_result("p", success=False)
    clock.advance(10)
    await breaker.record_result("p", success=False)
    clock.advance(10)
    assert await breaker.is_open("p") is False  # only 2 failures so far
    await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is True


async def test_breaker_does_not_open_when_failures_spread_beyond_60s(
    redis, clock
) -> None:
    await breaker.record_result("p", success=False)
    clock.advance(61)
    await breaker.record_result("p", success=False)  # streak restarts here
    clock.advance(10)
    await breaker.record_result("p", success=False)
    # Only 2 failures within the last 60s window (streak restarted).
    assert await breaker.is_open("p") is False


async def test_breaker_success_resets_the_failure_streak(redis, clock) -> None:
    await breaker.record_result("p", success=False)
    await breaker.record_result("p", success=False)
    await breaker.record_result("p", success=True)
    await breaker.record_result("p", success=False)
    await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is False


async def test_breaker_half_open_after_60s_then_success_closes_it(redis, clock) -> None:
    for _ in range(3):
        await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is True

    clock.advance(60)
    assert await breaker.is_open("p") is False  # half-open: trial allowed

    await breaker.record_result("p", success=True)
    assert await breaker.is_open("p") is False
    # The streak was reset by the close, so it takes 3 fresh failures again.
    await breaker.record_result("p", success=False)
    await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is False


async def test_breaker_half_open_trial_failure_reopens(redis, clock) -> None:
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)
    assert await breaker.is_open("p") is False  # half-open trial allowed

    await breaker.record_result("p", success=False)  # trial fails
    assert await breaker.is_open("p") is True

    clock.advance(59)
    assert await breaker.is_open("p") is True  # cooldown restarted at reopen
    clock.advance(1)
    assert await breaker.is_open("p") is False


async def test_breaker_is_per_provider(redis, clock) -> None:
    for _ in range(3):
        await breaker.record_result("a", success=False)
    assert await breaker.is_open("a") is True
    assert await breaker.is_open("b") is False
