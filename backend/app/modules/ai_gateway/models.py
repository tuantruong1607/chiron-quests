"""`ai_request_log` table (spec §5.1): one row per `complete()` call, never
containing essay/prompt content."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AIRequestLog(SQLModel, table=True):
    __tablename__ = "ai_request_log"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    task_key: str = Field(max_length=100)
    data_class: str = Field(max_length=1)
    provider: str = Field(max_length=50)
    model: str = Field(max_length=100)
    prompt_version: str = Field(max_length=50)
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    cost_vnd: int
    latency_ms: int
    status: str = Field(max_length=10)  # "ok" | "error"
    error_type: str | None = Field(default=None, max_length=50)
    retry_count: int
    fallback: bool
    correlation_id: str = Field(max_length=100)
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=DateTime(timezone=True),  # type: ignore
        index=True,
    )
