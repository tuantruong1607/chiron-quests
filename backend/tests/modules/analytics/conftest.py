from collections.abc import Generator

import pytest
from sqlmodel import Session, delete

from app.core.db import engine
from app.modules.analytics.models import AnalyticsEvent


@pytest.fixture(autouse=True)
def clean_analytics_events() -> Generator[None]:
    """`analytics_event` lives in the real Postgres DB (per env-notes.md, no
    separate test DB); delete this module's own rows before and after each
    test so tests don't see each other's rows."""

    def _clean() -> None:
        with Session(engine) as session:
            session.exec(delete(AnalyticsEvent))
            session.commit()

    _clean()
    yield
    _clean()


@pytest.fixture
def db() -> Generator[Session]:
    with Session(engine) as session:
        yield session
