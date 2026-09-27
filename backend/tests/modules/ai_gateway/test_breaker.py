import anyio
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


async def test_breaker_failure_while_open_before_cooldown_stays_open(
    redis, clock
) -> None:
    """A straggling failure (e.g. a retry that lands after the breaker has
    already opened) must not fall through to the streak-counting branch and
    accidentally close the breaker again."""
    for _ in range(3):
        await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is True

    clock.advance(30)  # still well within the cooldown
    await breaker.record_result("p", success=False)
    assert await breaker.is_open("p") is True

    # The cooldown restarts from this last failure's moment.
    clock.advance(59)
    assert await breaker.is_open("p") is True
    clock.advance(1)
    assert await breaker.is_open("p") is False


async def test_breaker_half_open_grants_exactly_one_trial(redis, clock) -> None:
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)

    # The first caller past the cooldown gets the trial...
    assert await breaker.is_open("p") is False
    # ...and every other concurrent caller still sees it as open, whether
    # they ask once or repeatedly, until the trial's outcome is recorded.
    assert await breaker.is_open("p") is True
    assert await breaker.is_open("p") is True


async def test_breaker_record_result_is_atomic_under_concurrency(redis, clock) -> None:
    """Ten concurrent failures must be applied without a lost update: the
    breaker opens on the 3rd and every failure after that (whatever order
    they're processed in) leaves `fail_count` frozen at exactly 3, because
    the read-decide-write happens atomically in a single Lua script."""

    async def _fail() -> None:
        await breaker.record_result("p", success=False)

    async with anyio.create_task_group() as tg:
        for _ in range(10):
            tg.start_soon(_fail)

    assert await breaker._load("p") == breaker._State(
        state="open", fail_count=3, streak_start=clock.t, opened_at=clock.t
    )
