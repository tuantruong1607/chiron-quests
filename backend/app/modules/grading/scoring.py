"""`round_half` (the VSTEP half-point rounding rule) and `apply_calibration`
(reading `grading/calibration/<version>.yaml`).
"""

from decimal import ROUND_FLOOR, Decimal
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

#: Directory holding `<version>.yaml` calibration files. A module-level
#: global (not a default argument) so tests can monkeypatch it to a tmp dir.
CALIBRATION_DIR = Path(__file__).parent / "calibration"

_QUARTER = Decimal("0.25")
_THREE_QUARTERS = Decimal("0.75")
_HALF = Decimal("0.5")
_ONE = Decimal("1")

CalibrationMethod = Literal["identity", "linear", "isotonic"]


def round_half(x: float) -> float:
    """VSTEP half-point rounding: within an integer band, a fractional part
    of .25-.74 rounds to .5; >= .75 rounds up to the next integer; < .25
    rounds down. Uses `Decimal` (built from `str(x)`, never `float`
    directly) so cases like 5.25/5.75 aren't tripped up by binary float
    representation error."""
    d = Decimal(str(x))
    base = d.to_integral_value(rounding=ROUND_FLOOR)
    frac = d - base
    if frac < _QUARTER:
        result = base
    elif frac < _THREE_QUARTERS:
        result = base + _HALF
    else:
        result = base + _ONE
    return float(result)


class CalibrationConfig(BaseModel):
    method: CalibrationMethod
    a: float | None = None
    b: float | None = None
    x: list[float] | None = None
    y: list[float] | None = None


#: (calibration dir, version) -> parsed config. Keyed on the directory too
#: so a test that monkeypatches `CALIBRATION_DIR` to a fresh tmp dir never
#: sees another test's (or the real repo's) cached file for the same
#: version name.
_cache: dict[tuple[str, str], CalibrationConfig] = {}


def _load_calibration(version: str) -> CalibrationConfig:
    key = (str(CALIBRATION_DIR), version)
    cached = _cache.get(key)
    if cached is not None:
        return cached
    path = CALIBRATION_DIR / f"{version}.yaml"
    if not path.is_file():
        raise ValueError(f"unknown calibration version '{version}'")
    raw = yaml.safe_load(path.read_text())
    config = CalibrationConfig.model_validate(raw)
    _cache[key] = config
    return config


def _isotonic_interp(raw: float, xs: list[float], ys: list[float]) -> float:
    """Piecewise-linear interpolation over the `(xs[i], ys[i])`
    breakpoints, clamped at the ends. `xs` must be sorted ascending."""
    if raw <= xs[0]:
        return ys[0]
    if raw >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]
        if x0 <= raw <= x1:
            y0, y1 = ys[i], ys[i + 1]
            if x1 == x0:
                return y0
            t = (raw - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return ys[-1]  # unreachable if xs is sorted, but keeps mypy happy


def apply_calibration(raw: float, version: str) -> float:
    """Map a raw mean-criteria score through the named calibration curve,
    clamped to [0, 10]. `method: identity` returns `raw` unchanged;
    `linear` applies `y = a*x + b`; `isotonic` piecewise-linearly
    interpolates over `x`/`y` breakpoints. Raises `ValueError` for an
    unknown method or a version with no matching yaml file."""
    config = _load_calibration(version)
    if config.method == "identity":
        result = raw
    elif config.method == "linear":
        if config.a is None or config.b is None:
            raise ValueError(f"calibration '{version}': linear method needs a/b")
        result = config.a * raw + config.b
    elif config.method == "isotonic":
        if not config.x or not config.y:
            raise ValueError(f"calibration '{version}': isotonic method needs x/y")
        result = _isotonic_interp(raw, config.x, config.y)
    else:  # pragma: no cover - CalibrationMethod's Literal already narrows this
        raise ValueError(f"calibration '{version}': unknown method '{config.method}'")
    return max(0.0, min(10.0, result))
