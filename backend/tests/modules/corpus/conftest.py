from collections.abc import AsyncGenerator, Generator

import pytest
import redis.asyncio as redis_lib
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine
from app.core.redis import get_redis
from app.modules.ai_gateway import service as ai_service
from app.modules.corpus.models import EvalRun, HumanLabel, TrainingCorpusItem

#: Same db-15 isolation pattern as tests/modules/ai_gateway/conftest.py.
TEST_REDIS_URL = "redis://localhost:6379/15"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def redis(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[redis_lib.Redis]:
    """Point `get_redis()` at a dedicated Redis db (15) and flush it before
    and after each test, so corpus's eval_cli tests (which exercise
    `ai_gateway.service.complete()`, and so its budget reservation) never
    touch the app's real db 0."""
    monkeypatch.setattr(settings, "REDIS_URL", TEST_REDIS_URL)
    get_redis.cache_clear()
    client = get_redis()
    await client.flushdb()
    yield client
    await client.flushdb()
    get_redis.cache_clear()


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Retry backoff must never actually wait in tests."""

    async def _instant_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(ai_service, "_sleep", _instant_sleep)


@pytest.fixture(autouse=True)
def clean_corpus_tables() -> Generator[None]:
    """`training_corpus_item`/`human_label`/`eval_run` live in the real
    Postgres DB (per env-notes.md, no separate test DB); delete this
    module's own rows before and after each test so tests don't see each
    other's rows."""

    def _clean() -> None:
        with Session(engine) as session:
            session.exec(delete(HumanLabel))
            session.exec(delete(EvalRun))
            session.exec(delete(TrainingCorpusItem))
            session.commit()

    _clean()
    yield
    _clean()


@pytest.fixture
def db() -> Generator[Session]:
    with Session(engine) as session:
        yield session
