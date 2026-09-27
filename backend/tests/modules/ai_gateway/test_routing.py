from pathlib import Path

import pytest
import yaml

from app.modules.ai_gateway.routing import (
    RoutingError,
    load_pricing,
    load_routing,
)
from app.modules.ai_gateway.service import AIError, task_config


def _write_routing(
    tmp_path: Path, providers: dict, data_class: str = "A", fallback: dict | None = None
) -> Path:
    task: dict = {
        "rubric_version": "writing-v1",
        "prompt_version": "writing-p1",
        "provider": "primary",
        "model": "primary-model",
        "data_class": data_class,
    }
    if fallback is not None:
        task["fallback"] = fallback
    path = tmp_path / "routing.yaml"
    path.write_text(
        yaml.safe_dump({"tasks": {"writing_grade": task}, "providers": providers})
    )
    return path


def test_load_routing_default_file_has_writing_grade_task() -> None:
    config = load_routing()
    route = config.tasks["writing_grade"]
    assert route.provider == "fake"
    assert route.model == "fake-grader"
    assert route.rubric_version == "writing-v1"
    assert route.data_class == "A"
    assert config.providers["fake"].no_training is True


def test_routing_rejects_class_a_route_to_provider_without_no_training(
    tmp_path: Path,
) -> None:
    path = _write_routing(tmp_path, providers={"primary": {"no_training": False}})
    with pytest.raises(RoutingError):
        load_routing(path)


def test_routing_allows_class_b_route_to_provider_without_no_training(
    tmp_path: Path,
) -> None:
    path = _write_routing(
        tmp_path, providers={"primary": {"no_training": False}}, data_class="B"
    )
    config = load_routing(path)
    assert config.tasks["writing_grade"].provider == "primary"


def test_routing_accepts_class_a_route_to_provider_with_no_training(
    tmp_path: Path,
) -> None:
    path = _write_routing(tmp_path, providers={"primary": {"no_training": True}})
    config = load_routing(path)
    assert config.tasks["writing_grade"].data_class == "A"


def test_routing_rejects_class_a_fallback_without_no_training(tmp_path: Path) -> None:
    path = _write_routing(
        tmp_path,
        providers={"primary": {"no_training": True}, "backup": {"no_training": False}},
        fallback={"provider": "backup", "model": "backup-model"},
    )
    with pytest.raises(RoutingError):
        load_routing(path)


def test_routing_rejects_unknown_provider(tmp_path: Path) -> None:
    path = _write_routing(tmp_path, providers={})
    with pytest.raises(RoutingError):
        load_routing(path)


def test_load_pricing_default_file_has_fake_grader_model() -> None:
    pricing = load_pricing()
    entry = pricing.models["fake-grader"]
    assert entry.input_vnd_per_1m > 0
    assert entry.output_vnd_per_1m > 0
    assert entry.cached_input_vnd_per_1m > 0


def test_task_config_returns_writing_grade_route() -> None:
    route = task_config("writing_grade")
    assert route.rubric_version == "writing-v1"
    assert route.prompt_version == "writing-p1"
    assert route.active_calibration == "writing-c0"


def test_task_config_raises_no_route_for_unknown_task() -> None:
    with pytest.raises(AIError) as exc_info:
        task_config("no_such_task")
    assert exc_info.value.kind == "no_route"
