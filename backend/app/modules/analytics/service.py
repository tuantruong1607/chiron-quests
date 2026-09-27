"""Analytics module public entry point (spec §5.1, §3 step 8): funnel
events by `src`.

`record_event` accepts all five event kinds and a caller-supplied
`visitor_hash` (already hashed - this module never sees a raw visitor id).
`app.modules.analytics.routes` is the only caller that hashes a raw id, via
`app.modules.guard.service.hash_visitor`; server-triggered events
(`submit`/`result_view`, from Task 7's free_tools API) call `record_event`
directly with the hash it already computed for its own guard checks."""

import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Literal

from sqlalchemy import Date, cast, func
from sqlmodel import Session, delete, select

from app.core.db import engine
from app.modules.analytics.models import AnalyticsEvent

__all__ = [
    "EventKind",
    "FunnelRow",
    "record_event",
    "funnel",
    "purge_events",
    "RETENTION_DAYS",
]

EventKind = Literal["tool_view", "submit", "result_view", "share_click", "signup_click"]

#: Rows older than this are purged (spec §5.1: "90 ngày").
RETENTION_DAYS = 90

#: `funnel`'s bucketing timezone (spec §3: events are analysed by VN date).
_VN_TZ = "Asia/Ho_Chi_Minh"

#: Label used for events with no `src` (spec: group by `coalesce(src, ...)`).
_DIRECT_SRC = "(direct)"


@dataclass
class FunnelRow:
    """One row of `funnel`'s result: DISTINCT visitor counts per event kind,
    for one `src` value."""

    src: str
    tool_view: int
    submit: int
    result_view: int
    share_click: int
    signup_click: int


def record_event(
    event: EventKind,
    visitor_hash: str,
    src: str | None,
    check_id: uuid.UUID | None = None,
    props: dict[str, object] | None = None,
) -> None:
    """Store one `analytics_event` row. Accepts all five event kinds (the
    frontend-facing `POST /api/v1/events` route restricts itself to
    `tool_view`/`share_click`/`signup_click`; `submit`/`result_view` are
    only ever recorded server-side by `free_tools`)."""
    with Session(engine) as session:
        session.add(
            AnalyticsEvent(
                event=event,
                visitor_hash=visitor_hash,
                src=src,
                check_id=check_id,
                props=props,
            )
        )
        session.commit()


def funnel(start: date, end: date) -> list[FunnelRow]:
    """Return one `FunnelRow` per distinct `src` (missing/NULL `src`
    grouped under `"(direct)"`), counting events in `[start, end]`
    (inclusive on both ends).

    Dates are bucketed by the **Asia/Ho_Chi_Minh calendar date** of each
    event's `created_at` (stored in UTC) - e.g. an event stored at
    2026-10-01 17:30 UTC is 2026-10-02 00:30 in Vietnam, so it counts
    against 2026-10-02, not 2026-10-01.

    Each event-kind count is the number of **distinct visitors**
    (`COUNT(DISTINCT visitor_hash)`) who fired that event in the window,
    not the raw number of events - this makes `funnel` a funnel of
    *people* moving from `tool_view` to `submit` to ... , where a visitor
    who pings `tool_view` twice (e.g. a page reload) still counts once at
    each stage instead of inflating the top of the funnel.
    """
    vn_date = cast(func.timezone(_VN_TZ, AnalyticsEvent.created_at), Date)
    src_expr = func.coalesce(AnalyticsEvent.src, _DIRECT_SRC)

    with Session(engine) as session:
        rows = session.exec(
            select(
                src_expr.label("src"),
                AnalyticsEvent.event,
                func.count(func.distinct(AnalyticsEvent.visitor_hash)),
            )
            .where(vn_date >= start, vn_date <= end)
            .group_by(src_expr, AnalyticsEvent.event)
        ).all()

    counts: dict[str, dict[str, int]] = {}
    for src, event, count in rows:
        counts.setdefault(src, {})[event] = count

    return [
        FunnelRow(
            src=src,
            tool_view=per_event.get("tool_view", 0),
            submit=per_event.get("submit", 0),
            result_view=per_event.get("result_view", 0),
            share_click=per_event.get("share_click", 0),
            signup_click=per_event.get("signup_click", 0),
        )
        for src, per_event in sorted(counts.items())
    ]


def purge_events(now: datetime) -> int:
    """Delete every `analytics_event` older than `RETENTION_DAYS`. Returns
    the number of rows deleted."""
    cutoff = now - timedelta(days=RETENTION_DAYS)
    with Session(engine) as session:
        ids = session.exec(
            select(AnalyticsEvent.id).where(AnalyticsEvent.created_at < cutoff)
        ).all()
        if not ids:
            return 0
        session.exec(
            delete(AnalyticsEvent).where(AnalyticsEvent.id.in_(ids))  # type: ignore
        )
        session.commit()
        return len(ids)
