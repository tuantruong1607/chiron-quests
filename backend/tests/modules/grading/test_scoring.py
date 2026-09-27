from pathlib import Path

import pytest
import yaml

from app.modules.grading import scoring
from app.modules.grading.scoring import apply_calibration, round_half


@pytest.mark.parametrize(
    "x,y",
    [
        (5.24, 5.0),
        (5.25, 5.5),
        (5.74, 5.5),
        (5.75, 6.0),
        (5.33, 5.5),
        (0.24, 0.0),
        (0.75, 1.0),
        (9.0, 9.0),
    ],
)
def test_round_half(x: float, y: float) -> None:
    assert round_half(x) == y


def test_identity_calibration_c0() -> None:
    assert apply_calibration(6.3, "writing-c0") == 6.3


def _write_calibration(dir_: Path, name: str, content: dict[str, object]) -> str:
    (dir_ / f"{name}.yaml").write_text(yaml.safe_dump(content))
    return name


def test_linear_calibration_applies_a_and_b(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(
        tmp_path, "lin-basic", {"method": "linear", "a": 1.0, "b": 0.5}
    )
    assert apply_calibration(5.0, version) == 5.5


def test_calibration_clamped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(
        tmp_path, "lin-clamp-hi", {"method": "linear", "a": 1.2, "b": 0}
    )
    assert apply_calibration(9.9, version) == 10.0


def test_calibration_clamped_at_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(
        tmp_path, "lin-clamp-lo", {"method": "linear", "a": 1.0, "b": -5}
    )
    assert apply_calibration(2.0, version) == 0.0


def test_isotonic_calibration_interpolates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(
        tmp_path,
        "iso-basic",
        {"method": "isotonic", "x": [0, 5, 10], "y": [0, 4, 10]},
    )
    # Midpoint between breakpoints (0,0)-(5,4): raw=2.5 -> y=2.0
    assert apply_calibration(2.5, version) == pytest.approx(2.0)
    # Exactly on a breakpoint.
    assert apply_calibration(5.0, version) == pytest.approx(4.0)


def test_isotonic_calibration_clamps_beyond_breakpoints(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(
        tmp_path,
        "iso-clamp",
        {"method": "isotonic", "x": [1, 9], "y": [2, 8]},
    )
    assert apply_calibration(0.0, version) == pytest.approx(2.0)
    assert apply_calibration(10.0, version) == pytest.approx(8.0)


def test_unknown_calibration_version_raises_value_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    with pytest.raises(ValueError):
        apply_calibration(5.0, "no-such-version")


def test_unknown_calibration_method_raises_value_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(scoring, "CALIBRATION_DIR", tmp_path)
    version = _write_calibration(tmp_path, "weird-method", {"method": "quadratic"})
    with pytest.raises(ValueError):
        apply_calibration(5.0, version)
