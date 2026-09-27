from datetime import date

import pytest
from pydantic import BaseModel
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.core.time import vn_today
from app.modules.ai_gateway import breaker, service
from app.modules.ai_gateway.models import AIRequestLog
from app.modules.ai_gateway.routing import (
    FallbackRoute,
    ProviderConfig,
    RoutingConfig,
    TaskRoute,
)
from app.modules.ai_gateway.types import AIError, AIRequest
from app.modules.guard.service import budget_used

pytestmark = pytest.mark.anyio


class Issue(BaseModel):
    quote: str
    note: str


class GradeResult(BaseModel):
    criteria: dict[str, float]
    issues: list[Issue]
    pii_spans: list[str]


def req(
    user: str = "an essay",
    correlation_id: str = "corr-1",
    task_key: str = "writing_grade",
) -> AIRequest:
    return AIRequest(
        task_key=task_key,
        data_class="A",
        system="You are a VSTEP writing grader.",
        user=user,
        response_schema=GradeResult,
        max_output_tokens=500,
        correlation_id=correlation_id,
    )


def _fallback_routing() -> RoutingConfig:
    return RoutingConfig(
        tasks={
            "writing_grade": TaskRoute(
                rubric_version="writing-v1",
                prompt_version="writing-p1",
                provider="fake",
                model="fake-grader",
                data_class="A",
                fallback=FallbackRoute(provider="fallback", model="fallback-model"),
            )
        },
        providers={
            "fake": ProviderConfig(no_training=True),
            "fallback": ProviderConfig(no_training=True),
        },
    )


def _last_log(correlation_id: str) -> AIRequestLog:
    with Session(engine) as session:
        row = session.exec(
            select(AIRequestLog)
            .where(AIRequestLog.correlation_id == correlation_id)
            .order_by(AIRequestLog.created_at.desc())
        ).first()
        assert row is not None
        return row


def _count_logs(correlation_id: str) -> int:
    with Session(engine) as session:
        rows = session.exec(
            select(AIRequestLog).where(AIRequestLog.correlation_id == correlation_id)
        ).all()
        return len(rows)


async def test_complete_success_returns_result_and_writes_one_log_row(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter()
    result = await service.complete(req(correlation_id="ok-1"))

    assert isinstance(result.data, GradeResult)
    assert result.provider == "fake"
    assert result.model == "fake-grader"
    assert result.fallback is False
    assert result.cost_vnd > 0
    assert result.latency_ms >= 0

    assert _count_logs("ok-1") == 1
    row = _last_log("ok-1")
    assert row.status == "ok"
    assert row.error_type is None
    assert row.retry_count == 0
    assert row.fallback is False
    assert row.task_key == "writing_grade"
    assert row.data_class == "A"
    assert row.provider == "fake"
    assert row.model == "fake-grader"
    assert row.cost_vnd == result.cost_vnd


async def test_log_row_written_without_content(redis, install_fake_adapter) -> None:
    install_fake_adapter()
    await service.complete(req(user="SECRET ESSAY", correlation_id="secret-1"))
    row = _last_log("secret-1")
    assert row.status == "ok"
    dumped = row.model_dump_json()
    assert "SECRET ESSAY" not in dumped


async def test_retries_twice_then_fails(redis, install_fake_adapter) -> None:
    fake = install_fake_adapter(fail_with=["server", "server", "server"])
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="fail-1"))
    assert exc_info.value.kind == "server"
    assert fake.calls == 3

    row = _last_log("fail-1")
    assert row.status == "error"
    assert row.error_type == "server"
    assert row.retry_count == 2
    assert row.cost_vnd == 0

    # 3 consecutive failures within 60s open this provider's breaker.
    assert await breaker.is_open("fake") is True


async def test_invalid_json_raises_schema_without_retrying(
    redis, install_fake_adapter
) -> None:
    fake = install_fake_adapter(responses=["not json"])
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="schema-1"))
    assert exc_info.value.kind == "schema"
    assert fake.calls == 1

    row = _last_log("schema-1")
    assert row.status == "error"
    assert row.error_type == "schema"
    assert row.retry_count == 0
    # Tokens were consumed even though validation failed, so cost is real.
    assert row.cost_vnd > 0


async def test_budget_refused_raises_budget_error(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_fake_adapter()
    monkeypatch.setattr(settings, "AI_DAILY_BUDGET_VND", 0)
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="budget-1"))
    assert exc_info.value.kind == "budget"

    row = _last_log("budget-1")
    assert row.status == "error"
    assert row.error_type == "budget"


async def test_settle_refunds_reservation_on_failure(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter(fail_with=["server", "server", "server"])
    day = vn_today()
    with pytest.raises(AIError):
        await service.complete(req(correlation_id="refund-1"))
    assert await budget_used(day) == 0


async def test_fallback_used_and_flagged_when_primary_breaker_open(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "load_routing", lambda *a, **k: _fallback_routing())
    monkeypatch.setattr(
        service, "load_pricing", lambda *a, **k: _pricing_with_fallback()
    )
    for _ in range(3):
        await breaker.record_result("fake", success=False)
    assert await breaker.is_open("fake") is True

    install_fake_adapter()  # primary, unused
    install_fake_adapter(provider="fallback")

    result = await service.complete(req(correlation_id="fallback-open-1"))
    assert result.fallback is True
    assert result.provider == "fallback"
    assert result.model == "fallback-model"

    row = _last_log("fallback-open-1")
    assert row.fallback is True
    assert row.provider == "fallback"


async def test_fallback_used_after_primary_retries_exhausted(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(service, "load_routing", lambda *a, **k: _fallback_routing())
    monkeypatch.setattr(
        service, "load_pricing", lambda *a, **k: _pricing_with_fallback()
    )

    install_fake_adapter(fail_with=["server", "server", "server"])
    install_fake_adapter(provider="fallback")

    result = await service.complete(req(correlation_id="fallback-retry-1"))
    assert result.fallback is True
    assert result.provider == "fallback"

    row = _last_log("fallback-retry-1")
    assert row.fallback is True
    assert (
        row.retry_count == 2
    )  # only the primary's retries; fallback succeeded first try


async def test_complete_raises_no_route_for_unknown_task(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter()
    with pytest.raises(AIError) as exc_info:
        await service.complete(
            req(correlation_id="no-route-1", task_key="no_such_task")
        )
    assert exc_info.value.kind == "no_route"
    assert _count_logs("no-route-1") == 0


async def test_unregistered_provider_raises_invalid_request(
    redis, monkeypatch: pytest.MonkeyPatch
) -> None:
    routing = RoutingConfig(
        tasks={
            "writing_grade": TaskRoute(
                rubric_version="writing-v1",
                prompt_version="writing-p1",
                provider="unregistered",
                model="fake-grader",
                data_class="A",
            )
        },
        providers={"unregistered": ProviderConfig(no_training=True)},
    )
    monkeypatch.setattr(service, "load_routing", lambda *a, **k: routing)
    day = vn_today()
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="unregistered-1"))
    assert exc_info.value.kind == "invalid_request"

    # The reservation must not leak just because `_get_adapter` failed
    # before any adapter call was made.
    assert await budget_used(day) == 0
    assert _count_logs("unregistered-1") == 1
    row = _last_log("unregistered-1")
    assert row.status == "error"
    assert row.error_type == "invalid_request"
    assert row.cost_vnd == 0


async def test_non_aierror_adapter_exception_settles_and_logs(
    redis, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An adapter bug that raises a plain exception (not an `AIError`) must
    still refund the reservation and write exactly one log row, not leak
    the budget or vanish silently."""

    class _BuggyAdapter:
        def __init__(self) -> None:
            self.calls = 0

        async def generate_json(self, **_kwargs: object) -> None:
            self.calls += 1
            raise RuntimeError("adapter bug")

    adapter = _BuggyAdapter()
    monkeypatch.setitem(service.ADAPTER_REGISTRY, "fake", lambda: adapter)
    day = vn_today()
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="runtime-err-1"))
    assert exc_info.value.kind == "server"
    # Normalized like any other "server" kind failure, so it's retried too.
    assert adapter.calls == 3

    assert await budget_used(day) == 0
    assert _count_logs("runtime-err-1") == 1
    row = _last_log("runtime-err-1")
    assert row.status == "error"
    assert row.error_type == "server"
    assert row.cost_vnd == 0


async def test_missing_pricing_entry_after_tokens_spent_settles_and_logs(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    """If pricing lookup fails only at call time (defense in depth on top of
    the routing-load validation), tokens already consumed must still be
    reflected in the log, the reservation refunded, and exactly one row
    written. Simulates pricing.yaml losing the model's entry *between* the
    pre-call cost estimate and the post-call actual-cost lookup (both go
    through `_pricing_for`/`load_pricing`, so the entry has to still be
    there for the first call and gone by the second to isolate the
    after-tokens-spent path the coordinator flagged)."""
    from app.modules.ai_gateway.routing import PricingConfig, load_pricing

    install_fake_adapter()
    real_pricing = load_pricing()
    calls = {"n": 0}

    def _flaky_load_pricing(*_a: object, **_k: object) -> PricingConfig:
        calls["n"] += 1
        return real_pricing if calls["n"] == 1 else PricingConfig(models={})

    monkeypatch.setattr(service, "load_pricing", _flaky_load_pricing)
    day = vn_today()
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="no-pricing-1"))
    assert exc_info.value.kind == "invalid_request"

    assert await budget_used(day) == 0
    row = _last_log("no-pricing-1")
    assert row.status == "error"
    assert row.error_type == "invalid_request"
    assert row.cost_vnd == 0
    assert row.input_tokens > 0  # tokens were spent even though pricing failed


async def test_attempt_stops_retrying_once_breaker_opens_mid_retry(
    redis, install_fake_adapter
) -> None:
    # Pre-seed 2 failures so the 3rd (from this call's first attempt) opens
    # the breaker mid-retry-loop; no further attempts should be made.
    await breaker.record_result("fake", success=False)
    await breaker.record_result("fake", success=False)
    fake = install_fake_adapter(fail_with=["server", "server", "server"])

    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="mid-retry-open-1"))
    assert exc_info.value.kind == "server"
    # Only 1 call happened before the breaker opened and retrying stopped;
    # exhausting retries would have made 3.
    assert fake.calls == 1

    row = _last_log("mid-retry-open-1")
    assert row.retry_count == 0


async def test_gateway_enforces_timeout(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    install_fake_adapter(latency_s=(1.0, 1.0))
    monkeypatch.setattr(service, "TIMEOUT_S", 0.05)
    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="timeout-1"))
    assert exc_info.value.kind == "timeout"

    row = _last_log("timeout-1")
    assert row.status == "error"
    assert row.error_type == "timeout"


async def test_no_fallback_configured_and_breaker_open_raises_circuit_open(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter()
    for _ in range(3):
        await breaker.record_result("fake", success=False)
    assert await breaker.is_open("fake") is True

    with pytest.raises(AIError) as exc_info:
        await service.complete(req(correlation_id="circuit-open-1"))
    assert exc_info.value.kind == "circuit_open"

    assert _count_logs("circuit-open-1") == 1
    row = _last_log("circuit-open-1")
    assert row.provider == "fake"
    assert row.status == "error"
    assert row.error_type == "circuit_open"
    assert row.retry_count == 0
    assert row.fallback is False
    assert row.cost_vnd == 0


async def test_ai_fake_provider_setting_forces_fake_adapter_for_any_provider(
    redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    routing = RoutingConfig(
        tasks={
            "writing_grade": TaskRoute(
                rubric_version="writing-v1",
                prompt_version="writing-p1",
                provider="anthropic",  # not registered - only reachable via AI_FAKE_PROVIDER
                model="fake-grader",
                data_class="A",
            )
        },
        providers={"anthropic": ProviderConfig(no_training=True)},
    )
    monkeypatch.setattr(service, "load_routing", lambda *a, **k: routing)
    monkeypatch.setattr(settings, "AI_FAKE_PROVIDER", True)
    monkeypatch.setattr(settings, "AI_FAKE_LATENCY_MIN_S", 0.0)
    monkeypatch.setattr(settings, "AI_FAKE_LATENCY_MAX_S", 0.0)

    result = await service.complete(req(correlation_id="force-fake-1"))
    assert isinstance(result.data, GradeResult)


def test_default_fake_latency_settings_are_10_to_40_seconds() -> None:
    assert settings.AI_FAKE_LATENCY_MIN_S == 10.0
    assert settings.AI_FAKE_LATENCY_MAX_S == 40.0


async def test_usage_summary_groups_by_day_provider_model_with_percentiles(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter()
    day = vn_today()
    for i in range(4):
        await service.complete(req(correlation_id=f"usage-{i}"))

    rows = await service.usage_summary(day, day)
    assert len(rows) == 1
    row = rows[0]
    assert row.day == day
    assert row.provider == "fake"
    assert row.model == "fake-grader"
    assert row.requests == 4
    assert row.errors == 0
    assert row.cost_vnd > 0
    assert row.p50_ms >= 0
    assert row.p95_ms >= row.p50_ms


async def test_usage_summary_counts_errors_separately(
    redis, install_fake_adapter
) -> None:
    install_fake_adapter(fail_with=["server", "server", "server"])
    day = vn_today()
    with pytest.raises(AIError):
        await service.complete(req(correlation_id="usage-err-1"))

    rows = await service.usage_summary(day, day)
    assert len(rows) == 1
    assert rows[0].requests == 1
    assert rows[0].errors == 1


async def test_usage_summary_empty_outside_range(redis, install_fake_adapter) -> None:
    install_fake_adapter()
    await service.complete(req(correlation_id="usage-range-1"))
    yesterday = date(2000, 1, 1)
    rows = await service.usage_summary(yesterday, yesterday)
    assert rows == []


def _pricing_with_fallback():
    from app.modules.ai_gateway.routing import ModelPricing, PricingConfig

    return PricingConfig(
        models={
            "fake-grader": ModelPricing(
                input_vnd_per_1m=5000,
                output_vnd_per_1m=15000,
                cached_input_vnd_per_1m=2500,
            ),
            "fallback-model": ModelPricing(
                input_vnd_per_1m=5000,
                output_vnd_per_1m=15000,
                cached_input_vnd_per_1m=2500,
            ),
        }
    )
