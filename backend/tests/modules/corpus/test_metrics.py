import pytest

from app.modules.corpus.metrics import compute_metrics
from app.modules.grading.service import GradingOutcome


def o(score: float, latency_ms: int = 1000, cost_vnd: int = 100) -> GradingOutcome:
    return GradingOutcome(
        raw_score=score,
        score=score,
        criteria=[],
        issues=[],
        pii_spans=[],
        rubric_version="writing-v1",
        prompt_version="writing-p1",
        calibration_version="writing-c0",
        provider="fake",
        model="fake-grader",
        fallback=False,
        latency_ms=latency_ms,
        cost_vnd=cost_vnd,
    )


def test_metrics_mae_and_consistency():
    m = compute_metrics(
        [6.0, 5.0], runs=[[o(6.5), o(6.0), o(6.5)], [o(5.0), o(6.0), o(5.0)]]
    )
    assert m.mae == pytest.approx(0.33, abs=0.01)
    assert m.consistency_rate == 0.5


def test_metrics_rates_are_none_when_not_measured():
    # Single run per item: consistency can't be measured either (a spread
    # of exactly one run is trivially 0, not a real "consistent" result).
    m = compute_metrics([6.0], runs=[[o(6.0)]])
    assert m.quote_valid_rate is None
    assert m.schema_valid_rate is None
    assert m.consistency_rate is None


def test_metrics_consistency_rate_measured_when_every_item_has_2plus_runs():
    m = compute_metrics([6.0, 5.0], runs=[[o(6.0), o(6.0)], [o(5.0), o(5.5)]])
    assert m.consistency_rate == 1.0


def test_metrics_schema_valid_rate_uses_attempts_and_failures():
    m = compute_metrics([6.0], runs=[[o(6.0)]], attempts=4, schema_failures=1)
    assert m.schema_valid_rate == pytest.approx(0.75)


def test_metrics_quote_valid_rate_uses_quote_counts():
    m = compute_metrics(
        [6.0], runs=[[o(6.0)]], quotes_total=20, quotes_valid=19
    )
    assert m.quote_valid_rate == pytest.approx(0.95)


def test_metrics_p95_latency_and_avg_cost():
    runs = [[o(6.0, latency_ms=1000, cost_vnd=100), o(6.0, latency_ms=2000, cost_vnd=200)]]
    m = compute_metrics([6.0], runs=runs)
    assert m.p95_latency_ms in (1000, 2000)
    assert m.avg_cost_vnd == pytest.approx(150.0)


def test_metrics_injection_ok_true_when_none_flagged():
    m = compute_metrics([6.0, 5.0], runs=[[o(6.0)], [o(5.0)]])
    assert m.injection_ok is True


def test_metrics_injection_ok_false_when_flagged_item_scored_too_high():
    m = compute_metrics(
        [6.0, 5.0],
        runs=[[o(7.0)], [o(5.0)]],
        injection_flags=[True, False],
    )
    assert m.injection_ok is False


def test_metrics_injection_ok_true_when_flagged_item_within_tolerance():
    m = compute_metrics(
        [6.0, 5.0],
        runs=[[o(6.5)], [o(5.0)]],
        injection_flags=[True, False],
    )
    assert m.injection_ok is True
