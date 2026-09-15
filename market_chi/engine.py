from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

from .models import fit_ar
from .chi import ChiResult, chi_from_discrete_poles


@dataclass(frozen=True)
class EngineConfig:
    dt: float = 1.0
    min_points: int = 100
    min_ar2_bic_gain: float = 6.0
    standardize: bool = True


@dataclass(frozen=True)
class MarketWindowResult:
    status: str
    chi_status: str
    chi: float
    chi_regime: str
    model_family: str
    bic_ar0: float
    bic_ar1: float
    bic_ar2: float
    ar2_bic_gain_vs_best_simple: float
    ar2_coefficients: tuple[float, ...]
    discrete_poles: tuple[complex, ...]
    continuous_poles: tuple[complex, ...]
    mean: float
    scale: float
    n: int
    reason: str

    def as_dict(self):
        d = asdict(self)
        d["discrete_poles"] = [{"real": float(v.real), "imag": float(v.imag)} for v in self.discrete_poles]
        d["continuous_poles"] = [{"real": float(v.real), "imag": float(v.imag)} for v in self.continuous_poles]
        return d


def _failed(status: str, n: int, mean: float, scale: float, reason: str) -> MarketWindowResult:
    nan = math.nan
    return MarketWindowResult(status, "REFUSED", nan, "unresolved", "none", nan, nan, nan, nan, (), (), (), mean, scale, n, reason)


def analyze_series(series, config: EngineConfig | None = None) -> MarketWindowResult:
    """Analyze one market window without presuming an oscillator.

    Current P0-Q admission scaffold:
      1. clean finite observations;
      2. compare AR(0), AR(1), and AR(2) by BIC;
      3. admit the second-order factor only if AR(2) beats the strongest simple
         candidate by the configured qualification margin;
      4. inspect AR(2) poles;
      5. emit lowercase χ only if those poles admit a canonical second-order
         continuous embedding.

    The AR family is a qualification scaffold, not the final Market System Model.
    """
    cfg = config or EngineConfig()
    x = np.asarray(series, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < cfg.min_points:
        return _failed("REFUSED_INPUT", n, math.nan, math.nan, "too_short")

    mean = float(np.mean(x))
    centered = x - mean
    scale = float(np.std(centered, ddof=0))
    if not math.isfinite(scale) or scale <= 1e-14:
        return _failed("REFUSED_INPUT", n, mean, scale, "degenerate_variance")
    y = centered / scale if cfg.standardize else centered

    try:
        ar0 = fit_ar(y, 0)
        ar1 = fit_ar(y, 1)
        ar2 = fit_ar(y, 2)
    except Exception as exc:
        return _failed("REFUSED_MODEL", n, mean, scale, f"fit_failure:{type(exc).__name__}")

    best_simple = min(ar0.bic, ar1.bic)
    gain = float(best_simple - ar2.bic)
    if gain < cfg.min_ar2_bic_gain:
        winner = "AR0" if ar0.bic <= ar1.bic else "AR1"
        return MarketWindowResult(
            "ADMITTED_NATIVE_SIMPLE", "REFUSED", math.nan, "unresolved", winner,
            ar0.bic, ar1.bic, ar2.bic, gain, ar2.coefficients, ar2.roots, (),
            mean, scale, n, f"AR2_not_supported_by_BIC_margin_{cfg.min_ar2_bic_gain:g}"
        )

    chi_result: ChiResult = chi_from_discrete_poles(ar2.roots, dt=cfg.dt)
    if not chi_result.admitted:
        return MarketWindowResult(
            "ADMITTED_SECOND_ORDER_DISCRETE", "REFUSED", math.nan, "unresolved", "AR2",
            ar0.bic, ar1.bic, ar2.bic, gain, ar2.coefficients, ar2.roots,
            chi_result.continuous_poles, mean, scale, n, chi_result.reason
        )

    return MarketWindowResult(
        "ADMITTED_SECOND_ORDER_CHI", "ADMITTED", chi_result.chi, chi_result.regime,
        "AR2_SECOND_ORDER", ar0.bic, ar1.bic, ar2.bic, gain, ar2.coefficients,
        ar2.roots, chi_result.continuous_poles, mean, scale, n, chi_result.reason
    )
