"""Public data shapes for the AI gateway.

These are plain dataclasses (not SQLModel/pydantic tables) because they
never touch the database directly and one of them (`AIRequest`) carries a
`type[BaseModel]`, which is awkward to validate as a pydantic field.
"""

from dataclasses import dataclass
from datetime import date
from typing import Literal

from pydantic import BaseModel

DataClass = Literal["A", "B", "C"]

#: Error kinds a caller of `complete()` can branch on. `rate_limit`,
#: `timeout` and `server` are retried by the gateway; the rest are not.
ErrorKind = Literal[
    "rate_limit",
    "timeout",
    "server",
    "invalid_request",
    "content_filter",
    "schema",
    "budget",
    "no_route",
    "circuit_open",
]

RETRYABLE_KINDS: frozenset[ErrorKind] = frozenset({"rate_limit", "timeout", "server"})


class AIError(Exception):
    """Raised by `complete()` and by `ProviderAdapter.generate_json()`.

    Adapters must normalize every provider-specific failure into one of
    `ErrorKind` before raising this.

    `cost_vnd`/`latency_ms` default to 0 (most kinds - budget, circuit_open,
    no_route, invalid_request, and a retryable kind exhausted without ever
    getting a response - never spent any tokens). `complete()` sets them on
    the `"schema"` kind it raises after an adapter response fails
    validation, since tokens were spent (and billed) on that call even
    though it didn't validate."""

    def __init__(
        self,
        kind: ErrorKind,
        message: str | None = None,
        cost_vnd: int = 0,
        latency_ms: int = 0,
    ) -> None:
        super().__init__(message or kind)
        self.kind: ErrorKind = kind
        self.cost_vnd = cost_vnd
        self.latency_ms = latency_ms


@dataclass
class AIRequest:
    task_key: str
    data_class: DataClass
    system: str
    user: str
    response_schema: type[BaseModel]
    max_output_tokens: int
    correlation_id: str


@dataclass
class AIResult:
    data: BaseModel
    provider: str
    model: str
    fallback: bool
    cost_vnd: int
    latency_ms: int


@dataclass
class RawResponse:
    """What a `ProviderAdapter` returns for one successful call."""

    text: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0


@dataclass
class UsageRow:
    day: date
    provider: str
    model: str
    requests: int
    errors: int
    cost_vnd: int
    p50_ms: int
    p95_ms: int
