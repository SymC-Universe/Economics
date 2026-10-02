from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from .q039_layer_l_v04 import (
    SESSION_SECONDS,
    _ar2_state,
    _native_context,
    _phase_features,
    equal_day_block_bootstrap,
    walkforward_nested,
)


@dataclass(frozen=True)
class HeterogeneityResult:
    status: str
    point: float
    lower: float
    upper: float
    p_value: float
    valid_replicates: int
    total_replicates: int


def factor2_repaired_arrays(
    kind: str,
    *,
    seed: int,
    coarse_seconds: int = 30,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n = SESSION_SECONDS // coarse_seconds - 1
    current = _ar2_state(n, rng)
    prev = np.vstack([np.zeros((1, 2)), current[:-1]])

    latent = np.zeros(n)
    for i in range(1, n):
        latent[i] = 0.9 * latent[i - 1] + rng.normal(scale=0.4)

    native = _native_context(n, rng, latent if kind == "latent_regime" else None)
    if kind == "latent_regime":
        native[:, 0] = latent

    if kind == "latent_regime":
        delta = (
            0.8 * latent[:, None] * np.array([[1.0, -0.7]])
            + rng.normal(scale=0.35, size=(n, 2))
        )
        activity = latent
    else:
        delta = rng.normal(scale=0.8, size=(n, 2))
        activity = rng.normal(size=n)

    u_parent = 0.5 + 0.12 * np.tanh(
        0.8 * activity + rng.normal(scale=0.3, size=n)
    )
    du = 0.18 * np.tanh(
        0.7 * activity + rng.normal(scale=0.3, size=n)
    )
    u1 = u_parent - 0.5 * du
    u2 = u_parent + 0.5 * du
    if np.any((u1 <= 0) | (u1 >= 1) | (u2 <= 0) | (u2 >= 1)):
        raise AssertionError("synthetic update fractions left physical interval")
    native[:, -1] = u_parent

    last_event = 0.7 * activity + rng.normal(scale=0.25, size=n)
    event_contrast = 0.5 * activity + rng.normal(scale=0.25, size=n)
    signed_vol_contrast = 0.65 * activity + rng.normal(scale=0.25, size=n)

    N = np.column_stack([current, prev, _phase_features(n), native])

    old_A2 = np.column_stack([
        N,
        last_event,
        event_contrast,
        u2,
        du,
        signed_vol_contrast,
    ])
    repaired_A2 = np.column_stack([
        N,
        last_event,
        event_contrast,
        du,
        signed_vol_contrast,
    ])
    repaired_F2 = np.column_stack([repaired_A2, delta])

    phase = _phase_features(n)
    noise = rng.normal(scale=0.45, size=(n, 2))
    if kind == "phase_only":
        y = phase @ np.array([
            [0.8, -0.2],
            [0.1, 0.7],
            [0.35, 0.1],
            [-0.2, 0.3],
        ]) + noise
    elif kind == "coarse_sufficient":
        y = 0.75 * current + 0.18 * prev + noise
    elif kind == "latent_regime":
        y = 0.65 * current + native[:, 0, None] * np.array([[0.9, -0.75]]) + noise
    elif kind == "semantic_recency":
        y = 0.55 * current + 0.90 * delta + noise
    else:
        raise ValueError(kind)

    return old_A2, repaired_A2, repaired_F2, y


def factor2_rank_audit(*, seed: int = 20261001, coarse_seconds: int = 30) -> dict[str, int]:
    old_A2, repaired_A2, repaired_F2, _ = factor2_repaired_arrays(
        "coarse_sufficient", seed=seed, coarse_seconds=coarse_seconds
    )
    old_X = np.column_stack([np.ones(len(old_A2)), old_A2])
    repaired_X = np.column_stack([np.ones(len(repaired_A2)), repaired_A2])
    repaired_F = np.column_stack([np.ones(len(repaired_F2)), repaired_F2])
    return {
        "old_rank": int(np.linalg.matrix_rank(old_X)),
        "old_p": int(old_X.shape[1]),
        "repaired_a2_rank": int(np.linalg.matrix_rank(repaired_X)),
        "repaired_a2_p": int(repaired_X.shape[1]),
        "repaired_f2_rank": int(np.linalg.matrix_rank(repaired_F)),
        "repaired_f2_p": int(repaired_F.shape[1]),
    }


def run_repaired_factor2_truth(
    kind: str,
    *,
    base_seed: int,
    coarse_seconds: int = 30,
    reps: int = 3000,
) -> dict[str, object]:
    day_results = []
    deltas = []
    for d in range(5):
        _, A2, F2, y = factor2_repaired_arrays(
            kind, seed=base_seed + d, coarse_seconds=coarse_seconds
        )
        result, delta = walkforward_nested(
            A2,
            F2,
            y,
            coarse_seconds=coarse_seconds,
            small_name="A2_STAR",
            large_name="F2_STAR",
        )
        day_results.append(result)
        deltas.append(delta)

    if any(r.status != "COMPLETE" for r in day_results):
        return {
            "status": "INVALID_TEST",
            "day_results": [r.to_dict() for r in day_results],
        }

    boot = equal_day_block_bootstrap(
        deltas,
        coarse_seconds=coarse_seconds,
        reps=reps,
        ci_level=0.98333,
    )
    positive_days = sum(r.point_contrast > 0 for r in day_results)
    mae_both = (
        np.mean([r.mae_large_d for r in day_results])
        < np.mean([r.mae_small_d for r in day_results])
        and np.mean([r.mae_large_i for r in day_results])
        < np.mean([r.mae_small_i for r in day_results])
    )
    if boot["lower"] > 0 and positive_days >= 4 and mae_both:
        label = "LAST_FAST_SEMANTIC_ADDS_P0D"
    elif boot["upper"] <= 0:
        label = "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D"
    else:
        label = "NEED_MORE_INFO_OR_MIXED_P0D"

    return {
        "status": "COMPLETE",
        "label": label,
        "bootstrap": boot,
        "positive_days": positive_days,
        "mae_both_improve": bool(mae_both),
        "day_results": [r.to_dict() for r in day_results],
    }


def _noncircular_indices(n: int, block: int, rng: np.random.Generator) -> np.ndarray:
    if block < 1 or block > n:
        raise ValueError("invalid block length")
    pieces = []
    total = 0
    max_start = n - block
    while total < n:
        start = int(rng.integers(0, max_start + 1))
        idx = np.arange(start, start + block, dtype=int)
        pieces.append(idx)
        total += block
    return np.concatenate(pieces)[:n]


def bootstrap_regime_heterogeneity(
    gains_by_day: list[np.ndarray],
    high_by_day: list[np.ndarray],
    *,
    block_observations: int = 12,
    reps: int = 10_000,
    seed: int,
) -> HeterogeneityResult:
    if len(gains_by_day) != 5 or len(high_by_day) != 5:
        raise ValueError("exactly five fresh days are required")

    gains = [np.asarray(x, dtype=float) for x in gains_by_day]
    highs = [np.asarray(x, dtype=bool) for x in high_by_day]
    if any(len(g) != len(h) for g, h in zip(gains, highs)):
        raise ValueError("gain/mask length mismatch")
    if any(np.any(~np.isfinite(g)) for g in gains):
        raise ValueError("non-finite gains")

    pooled_high = sum(int(h.sum()) for h in highs)
    pooled_low = sum(int((~h).sum()) for h in highs)
    days_high5 = sum(int(h.sum()) >= 5 for h in highs)
    days_low5 = sum(int((~h).sum()) >= 5 for h in highs)

    if (
        pooled_high < 20
        or pooled_low < 20
        or days_high5 < 4
        or days_low5 < 4
        or any(h.sum() == 0 or (~h).sum() == 0 for h in highs)
    ):
        return HeterogeneityResult(
            "REGIME_HETEROGENEITY_INSUFFICIENT_SUPPORT",
            math.nan, math.nan, math.nan, math.nan, 0, reps,
        )

    day_points = [
        float(g[h].mean() - g[~h].mean())
        for g, h in zip(gains, highs)
    ]
    point = float(np.mean(day_points))

    rng = np.random.default_rng(seed)
    vals = []
    invalid = 0
    for _ in range(reps):
        ds = []
        for g, h in zip(gains, highs):
            idx = _noncircular_indices(len(g), block_observations, rng)
            gb = g[idx]
            hb = h[idx]
            if hb.sum() == 0 or (~hb).sum() == 0:
                invalid += 1
                ds = []
                break
            ds.append(float(gb[hb].mean() - gb[~hb].mean()))
        if ds:
            vals.append(float(np.mean(ds)))

    if invalid / reps > 0.01 or len(vals) == 0:
        return HeterogeneityResult(
            "REGIME_HETEROGENEITY_BOOTSTRAP_UNSTABLE",
            point, math.nan, math.nan, math.nan, len(vals), reps,
        )

    arr = np.asarray(vals, dtype=float)
    lower, upper = np.quantile(arr, [0.025, 0.975])
    centered = arr - point
    p = (1.0 + float(np.sum(np.abs(centered) >= abs(point)))) / (len(arr) + 1.0)
    return HeterogeneityResult(
        "COMPLETE",
        point,
        float(lower),
        float(upper),
        float(p),
        len(arr),
        reps,
    )


def holm_adjust(p_values: list[float]) -> list[float]:
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1 or np.any(~np.isfinite(p)) or np.any((p < 0) | (p > 1)):
        raise ValueError("invalid p-values")
    m = len(p)
    order = np.argsort(p)
    adjusted_sorted = np.empty(m, dtype=float)
    running = 0.0
    for k, idx in enumerate(order):
        value = min(1.0, (m - k) * float(p[idx]))
        running = max(running, value)
        adjusted_sorted[k] = running
    out = np.empty(m, dtype=float)
    for k, idx in enumerate(order):
        out[idx] = adjusted_sorted[k]
    return [float(x) for x in out]
