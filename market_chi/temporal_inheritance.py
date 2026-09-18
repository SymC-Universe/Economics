from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np


@dataclass(frozen=True)
class InheritanceResult:
    status: str
    n_blocks: int
    factor: int
    full_r2: float
    last_only_r2: float
    delta_r2: float
    full_mae: float
    last_only_mae: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _as_2d(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim == 1:
        a = a[:, None]
    if a.ndim != 2:
        raise ValueError("fine_features must be 1D or 2D")
    return a


def summarize_fine_blocks(fine_features: np.ndarray, factor: int) -> tuple[np.ndarray, np.ndarray]:
    """Return structured within-block summaries and a last-observation baseline.

    The structured representation contains mean, standard deviation, minimum,
    maximum, last value, and least-squares slope for each fine-scale feature.
    Incomplete trailing blocks are dropped rather than padded.
    """
    x = _as_2d(fine_features)
    if factor < 2:
        raise ValueError("factor must be >= 2")
    n_blocks = len(x) // factor
    if n_blocks < 1:
        return np.empty((0, x.shape[1] * 6)), np.empty((0, x.shape[1]))
    x = x[: n_blocks * factor].reshape(n_blocks, factor, x.shape[1])
    if not np.all(np.isfinite(x)):
        raise ValueError("fine_features must be finite for qualification scaffold")
    t = np.arange(factor, dtype=float)
    t = t - t.mean()
    denom = float(np.sum(t * t))
    means = x.mean(axis=1)
    stds = x.std(axis=1)
    mins = x.min(axis=1)
    maxs = x.max(axis=1)
    lasts = x[:, -1, :]
    centered = x - means[:, None, :]
    slopes = np.sum(centered * t[None, :, None], axis=1) / denom
    full = np.concatenate([means, stds, mins, maxs, lasts, slopes], axis=1)
    return full, lasts


def _fit_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(train_x)), train_x])
    Xt = np.column_stack([np.ones(len(test_x)), test_x])
    beta, *_ = np.linalg.lstsq(X, train_y, rcond=None)
    return Xt @ beta


def _r2(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return math.nan if ss_tot <= 0 else 1.0 - ss_res / ss_tot


def walk_forward_inheritance(
    fine_features: np.ndarray,
    coarse_target: np.ndarray,
    factor: int,
    *,
    min_train_blocks: int = 30,
    test_block_size: int = 10,
) -> InheritanceResult:
    """Compare structured fast-substrate reconstruction with last-value carryover.

    This is an exploratory P0-Q scaffold. It does not establish substrate
    inheritance merely because reconstruction succeeds. It tests whether
    structured information from the faster substrate adds out-of-sample
    reconstruction value beyond the last fine-scale observation alone.
    """
    try:
        full, last = summarize_fine_blocks(fine_features, factor)
    except ValueError as exc:
        return InheritanceResult("REFUSED_INPUT", 0, factor, math.nan, math.nan, math.nan, math.nan, math.nan, str(exc))

    y = np.asarray(coarse_target, dtype=float).reshape(-1)
    n = min(len(full), len(y))
    full, last, y = full[:n], last[:n], y[:n]
    finite = np.isfinite(y) & np.all(np.isfinite(full), axis=1) & np.all(np.isfinite(last), axis=1)
    full, last, y = full[finite], last[finite], y[finite]
    n = len(y)
    if n < min_train_blocks + test_block_size:
        return InheritanceResult(
            "REFUSED_INSUFFICIENT_BLOCKS", n, factor, math.nan, math.nan, math.nan, math.nan, math.nan,
            "not enough aligned blocks for the requested walk-forward split",
        )

    pred_full = np.full(n, np.nan)
    pred_last = np.full(n, np.nan)
    start = min_train_blocks
    while start < n:
        stop = min(n, start + test_block_size)
        pred_full[start:stop] = _fit_predict(full[:start], y[:start], full[start:stop])
        pred_last[start:stop] = _fit_predict(last[:start], y[:start], last[start:stop])
        start = stop

    mask = np.isfinite(pred_full) & np.isfinite(pred_last)
    yy = y[mask]
    pf = pred_full[mask]
    pl = pred_last[mask]
    if len(yy) < test_block_size:
        return InheritanceResult(
            "REFUSED_INSUFFICIENT_TEST", n, factor, math.nan, math.nan, math.nan, math.nan, math.nan,
            "walk-forward evaluation produced too few test blocks",
        )
    r2f, r2l = _r2(yy, pf), _r2(yy, pl)
    maef = float(np.mean(np.abs(yy - pf)))
    mael = float(np.mean(np.abs(yy - pl)))
    return InheritanceResult(
        "COMPLETE", n, factor, r2f, r2l, r2f - r2l, maef, mael,
        "delta_r2 is descriptive P0-Q evidence; promotion requires frozen definitions and untouched validation",
    )
