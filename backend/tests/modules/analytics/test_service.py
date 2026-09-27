import uuid
from datetime import UTC, date, datetime, timedelta

from sqlmodel import Session, select

from app.modules.analytics import service
from app.modules.analytics.models import AnalyticsEvent


def _insert(
    session: Session,
    event: str,
    visitor_hash: str,
    src: str | None,
    created_at: datetime,
) -> None:
    session.add(
        AnalyticsEvent(
            event=event,
            visitor_hash=visitor_hash,
            src=src,
            created_at=created_at,
        )
    )
    session.commit()


def test_record_event_stores_all_five_kinds(db: Session) -> None:
    for event in ["tool_view", "submit", "result_view", "share_click", "signup_click"]:
        service.record_event(event, "hash-1", "fb-ads", check_id=None, props=None)

    rows = db.exec(select(AnalyticsEvent)).all()
    assert {row.event for row in rows} == {
        "tool_view",
        "submit",
        "result_view",
        "share_click",
        "signup_click",
    }
    assert all(row.src == "fb-ads" for row in rows)


def test_record_event_stores_check_id_and_props(db: Session) -> None:
    check_id = uuid.uuid4()
    service.record_event(
        "result_view", "hash-1", "fb-ads", check_id=check_id, props={"score": 6.5}
    )
    row = db.exec(select(AnalyticsEvent)).one()
    assert row.check_id == check_id
    assert row.props == {"score": 6.5}


def test_funnel_counts_by_src(db: Session) -> None:
    now = datetime(2026, 6, 1, 3, 0, tzinfo=UTC)  # 10:00 VN time
    _insert(db, "tool_view", "v1", "fb-ads", now)
    _insert(db, "tool_view", "v2", "fb-ads", now)
    _insert(db, "submit", "v1", "fb-ads", now)
    _insert(db, "tool_view", "v3", "zalo", now)

    rows = {row.src: row for row in service.funnel(date(2026, 6, 1), date(2026, 6, 1))}

    assert rows["fb-ads"].tool_view == 2
    assert rows["fb-ads"].submit == 1
    assert rows["fb-ads"].result_view == 0
    assert rows["zalo"].tool_view == 1
    assert rows["zalo"].submit == 0


def test_funnel_groups_missing_src_as_direct(db: Session) -> None:
    now = datetime(2026, 6, 1, 3, 0, tzinfo=UTC)
    _insert(db, "tool_view", "v1", None, now)

    rows = {row.src: row for row in service.funnel(date(2026, 6, 1), date(2026, 6, 1))}

    assert "(direct)" in rows
    assert rows["(direct)"].tool_view == 1


def test_funnel_counts_distinct_visitors_not_raw_events(db: Session) -> None:
    now = datetime(2026, 6, 1, 3, 0, tzinfo=UTC)
    # Same visitor pings tool_view three times - should count once.
    for _ in range(3):
        _insert(db, "tool_view", "v1", "fb-ads", now)

    rows = {row.src: row for row in service.funnel(date(2026, 6, 1), date(2026, 6, 1))}

    assert rows["fb-ads"].tool_view == 1


def test_funnel_vn_date_boundary(db: Session) -> None:
    # 2026-10-01 17:30 UTC is 2026-10-02 00:30 in Vietnam (UTC+7): must
    # count on the VN date, not the UTC date.
    boundary = datetime(2026, 10, 1, 17, 30, tzinfo=UTC)
    _insert(db, "tool_view", "v1", "fb-ads", boundary)

    on_utc_date = service.funnel(date(2026, 10, 1), date(2026, 10, 1))
    on_vn_date = service.funnel(date(2026, 10, 2), date(2026, 10, 2))

    assert all(row.tool_view == 0 for row in on_utc_date)
    assert any(row.src == "fb-ads" and row.tool_view == 1 for row in on_vn_date)


def test_funnel_window_is_inclusive_on_both_ends(db: Session) -> None:
    start_of_window = datetime(2026, 6, 1, 3, 0, tzinfo=UTC)  # VN 2026-06-01
    end_of_window = datetime(2026, 6, 3, 3, 0, tzinfo=UTC)  # VN 2026-06-03
    outside_window = datetime(2026, 6, 4, 3, 0, tzinfo=UTC)  # VN 2026-06-04
    _insert(db, "tool_view", "v1", "fb-ads", start_of_window)
    _insert(db, "tool_view", "v2", "fb-ads", end_of_window)
    _insert(db, "tool_view", "v3", "fb-ads", outside_window)

    rows = {
        row.src: row for row in service.funnel(date(2026, 6, 1), date(2026, 6, 3))
    }

    assert rows["fb-ads"].tool_view == 2


def test_purge_older_than_90_days(db: Session) -> None:
    now = datetime(2026, 6, 1, tzinfo=UTC)
    old = now - timedelta(days=91)
    boundary = now - timedelta(days=90, seconds=1)
    recent = now - timedelta(days=10)
    _insert(db, "tool_view", "v1", "fb-ads", old)
    _insert(db, "tool_view", "v2", "fb-ads", boundary)
    _insert(db, "tool_view", "v3", "fb-ads", recent)

    deleted = service.purge_events(now)

    assert deleted == 2
    remaining = db.exec(select(AnalyticsEvent)).all()
    assert [row.visitor_hash for row in remaining] == ["v3"]


def test_purge_returns_zero_when_nothing_to_delete(db: Session) -> None:
    now = datetime(2026, 6, 1, tzinfo=UTC)
    _insert(db, "tool_view", "v1", "fb-ads", now - timedelta(days=10))

    assert service.purge_events(now) == 0
