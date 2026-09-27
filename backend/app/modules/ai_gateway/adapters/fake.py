"""A local, no-network stand-in for a real provider adapter.

Used whenever `settings.AI_FAKE_PROVIDER` is set (so nothing in this repo
ever calls a real LLM SDK from tests/CI) and directly by tests that need to
script specific successes/failures.
"""

import json
import random

import anyio

from app.modules.ai_gateway.types import AIError, ErrorKind, RawResponse

#: Default response when `responses` is None. Shaped for the `writing_grade`
#: task (Task 5 will align its Pydantic schema to this shape). Kept as one
#: constant so the shape only needs updating in one place.
DEFAULT_WRITING_GRADE_RESPONSE = json.dumps(
    {
        "criteria": {
            "task_fulfilment": 6.0,
            "organization": 6.5,
            "vocabulary": 6.0,
            "grammar": 5.5,
        },
        "issues": [
            {"quote": "in my opinion i think that", "note": "redundant phrasing"},
            {"quote": "peoples", "note": "should be 'people'"},
        ],
        "pii_spans": [],
    }
)


class FakeAdapter:
    """`ProviderAdapter` implementation with no real network calls.

    `responses[i]` (or the fixed default) is returned on the i-th call;
    `fail_with[i]` (an `ErrorKind`), if present at that index, is raised
    instead. `latency_s` is a `(min, max)` seconds range slept before
    returning/raising, to simulate real-world latency.
    """

    def __init__(
        self,
        latency_s: tuple[float, float] = (0.0, 0.0),
        responses: list[str] | None = None,
        fail_with: list[ErrorKind] | None = None,
    ) -> None:
        self.latency_s = latency_s
        self.responses = responses
        self.fail_with = fail_with or []
        self.calls = 0

    async def generate_json(
        self,
        model: str,
        system: str,
        user: str,
        schema: dict[str, object],
        max_output_tokens: int,
        timeout_s: float,
    ) -> RawResponse:
        index = self.calls
        self.calls += 1

        lo, hi = self.latency_s
        if hi > 0:
            await anyio.sleep(random.uniform(lo, hi))

        if index < len(self.fail_with):
            raise AIError(self.fail_with[index])

        if self.responses is not None:
            text = (
                self.responses[index]
                if index < len(self.responses)
                else self.responses[-1]
            )
        else:
            text = DEFAULT_WRITING_GRADE_RESPONSE

        input_tokens = max(1, (len(system) + len(user)) // 4)
        output_tokens = min(max_output_tokens, max(1, len(text) // 4))
        return RawResponse(
            text=text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=0,
        )
