"""Loads and validates `routing.yaml` (task -> provider/model routing) and
`pricing.yaml` (per-model VND pricing), both versioned in this repo.
"""

from pathlib import Path

import yaml
from pydantic import BaseModel

from app.modules.ai_gateway.types import DataClass

_MODULE_DIR = Path(__file__).parent
DEFAULT_ROUTING_PATH = _MODULE_DIR / "routing.yaml"
DEFAULT_PRICING_PATH = _MODULE_DIR / "pricing.yaml"


class RoutingError(Exception):
    """Raised when `routing.yaml` is invalid, e.g. a data-class-A task is
    routed to a provider whose config lacks `no_training: true`."""


class ProviderConfig(BaseModel):
    no_training: bool = False
    terms_evidence: str = ""


class FallbackRoute(BaseModel):
    provider: str
    model: str


class TaskRoute(BaseModel):
    rubric_version: str
    prompt_version: str
    active_calibration: str = ""
    few_shot_ids: list[str] = []
    provider: str
    model: str
    params: dict[str, object] = {}
    data_class: DataClass
    fallback: FallbackRoute | None = None


class RoutingConfig(BaseModel):
    tasks: dict[str, TaskRoute]
    providers: dict[str, ProviderConfig]

    def _check_no_training(self, provider_name: str, task_key: str) -> None:
        provider = self.providers.get(provider_name)
        if provider is None:
            raise RoutingError(
                f"routing.yaml: task '{task_key}' references unknown provider '{provider_name}'"
            )
        if not provider.no_training:
            raise RoutingError(
                f"routing.yaml: task '{task_key}' is data_class A but provider "
                f"'{provider_name}' lacks no_training: true"
            )

    def validate_data_classes(self) -> None:
        for task_key, task in self.tasks.items():
            if task.data_class != "A":
                continue
            self._check_no_training(task.provider, task_key)
            if task.fallback is not None:
                self._check_no_training(task.fallback.provider, task_key)


def load_routing(path: str | Path | None = None) -> RoutingConfig:
    """Load and validate a routing YAML file (defaults to this module's
    `routing.yaml`). Raises `RoutingError` if a data-class-A task routes to
    a provider without `no_training: true`."""
    resolved = Path(path) if path is not None else DEFAULT_ROUTING_PATH
    raw = yaml.safe_load(resolved.read_text())
    config = RoutingConfig.model_validate(raw)
    config.validate_data_classes()
    return config


class ModelPricing(BaseModel):
    input_vnd_per_1m: int
    output_vnd_per_1m: int
    cached_input_vnd_per_1m: int


class PricingConfig(BaseModel):
    models: dict[str, ModelPricing]


def load_pricing(path: str | Path | None = None) -> PricingConfig:
    """Load `pricing.yaml` (per-model VND pricing per 1M tokens)."""
    resolved = Path(path) if path is not None else DEFAULT_PRICING_PATH
    raw = yaml.safe_load(resolved.read_text())
    return PricingConfig.model_validate(raw)
