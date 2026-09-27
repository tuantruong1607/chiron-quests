"""AI Gateway public entry point.

The only module allowed to call an LLM provider SDK directly (enforced by
`tests/test_module_boundaries.py`). Other modules must go through
`complete()`, `task_config()` and `usage_summary()` only.
"""

import math
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

import anyio
from anyio.to_thread import run_sync
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core.config import settings
from app.core.db import engine
from app.core.time import vn_today
from app.modules.ai_gateway import breaker
from app.modules.ai_gateway.adapters.base import ProviderAdapter
from app.modules.ai_gateway.adapters.fake import FakeAdapter
from app.modules.ai_gateway.models import AIRequestLog
from app.modules.ai_gateway.routing import (
    ModelPricing,
    RoutingError,
    TaskRoute,
    load_pricing,
    load_routing,
)
from app.modules.ai_gateway.types import (
    RETRYABLE_KINDS,
    AIError,
    AIRequest,
    AIResult,
    RawResponse,
    UsageRow,
)
from app.modules.guard.service import (
    maybe_send_budget_alert,
    reserve_budget,
    settle_budget,
)

__all__ = [
    "AIError",
    "AIRequest",
    "AIResult",
    "RoutingError",
    "complete",
    "task_config",
    "usage_summary",
]

#: Per-call adapter timeout (spec §4.2). A module-level global (not a
#: default argument) so tests can monkeypatch it.
TIMEOUT_S = 60.0
MAX_RETRIES = 2
_BACKOFFS_S = [2.0, 4.0]

#: Injectable sleep, so retry backoff never actually waits in tests.
_sleep: Callable[[float], Awaitable[None]] = anyio.sleep

#: provider name -> factory building one `ProviderAdapter`. Only `fake` is
#: registered until Task 13 adds real provider SDKs.
ADAPTER_REGISTRY: dict[str, Callable[[], ProviderAdapter]] = {
    "fake": lambda: FakeAdapter(),
}


def task_config(task_key: str) -> TaskRoute:
    """Return `routing.yaml`'s route for `task_key` (rubric/prompt version,
    active calibration, few-shot ids, provider/model, params, data_class).
    Raises `AIError("no_route")` if the task isn't configured."""
    routing = load_routing()
    route = routing.tasks.get(task_key)
    if route is None:
        raise AIError("no_route", f"no routing.yaml entry for task '{task_key}'")
    return route


def _get_adapter(provider: str) -> ProviderAdapter:
    if settings.AI_FAKE_PROVIDER:
        return FakeAdapter(
            latency_s=(settings.AI_FAKE_LATENCY_MIN_S, settings.AI_FAKE_LATENCY_MAX_S)
        )
    factory = ADAPTER_REGISTRY.get(provider)
    if factory is None:
        raise AIError(
            "invalid_request", f"no adapter registered for provider '{provider}'"
        )
    return factory()


def _ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        return 0
    return -(-numerator // denominator)


def _cost_vnd(
    pricing: ModelPricing, input_tokens: int, output_tokens: int, cached_tokens: int
) -> int:
    non_cached_input = max(input_tokens - cached_tokens, 0)
    micro_vnd = (
        non_cached_input * pricing.input_vnd_per_1m
        + cached_tokens * pricing.cached_input_vnd_per_1m
        + output_tokens * pricing.output_vnd_per_1m
    )
    return _ceil_div(micro_vnd, 1_000_000)


def _pricing_for(model: str) -> ModelPricing:
    pricing = load_pricing()
    entry = pricing.models.get(model)
    if entry is None:
        raise AIError("invalid_request", f"no pricing.yaml entry for model '{model}'")
    return entry


def _estimate_cost(model: str, req: AIRequest) -> int:
    pricing = _pricing_for(model)
    input_tokens_est = math.ceil((len(req.system) + len(req.user)) / 4)
    return _cost_vnd(pricing, input_tokens_est, req.max_output_tokens, 0)


def _actual_cost(model: str, raw: RawResponse) -> int:
    pricing = _pricing_for(model)
    return _cost_vnd(pricing, raw.input_tokens, raw.output_tokens, raw.cached_tokens)


async def _call_adapter_with_timeout(
    adapter: ProviderAdapter,
    model: str,
    req: AIRequest,
    schema_dict: dict[str, object],
) -> RawResponse:
    """Enforce the gateway-side timeout (spec §4.2: 60s per call) around an
    adapter call, on top of whatever `timeout_s` the adapter itself does
    with the provider SDK - a slow/hanging adapter can't block `complete()`
    past `TIMEOUT_S`."""
    try:
        with anyio.fail_after(TIMEOUT_S):
            return await adapter.generate_json(
                model=model,
                system=req.system,
                user=req.user,
                schema=schema_dict,
                max_output_tokens=req.max_output_tokens,
                timeout_s=TIMEOUT_S,
            )
    except TimeoutError:
        raise AIError("timeout", f"gateway timeout after {TIMEOUT_S}s") from None


async def _attempt(
    provider: str, model: str, req: AIRequest, schema_dict: dict[str, object]
) -> tuple[RawResponse | None, AIError | None, int]:
    """Call `provider`/`model` with up to `MAX_RETRIES` retries on a
    retryable error kind. Every attempt's outcome feeds that provider's
    breaker, and retrying stops as soon as the breaker opens (no point
    hammering a provider we've just tripped). Returns (response, error,
    retries_used) - exactly one of response/error is set.

    `_get_adapter` is called once, outside the retry loop and its own try -
    a config error there (e.g. an unregistered provider) propagates
    straight out of this function to `complete()`'s single settle/log path,
    rather than being retried."""
    adapter = _get_adapter(provider)
    attempt = 0
    while True:
        try:
            raw = await _call_adapter_with_timeout(adapter, model, req, schema_dict)
        except AIError as exc:
            normalized = exc
        except Exception as exc:  # normalize any adapter bug to a server error
            normalized = AIError("server", str(exc))
        else:
            await breaker.record_result(provider, success=True)
            return raw, None, attempt

        await breaker.record_result(provider, success=False)
        if normalized.kind not in RETRYABLE_KINDS or attempt >= MAX_RETRIES:
            return None, normalized, attempt
        if await breaker.is_open(provider):
            return None, normalized, attempt
        await _sleep(_BACKOFFS_S[attempt])
        attempt += 1


@dataclass
class _Outcome:
    raw: RawResponse | None
    error: AIError | None
    retries: int
    fallback: bool
    provider: str
    model: str


async def _run_route(
    route: TaskRoute,
    use_fallback_initial: bool,
    req: AIRequest,
    schema_dict: dict[str, object],
) -> _Outcome:
    if use_fallback_initial:
        assert route.fallback is not None
        raw, err, retries = await _attempt(
            route.fallback.provider, route.fallback.model, req, schema_dict
        )
        return _Outcome(
            raw, err, retries, True, route.fallback.provider, route.fallback.model
        )

    raw, err, retries = await _attempt(route.provider, route.model, req, schema_dict)
    if err is not None and err.kind in RETRYABLE_KINDS and route.fallback is not None:
        fb_raw, fb_err, fb_retries = await _attempt(
            route.fallback.provider, route.fallback.model, req, schema_dict
        )
        return _Outcome(
            fb_raw,
            fb_err,
            retries + fb_retries,
            True,
            route.fallback.provider,
            route.fallback.model,
        )
    return _Outcome(raw, err, retries, False, route.provider, route.model)


def _insert_log_row(row: AIRequestLog) -> None:
    with Session(engine) as session:
        session.add(row)
        session.commit()


async def _write_log(
    *,
    task_key: str,
    data_class: str,
    provider: str,
    model: str,
    prompt_version: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int,
    cost_vnd: int,
    latency_ms: int,
    status: str,
    error_type: str | None,
    retry_count: int,
    fallback: bool,
    correlation_id: str,
) -> None:
    row = AIRequestLog(
        task_key=task_key,
        data_class=data_class,
        provider=provider,
        model=model,
        prompt_version=prompt_version,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_tokens=cached_tokens,
        cost_vnd=cost_vnd,
        latency_ms=latency_ms,
        status=status,
        error_type=error_type,
        retry_count=retry_count,
        fallback=fallback,
        correlation_id=correlation_id,
    )
    # Sync DB write dispatched to a worker thread so `complete()` stays async
    # without a separate async DB engine for one insert per call.
    await run_sync(lambda: _insert_log_row(row))


async def _settle_and_log(
    *,
    req: AIRequest,
    route: TaskRoute,
    estimated_cost: int,
    actual_cost: int,
    day: date,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int,
    latency_ms: int,
    status: str,
    error_type: str | None,
    retry_count: int,
    fallback: bool,
) -> None:
    """Always-run tail of a reserved `complete()` call: settle the budget
    reservation against the real cost (0 if nothing was actually spent),
    send a threshold alert if crossed, and write exactly one log row."""
    await settle_budget(estimated_cost, actual_cost, day)
    await maybe_send_budget_alert(day)
    await _write_log(
        task_key=req.task_key,
        data_class=req.data_class,
        provider=provider,
        model=model,
        prompt_version=route.prompt_version,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_tokens=cached_tokens,
        cost_vnd=actual_cost,
        latency_ms=latency_ms,
        status=status,
        error_type=error_type,
        retry_count=retry_count,
        fallback=fallback,
        correlation_id=req.correlation_id,
    )


async def complete(req: AIRequest) -> AIResult:
    routing = load_routing()
    route = routing.tasks.get(req.task_key)
    if route is None:
        raise AIError("no_route", f"no routing.yaml entry for task '{req.task_key}'")

    day = vn_today()
    schema_dict = req.response_schema.model_json_schema()

    use_fallback_initial = False
    if await breaker.is_open(route.provider):
        if route.fallback is None:
            # Nothing was reserved yet, so there's nothing to settle - just
            # record the refusal.
            await _write_log(
                task_key=req.task_key,
                data_class=req.data_class,
                provider=route.provider,
                model=route.model,
                prompt_version=route.prompt_version,
                input_tokens=0,
                output_tokens=0,
                cached_tokens=0,
                cost_vnd=0,
                latency_ms=0,
                status="error",
                error_type="circuit_open",
                retry_count=0,
                fallback=False,
                correlation_id=req.correlation_id,
            )
            raise AIError(
                "circuit_open", f"circuit open for provider '{route.provider}'"
            )
        use_fallback_initial = True

    provider, model = (
        (route.fallback.provider, route.fallback.model)
        if use_fallback_initial and route.fallback is not None
        else (route.provider, route.model)
    )
    estimated_cost = _estimate_cost(model, req)

    if not await reserve_budget(estimated_cost, day):
        await _write_log(
            task_key=req.task_key,
            data_class=req.data_class,
            provider=provider,
            model=model,
            prompt_version=route.prompt_version,
            input_tokens=0,
            output_tokens=0,
            cached_tokens=0,
            cost_vnd=0,
            latency_ms=0,
            status="error",
            error_type="budget",
            retry_count=0,
            fallback=use_fallback_initial,
            correlation_id=req.correlation_id,
        )
        raise AIError("budget", "daily AI budget exhausted")

    # From here on the budget has been reserved: every exit path below -
    # success, a classified AIError, an unexpected exception, or a
    # cancellation - must settle it and write exactly one log row.
    fallback_flag = use_fallback_initial
    retries = 0
    input_tokens = output_tokens = cached_tokens = 0
    actual_cost = 0
    data = None
    error: AIError | None = None
    started = anyio.current_time()

    try:
        outcome = await _run_route(route, use_fallback_initial, req, schema_dict)
        provider, model, fallback_flag, retries = (
            outcome.provider,
            outcome.model,
            outcome.fallback,
            outcome.retries,
        )
        if outcome.error is not None:
            raise outcome.error
        raw = outcome.raw
        assert raw is not None
        input_tokens, output_tokens, cached_tokens = (
            raw.input_tokens,
            raw.output_tokens,
            raw.cached_tokens,
        )
        # Tokens were spent (and billable) whether or not the response
        # turns out to validate, so price it before validating.
        actual_cost = _actual_cost(model, raw)
        try:
            data = req.response_schema.model_validate_json(raw.text)
        except ValidationError as exc:
            raise AIError(
                "schema", "adapter response failed schema validation"
            ) from exc
    except AIError as exc:
        error = exc
    except anyio.get_cancelled_exc_class():
        latency_ms = int((anyio.current_time() - started) * 1000)
        await _settle_and_log(
            req=req,
            route=route,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            day=day,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
            latency_ms=latency_ms,
            status="error",
            error_type="cancelled",
            retry_count=retries,
            fallback=fallback_flag,
        )
        raise
    except Exception as exc:  # normalize any unexpected bug
        error = AIError("server", str(exc))

    latency_ms = int((anyio.current_time() - started) * 1000)

    if error is not None:
        await _settle_and_log(
            req=req,
            route=route,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            day=day,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
            latency_ms=latency_ms,
            status="error",
            error_type=error.kind,
            retry_count=retries,
            fallback=fallback_flag,
        )
        raise error

    await _settle_and_log(
        req=req,
        route=route,
        estimated_cost=estimated_cost,
        actual_cost=actual_cost,
        day=day,
        provider=provider,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_tokens=cached_tokens,
        latency_ms=latency_ms,
        status="ok",
        error_type=None,
        retry_count=retries,
        fallback=fallback_flag,
    )
    assert data is not None
    return AIResult(
        data=data,
        provider=provider,
        model=model,
        fallback=fallback_flag,
        cost_vnd=actual_cost,
        latency_ms=latency_ms,
    )


def _percentile(sorted_values: list[int], pct: float) -> int:
    if not sorted_values:
        return 0
    rank = math.ceil(pct * len(sorted_values))
    index = min(max(rank - 1, 0), len(sorted_values) - 1)
    return sorted_values[index]


def _fetch_logs_for_range(start: date, end: date) -> list[AIRequestLog]:
    # VN is UTC+7; widen the UTC window by a day on each side so no row near
    # a VN-day boundary is missed, then bucket precisely by VN day below.
    lo = datetime.combine(start, datetime.min.time(), tzinfo=UTC) - timedelta(days=1)
    hi = datetime.combine(end, datetime.min.time(), tzinfo=UTC) + timedelta(days=2)
    with Session(engine) as session:
        statement = select(AIRequestLog).where(
            AIRequestLog.created_at >= lo, AIRequestLog.created_at < hi
        )
        return list(session.exec(statement))


async def usage_summary(start: date, end: date) -> list[UsageRow]:
    """Aggregate `ai_request_log` rows in `[start, end]` (inclusive, by VN
    day) into per-day/provider/model usage rows with p50/p95 latency."""
    rows = await run_sync(lambda: _fetch_logs_for_range(start, end))

    buckets: dict[tuple[date, str, str], list[AIRequestLog]] = defaultdict(list)
    for row in rows:
        day = vn_today(now=row.created_at)
        if day < start or day > end:
            continue
        buckets[(day, row.provider, row.model)].append(row)

    results = []
    for (day, provider, model), items in buckets.items():
        latencies = sorted(item.latency_ms for item in items)
        results.append(
            UsageRow(
                day=day,
                provider=provider,
                model=model,
                requests=len(items),
                errors=sum(1 for item in items if item.status == "error"),
                cost_vnd=sum(item.cost_vnd for item in items),
                p50_ms=_percentile(latencies, 0.50),
                p95_ms=_percentile(latencies, 0.95),
            )
        )
    results.sort(key=lambda r: (r.day, r.provider, r.model))
    return results
