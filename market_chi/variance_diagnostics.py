from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np

from .models import ARFit


@dataclass(frozen=True)
class VarianceDiagnostic:
    status: str
    n_residuals: int
    max_lag: int
    squared_residual_acf_energy: float
    max_abs_squared_residual_acf: float
    block_variance_cv: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def ar_residuals(x, fit: ARFit) -> np.ndarray:
    y = np.asarray(x, dtype=float)
    y = y[np.isfinite(y)]
    p = fit.order
    if len(y) <= p:
        return np.array([], dtype=float)
    if p == 0:
        return y - fit.intercept
    out = np.empty(len(y) - p, dtype=float)
    coeff = np.asarray(fit.coefficients, dtype=float)
    for i, t in enumerate(range(p, len(y))):
        pred = fit.intercept
        for lag in range(1, p + 1):
            pred += coeff[lag - 1] * y[t - lag]
        out[i] = y[t] - pred
    return out


def _acf(x: np.ndarray, lag: int) -> float:
    if lag <= 0 or lag >= len(x):
        return math.nan
    a = x[:-lag]
    b = x[lag:]
    a = a - a.mean()
    b = b - b.mean()
    den = math.sqrt(float(np.dot(a, a) * np.dot(b, b)))
    if den <= 0:
        return math.nan
    return float(np.dot(a, b) / den)


def variance_structure_diagnostic(
    residuals,
    *,
    max_lag: int = 20,
    block_size: int = 50,
) -> VarianceDiagnostic:
    """Report volatility clustering without imposing an admission threshold.

    The diagnostic is intentionally threshold-free at this stage. It summarizes
    serial structure in squared residuals and variation of local residual
    variance. Qualification studies can then determine whether these measures
    discriminate false second-order admissions without rejecting valid ones.
    """
    e = np.asarray(residuals, dtype=float)
    e = e[np.isfinite(e)]
    n = len(e)
    if n < max(40, max_lag + 5):
        return VarianceDiagnostic(
            "REFUSED_INPUT", n, max_lag, math.nan, math.nan, math.nan,
            "too few residuals",
        )
    sq = e * e
    acfs = np.array([_acf(sq, k) for k in range(1, min(max_lag, n - 2) + 1)], dtype=float)
    acfs = acfs[np.isfinite(acfs)]
    if len(acfs) == 0:
        return VarianceDiagnostic(
            "REFUSED_DEGENERATE", n, max_lag, math.nan, math.nan, math.nan,
            "squared residual autocorrelations are undefined",
        )
    energy = float(np.sum(acfs * acfs))
    max_abs = float(np.max(np.abs(acfs)))

    blocks = n // block_size if block_size > 1 else 0
    if blocks >= 3:
        trimmed = e[:blocks * block_size].reshape(blocks, block_size)
        vars_ = np.var(trimmed, axis=1)
        mean_var = float(np.mean(vars_))
        block_cv = float(np.std(vars_) / mean_var) if mean_var > 0 else math.nan
    else:
        block_cv = math.nan

    return VarianceDiagnostic(
        "COMPLETE", n, max_lag, energy, max_abs, block_cv,
        "report-only P0-Q variance-structure diagnostic; no chi gate threshold is implied",
    )
