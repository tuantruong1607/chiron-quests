import hashlib
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlmodel import Session, select

from app.modules.corpus import service
from app.modules.corpus.models import HumanLabel, TrainingCorpusItem
from app.modules.grading.service import GradingOutcome, PiiSpan

P = "Write about your hometown."
ESSAY_WITH_NAME = "My name is Nam and I live in Hanoi. Call me at 0912 345 678."


def outcome(pii: list[PiiSpan] | None = None) -> GradingOutcome:
    return GradingOutcome(
        raw_score=6.0,
        score=6.0,
        criteria=[],
        issues=[],
        pii_spans=pii or [],
        rubric_version="writing-v1",
        prompt_version="writing-p1",
        calibration_version="writing-c0",
        provider="fake",
        model="fake-grader",
        fallback=False,
        latency_ms=1000,
        cost_vnd=100,
    )


def latest_item(db: Session) -> TrainingCorpusItem | None:
    return db.exec(
        select(TrainingCorpusItem).order_by(TrainingCorpusItem.created_at.desc())
    ).first()


def test_store_and_delete_by_code(db: Session):
    code = service.add_item(
        "free_check",
        "task1",
        P,
        ESSAY_WITH_NAME,
        outcome(pii=[PiiSpan(text="Nam", kind="name")]),
    )
    item = latest_item(db)
    assert item is not None
    assert "Nam" not in item.essay_redacted
    assert "[SĐT]" in item.essay_redacted
    assert code is not None and len(code) == 16
    assert item.delete_code_hash != code
    assert item.delete_code_hash == hashlib.sha256(code.encode()).hexdigest()

    assert service.delete_by_code(code) is True
    assert latest_item(db) is None


def test_delete_by_code_wrong_code_returns_false(db: Session):
    service.add_item("free_check", "task1", P, ESSAY_WITH_NAME, outcome())
    assert service.delete_by_code("not-the-real-code!") is False
    assert latest_item(db) is not None


def test_add_item_returns_none_delete_code_for_volunteer_and_synthetic(db: Session):
    for source in ("volunteer", "synthetic"):
        code = service.add_item(source, "task1", P, ESSAY_WITH_NAME, outcome())
        assert code is None
        item = latest_item(db)
        assert item is not None
        assert item.delete_code_hash is None


def test_add_item_stores_ai_result_and_none_outcome(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    item = latest_item(db)
    assert item is not None
    assert item.ai_result is not None
    assert item.ai_result["score"] == 6.0
    assert item.rubric_version == "writing-v1"
    assert item.model == "fake-grader"

    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, None)
    item2 = latest_item(db)
    assert item2 is not None
    assert item2.ai_result is None
    assert item2.rubric_version is None


def test_add_item_stores_check_id(db: Session):
    check_id = uuid.uuid4()
    service.add_item(
        "free_check", "task1", P, ESSAY_WITH_NAME, outcome(), check_id=check_id
    )
    item = latest_item(db)
    assert item is not None
    assert item.check_id == check_id


def test_add_label_valid(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    item = latest_item(db)
    assert item is not None
    service.add_label(
        item.id,
        labeler="founder",
        criteria_scores={"task_fulfilment": 6.5, "organization": 7.0},
        overall_score=6.5,
        issue_verdicts=[True, False],
        missed_issues="missed a comma splice",
        notes="solid essay",
    )
    label = db.exec(select(HumanLabel).where(HumanLabel.item_id == item.id)).first()
    assert label is not None
    assert label.overall_score == 6.5
    assert label.criteria_scores == {"task_fulfilment": 6.5, "organization": 7.0}
    assert label.issue_verdicts == [True, False]


def test_add_label_rejects_score_not_multiple_of_half(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    item = latest_item(db)
    assert item is not None
    with pytest.raises(ValueError):
        service.add_label(
            item.id,
            labeler="founder",
            criteria_scores={"task_fulfilment": 6.3},
            overall_score=6.5,
            issue_verdicts=None,
            missed_issues="",
            notes="",
        )
    with pytest.raises(ValueError):
        service.add_label(
            item.id,
            labeler="founder",
            criteria_scores={"task_fulfilment": 6.5},
            overall_score=6.3,
            issue_verdicts=None,
            missed_issues="",
            notes="",
        )


def test_add_label_rejects_score_out_of_range(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    item = latest_item(db)
    assert item is not None
    with pytest.raises(ValueError):
        service.add_label(
            item.id,
            labeler="founder",
            criteria_scores={"task_fulfilment": 10.5},
            overall_score=6.5,
            issue_verdicts=None,
            missed_issues="",
            notes="",
        )


def test_add_label_rejects_missing_item(db: Session):
    with pytest.raises(ValueError):
        service.add_label(
            uuid.uuid4(),
            labeler="founder",
            criteria_scores={"task_fulfilment": 6.5},
            overall_score=6.5,
            issue_verdicts=None,
            missed_issues="",
            notes="",
        )


def test_mark_thumbs_down_sets_flag_when_check_id_matches(db: Session):
    check_id = uuid.uuid4()
    service.add_item(
        "free_check", "task1", P, ESSAY_WITH_NAME, outcome(), check_id=check_id
    )
    service.mark_thumbs_down(check_id)
    item = latest_item(db)
    assert item is not None
    assert item.thumbs_down is True


def test_mark_thumbs_down_is_noop_when_no_item_for_check_id(db: Session):
    service.mark_thumbs_down(uuid.uuid4())  # must not raise


def test_purge_expired_deletes_old_items_and_cascades_labels(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    item = latest_item(db)
    assert item is not None
    item_id = item.id
    service.add_label(
        item_id,
        labeler="founder",
        criteria_scores={"task_fulfilment": 6.5},
        overall_score=6.5,
        issue_verdicts=None,
        missed_issues="",
        notes="",
    )
    old_created_at = datetime.now(UTC) - timedelta(days=800)
    db.exec(
        TrainingCorpusItem.__table__.update()
        .where(TrainingCorpusItem.id == item_id)
        .values(created_at=old_created_at)
    )
    db.commit()

    deleted_count = service.purge_expired(datetime.now(UTC))
    assert deleted_count == 1
    assert latest_item(db) is None
    assert (
        db.exec(select(HumanLabel).where(HumanLabel.item_id == item_id)).first()
        is None
    )


def test_purge_expired_keeps_recent_items(db: Session):
    service.add_item("volunteer", "task1", P, ESSAY_WITH_NAME, outcome())
    deleted_count = service.purge_expired(datetime.now(UTC))
    assert deleted_count == 0
    assert latest_item(db) is not None
