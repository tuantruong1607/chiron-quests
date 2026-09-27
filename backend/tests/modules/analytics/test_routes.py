from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.modules.analytics.models import AnalyticsEvent
from app.modules.guard.service import hash_visitor


def test_frontend_can_post_tool_view_event(client: TestClient, db: Session) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": "raw-visitor-abc", "src": "fb-ads"},
    )

    assert response.status_code == 204
    row = db.exec(select(AnalyticsEvent)).one()
    assert row.event == "tool_view"
    assert row.src == "fb-ads"


def test_raw_visitor_id_is_never_stored(client: TestClient, db: Session) -> None:
    raw_visitor_id = "raw-visitor-abc"
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": raw_visitor_id},
    )

    assert response.status_code == 204
    row = db.exec(select(AnalyticsEvent)).one()
    assert row.visitor_hash != raw_visitor_id
    assert raw_visitor_id not in row.visitor_hash
    assert row.visitor_hash == hash_visitor(raw_visitor_id)


def test_frontend_cannot_post_submit_event(client: TestClient, db: Session) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "submit", "visitor_id": "v1"},
    )

    assert response.status_code == 422
    assert db.exec(select(AnalyticsEvent)).first() is None


def test_frontend_cannot_post_result_view_event(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "result_view", "visitor_id": "v1"},
    )

    assert response.status_code == 422


def test_props_over_key_limit_is_rejected(client: TestClient, db: Session) -> None:
    props = {f"k{i}": i for i in range(21)}
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": "v1", "props": props},
    )

    assert response.status_code == 422
    assert db.exec(select(AnalyticsEvent)).first() is None


def test_props_within_key_limit_is_accepted(client: TestClient) -> None:
    props = {f"k{i}": i for i in range(20)}
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": "v1", "props": props},
    )

    assert response.status_code == 204


def test_props_over_byte_limit_is_rejected(client: TestClient, db: Session) -> None:
    props = {"blob": "x" * 3000}
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": "v1", "props": props},
    )

    assert response.status_code == 422
    assert db.exec(select(AnalyticsEvent)).first() is None


def test_src_over_max_length_is_rejected(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "tool_view", "visitor_id": "v1", "src": "s" * 65},
    )

    assert response.status_code == 422


def test_unknown_event_kind_is_rejected(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/events",
        json={"event": "bogus", "visitor_id": "v1"},
    )

    assert response.status_code == 422
