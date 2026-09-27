from datetime import date

import pytest

from app.core.config import settings
from app.modules.guard.service import (
    budget_used,
    maybe_send_budget_alert,
    reserve_budget,
    settle_budget,
)

pytestmark = pytest.mark.anyio

D = date(2026, 10, 1)


async def test_reserve_budget_refuses_over_cap(
    redis, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 1000)
    assert await reserve_budget(800, D)
    assert not await reserve_budget(300, D)


async def test_reserve_budget_allows_up_to_cap(
    redis, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 1000)
    assert await reserve_budget(1000, D)
    assert await budget_used(D) == 1000


async def test_settle_adjusts_to_actual(redis) -> None:
    await reserve_budget(1000, D)
    await settle_budget(1000, 400, D)
    assert await budget_used(D) == 400


async def test_settle_never_goes_below_zero(redis) -> None:
    await reserve_budget(100, D)
    await settle_budget(100, -5000, D)
    assert await budget_used(D) == 0


async def test_settle_can_increase_usage_when_actual_exceeds_reserved(
    redis,
) -> None:
    await reserve_budget(100, D)
    await settle_budget(100, 150, D)
    assert await budget_used(D) == 150


async def test_alert_sent_once_per_threshold(
    redis, outbox: list[tuple[str, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 1000)
    await reserve_budget(550, D)  # 55% -> crosses the 50% threshold only

    await maybe_send_budget_alert(D)
    assert len(outbox) == 1

    await maybe_send_budget_alert(D)  # calling again must not resend
    assert len(outbox) == 1


async def test_maybe_send_budget_alert_noop_when_cap_not_positive(
    redis, outbox: list[tuple[str, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 0)
    await maybe_send_budget_alert(D)
    assert outbox == []


async def test_alert_sends_each_newly_crossed_threshold(
    redis, outbox: list[tuple[str, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 1000)

    await reserve_budget(600, D)  # 60% -> crosses 50%
    await maybe_send_budget_alert(D)
    assert len(outbox) == 1

    await reserve_budget(250, D)  # now 85% -> crosses 80% too
    await maybe_send_budget_alert(D)
    assert len(outbox) == 2

    await reserve_budget(150, D)  # now 100% -> crosses 100% too
    await maybe_send_budget_alert(D)
    assert len(outbox) == 3

    await maybe_send_budget_alert(D)  # no new threshold crossed
    assert len(outbox) == 3
