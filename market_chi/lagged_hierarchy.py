from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np

from .temporal_inheritance import summarize_fine_blocks


@dataclass(frozen=True)
class LaggedHierarchyResult:
    status: str
    n_aligned_blocks: int
    factor: int
    lead_blocks: int
    structured_r2: float
    last_fast_r2: float
    coarse_persistence_r2: float
    delta_r2_vs_last: float
    delta_r2_vs_persistence: float
    structured_mae: float
    last_fast_mae: float
    coarse_persistence_mae: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _fit_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(train_x)), train_x])
    Xt = np.column_stack([np.ones(len(test_x)), test_x])
    beta, *_ = np.linalg.lstsq(X, train_y, rcond=None)
    return Xt @ beta


def _r2(y: np.ndarray, pred: np.ndarray) -> float:
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return math.nan if ss_tot <= 0 else 1.0 - ss_res / ss_tot


def walk_forward_lagged_hierarchy(
    fine_features: np.ndarray,
    coarse_target: np.ndarray,
    factor: int,
    *,
    lead_blocks: int = 1,
    min_train_blocks: int = 30,
    test_block_size: int = 10,
) -> LaggedHierarchyResult:
    """Test whether fast-block structure predicts a future coarse state.

    The information block is summarized at index t. The target is coarse_target
    at t + lead_blocks. Comparators are:
      1. a fitted model using only the last fast observation in block t;
      2. direct persistence of the current coarse target value at t.

    This is a P0-Q qualification scaffold. It does not define an event threshold
    or license a predictive claim from reconstruction performance alone.
    """
    if lead_blocks < 1:
        raise ValueError("lead_blocks must be >= 1")

    try:
        structured, last = summarize_fine_blocks(fine_features, factor)
    except ValueError as exc:
        return LaggedHierarchyResult(
            "REFUSED_INPUT", 0, factor, lead_blocks,
            math.nan, math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan, str(exc)
        )

    y = np.asarray(coarse_target, dtype=float).reshape(-1)
    n0 = min(len(structured), len(y))
    structured = structured[:n0]
    last = last[:n0]
    y = y[:n0]

    if n0 <= lead_blocks:
        return LaggedHierarchyResult(
            "REFUSED_INSUFFICIENT_BLOCKS", 0, factor, lead_blocks,
            math.nan, math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan, "not enough blocks after lead alignment"
        )

    x_struct = structured[:-lead_blocks]
    x_last = last[:-lead_blocks]
    current_y = y[:-lead_blocks]
    future_y = y[lead_blocks:]

    finite = (
        np.isfinite(future_y)
        & np.isfinite(current_y)
        & np.all(np.isfinite(x_struct), axis=1)
        & np.all(np.isfinite(x_last), axis=1)
    )
    x_struct = x_struct[finite]
    x_last = x_last[finite]
    current_y = current_y[finite]
    future_y = future_y[finite]
    n = len(future_y)

    if n < min_train_blocks + test_block_size:
        return LaggedHierarchyResult(
            "REFUSED_INSUFFICIENT_BLOCKS", n, factor, lead_blocks,
            math.nan, math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan,
            "not enough aligned blocks for the requested walk-forward split",
        )

    pred_struct = np.full(n, np.nan)
    pred_last = np.full(n, np.nan)
    pred_persist = np.full(n, np.nan)

    start = min_train_blocks
    while start < n:
        stop = min(n, start + test_block_size)
        pred_struct[start:stop] = _fit_predict(
            x_struct[:start], future_y[:start], x_struct[start:stop]
        )
        pred_last[start:stop] = _fit_predict(
            x_last[:start], future_y[:start], x_last[start:stop]
        )
        pred_persist[start:stop] = current_y[start:stop]
        start = stop

    mask = np.isfinite(pred_struct) & np.isfinite(pred_last) & np.isfinite(pred_persist)
    yy = future_y[mask]
    ps = pred_struct[mask]
    pl = pred_last[mask]
    pp = pred_persist[mask]

    if len(yy) < test_block_size:
        return LaggedHierarchyResult(
            "REFUSED_INSUFFICIENT_TEST", n, factor, lead_blocks,
            math.nan, math.nan, math.nan, math.nan, math.nan,
            math.nan, math.nan, math.nan,
            "walk-forward evaluation produced too few test blocks",
        )

    r2s = _r2(yy, ps)
    r2l = _r2(yy, pl)
    r2p = _r2(yy, pp)
    maes = float(np.mean(np.abs(yy - ps)))
    mael = float(np.mean(np.abs(yy - pl)))
    maep = float(np.mean(np.abs(yy - pp)))

    return LaggedHierarchyResult(
        "COMPLETE",
        n,
        factor,
        lead_blocks,
        r2s,
        r2l,
        r2p,
        r2s - r2l,
        r2s - r2p,
        maes,
        mael,
        maep,
        "development metric only; event definitions and promotion thresholds remain unfrozen",
    )
