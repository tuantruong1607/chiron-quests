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


async def test_release_trial_lets_the_next_caller_claim_it(redis, clock) -> None:
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)

    blocked, token = await breaker.try_claim("p")
    assert blocked is False
    assert token is not None
    assert await breaker.is_open("p") is True  # blocked: trial already held

    await breaker.release_trial("p", token)
    assert await breaker.is_open("p") is False  # claimable again immediately


async def test_release_trial_is_a_no_op_when_nothing_was_claimed(redis, clock) -> None:
    await breaker.release_trial("p", "some-token")  # closed breaker, no key at all
    assert await breaker.is_open("p") is False


async def test_release_trial_with_wrong_token_leaves_the_key(redis, clock) -> None:
    """Compare-and-delete: releasing with a token that doesn't match the
    one currently held must not delete someone else's claim."""
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)

    blocked, token = await breaker.try_claim("p")
    assert blocked is False
    assert token is not None

    await breaker.release_trial("p", "not-the-real-token")
    # Still held: a third caller must still be blocked.
    assert await breaker.is_open("p") is True

    # The real token still works.
    await breaker.release_trial("p", token)
    assert await breaker.is_open("p") is False


async def test_trial_ttl_can_exceed_the_default_cooldown(redis, clock) -> None:
    """`ttl_s` is meant to be set to the caller's own call timeout plus a
    margin (e.g. TIMEOUT_S + 10 > OPEN_COOLDOWN_S's default 60s), so a slow
    trial call can't outlive its own claim and let a second trial start
    concurrently."""
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)

    blocked, token = await breaker.try_claim("p", 70.0)
    assert blocked is False
    assert token is not None
    # Still held by the first claim well past the *default* 60s window.
    clock.advance(65)
    assert await breaker.is_open("p") is True


async def test_cross_worker_claim_is_not_undone_by_an_unrelated_release(
    redis, clock
) -> None:
    """A trial claimed by one worker (for provider P) must stay blocked for
    a third caller even after some *other* call - one that never held P's
    trial at all - tries to release a (wrong) token for P. This is the
    scenario a blanket, non-compare-and-delete release would have broken:
    an unrelated error on a different attempt must never delete another
    worker's live claim."""
    for _ in range(3):
        await breaker.record_result("p", success=False)
    clock.advance(60)

    # Worker A claims P's one half-open trial.
    blocked, worker_a_token = await breaker.try_claim("p")
    assert blocked is False
    assert worker_a_token is not None

    # Some unrelated call - e.g. one that never actually claimed anything
    # for "p" - tries to release with a token it doesn't hold.
    await breaker.release_trial("p", "unrelated-token")

    # A third caller must still see the breaker as blocked: worker A's
    # claim is untouched.
    assert await breaker.is_open("p") is True
