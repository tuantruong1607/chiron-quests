import pytest

from app.modules.ai_gateway import service
from app.modules.ai_gateway.types import AIError

pytestmark = pytest.mark.anyio


def test_override_route_changes_task_config_within_context():
    base = service.task_config("writing_grade")
    with service.override_route("writing_grade", provider="openai", model="gpt-x"):
        overridden = service.task_config("writing_grade")
        assert overridden.provider == "openai"
        assert overridden.model == "gpt-x"
        # Everything else carries over from the base route unchanged.
        assert overridden.rubric_version == base.rubric_version
        assert overridden.prompt_version == base.prompt_version

    # Restored once the context manager exits.
    assert service.task_config("writing_grade") == base


def test_override_route_can_override_prompt_and_calibration_version():
    with service.override_route(
        "writing_grade", prompt_version="writing-p2", active_calibration="writing-c1"
    ):
        route = service.task_config("writing_grade")
        assert route.prompt_version == "writing-p2"
        assert route.active_calibration == "writing-c1"


def test_override_route_nests_and_restores_outer_override():
    with service.override_route("writing_grade", provider="outer"):
        with service.override_route("writing_grade", model="inner-model"):
            inner = service.task_config("writing_grade")
            assert inner.provider == "outer"
            assert inner.model == "inner-model"
        restored = service.task_config("writing_grade")
        assert restored.provider == "outer"
        assert restored.model != "inner-model"


def test_override_route_unknown_task_raises_no_route():
    with pytest.raises(AIError) as exc_info:
        with service.override_route("does_not_exist", provider="x"):
            pass
    assert exc_info.value.kind == "no_route"


async def test_complete_uses_overridden_route(redis, install_fake_adapter) -> None:
    install_fake_adapter(provider="overridden")
    from app.modules.ai_gateway.types import AIRequest
    from tests.modules.ai_gateway.test_service import GradeResult

    with service.override_route("writing_grade", provider="overridden"):
        result = await service.complete(
            AIRequest(
                task_key="writing_grade",
                data_class="A",
                system="sys",
                user="usr",
                response_schema=GradeResult,
                max_output_tokens=200,
                correlation_id="override-1",
            )
        )
    assert result.provider == "overridden"
