"""Grading module public entry point.

Other modules (Task 6's corpus tooling, Task 7's `free_tools` grading job)
must import this module only via `app.modules.grading.service`, per the
module-boundary rule.
"""

from dataclasses import dataclass
from statistics import mean

from app.modules.ai_gateway import service as ai
from app.modules.grading.evidence import normalize_for_match, verify_quotes
from app.modules.grading.prompts import build_writing_prompt, load_rubric
from app.modules.grading.schema import (
    CriterionScore,
    Issue,
    PiiSpan,
    TaskType,
    WritingGradeOutput,
)
from app.modules.grading.scoring import apply_calibration, round_half

__all__ = [
    "TaskType",
    "PiiSpan",
    "CriterionScore",
    "Issue",
    "GradingOutcome",
    "GradingFailed",
    "grade_writing",
    "apply_calibration",
    "round_half",
    "verify_quotes",
    "normalize_for_match",
    "build_writing_prompt",
    "load_rubric",
]

#: Total AI calls for one `grade_writing()` invocation: 1 initial attempt
#: plus at most this many content retries (schema failure, or every issue's
#: quote failing verification).
MAX_CONTENT_RETRIES = 2
MAX_ISSUES = 3

#: writing-v1's four criteria - the exact set of `criteria[].key` values the
#: model must return (no more, no fewer) for both task1 and task2. A
#: mismatch (missing/extra key) is treated as a schema failure and retried
#: the same as an `AIError("schema")`.
RUBRIC_CRITERION_KEYS = frozenset(
    {"task_fulfilment", "organization", "vocabulary", "grammar"}
)


class GradingFailed(Exception):
    """Raised by `grade_writing()` once content retries are exhausted, or
    immediately for a non-content `AIError` (budget, circuit_open, timeout,
    etc.). `reason` is the underlying `AIError.kind`, or a grading-specific
    reason (`"no_valid_quotes"`, `"bad_criteria"`) for a content failure."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass
class GradingOutcome:
    raw_score: float
    score: float
    criteria: list[CriterionScore]
    issues: list[Issue]
    pii_spans: list[PiiSpan]
    rubric_version: str
    prompt_version: str
    calibration_version: str
    provider: str
    model: str
    fallback: bool
    latency_ms: int
    cost_vnd: int
    #: Quote-verification counts, summed across every attempt that reached
    #: `verify_quotes()` (schema-valid, criteria-valid responses only) -
    #: Task 6's `eval_cli` needs these to compute a real `quote_valid_rate`
    #: (spec §4.3), since only the already-filtered valid issues survive
    #: on `issues` above.
    quotes_total: int = 0
    quotes_valid: int = 0


def _has_valid_criteria_keys(output: WritingGradeOutput) -> bool:
    keys = [c.key for c in output.criteria]
    return (
        len(keys) == len(RUBRIC_CRITERION_KEYS) and set(keys) == RUBRIC_CRITERION_KEYS
    )


async def grade_writing(
    task_type: TaskType, prompt: str, essay: str, correlation_id: str
) -> GradingOutcome:
    """Grade one writing submission via the AI gateway, retrying up to
    `MAX_CONTENT_RETRIES` times on a content failure (schema-invalid output,
    a wrong set of criterion keys, or every reported issue's quote failing
    `verify_quotes`), then raising `GradingFailed`. Any other `AIError`
    (budget, circuit_open, timeout after the gateway's own retries, ...)
    raises `GradingFailed` immediately, with no content retry.

    `cost_vnd`/`latency_ms` on the returned outcome are the *sum* across
    every AI call, whether it returned an `AIResult` (including one later
    retried for failing quote/criteria verification) or raised an
    `AIError` that itself spent tokens (a `"schema"` failure - the gateway
    attaches that call's cost/latency to the exception). A non-content
    `AIError` that never reached a provider response (budget,
    circuit_open, no_route, ...) carries `cost_vnd=latency_ms=0` and so
    adds nothing."""
    route = ai.task_config("writing_grade")
    rubric = load_rubric(route.rubric_version)
    messages = build_writing_prompt(task_type, prompt, essay, rubric)

    total_cost_vnd = 0
    total_latency_ms = 0
    total_quotes_total = 0
    total_quotes_valid = 0
    provider = route.provider
    model = route.model
    fallback = False

    attempt = 0
    while True:
        attempt += 1
        request = ai.AIRequest(
            task_key="writing_grade",
            data_class=route.data_class,
            system=messages.system,
            user=messages.user,
            response_schema=WritingGradeOutput,
            max_output_tokens=1500,
            correlation_id=correlation_id,
        )
        try:
            result = await ai.complete(request)
        except ai.AIError as exc:
            # A schema failure still spent tokens on that call (the gateway
            # attaches their cost/latency to the exception itself, since it
            # never produced an `AIResult` to carry them on).
            total_cost_vnd += exc.cost_vnd
            total_latency_ms += exc.latency_ms
            if exc.kind == "schema" and attempt <= MAX_CONTENT_RETRIES:
                continue
            raise GradingFailed(reason=exc.kind) from exc

        total_cost_vnd += result.cost_vnd
        total_latency_ms += result.latency_ms
        provider, model, fallback = result.provider, result.model, result.fallback

        output = result.data
        assert isinstance(output, WritingGradeOutput)

        if not _has_valid_criteria_keys(output):
            if attempt <= MAX_CONTENT_RETRIES:
                continue
            raise GradingFailed(reason="bad_criteria")

        valid_issues, _dropped = verify_quotes(essay, output.issues)
        total_quotes_total += len(output.issues)
        total_quotes_valid += len(valid_issues)
        if output.issues and not valid_issues:
            if attempt <= MAX_CONTENT_RETRIES:
                continue
            raise GradingFailed(reason="no_valid_quotes")

        raw_score = mean(criterion.score for criterion in output.criteria)
        score = round_half(apply_calibration(raw_score, route.active_calibration))

        return GradingOutcome(
            raw_score=raw_score,
            score=score,
            criteria=output.criteria,
            issues=valid_issues[:MAX_ISSUES],
            pii_spans=output.pii_spans,
            rubric_version=route.rubric_version,
            prompt_version=route.prompt_version,
            calibration_version=route.active_calibration,
            provider=provider,
            model=model,
            fallback=fallback,
            latency_ms=total_latency_ms,
            cost_vnd=total_cost_vnd,
            quotes_total=total_quotes_total,
            quotes_valid=total_quotes_valid,
        )
