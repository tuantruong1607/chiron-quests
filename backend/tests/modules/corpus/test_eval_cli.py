import pytest
from sqlmodel import Session, select

from app.modules.ai_gateway.adapters.fake import FakeAdapter
from app.modules.corpus import service
from app.modules.corpus.eval_cli import run_eval
from app.modules.corpus.models import EvalRun

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _seed_two_items(db: Session) -> None:
    for i in range(2):
        item_id, _ = service.add_item_and_get_id(
            "volunteer",
            "task1",
            f"Prompt {i}",
            f"Essay body {i}",
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
    assert metrics.schema_valid_rate < 1.0


@pytest.fixture
def install_fake_adapter(monkeypatch: pytest.MonkeyPatch):
    from app.modules.ai_gateway import service as ai_service

    def _install(provider: str = "fake", **kwargs: object) -> FakeAdapter:
        adapter = FakeAdapter(**kwargs)  # type: ignore[arg-type]
        monkeypatch.setitem(ai_service.ADAPTER_REGISTRY, provider, lambda: adapter)
        return adapter

    return _install
