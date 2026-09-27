import pytest
from sqlmodel import Session, select

from app.modules.ai_gateway.adapters.fake import FakeAdapter
from app.modules.corpus import service
from app.modules.corpus.eval_cli import (
    NoLabeledItemsError,
    _check_thresholds,
    _print_report,
    run_eval,
)
from app.modules.corpus.metrics import EvalMetrics
from app.modules.corpus.models import EvalRun

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _seed_two_items(db: Session) -> None:
    # FakeAdapter's default response quotes "in my opinion i think that"
    # and "peoples" - the essay must actually contain them, or every
    # grading attempt fails quote verification (no_valid_quotes) and the
    # eval never produces a genuine outcome to measure.
    for i in range(2):
        item_id, _ = service.add_item_and_get_id(
            "volunteer",
            "task1",
            f"Prompt {i}",
            f"In my opinion i think that essay {i} is about many peoples.",
            None,
            split="test",
            dataset_version="v0",
        )
        service.add_label(
            item_id,
            labeler="founder",
            criteria_scores={"task_fulfilment": 6.0},
            overall_score=6.0,
            issue_verdicts=None,
            missed_issues="",
            notes="",
        )


async def test_eval_cli_writes_eval_run_and_returns_metrics(
    db: Session, redis, install_fake_adapter
) -> None:
    install_fake_adapter(provider="fake")
    _seed_two_items(db)

    metrics = await run_eval(
        provider="fake",
        model="fake-grader",
        repeat=2,
        dataset_version="v0",
        split="test",
    )

    assert metrics.mae >= 0
    assert 0 <= metrics.consistency_rate <= 1

    run = db.exec(select(EvalRun)).first()
    assert run is not None
    assert run.provider == "fake"
    assert run.model == "fake-grader"
    assert run.dataset_version == "v0"
    assert run.split == "test"
    assert run.metrics["mae"] == pytest.approx(metrics.mae)


async def test_eval_cli_counts_schema_failures_from_grading_failed(
    db: Session, redis, install_fake_adapter
) -> None:
    install_fake_adapter(
        provider="fake", fail_with=["schema", "schema", "schema"]
    )
    _seed_two_items(db)

    metrics = await run_eval(
        provider="fake",
        model="fake-grader",
        repeat=1,
        dataset_version="v0",
        split="test",
    )
    # Every attempt fails schema validation on every retry, so nothing gets
    # a usable outcome and the schema-valid rate must reflect that.
    assert metrics.schema_valid_rate is not None
    assert metrics.schema_valid_rate < 1.0


async def test_eval_cli_refuses_when_no_labeled_items(db: Session, redis) -> None:
    with pytest.raises(NoLabeledItemsError):
        await run_eval(
            provider="fake",
            model="fake-grader",
            repeat=3,
            dataset_version="no-such-version",
            split="test",
        )


async def test_eval_cli_records_real_quote_valid_rate(
    db: Session, redis, install_fake_adapter
) -> None:
    install_fake_adapter(provider="fake")
    _seed_two_items(db)

    metrics = await run_eval(
        provider="fake",
        model="fake-grader",
        repeat=1,
        dataset_version="v0",
        split="test",
    )
    # FakeAdapter's default response includes 2 issues, both with quotes
    # that verify against its own default essay-shaped text is irrelevant
    # here - what matters is quote_valid_rate is computed from real
    # counts, not left at an unmeasured/default value, once there is at
    # least one attempt.
    assert metrics.quote_valid_rate is not None


async def test_eval_cli_never_uses_fallback_provider(
    db: Session, redis, install_fake_adapter, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Even when the underlying route has a configured fallback, eval_cli
    must never silently grade on it - the primary's failures must show up
    as failed repeats, never as a fallback success."""
    from app.modules.ai_gateway import service as ai_service
    from app.modules.ai_gateway.routing import (
        FallbackRoute,
        ProviderConfig,
        RoutingConfig,
        TaskRoute,
    )

    install_fake_adapter(provider="primary", fail_with=["rate_limit"] * 10)
    install_fake_adapter(provider="backup")  # would succeed if ever used

    fallback_routing = RoutingConfig(
        tasks={
            "writing_grade": TaskRoute(
                rubric_version="writing-v1",
                prompt_version="writing-p1",
                active_calibration="writing-c0",
                provider="primary",
                model="primary-model",
                data_class="A",
                fallback=FallbackRoute(provider="backup", model="backup-model"),
            )
        },
        providers={
            "primary": ProviderConfig(no_training=True),
            "backup": ProviderConfig(no_training=True),
        },
    )
    monkeypatch.setattr(ai_service, "load_routing", lambda *a, **k: fallback_routing)

    item_id, _ = service.add_item_and_get_id(
        "volunteer",
        "task1",
        "P",
        "E",
        None,
        split="test",
        dataset_version="v-fallback",
    )
    service.add_label(
        item_id,
        labeler="founder",
        criteria_scores={"task_fulfilment": 6.0},
        overall_score=6.0,
        issue_verdicts=None,
        missed_issues="",
        notes="",
    )

    metrics = await run_eval(
        provider="primary",
        model="primary-model",
        repeat=1,
        dataset_version="v-fallback",
        split="test",
    )

    # Without disabling fallback, the primary's rate_limit failures would
    # transparently retry onto "backup" and succeed with fallback=True;
    # with fallback forced off, every repeat instead fails outright.
    assert metrics.schema_valid_rate == 0.0

    run = db.exec(
        select(EvalRun).where(EvalRun.dataset_version == "v-fallback")
    ).first()
    assert run is not None
    assert run.metrics["fallback_count"] == 0


async def test_eval_run_metrics_include_audit_fields(
    db: Session, redis, install_fake_adapter
) -> None:
    install_fake_adapter(provider="fake")
    _seed_two_items(db)

    await run_eval(
        provider="fake",
        model="fake-grader",
        repeat=2,
        dataset_version="v0",
        split="test",
    )
    run = db.exec(select(EvalRun)).first()
    assert run is not None
    assert run.metrics["n_items"] == 2
    assert len(run.metrics["item_ids"]) == 2
    assert run.metrics["attempts"] == 4  # 2 items * repeat=2
    assert run.metrics["schema_failures"] == 0
    assert run.metrics["fallback_count"] == 0


def test_print_report_shows_not_measured_and_incomplete_when_unmeasured(
    capsys: pytest.CaptureFixture[str],
) -> None:
    metrics = EvalMetrics(
        mae=0.5,
        consistency_rate=None,
        quote_valid_rate=None,
        schema_valid_rate=1.0,
        p95_latency_ms=1000,
        avg_cost_vnd=100.0,
        injection_ok=True,
    )
    _print_report(metrics)
    out = capsys.readouterr().out
    assert out.count("N/A (not measured)") == 2
    assert "Overall: INCOMPLETE" in out


def test_check_thresholds_never_passes_a_none_metric():
    metrics = EvalMetrics(
        mae=None,  # type: ignore[arg-type]
        consistency_rate=1.0,
        quote_valid_rate=1.0,
        schema_valid_rate=1.0,
        p95_latency_ms=1000,
        avg_cost_vnd=100.0,
        injection_ok=True,
    )
    passed, incomplete = _check_thresholds(metrics)
    assert passed["mae"] is False
    assert incomplete is True


@pytest.fixture
def install_fake_adapter(monkeypatch: pytest.MonkeyPatch):
    from app.modules.ai_gateway import service as ai_service

    def _install(provider: str = "fake", **kwargs: object) -> FakeAdapter:
        adapter = FakeAdapter(**kwargs)  # type: ignore[arg-type]
        monkeypatch.setitem(ai_service.ADAPTER_REGISTRY, provider, lambda: adapter)
        return adapter

    return _install
