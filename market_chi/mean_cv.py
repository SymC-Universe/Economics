from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np

from .models import fit_ar, ARFit


@dataclass(frozen=True)
class MeanCVResult:
    status: str
    n: int
    folds: int
    test_points: int
    mse_ar0: float
    mse_ar1: float
    mse_ar2: float
    ar2_gain_vs_best_simple: float
    ar2_fold_win_fraction: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _predict_at(fit: ARFit, x: np.ndarray, t: int) -> float:
    pred = fit.intercept
    for lag, phi in enumerate(fit.coefficients, start=1):
        pred += phi * x[t - lag]
    return float(pred)


def walk_forward_mean_comparison(
    series,
    *,
    min_train: int = 400,
    test_block: int = 100,
) -> MeanCVResult:
    """Compare AR0/AR1/AR2 one-step conditional-mean performance out of sample.

    Each fold fits only on the prefix preceding the test block. Test predictions
    use realized lagged observations and therefore evaluate one-step conditional
    mean structure rather than recursive long-horizon forecasting.

    No admission threshold is imposed here; the output is a P0-Q diagnostic.
    """
    x = np.asarray(series, dtype=float)
    if x.ndim != 1:
        return MeanCVResult("REFUSED_INPUT", len(x), 0, 0, *(math.nan,)*5, "series must be one-dimensional")
    if not np.all(np.isfinite(x)):
        return MeanCVResult("REFUSED_INPUT", len(x), 0, 0, *(math.nan,)*5, "series must be finite and contiguous")
    n = len(x)
    if min_train < 50 or test_block < 10 or n < min_train + test_block:
        return MeanCVResult("REFUSED_INSUFFICIENT_DATA", n, 0, 0, *(math.nan,)*5, "insufficient data for requested walk-forward split")

    sse = {0: 0.0, 1: 0.0, 2: 0.0}
    count = 0
    folds = 0
    ar2_wins = 0
    start = min_train
    while start < n:
        stop = min(n, start + test_block)
        train = x[:start]
        fits = {p: fit_ar(train, p) for p in (0, 1, 2)}
        fold_sse = {0: 0.0, 1: 0.0, 2: 0.0}
        fold_n = 0
        for t in range(start, stop):
            if t < 2:
                continue
            y = x[t]
            for p in (0, 1, 2):
                err = y - _predict_at(fits[p], x, t)
                fold_sse[p] += err * err
                sse[p] += err * err
            fold_n += 1
        if fold_n:
            simple = min(fold_sse[0], fold_sse[1])
            if fold_sse[2] < simple:
                ar2_wins += 1
            count += fold_n
            folds += 1
        start = stop

    if count == 0 or folds == 0:
        return MeanCVResult("REFUSED_NO_TEST_POINTS", n, folds, count, *(math.nan,)*5, "no valid test observations")

    mse0, mse1, mse2 = (sse[p] / count for p in (0, 1, 2))
    best_simple = min(mse0, mse1)
    gain = (best_simple - mse2) / best_simple if best_simple > 0 else math.nan
    return MeanCVResult(
        "COMPLETE", n, folds, count,
        float(mse0), float(mse1), float(mse2), float(gain),
        float(ar2_wins / folds),
        "report-only P0-Q walk-forward conditional-mean comparison; no chi gate threshold is implied",
    )
