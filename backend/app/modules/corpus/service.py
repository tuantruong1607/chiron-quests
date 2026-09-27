"""Corpus module public entry point (spec §5.1, §5.4).

Every function here does synchronous DB work directly (no async DB engine
exists in this repo - see `ai_gateway.service`'s own sync-DB-write-in-a-
worker-thread pattern). Task 7's async job calls these via
`anyio.to_thread.run_sync` rather than this module offering an async
wrapper itself, keeping exactly one (sync) implementation of each.
"""

import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal, cast

from sqlmodel import Session, delete, select

from app.core.db import engine
from app.modules.corpus.models import EvalRun, HumanLabel, TrainingCorpusItem
from app.modules.corpus.redact import redact
from app.modules.grading.service import GradingOutcome, TaskType

__all__ = [
    "Source",
    "Split",
    "add_item",
    "add_item_and_get_id",
    "add_label",
    "mark_thumbs_down",
    "delete_by_code",
    "purge_expired",
    "labeled_items_for_eval",
    "record_eval_run",
    "LabeledItem",
]

#: Sources that require consent before storage get a delete code (spec
#: §5.1: "Với free_check/paid_user: chỉ khi đồng ý").
Source = Literal["free_check", "volunteer", "synthetic", "paid_user"]
Split = Literal["unassigned", "dev", "test"]

#: Sources whose items are only ever stored with consent, and so get a
#: delete code the person can use to have their data removed.
_CONSENTED_SOURCES: frozenset[str] = frozenset({"free_check", "paid_user"})

#: Items older than this are purged (spec §5.1: "24 tháng").
RETENTION_DAYS = 730

#: Valid human-label scores: 0-10 inclusive, in steps of 0.5.
_VALID_SCORES = {round(i * 0.5, 1) for i in range(21)}


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def _outcome_to_dict(outcome: GradingOutcome) -> dict[str, object]:
    """`GradingOutcome` is a plain dataclass whose `criteria`/`issues`/
    `pii_spans` are pydantic models - `dataclasses.asdict` alone would
    leave those as non-JSON-serializable objects inside the dict, so each
    is dumped with `model_dump()` explicitly."""
    return {
        "raw_score": outcome.raw_score,
        "score": outcome.score,
        "criteria": [c.model_dump() for c in outcome.criteria],
        "issues": [i.model_dump() for i in outcome.issues],
        "pii_spans": [p.model_dump() for p in outcome.pii_spans],
        "rubric_version": outcome.rubric_version,
        "prompt_version": outcome.prompt_version,
        "calibration_version": outcome.calibration_version,
        "provider": outcome.provider,
        "model": outcome.model,
        "fallback": outcome.fallback,
        "latency_ms": outcome.latency_ms,
        "cost_vnd": outcome.cost_vnd,
    }


def add_item(
    source: Source,
    task_type: TaskType,
    prompt: str,
    essay: str,
    outcome: GradingOutcome | None,
    check_id: uuid.UUID | None = None,
    *,
    split: Split = "unassigned",
    dataset_version: str | None = None,
    is_injection: bool = False,
) -> str | None:
    """Redact PII from `prompt`/`essay` (using `outcome.pii_spans` when an
    outcome is given) and store a `training_corpus_item`. Returns a 16-char
    URL-safe delete code (only its sha256 hash is stored) for `free_check`/
    `paid_user`, `None` for any other source.

    `split`/`dataset_version`/`is_injection` are keyword-only, defaulting to
    the item's normal "not yet part of an eval set" values - `import_cli`
    passes them explicitly to place items into the bake-off eval set (spec
    §4.3)."""
    _item_id, delete_code = add_item_and_get_id(
        source,
        task_type,
        prompt,
        essay,
        outcome,
        check_id,
        split=split,
        dataset_version=dataset_version,
        is_injection=is_injection,
    )
    return delete_code


def add_item_and_get_id(
    source: Source,
    task_type: TaskType,
    prompt: str,
    essay: str,
    outcome: GradingOutcome | None,
    check_id: uuid.UUID | None = None,
    *,
    split: Split = "unassigned",
    dataset_version: str | None = None,
    is_injection: bool = False,
) -> tuple[uuid.UUID, str | None]:
    """Same as `add_item`, but also returns the created item's id -
    `import_cli` needs it right away to attach the imported label."""
    pii_spans = outcome.pii_spans if outcome is not None else []
    prompt_redacted = redact(prompt, pii_spans)
    essay_redacted = redact(essay, pii_spans)

    delete_code: str | None = None
    delete_code_hash: str | None = None
    if source in _CONSENTED_SOURCES:
        delete_code = secrets.token_urlsafe(12)
        delete_code_hash = _hash_code(delete_code)

    item = TrainingCorpusItem(
        source=source,
        task_type=task_type,
        prompt_redacted=prompt_redacted,
        essay_redacted=essay_redacted,
        ai_result=_outcome_to_dict(outcome) if outcome is not None else None,
        rubric_version=outcome.rubric_version if outcome is not None else None,
        model=outcome.model if outcome is not None else None,
        check_id=check_id,
        delete_code_hash=delete_code_hash,
        split=split,
        dataset_version=dataset_version,
        is_injection=is_injection,
    )
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        item_id = item.id

    return item_id, delete_code


def add_label(
    item_id: uuid.UUID,
    labeler: str,
    criteria_scores: dict[str, float],
    overall_score: float,
    issue_verdicts: list[bool] | None,
    missed_issues: str,
    notes: str,
) -> None:
    """Store a `human_label` for `item_id`. Every criteria score and the
    overall score must be in [0, 10] in steps of 0.5, and `item_id` must
    name an existing `training_corpus_item` - either violation raises
    `ValueError`."""
    for score in [*criteria_scores.values(), overall_score]:
        if round(score, 1) not in _VALID_SCORES:
            raise ValueError(f"score {score} must be in [0, 10] in steps of 0.5")

    with Session(engine) as session:
        item = session.get(TrainingCorpusItem, item_id)
        if item is None:
            raise ValueError(f"no training_corpus_item with id {item_id}")

        label = HumanLabel(
            item_id=item_id,
            labeler=labeler,
            criteria_scores=criteria_scores,
            overall_score=overall_score,
            issue_verdicts=issue_verdicts,
            missed_issues=missed_issues,
            notes=notes,
        )
        session.add(label)
        session.commit()


def mark_thumbs_down(check_id: uuid.UUID) -> None:
    """Set `thumbs_down=true` on the `training_corpus_item` that `check_id`
    produced, if one exists (a no-op otherwise - the check may not have
    been stored, e.g. no consent)."""
    with Session(engine) as session:
        item = session.exec(
            select(TrainingCorpusItem).where(TrainingCorpusItem.check_id == check_id)
        ).first()
        if item is None:
            return
        item.thumbs_down = True
        session.add(item)
        session.commit()


def delete_by_code(code: str) -> bool:
    """Delete the `training_corpus_item` whose `delete_code_hash` matches
    `code`'s sha256 hash (its `human_label` rows cascade). Returns whether
    an item was found and deleted."""
    code_hash = _hash_code(code)
    with Session(engine) as session:
        item = session.exec(
            select(TrainingCorpusItem).where(
                TrainingCorpusItem.delete_code_hash == code_hash
            )
        ).first()
        if item is None:
            return False
        session.delete(item)
        session.commit()
        return True


def purge_expired(now: datetime) -> int:
    """Delete every `training_corpus_item` older than `RETENTION_DAYS`
    (its `human_label` rows cascade). Returns the number of items deleted."""
    cutoff = now - timedelta(days=RETENTION_DAYS)
    with Session(engine) as session:
        ids = session.exec(
            select(TrainingCorpusItem.id).where(TrainingCorpusItem.created_at < cutoff)
        ).all()
        if not ids:
            return 0
        session.exec(
            delete(TrainingCorpusItem).where(
                TrainingCorpusItem.id.in_(ids)  # type: ignore
            )
        )
        session.commit()
        return len(ids)


@dataclass
class LabeledItem:
    """A plain (detached-safe) snapshot of one `training_corpus_item` and
    its latest `human_label`, for `eval_cli` to grade without holding a DB
    session open across AI calls."""

    id: uuid.UUID
    task_type: TaskType
    prompt_redacted: str
    essay_redacted: str
    is_injection: bool
    overall_score: float


def labeled_items_for_eval(dataset_version: str, split: Split) -> list[LabeledItem]:
    """Return every `training_corpus_item` in `dataset_version`/`split`
    paired with its latest `human_label` (by `created_at`) - `eval_cli`'s
    input set. An item with no label is skipped (nothing to compare
    against)."""
    with Session(engine) as session:
        items = session.exec(
            select(TrainingCorpusItem).where(
                TrainingCorpusItem.dataset_version == dataset_version,
                TrainingCorpusItem.split == split,
            )
        ).all()
        results: list[LabeledItem] = []
        for item in items:
            label = session.exec(
                select(HumanLabel)
                .where(HumanLabel.item_id == item.id)
                .order_by(HumanLabel.created_at.desc())  # type: ignore
            ).first()
            if label is not None:
                results.append(
                    LabeledItem(
                        id=item.id,
                        task_type=cast(TaskType, item.task_type),
                        prompt_redacted=item.prompt_redacted,
                        essay_redacted=item.essay_redacted,
                        is_injection=item.is_injection,
                        overall_score=label.overall_score,
                    )
                )
        return results


def record_eval_run(
    *,
    rubric_version: str,
    prompt_version: str,
    calibration_version: str,
    provider: str,
    model: str,
    dataset_version: str,
    split: Split,
    metrics: dict[str, object],
) -> None:
    """Store one `eval_run` row (spec §5.1)."""
    with Session(engine) as session:
        session.add(
            EvalRun(
                rubric_version=rubric_version,
                prompt_version=prompt_version,
                calibration_version=calibration_version,
                provider=provider,
                model=model,
                dataset_version=dataset_version,
                split=split,
                metrics=metrics,
            )
        )
        session.commit()
