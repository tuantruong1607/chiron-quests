from collections.abc import AsyncGenerator

import pytest
import redis.asyncio as redis_lib

from app.core.config import settings
from app.core.redis import get_redis

TEST_REDIS_URL = "redis://localhost:6379/15"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def redis(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[redis_lib.Redis]:
    """Point `get_redis()` at a dedicated Redis db (15) and flush it before
    and after each test, so guard tests never touch the app's real db 0."""
    monkeypatch.setattr(settings, "REDIS_URL", TEST_REDIS_URL)
    get_redis.cache_clear()
    client = get_redis()
    await client.flushdb()
    yield client
    await client.flushdb()
    get_redis.cache_clear()


@pytest.fixture
def outbox(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    """Capture calls to `guard.budget.send_alert` instead of sending email."""
    sent: list[tuple[str, str]] = []

    def fake_send_alert(subject: str, body: str) -> None:
        sent.append((subject, body))

    monkeypatch.setattr("app.modules.guard.budget.send_alert", fake_send_alert)
    return sent
