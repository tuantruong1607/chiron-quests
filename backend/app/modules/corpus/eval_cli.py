"""`python -m app.modules.corpus.eval_cli --provider <p> --model <m> \
--repeat 3 --dataset-version <v> --split test [--prompt-version <p>] \
[--calibration <c>]`

Runs `grade_writing()` `repeat` times per labeled item in a dataset
version/split, writes one `eval_run` row, and prints a table of the
resulting metrics against spec §4.3's thresholds.
"""

import argparse
import asyncio
import sys
from typing import cast

from app.modules.ai_gateway import service as ai
from app.modules.corpus import service
from app.modules.corpus.metrics import EvalMetrics, compute_metrics
from app.modules.corpus.service import Split
from app.modules.grading.service import GradingFailed, GradingOutcome, grade_writing

#: Spec §4.3 bake-off thresholds.
THRESHOLDS = [
    ("mae", "<=", 0.75),
    ("consistency_rate", ">=", 0.90),
    ("quote_valid_rate", ">=", 0.95),
    ("schema_valid_rate", ">=", 0.98),
    ("p95_latency_ms", "<=", 60_000),
    ("avg_cost_vnd", "<=", 1_500),
]


class NoLabeledItemsError(RuntimeError):
    """Raised by `run_eval` when `dataset_version`/`split` has no labeled
    items to grade - running an eval against nothing would otherwise
    silently write a meaningless `eval_run` row."""


def _check_thresholds(metrics: EvalMetrics) -> tuple[dict[str, bool], bool]:
    """Returns (per-field pass/fail, whether any gate metric is
    unmeasured). A `None` metric never counts as a pass."""
    passed: dict[str, bool] = {}
    incomplete = False
    for field, op, threshold in THRESHOLDS:
        value = getattr(metrics, field)
        if value is None:
            passed[field] = False
            incomplete = True
        else:
            passed[field] = value <= threshold if op == "<=" else value >= threshold
    passed["injection_ok"] = metrics.injection_ok
    return passed, incomplete


async def run_eval(
    *,
    provider: str,
    model: str,
    repeat: int,
    dataset_version: str,
    split: Split,
    prompt_version: str | None = None,
    calibration: str | None = None,
) -> EvalMetrics:
    """Grade every labeled item in `dataset_version`/`split` `repeat`
    times, against `provider`/`model` (and, if given, `prompt_version`/
    `calibration`), write the resulting `eval_run` row, and return its
    metrics. Raises `NoLabeledItemsError` if there are no labeled items to
    grade.

    The route's `fallback` is always disabled for the duration of the
    eval (spec §4.3: the eval measures one named provider/model, and must
    never silently grade on a different one) - any outcome that still
    comes back with `fallback=True` (e.g. a stale route) is treated as a
    failed repeat and counted separately as `fallback_count`."""
    items = service.labeled_items_for_eval(dataset_version, split)
    if not items:
        raise NoLabeledItemsError(
            f"No labeled items found for dataset_version={dataset_version!r} "
            f"split={split!r} - nothing to evaluate."
        )

    override_fields: dict[str, object] = {
        "provider": provider,
        "model": model,
        "fallback": None,
    }
    if prompt_version is not None:
        override_fields["prompt_version"] = prompt_version
    if calibration is not None:
        override_fields["active_calibration"] = calibration

    labels: list[float] = []
    runs: list[list[GradingOutcome]] = []
    injection_flags: list[bool] = []
    attempts = 0
    schema_failures = 0
    fallback_count = 0
    quotes_total = 0
    quotes_valid = 0

    for item in items:
        item_outcomes: list[GradingOutcome] = []
        for _ in range(repeat):
            attempts += 1
            with ai.override_route("writing_grade", **override_fields):
                try:
                    outcome = await grade_writing(
                        item.task_type,
                        item.prompt_redacted,
                        item.essay_redacted,
                        correlation_id=f"eval-{item.id}",
                    )
                except GradingFailed:
                    schema_failures += 1
                    continue
            if outcome.fallback:
                # Should never happen with fallback disabled above, but
                # never silently score on it if it somehow does.
                fallback_count += 1
                schema_failures += 1
                continue
            quotes_total += outcome.quotes_total
            quotes_valid += outcome.quotes_valid
            item_outcomes.append(outcome)

        if not item_outcomes:
            # Every repeat failed for this item - nothing to score it
            # against; it still counted toward attempts/schema_failures.
            continue
        labels.append(item.overall_score)
        runs.append(item_outcomes)
        injection_flags.append(item.is_injection)

    route = ai.task_config("writing_grade")
    metrics = compute_metrics(
        labels,
        runs,
        injection_flags=injection_flags,
        attempts=attempts,
        schema_failures=schema_failures,
        quotes_total=quotes_total,
        quotes_valid=quotes_valid,
    )

    service.record_eval_run(
        rubric_version=route.rubric_version,
        prompt_version=prompt_version or route.prompt_version,
        calibration_version=calibration or route.active_calibration,
        provider=provider,
        model=model,
        dataset_version=dataset_version,
        split=split,
        metrics={
            "mae": metrics.mae,
            "consistency_rate": metrics.consistency_rate,
            "quote_valid_rate": metrics.quote_valid_rate,
            "schema_valid_rate": metrics.schema_valid_rate,
            "p95_latency_ms": metrics.p95_latency_ms,
            "avg_cost_vnd": metrics.avg_cost_vnd,
            "injection_ok": metrics.injection_ok,
            # Spec §7.4 audit trail: which items and how many attempts/
            # failures produced this run's metrics.
            "item_ids": [str(item.id) for item in items],
            "n_items": len(items),
            "attempts": attempts,
            "schema_failures": schema_failures,
            "fallback_count": fallback_count,
        },
    )

    return metrics


def _fmt(value: float | int | None, fmt: str) -> str:
    return "N/A (not measured)" if value is None else format(value, fmt)


def _print_report(metrics: EvalMetrics) -> None:
    passed, incomplete = _check_thresholds(metrics)
    rows = [
        ("mae", "MAE vs founder score", _fmt(metrics.mae, ".3f"), "<= 0.75"),
        (
            "consistency_rate",
            "Consistency rate (spread<=0.5)",
            _fmt(metrics.consistency_rate, ".3f"),
            ">= 0.90",
        ),
        (
            "quote_valid_rate",
            "Quote valid rate",
            _fmt(metrics.quote_valid_rate, ".3f"),
            ">= 0.95",
        ),
        (
            "schema_valid_rate",
            "Schema valid rate",
            _fmt(metrics.schema_valid_rate, ".3f"),
            ">= 0.98",
        ),
        (
            "p95_latency_ms",
            "p95 latency (ms)",
            _fmt(metrics.p95_latency_ms, "d"),
            "<= 60000",
        ),
        (
            "avg_cost_vnd",
            "Avg cost (VND)",
            _fmt(metrics.avg_cost_vnd, ".1f"),
            "<= 1500",
        ),
        (
            "injection_ok",
            "Injection doesn't raise score",
            str(metrics.injection_ok),
            "must be True",
        ),
    ]
    print(f"{'Metric':<32}{'Value':<20}{'Threshold':<14}{'Result'}")  # noqa: T201
    for field, name, value, threshold in rows:
        result = "PASS" if passed[field] else "FAIL"
        print(f"{name:<32}{value:<20}{threshold:<14}{result}")  # noqa: T201
    if incomplete:
        overall = "INCOMPLETE"
    else:
        overall = "PASS" if all(passed.values()) else "FAIL"
    print(f"\nOverall: {overall}")  # noqa: T201


async def _main_async(args: argparse.Namespace) -> None:
    metrics = await run_eval(
        provider=args.provider,
        model=args.model,
        repeat=args.repeat,
        dataset_version=args.dataset_version,
        split=cast(Split, args.split),
        prompt_version=args.prompt_version,
        calibration=args.calibration,
    )
    _print_report(metrics)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run an eval against a labeled corpus split (spec §4.3)."
    )
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--dataset-version", required=True)
    parser.add_argument(
        "--split", default="test", choices=["unassigned", "dev", "test"]
    )
    parser.add_argument("--prompt-version", default=None)
    parser.add_argument("--calibration", default=None)
    args = parser.parse_args()
    try:
        asyncio.run(_main_async(args))
    except NoLabeledItemsError as exc:
        print(str(exc), file=sys.stderr)  # noqa: T201
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
