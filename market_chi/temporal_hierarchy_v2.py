from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Iterable, Sequence

import numpy as np


SEMANTIC_DIM = 2
PRIMARY_PAIRS = ((15, 30), (30, 60), (60, 300))
SESSION_SECONDS = 21 * 60 * 60
INITIAL_TRAIN_SECONDS = 5 * 60 * 60
REFIT_SECONDS = 60 * 60
BOOTSTRAP_BLOCK_SECONDS = 60 * 60


@dataclass(frozen=True)
class PairDayResult:
    status: str
    fine_seconds: int
    coarse_seconds: int
    lead_blocks: int
    n_observations: int
    n_predictions: int
    delta_b_mean: float
    delta_l_mean: float
    day_delta_b_mean: float
    depth_mae_baseline: float
    depth_mae_last: float
    depth_mae_structured: float
    imbalance_mae_baseline: float
    imbalance_mae_last: float
    imbalance_mae_structured: float
    depth_r2_baseline: float
    depth_r2_last: float
    depth_r2_structured: float
    imbalance_r2_baseline: float
    imbalance_r2_last: float
    imbalance_r2_structured: float
    max_train_target_end_ns: int | None
    min_test_source_start_ns: int | None
    leakage_guard_passed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class BootstrapResult:
    point: float
    lower: float
    upper: float
    reps_requested: int
    reps_valid: int
    block_length_observations: int
    seed: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _unit_semantic_directions() -> tuple[np.ndarray, np.ndarray]:
    sym = np.ones(20, dtype=float)
    imb = np.concatenate([np.ones(10, dtype=float), -np.ones(10, dtype=float)])
    sym /= np.linalg.norm(sym)
    imb /= np.linalg.norm(imb)
    return sym, imb


def semantic_scores_from_depth(depth20: np.ndarray) -> np.ndarray:
    """Project L10 bid/ask size vectors onto fixed semantic directions.

    Input columns must be bid levels 0..9 followed by ask levels 0..9.
    The transform is log1p then projection. No PCA is fit.
    """
    x = np.asarray(depth20, dtype=float)
    if x.ndim != 2 or x.shape[1] != 20:
        raise ValueError("depth20 must have shape (n, 20)")
    if np.any(~np.isfinite(x)) or np.any(x < 0):
        raise ValueError("depth20 must be finite and nonnegative")
    z = np.log1p(x)
    sym, imb = _unit_semantic_directions()
    return np.column_stack([z @ sym, z @ imb])


def _aggregate_fixed_blocks(
    times_ns: np.ndarray,
    semantic_seconds: np.ndarray,
    *,
    scale_seconds: int,
    day_start_ns: int,
    coverage_threshold: float = 0.80,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return eligible block indices, starts, and 2D mean semantic states."""
    t = np.asarray(times_ns, dtype=np.int64)
    s = np.asarray(semantic_seconds, dtype=float)
    if t.ndim != 1 or s.ndim != 2 or s.shape[1] != 2 or len(t) != len(s):
        raise ValueError("times/semantic shape mismatch")
    if scale_seconds < 1 or SESSION_SECONDS % scale_seconds != 0:
        raise ValueError("scale_seconds must divide the fixed 21-hour session")
    if np.any(~np.isfinite(s)):
        raise ValueError("semantic_seconds must be finite")
    if len(t) and np.any(np.diff(t) < 0):
        raise ValueError("times_ns must be monotone")

    scale_ns = int(scale_seconds * 1_000_000_000)
    session_end = day_start_ns + int(SESSION_SECONDS * 1_000_000_000)
    mask = (t >= day_start_ns) & (t < session_end)
    t = t[mask]
    s = s[mask]
    if not len(t):
        return (
            np.empty(0, dtype=int),
            np.empty(0, dtype=np.int64),
            np.empty((0, 2), dtype=float),
        )

    idx = ((t - day_start_ns) // scale_ns).astype(int)
    n_blocks = SESSION_SECONDS // scale_seconds
    states = np.full((n_blocks, 2), np.nan, dtype=float)
    counts = np.zeros(n_blocks, dtype=int)

    for b in np.unique(idx):
        rows = s[idx == b]
        counts[b] = len(rows)
        if len(rows) >= math.ceil(scale_seconds * coverage_threshold):
            states[b] = rows.mean(axis=0)

    good = np.all(np.isfinite(states), axis=1)
    block_idx = np.flatnonzero(good)
    starts = day_start_ns + block_idx.astype(np.int64) * scale_ns
    return block_idx, starts, states[good]


def _r2(y: np.ndarray, pred: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    pred = np.asarray(pred, dtype=float)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return math.nan if ss_tot <= 0 else 1.0 - ss_res / ss_tot


def _fit_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(train_x)), train_x])
    Xt = np.column_stack([np.ones(len(test_x)), test_x])
    beta, *_ = np.linalg.lstsq(X, train_y, rcond=None)
    return Xt @ beta


def _slope(values: np.ndarray) -> np.ndarray:
    n = len(values)
    t = np.arange(n, dtype=float)
    t -= t.mean()
    denom = float(np.sum(t * t))
    if denom <= 0:
        return np.zeros(values.shape[1], dtype=float)
    centered = values - values.mean(axis=0, keepdims=True)
    return np.sum(centered * t[:, None], axis=0) / denom


def build_pair_observations(
    times_ns: np.ndarray,
    semantic_seconds: np.ndarray,
    *,
    fine_seconds: int,
    coarse_seconds: int,
    day_start_ns: int,
    lead_blocks: int = 1,
    coverage_threshold: float = 0.80,
) -> dict[str, np.ndarray]:
    if lead_blocks < 1:
        raise ValueError("lead_blocks must be >= 1")
    if coarse_seconds % fine_seconds != 0:
        raise ValueError("coarse_seconds must be an integer multiple of fine_seconds")
    if (fine_seconds, coarse_seconds) not in PRIMARY_PAIRS:
        raise ValueError("pair is outside frozen hierarchy")

    fi, fs, fv = _aggregate_fixed_blocks(
        times_ns, semantic_seconds, scale_seconds=fine_seconds,
        day_start_ns=day_start_ns, coverage_threshold=coverage_threshold
    )
    ci, cs, cv = _aggregate_fixed_blocks(
        times_ns, semantic_seconds, scale_seconds=coarse_seconds,
        day_start_ns=day_start_ns, coverage_threshold=coverage_threshold
    )
    fmap = {int(i): fv[j] for j, i in enumerate(fi)}
    cmap = {int(i): cv[j] for j, i in enumerate(ci)}
    cstart = {int(i): int(cs[j]) for j, i in enumerate(ci)}
    factor = coarse_seconds // fine_seconds

    baseline = []
    last_fast = []
    structured = []
    targets = []
    source_blocks = []
    target_blocks = []
    source_starts = []
    target_ends = []

    for cb in sorted(cmap):
        tb = cb + lead_blocks
        if tb not in cmap:
            continue
        child = [cb * factor + j for j in range(factor)]
        if any(x not in fmap for x in child):
            continue
        fine_vals = np.vstack([fmap[x] for x in child])
        current = cmap[cb]
        phase = (cb * coarse_seconds) / SESSION_SECONDS
        cyc = np.array([math.sin(2 * math.pi * phase), math.cos(2 * math.pi * phase)])
        b = np.concatenate([current, cyc])
        l = np.concatenate([fine_vals[-1], cyc])
        extra = np.concatenate([fine_vals.std(axis=0), _slope(fine_vals)])
        st = np.concatenate([b, extra])

        baseline.append(b)
        last_fast.append(l)
        structured.append(st)
        targets.append(cmap[tb])
        source_blocks.append(cb)
        target_blocks.append(tb)
        source_starts.append(cstart[cb])
        target_ends.append(cstart[tb] + coarse_seconds * 1_000_000_000)

    return {
        "baseline_x": np.asarray(baseline, dtype=float),
        "last_x": np.asarray(last_fast, dtype=float),
        "structured_x": np.asarray(structured, dtype=float),
        "y": np.asarray(targets, dtype=float),
        "source_block": np.asarray(source_blocks, dtype=int),
        "target_block": np.asarray(target_blocks, dtype=int),
        "source_start_ns": np.asarray(source_starts, dtype=np.int64),
        "target_end_ns": np.asarray(target_ends, dtype=np.int64),
    }


def evaluate_pair_day(
    times_ns: np.ndarray,
    semantic_seconds: np.ndarray,
    *,
    fine_seconds: int,
    coarse_seconds: int,
    day_start_ns: int,
    lead_blocks: int = 1,
    coverage_threshold: float = 0.80,
) -> tuple[PairDayResult, dict[str, np.ndarray]]:
    obs = build_pair_observations(
        times_ns, semantic_seconds,
        fine_seconds=fine_seconds, coarse_seconds=coarse_seconds,
        day_start_ns=day_start_ns, lead_blocks=lead_blocks,
        coverage_threshold=coverage_threshold,
    )
    n = len(obs["y"])
    min_train_blocks = INITIAL_TRAIN_SECONDS // coarse_seconds
    test_chunk_blocks = REFIT_SECONDS // coarse_seconds
    min_eval_blocks = 8 * 60 * 60 // coarse_seconds

    if n < min_train_blocks + min_eval_blocks:
        result = PairDayResult(
            "REFUSED_INSUFFICIENT_EVALUATION", fine_seconds, coarse_seconds, lead_blocks,
            n, 0, *(math.nan for _ in range(14)), None, None, False,
            "fewer than 8 wall-clock hours of eligible post-training evaluation remain",
        )
        return result, obs

    y = obs["y"]
    px_b = np.full_like(y, np.nan)
    px_l = np.full_like(y, np.nan)
    px_s = np.full_like(y, np.nan)
    loss_b = np.full(n, np.nan)
    loss_l = np.full(n, np.nan)
    loss_s = np.full(n, np.nan)
    max_train_target_end = None
    min_test_source_start = None
    leakage_ok = True

    start_block = min_train_blocks
    max_source_block = int(np.max(obs["source_block"]))

    while start_block <= max_source_block:
        stop_block = start_block + test_chunk_blocks
        test_mask = (
            (obs["source_block"] >= start_block)
            & (obs["source_block"] < stop_block)
        )
        if not np.any(test_mask):
            start_block = stop_block
            continue
        first_test_ns = int(np.min(obs["source_start_ns"][test_mask]))
        train_mask = obs["target_end_ns"] <= first_test_ns
        if not np.any(train_mask):
            start_block = stop_block
            continue

        mt = int(np.max(obs["target_end_ns"][train_mask]))
        if mt > first_test_ns:
            leakage_ok = False
        max_train_target_end = mt if max_train_target_end is None else max(max_train_target_end, mt)
        min_test_source_start = first_test_ns if min_test_source_start is None else min(min_test_source_start, first_test_ns)

        train_y = y[train_mask]
        sd = train_y.std(axis=0)
        if np.any(~np.isfinite(sd)) or np.any(sd <= 0):
            start_block = stop_block
            continue

        pb = _fit_predict(obs["baseline_x"][train_mask], train_y, obs["baseline_x"][test_mask])
        pl = _fit_predict(obs["last_x"][train_mask], train_y, obs["last_x"][test_mask])
        ps = _fit_predict(obs["structured_x"][train_mask], train_y, obs["structured_x"][test_mask])
        px_b[test_mask] = pb
        px_l[test_mask] = pl
        px_s[test_mask] = ps
        yy = y[test_mask]
        loss_b[test_mask] = np.mean(((yy - pb) / sd) ** 2, axis=1)
        loss_l[test_mask] = np.mean(((yy - pl) / sd) ** 2, axis=1)
        loss_s[test_mask] = np.mean(((yy - ps) / sd) ** 2, axis=1)
        start_block = stop_block

    pred_mask = np.all(np.isfinite(px_s), axis=1) & np.isfinite(loss_s)
    if np.sum(pred_mask) < min_eval_blocks:
        result = PairDayResult(
            "REFUSED_INSUFFICIENT_EVALUATION", fine_seconds, coarse_seconds, lead_blocks,
            n, int(np.sum(pred_mask)), *(math.nan for _ in range(14)),
            max_train_target_end, min_test_source_start, leakage_ok,
            "fewer than 8 wall-clock hours of valid out-of-sample predictions",
        )
        return result, {**obs, "loss_b": loss_b, "loss_l": loss_l, "loss_s": loss_s}

    yy = y[pred_mask]
    pb = px_b[pred_mask]
    pl = px_l[pred_mask]
    ps = px_s[pred_mask]

    mae_b = np.mean(np.abs(yy - pb), axis=0)
    mae_l = np.mean(np.abs(yy - pl), axis=0)
    mae_s = np.mean(np.abs(yy - ps), axis=0)

    result = PairDayResult(
        "COMPLETE", fine_seconds, coarse_seconds, lead_blocks, n, int(np.sum(pred_mask)),
        float(np.mean(loss_b[pred_mask] - loss_s[pred_mask])),
        float(np.mean(loss_l[pred_mask] - loss_s[pred_mask])),
        float(np.mean(loss_b[pred_mask] - loss_s[pred_mask])),
        float(mae_b[0]), float(mae_l[0]), float(mae_s[0]),
        float(mae_b[1]), float(mae_l[1]), float(mae_s[1]),
        _r2(yy[:, 0], pb[:, 0]), _r2(yy[:, 0], pl[:, 0]), _r2(yy[:, 0], ps[:, 0]),
        _r2(yy[:, 1], pb[:, 1]), _r2(yy[:, 1], pl[:, 1]), _r2(yy[:, 1], ps[:, 1]),
        max_train_target_end, min_test_source_start, leakage_ok,
        "development-only fixed semantic hierarchy evaluation",
    )
    extra = {
        **obs,
        "pred_mask": pred_mask,
        "pred_baseline": px_b,
        "pred_last": px_l,
        "pred_structured": px_s,
        "loss_b": loss_b,
        "loss_l": loss_l,
        "loss_s": loss_s,
        "delta_b": loss_b - loss_s,
        "delta_l": loss_l - loss_s,
    }
    return result, extra


def circular_block_indices(n: int, block_length: int, rng: np.random.Generator) -> np.ndarray:
    if n < 1 or block_length < 1 or block_length > n:
        raise ValueError("invalid circular block request")
    chunks = []
    total = 0
    while total < n:
        start = int(rng.integers(0, n))
        idx = (start + np.arange(block_length, dtype=int)) % n
        chunks.append(idx)
        total += block_length
    return np.concatenate(chunks)[:n]


def bootstrap_delta_by_day(
    delta_by_day: Sequence[np.ndarray],
    *,
    coarse_seconds: int,
    reps: int = 10_000,
    seed: int = 20260929,
) -> BootstrapResult:
    arrays = [np.asarray(x, dtype=float) for x in delta_by_day]
    arrays = [x[np.isfinite(x)] for x in arrays]
    if not arrays or any(len(x) == 0 for x in arrays):
        raise ValueError("each day must contain finite delta observations")
    block_length = BOOTSTRAP_BLOCK_SECONDS // coarse_seconds
    if any(len(x) < block_length for x in arrays):
        raise ValueError("day too short for one-hour bootstrap block")
    point = float(np.mean(np.concatenate(arrays)))
    rng = np.random.default_rng(seed)
    vals = np.empty(reps, dtype=float)
    valid = 0
    for _ in range(reps):
        sampled = []
        for x in arrays:
            idx = circular_block_indices(len(x), block_length, rng)
            sampled.append(x[idx])
        v = float(np.mean(np.concatenate(sampled)))
        if np.isfinite(v):
            vals[valid] = v
            valid += 1
    if valid < int(0.95 * reps):
        raise RuntimeError("fewer than 95% bootstrap replicates valid")
    vals = vals[:valid]
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return BootstrapResult(point, float(lo), float(hi), reps, valid, block_length, seed)


def classify_pair(
    bootstrap: BootstrapResult,
    day_deltas: Sequence[float],
    *,
    depth_mae_baseline: float,
    depth_mae_structured: float,
    imbalance_mae_baseline: float,
    imbalance_mae_structured: float,
) -> str:
    if bootstrap.upper < 0:
        return "SUBTRACTS_P0D"
    positive_days = sum(float(x) > 0 for x in day_deltas if np.isfinite(x))
    both_mae = (
        depth_mae_structured < depth_mae_baseline
        and imbalance_mae_structured < imbalance_mae_baseline
    )
    if bootstrap.lower > 0 and positive_days >= 4 and both_mae:
        return "ADDS_P0D"
    return "NEED_MORE_INFO_OR_MIXED"
