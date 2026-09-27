from collections.abc import AsyncGenerator, Callable, Generator

import pytest
import redis.asyncio as redis_lib
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine
from app.core.redis import get_redis
from app.modules.ai_gateway import breaker, service
from app.modules.ai_gateway.adapters.fake import FakeAdapter
from app.modules.ai_gateway.models import AIRequestLog

# Same db-15 isolation pattern as tests/modules/guard/conftest.py, kept local
# to this package rather than shared so guard's own tests are untouched.
TEST_REDIS_URL = "redis://localhost:6379/15"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def redis(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[redis_lib.Redis]:
    """Point `get_redis()` at a dedicated Redis db (15) and flush it before
    and after each test, so ai_gateway tests never touch the app's real
    db 0."""
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

    monkeypatch.setattr(service, "_sleep", _instant_sleep)


@pytest.fixture(autouse=True)
def clean_ai_request_log() -> Generator[None]:
    """`ai_request_log` lives in the real Postgres DB (per env-notes.md, no
    separate test DB); delete this module's own rows before and after each
    test so tests don't see each other's log rows."""
    with Session(engine) as session:
        session.exec(delete(AIRequestLog))
        session.commit()
    yield
    with Session(engine) as session:
        session.exec(delete(AIRequestLog))
        session.commit()


class Clock:
    """A controllable stand-in for `breaker.now`, installed by the `clock`
    fixture."""

    def __init__(self) -> None:
        self._t = 1_700_000_000.0

    def __call__(self) -> float:
        return self._t

    @property
    def t(self) -> float:
        return self._t

    def advance(self, seconds: float) -> None:
        self._t += seconds


@pytest.fixture
def clock(monkeypatch: pytest.MonkeyPatch) -> Clock:
    c = Clock()
    monkeypatch.setattr(breaker, "now", c)
    return c


@pytest.fixture
def install_fake_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., FakeAdapter]:
    """Register a `FakeAdapter` (built from the given kwargs) as the
    adapter for `provider` (default "fake"), returning it so the test can
    inspect `.calls`."""

    def _install(provider: str = "fake", **kwargs: object) -> FakeAdapter:
        adapter = FakeAdapter(**kwargs)  # type: ignore[arg-type]
        monkeypatch.setitem(service.ADAPTER_REGISTRY, provider, lambda: adapter)
        return adapter

    return _install
