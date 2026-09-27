"""The interface every provider adapter (fake now, real ones in Task 13)
must implement. Adapters normalize provider-specific failures to `AIError`.
"""

from typing import Protocol

from app.modules.ai_gateway.types import RawResponse


class ProviderAdapter(Protocol):
    async def generate_json(
        self,
        model: str,
        system: str,
        user: str,
        schema: dict[str, object],
        max_output_tokens: int,
        timeout_s: float,
    ) -> RawResponse: ...
