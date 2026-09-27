"""`training_corpus_item`, `human_label`, `eval_run` tables (spec §5.1).

Spec deviations (see task-6-report.md for the full rationale):
- `training_corpus_item.check_id` is not in the spec's column list, but is
  needed for `mark_thumbs_down(check_id)` to find the item a `free_check`
  produced.
- `training_corpus_item.is_injection` is not in the spec's column list, but
  is needed by `compute_metrics`'s injection-score check (spec §4.3) and by
  `import_cli`, which reads an optional `is_injection` flag per line for the
  bake-off eval set (spec §4.3 requires at least 2 injection items in it).
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column
from sqlalchemy import DateTime as SADateTime
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class TrainingCorpusItem(SQLModel, table=True):
    __tablename__ = "training_corpus_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    source: str = Field(max_length=20)
    task_type: str = Field(max_length=10)
    prompt_redacted: str
    essay_redacted: str
    ai_result: dict[str, object] | None = Field(default=None, sa_column=Column(JSON))
    rubric_version: str | None = Field(default=None, max_length=50)
    model: str | None = Field(default=None, max_length=100)
    split: str = Field(default="unassigned", max_length=20)
    dataset_version: str | None = Field(default=None, max_length=50)
    thumbs_down: bool = Field(default=False)
    delete_code_hash: str | None = Field(default=None, unique=True, max_length=64)
    # Spec deviation - see module docstring.
    check_id: uuid.UUID | None = Field(default=None, index=True)
    # Spec deviation - see module docstring.
    is_injection: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=SADateTime(timezone=True),  # type: ignore
        index=True,
    )


class HumanLabel(SQLModel, table=True):
    __tablename__ = "human_label"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    item_id: uuid.UUID = Field(
        foreign_key="training_corpus_item.id", ondelete="CASCADE", index=True
    )
    labeler: str = Field(max_length=100)
    criteria_scores: dict[str, float] = Field(sa_column=Column(JSON))
    overall_score: float
    issue_verdicts: list[bool] | None = Field(default=None, sa_column=Column(JSON))
    missed_issues: str = Field(default="")
    notes: str = Field(default="")
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=SADateTime(timezone=True),  # type: ignore
        index=True,
    )


class EvalRun(SQLModel, table=True):
    __tablename__ = "eval_run"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    rubric_version: str = Field(max_length=50)
    prompt_version: str = Field(max_length=50)
    calibration_version: str = Field(max_length=50)
    provider: str = Field(max_length=50)
    model: str = Field(max_length=100)
    dataset_version: str = Field(max_length=50)
    split: str = Field(max_length=20)
    metrics: dict[str, object] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=SADateTime(timezone=True),  # type: ignore
        index=True,
    )
