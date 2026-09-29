from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

SESSION_SECONDS = 21 * 60 * 60
INITIAL_TRAIN_SECONDS = 5 * 60 * 60
REFIT_SECONDS = 60 * 60
BOOTSTRAP_SEED = 20260929


@dataclass(frozen=True)
class NestedDayResult:
    status: str
    coarse_seconds: int
    model_small: str
    model_large: str
    n_predictions: int
    point_contrast: float
    mae_small_d: float
    mae_large_d: float
    mae_small_i: float
    mae_large_i: float
    reason: str

    def to_dict(self):
        return asdict(self)


def _phase_features(n: int) -> np.ndarray:
    p = np.arange(n, dtype=float) / max(1, n)
    return np.column_stack([
        np.sin(2 * np.pi * p),
        np.cos(2 * np.pi * p),
        np.sin(4 * np.pi * p),
        np.cos(4 * np.pi * p),
    ])


def _ar2_state(n: int, rng: np.random.Generator, phi: float = 0.82) -> np.ndarray:
    x = np.zeros((n, 2), dtype=float)
    x[0] = rng.normal(scale=0.5, size=2)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + rng.normal(scale=0.35, size=2)
    return x


def _slope5(x: np.ndarray) -> np.ndarray:
    # x shape (..., 5, 2)
    t = np.arange(5, dtype=float)
    t -= t.mean()
    denom = float(np.sum(t * t))
    centered = x - x.mean(axis=-2, keepdims=True)
    return np.sum(centered * t.reshape((1,) * (x.ndim - 2) + (5, 1)), axis=-2) / denom


def _native_context(n: int, rng: np.random.Generator, latent: np.ndarray | None = None) -> np.ndarray:
    if latent is None:
        latent = rng.normal(size=n)
    event = np.exp(0.25 * latent + rng.normal(scale=0.2, size=n))
    volume = np.exp(0.20 * latent + rng.normal(scale=0.25, size=n))
    signed_volume = 0.6 * latent + rng.normal(scale=0.4, size=n)
    spread = np.exp(-0.10 * latent + rng.normal(scale=0.1, size=n))
    micro = 0.3 * latent + rng.normal(scale=0.3, size=n)
    imbalance = 0.5 * latent + rng.normal(scale=0.3, size=n)
    stale_mean = np.exp(-0.15 * latent + rng.normal(scale=0.15, size=n))
    stale_max = stale_mean + np.abs(rng.normal(scale=0.2, size=n))
    update = 1.0 / (1.0 + np.exp(-(0.5 * latent + rng.normal(scale=0.3, size=n))))
    return np.column_stack([
        np.log1p(event),
        np.log1p(volume),
        np.sign(signed_volume) * np.log1p(np.abs(signed_volume)),
        spread,
        micro,
        imbalance,
        stale_mean,
        stale_max,
        update,
    ])


def _base_N(current: np.ndarray, prev: np.ndarray, native: np.ndarray) -> np.ndarray:
    return np.column_stack([current, prev, _phase_features(len(current)), native])


def _train_standardize(train_x: np.ndarray, test_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu = train_x.mean(axis=0)
    sd = train_x.std(axis=0, ddof=0)
    if np.any(~np.isfinite(sd)) or np.any(sd <= 1e-12):
        keep = np.isfinite(sd) & (sd > 1e-12)
        train_x = train_x[:, keep]
        test_x = test_x[:, keep]
        mu = mu[keep]
        sd = sd[keep]
    return (train_x - mu) / sd, (test_x - mu) / sd


def _fit_predict_checked(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray):
    tr, te = _train_standardize(train_x, test_x)
    X = np.column_stack([np.ones(len(tr)), tr])
    Xt = np.column_stack([np.ones(len(te)), te])
    rank = int(np.linalg.matrix_rank(X))
    p = X.shape[1]
    cond = float(np.linalg.cond(X))
    if rank < p:
        return None, "RANK_DEFICIENT", rank, p, cond
    if cond > 1e8:
        return None, "ILL_CONDITIONED", rank, p, cond
    beta, *_ = np.linalg.lstsq(X, train_y, rcond=None)
    return Xt @ beta, "OK", rank, p, cond


def walkforward_nested(
    small_x: np.ndarray,
    large_x: np.ndarray,
    y: np.ndarray,
    *,
    coarse_seconds: int,
    small_name: str,
    large_name: str,
) -> tuple[NestedDayResult, np.ndarray]:
    n = len(y)
    if not (len(small_x) == len(large_x) == n):
        raise ValueError("length mismatch")
    pmax = max(small_x.shape[1], large_x.shape[1]) + 1
    min_train = max(INITIAL_TRAIN_SECONDS // coarse_seconds, 5 * pmax)
    chunk = max(1, REFIT_SECONDS // coarse_seconds)
    if n <= min_train + 1:
        return (
            NestedDayResult(
                "INVALID_TEST_INSUFFICIENT_IDENTIFICATION", coarse_seconds,
                small_name, large_name, 0, math.nan,
                math.nan, math.nan, math.nan, math.nan,
                "insufficient synthetic session length",
            ),
            np.empty(0),
        )

    loss_delta = np.full(n, np.nan)
    pred_s = np.full_like(y, np.nan)
    pred_l = np.full_like(y, np.nan)

    start = min_train
    while start < n:
        stop = min(n, start + chunk)
        train = np.arange(start)
        test = np.arange(start, stop)
        train_y = y[train]
        target_sd = train_y.std(axis=0, ddof=0)
        if np.any(target_sd <= 1e-12):
            start = stop
            continue

        ps, ss, *_ = _fit_predict_checked(small_x[train], train_y, small_x[test])
        pl, sl, *_ = _fit_predict_checked(large_x[train], train_y, large_x[test])
        if ss != "OK" or sl != "OK":
            start = stop
            continue

        pred_s[test] = ps
        pred_l[test] = pl
        es = (y[test] - ps) / target_sd
        el = (y[test] - pl) / target_sd
        ls = 0.5 * np.sum(es * es, axis=1)
        ll = 0.5 * np.sum(el * el, axis=1)
        loss_delta[test] = ls - ll
        start = stop

    mask = np.isfinite(loss_delta)
    required = 8 * 60 * 60 // coarse_seconds
    if int(mask.sum()) < required:
        return (
            NestedDayResult(
                "INVALID_TEST_INSUFFICIENT_IDENTIFICATION", coarse_seconds,
                small_name, large_name, int(mask.sum()), math.nan,
                math.nan, math.nan, math.nan, math.nan,
                "fewer than 8 wall-clock hours of synthetic OOS predictions",
            ),
            loss_delta[mask],
        )

    yy = y[mask]
    ps = pred_s[mask]
    pl = pred_l[mask]
    mae_s = np.mean(np.abs(yy - ps), axis=0)
    mae_l = np.mean(np.abs(yy - pl), axis=0)
    result = NestedDayResult(
        "COMPLETE", coarse_seconds, small_name, large_name, int(mask.sum()),
        float(np.mean(loss_delta[mask])),
        float(mae_s[0]), float(mae_l[0]),
        float(mae_s[1]), float(mae_l[1]),
        "synthetic walk-forward nested-model qualification",
    )
    return result, loss_delta[mask]


def _noncircular_indices(n: int, block: int, rng: np.random.Generator) -> np.ndarray:
    if block < 1 or block > n:
        raise ValueError("invalid block")
    out = []
    total = 0
    max_start = n - block
    while total < n:
        s = int(rng.integers(0, max_start + 1))
        idx = np.arange(s, s + block, dtype=int)
        out.append(idx)
        total += block
    return np.concatenate(out)[:n]


def equal_day_block_bootstrap(
    by_day: list[np.ndarray],
    *,
    coarse_seconds: int,
    reps: int = 10_000,
    seed: int = BOOTSTRAP_SEED,
    ci_level: float = 0.98333,
) -> dict[str, float]:
    arrays = [np.asarray(a, dtype=float) for a in by_day]
    block = max(1, 3600 // coarse_seconds)
    if any(len(a) < block for a in arrays):
        raise ValueError("synthetic OOS too short for one-hour block")
    point = float(np.mean([a.mean() for a in arrays]))
    rng = np.random.default_rng(seed)
    vals = np.empty(reps)
    for r in range(reps):
        vals[r] = np.mean([
            a[_noncircular_indices(len(a), block, rng)].mean()
            for a in arrays
        ])
    alpha = 1.0 - ci_level
    lo, hi = np.quantile(vals, [alpha / 2.0, 1.0 - alpha / 2.0])
    return {"point": point, "lower": float(lo), "upper": float(hi)}


def factor2_day(kind: str, *, seed: int, coarse_seconds: int = 30):
    rng = np.random.default_rng(seed)
    n = SESSION_SECONDS // coarse_seconds - 1
    current = _ar2_state(n, rng)
    prev = np.vstack([np.zeros((1, 2)), current[:-1]])
    latent = np.zeros(n)
    for i in range(1, n):
        latent[i] = 0.9 * latent[i - 1] + rng.normal(scale=0.4)

    native = _native_context(n, rng, latent if kind == "latent_regime" else None)
    N = _base_N(current, prev, native)

    if kind == "latent_regime":
        delta = 0.8 * latent[:, None] * np.array([[1.0, -0.7]]) + rng.normal(scale=0.35, size=(n, 2))
        activity_signal = latent
    else:
        delta = rng.normal(scale=0.8, size=(n, 2))
        activity_signal = rng.normal(size=n)

    child1 = current - 0.5 * delta
    child2 = current + 0.5 * delta

    last_event = 0.7 * activity_signal + rng.normal(scale=0.25, size=n)
    event_contrast = 0.5 * activity_signal + rng.normal(scale=0.25, size=n)
    last_update = 0.4 * activity_signal + rng.normal(scale=0.25, size=n)
    update_contrast = 0.35 * activity_signal + rng.normal(scale=0.25, size=n)
    signed_vol_contrast = 0.65 * activity_signal + rng.normal(scale=0.25, size=n)
    fine_native = np.column_stack([
        last_event, event_contrast, last_update, update_contrast, signed_vol_contrast
    ])

    A2 = np.column_stack([N, fine_native])
    F2 = np.column_stack([A2, child2 - child1])

    phase = _phase_features(n)
    noise = rng.normal(scale=0.45, size=(n, 2))
    if kind == "phase_only":
        y = phase @ np.array([[0.8, -0.2], [0.1, 0.7], [0.35, 0.1], [-0.2, 0.3]]) + noise
    elif kind == "coarse_sufficient":
        y = 0.75 * current + 0.18 * prev + noise
    elif kind == "latent_regime":
        y = 0.65 * current + latent[:, None] * np.array([[0.9, -0.75]]) + noise
    elif kind == "semantic_recency":
        y = 0.55 * current + 0.80 * delta + noise
    else:
        raise ValueError(kind)

    return A2, F2, y


def run_factor2_truth(
    kind: str,
    *,
    base_seed: int,
    coarse_seconds: int = 30,
    reps: int = 3000,
) -> dict[str, object]:
    day_results = []
    deltas = []
    for d in range(5):
        A2, F2, y = factor2_day(kind, seed=base_seed + d, coarse_seconds=coarse_seconds)
        r, delta = walkforward_nested(
            A2, F2, y,
            coarse_seconds=coarse_seconds,
            small_name="A2", large_name="F2",
        )
        day_results.append(r)
        deltas.append(delta)

    if any(r.status != "COMPLETE" for r in day_results):
        return {"status": "INVALID_TEST", "day_results": [r.to_dict() for r in day_results]}

    boot = equal_day_block_bootstrap(
        deltas, coarse_seconds=coarse_seconds, reps=reps, ci_level=0.98333
    )
    positive_days = sum(r.point_contrast > 0 for r in day_results)
    mae_both = (
        np.mean([r.mae_large_d for r in day_results]) < np.mean([r.mae_small_d for r in day_results])
        and np.mean([r.mae_large_i for r in day_results]) < np.mean([r.mae_small_i for r in day_results])
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


def _ordered_basis() -> tuple[np.ndarray, np.ndarray]:
    # Subspace with mean zero and last value fixed to zero.
    t = np.arange(5, dtype=float)
    constraints = np.vstack([np.ones(5), np.array([0, 0, 0, 0, 1.0])])
    # Null space via SVD.
    _, _, vh = np.linalg.svd(constraints)
    null = vh[2:].T  # 5 x 3
    slope = t - t.mean()
    slope_proj = null @ (null.T @ slope)
    v1 = slope_proj / np.linalg.norm(slope_proj)
    # A second vector orthogonal to v1 inside the constraint null.
    cand = null[:, 0]
    cand = cand - v1 * float(v1 @ cand)
    if np.linalg.norm(cand) < 1e-8:
        cand = null[:, 1] - v1 * float(v1 @ null[:, 1])
    v2 = cand / np.linalg.norm(cand)
    return v1, v2


def p60_day(*, seed: int, ordered_effect: float = 0.9, permuted_children: np.ndarray | None = None):
    rng = np.random.default_rng(seed)
    coarse_seconds = 300
    n = SESSION_SECONDS // coarse_seconds - 1
    current = _ar2_state(n, rng)
    prev = np.vstack([np.zeros((1, 2)), current[:-1]])
    native = _native_context(n, rng)
    N = _base_N(current, prev, native)

    v1, v2 = _ordered_basis()
    theta_d = rng.uniform(0, 2 * np.pi, size=n)
    theta_i = rng.uniform(0, 2 * np.pi, size=n)
    amp_d = rng.uniform(0.7, 1.3, size=n)
    amp_i = rng.uniform(0.7, 1.3, size=n)

    pat_d = amp_d[:, None] * (
        np.cos(theta_d)[:, None] * v1[None, :]
        + np.sin(theta_d)[:, None] * v2[None, :]
    )
    pat_i = amp_i[:, None] * (
        np.cos(theta_i)[:, None] * v1[None, :]
        + np.sin(theta_i)[:, None] * v2[None, :]
    )
    children = np.stack([
        current[:, 0, None] + pat_d,
        current[:, 1, None] + pat_i,
    ], axis=2)  # n,5,2

    # Fine-native child activity paths.
    event_children = rng.normal(size=(n, 5)) + native[:, 0, None]
    update_children = rng.normal(scale=0.3, size=(n, 5)) + native[:, -1, None]

    event_last = event_children[:, -1]
    event_sd = event_children.std(axis=1)
    event_slope = _slope5(event_children[:, :, None])[:, 0]
    update_last = update_children[:, -1]
    update_sd = update_children.std(axis=1)
    update_slope = _slope5(update_children[:, :, None])[:, 0]
    A = np.column_stack([
        N, event_last, event_sd, event_slope,
        update_last, update_sd, update_slope
    ])

    use_children = children.copy()
    if permuted_children is not None:
        # permutations shape n,4; indices for first four positions. Last remains fixed.
        first4 = np.take_along_axis(
            use_children[:, :4, :],
            permuted_children[:, :, None],
            axis=1,
        )
        use_children[:, :4, :] = first4

    sem_last = use_children[:, -1, :]
    sem_sd = use_children.std(axis=1)
    sem_slope = _slope5(use_children)

    L = np.column_stack([A, sem_last])
    U = np.column_stack([L, sem_sd])
    S = np.column_stack([U, sem_slope])

    true_slope = _slope5(children)
    y = 0.50 * current + ordered_effect * true_slope + rng.normal(scale=0.35, size=(n, 2))
    return A, L, U, S, y, children


def run_p60_ordered_truth(*, base_seed: int = 20261015, reps: int = 3000) -> dict[str, object]:
    a_s_results = []
    u_s_results = []
    a_s_delta = []
    u_s_delta = []

    for d in range(5):
        A, L, U, S, y, _ = p60_day(seed=base_seed + d)
        r_as, d_as = walkforward_nested(
            A, S, y, coarse_seconds=300, small_name="A", large_name="S"
        )
        r_us, d_us = walkforward_nested(
            U, S, y, coarse_seconds=300, small_name="U", large_name="S"
        )
        a_s_results.append(r_as)
        u_s_results.append(r_us)
        a_s_delta.append(d_as)
        u_s_delta.append(d_us)

    if any(r.status != "COMPLETE" for r in a_s_results + u_s_results):
        return {"status": "INVALID_TEST"}

    boot_as = equal_day_block_bootstrap(a_s_delta, coarse_seconds=300, reps=reps, ci_level=0.98333)
    boot_us = equal_day_block_bootstrap(u_s_delta, coarse_seconds=300, reps=reps, ci_level=0.95)
    positive_days = sum(r.point_contrast > 0 for r in a_s_results)
    mae_both = (
        np.mean([r.mae_large_d for r in a_s_results]) < np.mean([r.mae_small_d for r in a_s_results])
        and np.mean([r.mae_large_i for r in a_s_results]) < np.mean([r.mae_small_i for r in a_s_results])
    )
    primary_pass = boot_as["lower"] > 0 and positive_days >= 4 and mae_both
    if primary_pass and boot_us["lower"] > 0:
        label = "ORDERED_SEMANTIC_PATH_ADDS_P0D"
    elif primary_pass:
        label = "FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D"
    elif boot_as["upper"] <= 0:
        label = "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D"
    else:
        label = "NEED_MORE_INFO_OR_MIXED_P0D"

    return {
        "status": "COMPLETE",
        "label": label,
        "A_to_S": boot_as,
        "U_to_S": boot_us,
        "A_to_S_day_results": [r.to_dict() for r in a_s_results],
        "U_to_S_day_results": [r.to_dict() for r in u_s_results],
    }


def run_order_specificity(
    *,
    base_seed: int = 20261015,
    permutation_seed: int = 20261002,
    permutations: int = 200,
) -> dict[str, object]:
    # True order U->S point contrast across five days.
    true_day = []
    stored = []
    for d in range(5):
        A, L, U, S, y, children = p60_day(seed=base_seed + d)
        r, delta = walkforward_nested(
            U, S, y, coarse_seconds=300, small_name="U", large_name="S"
        )
        true_day.append(float(np.mean(delta)))
        stored.append((y, children, base_seed + d))
    true_point = float(np.mean(true_day))

    rng = np.random.default_rng(permutation_seed)
    perm_points = np.empty(permutations)
    for p in range(permutations):
        vals = []
        for y, children, seed in stored:
            n = len(children)
            perms = np.empty((n, 4), dtype=int)
            for i in range(n):
                perms[i] = rng.permutation(4)
            A, L, U, S, y2, _ = p60_day(seed=seed, permuted_children=perms)
            # y2 is deterministic for seed and therefore equals y.
            r, delta = walkforward_nested(
                U, S, y2, coarse_seconds=300, small_name="U", large_name="S"
            )
            vals.append(float(np.mean(delta)))
        perm_points[p] = float(np.mean(vals))
    q95 = float(np.quantile(perm_points, 0.95))
    return {
        "true_point": true_point,
        "permutation_q95": q95,
        "passes": bool(true_point > q95),
        "permutations": permutations,
        "seed": permutation_seed,
    }
