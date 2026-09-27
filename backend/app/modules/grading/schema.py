"""Strict Pydantic shapes for the writing-grade AI output.

`strict=True` on every model here means a JSON string like `"6.5"` for a
`float` field is rejected outright (Review Focus #4) rather than silently
coerced - the grading pipeline would rather retry/fail than accept a
malformed score.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskType = Literal["task1", "task2"]

PiiKind = Literal["name", "address", "phone", "email", "id", "org"]


class CriterionScore(BaseModel):
    model_config = ConfigDict(strict=True)

    key: str
    score: float = Field(ge=0, le=10)
    comment_vi: str


class Issue(BaseModel):
    model_config = ConfigDict(strict=True)

    quote: str
    explanation_vi: str
    suggestion: str


class PiiSpan(BaseModel):
    model_config = ConfigDict(strict=True)

    text: str
    kind: PiiKind


class WritingGradeOutput(BaseModel):
    """The exact JSON shape the AI gateway must return for `writing_grade`.
    Passed as `AIRequest.response_schema`; validated by `ai_gateway.service`
    via `model_validate_json` and, on failure, surfaced as an
    `AIError("schema")`."""

    model_config = ConfigDict(strict=True)

    criteria: list[CriterionScore]
    issues: list[Issue]
    pii_spans: list[PiiSpan]
