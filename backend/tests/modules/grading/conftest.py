from collections.abc import Sequence

import pytest

from app.modules.ai_gateway import service as ai_service
from app.modules.ai_gateway.types import AIError, AIResult


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class FakeGateway:
    """Stands in for `app.modules.ai_gateway.service.complete()`. Queue
    `AIResult`s and/or `AIError`s with `.returns()`; each call to
    `grade_writing()` that goes through `ai.complete(...)` pops the next
    queued item (raising it if it's an `AIError`) and increments `.calls`.
    The last queued item repeats if the queue is exhausted."""

    def __init__(self) -> None:
        self.calls = 0
        self._queue: list[AIResult | AIError] = []

    def returns(self, items: Sequence[AIResult | AIError]) -> None:
        self._queue = list(items)

    async def _complete(self, req: object) -> AIResult:
        self.calls += 1
        if not self._queue:
            raise AssertionError("FakeGateway: no more queued responses")
        item = self._queue.pop(0)
        if isinstance(item, AIError):
            raise item
        return item


@pytest.fixture
def fake_gateway(monkeypatch: pytest.MonkeyPatch) -> FakeGateway:
    gateway = FakeGateway()
    monkeypatch.setattr(ai_service, "complete", gateway._complete)
    return gateway
