import json

import pytest
from pydantic import ValidationError

from app.modules.ai_gateway.adapters.fake import DEFAULT_WRITING_GRADE_RESPONSE
from app.modules.grading.schema import WritingGradeOutput


def json_with(score: object) -> str:
    return json.dumps(
        {
            "criteria": [
                {"key": "task_fulfilment", "score": score, "comment_vi": "ok"},
                {"key": "organization", "score": 6, "comment_vi": "ok"},
                {"key": "vocabulary", "score": 6, "comment_vi": "ok"},
                {"key": "grammar", "score": 6, "comment_vi": "ok"},
            ],
            "issues": [],
            "pii_spans": [],
        }
    )


def test_schema_accepts_valid_output() -> None:
    output = WritingGradeOutput.model_validate_json(json_with(score=6.5))
    assert output.criteria[0].score == 6.5


def test_schema_rejects_string_score() -> None:  # Review Focus #4
    with pytest.raises(ValidationError):
        WritingGradeOutput.model_validate_json(json_with(score="6.5"))


def test_schema_rejects_out_of_range_score() -> None:
    with pytest.raises(ValidationError):
        WritingGradeOutput.model_validate_json(json_with(score=11))


def test_schema_rejects_negative_score() -> None:
    with pytest.raises(ValidationError):
        WritingGradeOutput.model_validate_json(json_with(score=-1))


def test_schema_rejects_unknown_pii_kind() -> None:
    payload = json.loads(json_with(score=6))
    payload["pii_spans"] = [{"text": "0912345678", "kind": "not-a-kind"}]
    with pytest.raises(ValidationError):
        WritingGradeOutput.model_validate_json(json.dumps(payload))


def test_fake_adapter_default_response_matches_schema() -> None:
    """The FakeAdapter's fixed default response (used by ai_gateway tests
    and by grading tests that don't script a custom response) must itself
    validate against `WritingGradeOutput` - Task 5's schema is built to fit
    Task 4's fixture, not the other way around."""
    output = WritingGradeOutput.model_validate_json(DEFAULT_WRITING_GRADE_RESPONSE)
    assert {c.key for c in output.criteria} == {
        "task_fulfilment",
        "organization",
        "vocabulary",
        "grammar",
    }
    assert len(output.issues) == 2
    assert output.pii_spans == []
