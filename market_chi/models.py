from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ARFit:
    order: int
    coefficients: tuple[float, ...]
    intercept: float
    residual_variance: float
    rss: float
    bic: float
    n_effective: int
    roots: tuple[complex, ...]


def _design_ar(x: np.ndarray, order: int) -> tuple[np.ndarray, np.ndarray]:
    if order == 0:
        return np.ones((len(x), 1), dtype=float), x.copy()
    n = len(x)
    y = x[order:]
    cols = [np.ones(n - order, dtype=float)]
    for lag in range(1, order + 1):
        cols.append(x[order - lag:n - lag])
    return np.column_stack(cols), y


def _ar_roots(coefficients: np.ndarray) -> np.ndarray:
    """Return discrete-time propagation roots for y_t=sum(phi_i y_{t-i})+e_t."""
    p = len(coefficients)
    if p == 0:
        return np.array([], dtype=complex)
    poly = np.concatenate(([1.0], -np.asarray(coefficients, dtype=float)))
    return np.roots(poly).astype(complex)


def fit_ar(x, order: int) -> ARFit:
    """OLS AR(p) with intercept and Gaussian quasi-likelihood BIC.

    This is a P0-Q model-admission primitive, not a final econometric model.
    """
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if order < 0 or order > 2:
        raise ValueError("current qualification engine supports AR orders 0, 1, and 2")
    if len(x) < max(40, 10 * (order + 1)):
        raise ValueError("series too short for requested qualification fit")

    X, y = _design_ar(x, order)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    resid = y - fitted
    rss = float(np.dot(resid, resid))
    n = len(y)
    eps = np.finfo(float).tiny
    sigma2 = max(rss / n, eps)
    k = order + 1
    bic = float(n * np.log(sigma2) + k * np.log(n))
    coeff = beta[1:] if order else np.array([], dtype=float)
    roots = _ar_roots(coeff)
    return ARFit(
        order=order,
        coefficients=tuple(float(v) for v in coeff),
        intercept=float(beta[0]),
        residual_variance=sigma2,
        rss=rss,
        bic=bic,
        n_effective=n,
        roots=tuple(complex(r) for r in roots),
    )
