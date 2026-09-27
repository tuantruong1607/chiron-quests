"""`analytics_event` table (spec §5.1): one row per funnel event, keyed by
`src` (marketing/community source tag) and a stable `visitor_hash` (never
the raw visitor id - see `app.modules.guard.service.hash_visitor`).
Retention: 90 days (`purge_events`)."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Column, Index
from sqlalchemy import DateTime as SADateTime
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class AnalyticsEvent(SQLModel, table=True):
    __tablename__ = "analytics_event"
    __table_args__ = (
        Index("ix_analytics_event_event_created_at", "event", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    event: str = Field(max_length=20)
    visitor_hash: str = Field(max_length=64)
    src: str | None = Field(default=None, max_length=64)
    check_id: uuid.UUID | None = Field(default=None)
    props: dict[str, object] | None = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_type=SADateTime(timezone=True),  # type: ignore
        index=True,
    )
