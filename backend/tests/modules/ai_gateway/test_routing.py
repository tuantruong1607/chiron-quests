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
    tmp_path: Path,
    providers: dict,
    data_class: str = "A",
    fallback: dict | None = None,
    priced_models: list[str] | None = None,
) -> tuple[Path, Path]:
    task: dict = {
        "rubric_version": "writing-v1",
        "prompt_version": "writing-p1",
        "provider": "primary",
        "model": "primary-model",
        "data_class": data_class,
    }
    if fallback is not None:
        task["fallback"] = fallback
    routing_path = tmp_path / "routing.yaml"
    routing_path.write_text(
        yaml.safe_dump({"tasks": {"writing_grade": task}, "providers": providers})
    )

    if priced_models is None:
        priced_models = ["primary-model"]
        if fallback is not None:
            priced_models.append(fallback["model"])
    pricing_path = tmp_path / "pricing.yaml"
    pricing_path.write_text(
        yaml.safe_dump(
            {
                "models": {
                    model: {
                        "input_vnd_per_1m": 1000,
                        "output_vnd_per_1m": 2000,
                        "cached_input_vnd_per_1m": 500,
                    }
                    for model in priced_models
                }
            }
        )
    )
    return routing_path, pricing_path


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
    routing_path, pricing_path = _write_routing(
        tmp_path, providers={"primary": {"no_training": False}}
    )
    with pytest.raises(RoutingError):
        load_routing(routing_path, pricing_path)


def test_routing_allows_class_b_route_to_provider_without_no_training(
    tmp_path: Path,
) -> None:
    routing_path, pricing_path = _write_routing(
        tmp_path, providers={"primary": {"no_training": False}}, data_class="B"
    )
    config = load_routing(routing_path, pricing_path)
    assert config.tasks["writing_grade"].provider == "primary"


def test_routing_accepts_class_a_route_to_provider_with_no_training(
    tmp_path: Path,
) -> None:
    routing_path, pricing_path = _write_routing(
        tmp_path, providers={"primary": {"no_training": True}}
    )
    config = load_routing(routing_path, pricing_path)
    assert config.tasks["writing_grade"].data_class == "A"


def test_routing_rejects_class_a_fallback_without_no_training(tmp_path: Path) -> None:
    routing_path, pricing_path = _write_routing(
        tmp_path,
        providers={"primary": {"no_training": True}, "backup": {"no_training": False}},
        fallback={"provider": "backup", "model": "backup-model"},
    )
    with pytest.raises(RoutingError):
        load_routing(routing_path, pricing_path)


def test_routing_rejects_unknown_provider(tmp_path: Path) -> None:
    routing_path, pricing_path = _write_routing(tmp_path, providers={})
    with pytest.raises(RoutingError):
        load_routing(routing_path, pricing_path)


def test_routing_rejects_model_with_no_pricing_entry(tmp_path: Path) -> None:
    routing_path, pricing_path = _write_routing(
        tmp_path, providers={"primary": {"no_training": True}}, priced_models=[]
    )
    with pytest.raises(RoutingError):
        load_routing(routing_path, pricing_path)


def test_routing_rejects_fallback_model_with_no_pricing_entry(tmp_path: Path) -> None:
    routing_path, pricing_path = _write_routing(
        tmp_path,
        providers={"primary": {"no_training": True}, "backup": {"no_training": True}},
        fallback={"provider": "backup", "model": "backup-model"},
        priced_models=["primary-model"],  # fallback's "backup-model" left unpriced
    )
    with pytest.raises(RoutingError):
        load_routing(routing_path, pricing_path)


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
