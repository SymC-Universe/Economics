from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Any

import numpy as np

from .q040_observation_episode_v01 import (
    BASE_COV_INV,
    EXPECTED,
    SCALES,
    build_observation_episode_world,
    nc20_cells,
)

FOLDS = (
    (0, 2048, 2048, 2560),
    (0, 2560, 2560, 3072),
    (0, 3072, 3072, 3584),
    (0, 3584, 3584, 4096),
)
BASELINE_CANDIDATES = (
    ("K1", 10), ("K1", 20), ("K1", 40),
    ("K2", 10), ("K2", 20), ("K2", 40),
)
ENTRY_Q = (0.95, 0.975, 0.99)
RETURN_Q = (0.50, 0.60, 0.70)
SUSTAIN_K = (2, 3, 5)
MIN_SEP = (2, 5, 10)
MAX_MATCH = 5
TUPLE_SCORE_HORIZON = 80


@dataclass(frozen=True)
class BaselineCandidateScore:
    kind: str
    horizon: int
    median_error: float
    n_cells: int
    unavailable_fraction: float


@dataclass(frozen=True)
class MetricTupleScore:
    metric: str
    entry_q: float
    return_q: float
    sustain_k: int
    min_sep: int
    entry_error: float
    return_error: float
    false_event_rate: float
    n_world_folds: int
    refused_folds: int


def estimate_baseline(z: np.ndarray, kind: str, horizon: int) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(z, dtype=float)
    n, p = z.shape
    b = np.full((n, p), np.nan, dtype=float)
    vel = np.full((n, p), np.nan, dtype=float)

    for t in range(1, n):
        lo = max(0, t - horizon)
        hist = z[lo:t]
        valid = np.all(np.isfinite(hist), axis=1)
        hv = hist[valid]
        if kind == "K1":
            if len(hv) < 5:
                continue
            b[t] = np.median(hv, axis=0)
            prev_lo = max(0, t - 1 - horizon)
            prev = z[prev_lo:t - 1]
            prev = prev[np.all(np.isfinite(prev), axis=1)]
            if len(prev) >= 5:
                prev_b = np.median(prev, axis=0)
                vel[t] = b[t] - prev_b
            else:
                vel[t] = 0.0
        elif kind == "K2":
            if len(hv) < 10:
                continue
            # Preserve actual lag positions after dropping invalid observations.
            idx = np.arange(lo, t, dtype=float)[valid]
            x = idx - float(t)
            X = np.column_stack([np.ones(len(x)), x])
            if np.linalg.matrix_rank(X) < 2:
                continue
            beta, *_ = np.linalg.lstsq(X, hv, rcond=None)
            b[t] = beta[0]
            vel[t] = beta[1]
        else:
            raise ValueError(kind)
    return b, vel


def baseline_error(world: dict[str, Any], kind: str, horizon: int) -> tuple[float, float]:
    z = world["arrays"]["Z_observed"]
    truth = world["arrays"]["baseline_true"]
    b, _ = estimate_baseline(z, kind, horizon)
    valid = np.all(np.isfinite(b), axis=1) & np.all(np.isfinite(z), axis=1)
    unavailable = 1.0 - float(np.mean(valid))
    if not np.any(valid):
        return math.inf, unavailable
    e = b[valid] - truth[valid]
    d = np.sqrt(np.maximum(0.0, np.einsum("ni,ij,nj->n", e, BASE_COV_INV, e)))
    return float(np.median(d)), unavailable


def robust_d1_fit(train_resid: np.ndarray) -> dict[str, Any] | None:
    x = train_resid[np.all(np.isfinite(train_resid), axis=1)]
    if len(x) < 20:
        return None
    center = np.median(x, axis=0)
    mad = np.median(np.abs(x - center), axis=0)
    scale = 1.4826 * mad
    scale = np.maximum(scale, 1e-8)
    if np.any(~np.isfinite(scale)):
        return None
    return {"metric": "D1", "center": center, "scale": scale}


def d1_distance(resid: np.ndarray, fit: dict[str, Any], *, innovation: bool = False) -> np.ndarray:
    x = np.asarray(resid, dtype=float)
    if innovation:
        y = x / fit["scale"]
    else:
        y = (x - fit["center"]) / fit["scale"]
    out = np.sqrt(np.sum(y * y, axis=1))
    out[np.any(~np.isfinite(x), axis=1)] = np.nan
    return out


def shrinkage_covariance(train_resid: np.ndarray) -> tuple[np.ndarray, float, float] | None:
    x = train_resid[np.all(np.isfinite(train_resid), axis=1)]
    if len(x) < 20:
        return None
    mean = np.mean(x, axis=0)
    xc = x - mean
    n, p = xc.shape
    S = (xc.T @ xc) / float(n)
    mu = float(np.trace(S) / p)
    T = mu * np.eye(p)
    gamma = float(np.sum((S - T) ** 2))
    beta_sum = 0.0
    for row in xc:
        outer = np.outer(row, row)
        beta_sum += float(np.sum((outer - S) ** 2))
    beta = beta_sum / float(n * n)
    if gamma <= 1e-18:
        lam = 1.0
    else:
        lam = min(1.0, max(0.0, beta / gamma))
    cov = (1.0 - lam) * S + lam * T
    eig = np.linalg.eigvalsh(cov)
    if np.any(~np.isfinite(eig)) or np.any(eig <= 0):
        return None
    reff = float(np.trace(cov) ** 2 / np.trace(cov @ cov))
    cond = float(np.max(eig) / np.min(eig))
    if reff < 0.5 * p or cond > 1e6:
        return None
    return cov, reff, cond


def d2_fit(train_resid: np.ndarray) -> dict[str, Any] | None:
    x = train_resid[np.all(np.isfinite(train_resid), axis=1)]
    if len(x) < 20:
        return None
    result = shrinkage_covariance(x)
    if result is None:
        return None
    cov, reff, cond = result
    mean = np.mean(x, axis=0)
    try:
        inv = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        return None
    if np.any(~np.isfinite(inv)):
        return None
    return {
        "metric": "D2",
        "mean": mean,
        "inv": inv,
        "effective_rank": reff,
        "condition": cond,
    }


def d2_distance(resid: np.ndarray, fit: dict[str, Any], *, innovation: bool = False) -> np.ndarray:
    x = np.asarray(resid, dtype=float)
    y = x if innovation else (x - fit["mean"])
    out = np.sqrt(np.maximum(0.0, np.einsum("ni,ij,nj->n", y, fit["inv"], y)))
    out[np.any(~np.isfinite(x), axis=1)] = np.nan
    return out


def fit_metric(metric: str, train_resid: np.ndarray) -> dict[str, Any] | None:
    if metric == "D1":
        return robust_d1_fit(train_resid)
    if metric == "D2":
        return d2_fit(train_resid)
    raise ValueError(metric)


def apply_metric(metric: str, resid: np.ndarray, fit: dict[str, Any], *, innovation: bool = False) -> np.ndarray:
    if metric == "D1":
        return d1_distance(resid, fit, innovation=innovation)
    return d2_distance(resid, fit, innovation=innovation)


def _innovation_residual(resid: np.ndarray) -> np.ndarray:
    out = np.full_like(resid, np.nan)
    valid = np.all(np.isfinite(resid[1:]), axis=1) & np.all(np.isfinite(resid[:-1]), axis=1)
    idx = np.flatnonzero(valid) + 1
    out[idx] = resid[idx] - resid[idx - 1]
    return out


def detect_episodes(
    d: np.ndarray,
    j: np.ndarray,
    *,
    entry_threshold: float,
    innovation_threshold: float,
    return_threshold: float,
    sustain_k: int,
    min_sep: int,
    start: int,
    stop: int,
    horizon: int = TUPLE_SCORE_HORIZON,
) -> list[dict[str, Any]]:
    episodes: list[dict[str, Any]] = []
    active: dict[str, Any] | None = None
    sustain_run = 0
    last_entry = -10**9

    for t in range(max(start, 1), stop):
        if not (math.isfinite(float(d[t])) and math.isfinite(float(j[t]))):
            continue

        if active is None:
            prev_ok = math.isfinite(float(d[t - 1]))
            crossing = prev_ok and d[t] >= entry_threshold and d[t - 1] < entry_threshold
            if crossing and t - last_entry >= min_sep:
                active = {"entry": t, "outcome": None, "terminal": None}
                last_entry = t
                sustain_run = 0
            continue

        if t - active["entry"] >= horizon:
            active["outcome"] = "RIGHT_CENSORED"
            active["terminal"] = t
            episodes.append(active)
            active = None
            sustain_run = 0
            continue

        if j[t] >= innovation_threshold and t - last_entry >= min_sep:
            active["outcome"] = "INTERRUPTED_BY_NEW_PERTURBATION"
            active["terminal"] = t
            episodes.append(active)
            active = {"entry": t, "outcome": None, "terminal": None}
            last_entry = t
            sustain_run = 0
            continue

        if d[t] <= return_threshold:
            sustain_run += 1
            if sustain_run >= sustain_k:
                active["outcome"] = "SUSTAINED_RETURN"
                active["terminal"] = t
                episodes.append(active)
                active = None
                sustain_run = 0
        else:
            sustain_run = 0

    if active is not None:
        active["outcome"] = "RIGHT_CENSORED"
        active["terminal"] = stop - 1
        episodes.append(active)
    return episodes


def _truth_episodes_in_range(world: dict[str, Any], start: int, stop: int) -> list[dict[str, Any]]:
    return [
        ep for ep in world["episodes"]
        if start <= int(ep["entry_index"]) < stop
    ]


def _greedy_matches(
    detected: list[dict[str, Any]],
    truth: list[dict[str, Any]],
    tolerance: int = MAX_MATCH,
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], int, int]:
    unmatched = set(range(len(detected)))
    pairs = []
    missed = 0
    for tr in truth:
        best = None
        best_dt = None
        for i in unmatched:
            dt = abs(int(detected[i]["entry"]) - int(tr["entry_index"]))
            if dt <= tolerance and (best_dt is None or dt < best_dt):
                best = i
                best_dt = dt
        if best is None:
            missed += 1
        else:
            pairs.append((detected[best], tr))
            unmatched.remove(best)
    return pairs, missed, len(unmatched)


def score_detected(
    detected: list[dict[str, Any]],
    truth: list[dict[str, Any]],
    horizon: int = TUPLE_SCORE_HORIZON,
) -> tuple[float, float, float]:
    if not truth:
        return math.inf, math.inf, float(len(detected) > 0)

    pairs, missed, false_n = _greedy_matches(detected, truth)
    entry_sum = sum(abs(int(d["entry"]) - int(t["entry_index"])) for d, t in pairs)
    entry_error = (entry_sum + 10.0 * missed) / len(truth)

    return_terms = []
    for d, t in pairs:
        if t["outcome"] != "SUSTAINED_RETURN":
            continue
        true_idx = int(t["sustained_return_index"])
        if d["outcome"] == "SUSTAINED_RETURN":
            return_terms.append(abs(int(d["terminal"]) - true_idx))
        else:
            return_terms.append(float(horizon))
    if not return_terms:
        true_sustained = sum(t["outcome"] == "SUSTAINED_RETURN" for t in truth)
        return_error = float(horizon if true_sustained else 0.0)
    else:
        return_error = float(np.mean(return_terms))

    false_rate = false_n / max(1, len(detected))
    return float(entry_error), return_error, float(false_rate)


def metric_fold_arrays(
    world: dict[str, Any],
    baseline_kind: str,
    baseline_horizon: int,
    metric: str,
    train_stop: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]] | None:
    z = world["arrays"]["Z_observed"]
    b, _ = estimate_baseline(z, baseline_kind, baseline_horizon)
    resid = z - b
    fit = fit_metric(metric, resid[:train_stop])
    if fit is None:
        return None
    d = apply_metric(metric, resid, fit, innovation=False)
    innov = _innovation_residual(resid)
    j = apply_metric(metric, innov, fit, innovation=True)
    return d, j, fit


def rank_event_tuples(
    worlds: list[dict[str, Any]],
    *,
    baseline_kind: str,
    baseline_horizon: int,
    metric: str,
) -> list[MetricTupleScore]:
    accum: dict[tuple[float, float, int, int], list[tuple[float, float, float]]] = {
        (qe, qr, sk, ms): []
        for qe in ENTRY_Q
        for qr in RETURN_Q
        for sk in SUSTAIN_K
        for ms in MIN_SEP
    }
    refused = 0
    usable = 0

    for world in worlds:
        for _, train_stop, test_start, test_stop in FOLDS:
            arrays = metric_fold_arrays(
                world, baseline_kind, baseline_horizon, metric, train_stop
            )
            if arrays is None:
                refused += 1
                continue
            d, j, _ = arrays
            train_d = d[:train_stop]
            train_j = j[:train_stop]
            train_d = train_d[np.isfinite(train_d)]
            train_j = train_j[np.isfinite(train_j)]
            if len(train_d) < 100 or len(train_j) < 100:
                refused += 1
                continue
            usable += 1
            truth = _truth_episodes_in_range(world, test_start, test_stop)

            for qe in ENTRY_Q:
                et = float(np.quantile(train_d, qe))
                jt = float(np.quantile(train_j, qe))
                for qr in RETURN_Q:
                    rt = float(np.quantile(train_d, qr))
                    for sk in SUSTAIN_K:
                        for ms in MIN_SEP:
                            det = detect_episodes(
                                d, j,
                                entry_threshold=et,
                                innovation_threshold=jt,
                                return_threshold=rt,
                                sustain_k=sk,
                                min_sep=ms,
                                start=test_start,
                                stop=test_stop,
                                horizon=TUPLE_SCORE_HORIZON,
                            )
                            accum[(qe, qr, sk, ms)].append(
                                score_detected(det, truth, TUPLE_SCORE_HORIZON)
                            )

    scores = []
    for key, vals in accum.items():
        if vals:
            arr = np.asarray(vals, dtype=float)
            entry = float(np.median(arr[:, 0]))
            ret = float(np.median(arr[:, 1]))
            false = float(np.median(arr[:, 2]))
        else:
            entry = ret = false = math.inf
        qe, qr, sk, ms = key
        scores.append(MetricTupleScore(
            metric, qe, qr, sk, ms, entry, ret, false, usable, refused
        ))

    return sorted(
        scores,
        key=lambda s: (
            s.entry_error,
            s.return_error,
            s.false_event_rate,
            ENTRY_Q.index(s.entry_q),
            SUSTAIN_K.index(s.sustain_k),
            -s.min_sep,
            RETURN_Q.index(s.return_q),
        ),
    )


def horizon_qualification(worlds: list[dict[str, Any]]) -> dict[str, Any]:
    # Generator truth only.
    required = {"NC-R1", "NC-R3", "NC-R4", "NC-R6", "NC-R7", "NC-R10", "NC-R15", "NC-R17", "NC-R20"}
    by_control: dict[str, list[dict[str, Any]]] = {}
    for w in worlds:
        cid = w["metadata"]["control_id"]
        if cid in required:
            by_control.setdefault(cid, []).extend(w["episodes"])

    def cif(episodes: list[dict[str, Any]], h: int) -> float:
        if not episodes:
            return math.nan
        count = 0
        for ep in episodes:
            if ep["outcome"] == "SUSTAINED_RETURN":
                dt = int(ep["sustained_return_index"]) - int(ep["entry_index"])
                if dt <= h:
                    count += 1
        return count / len(episodes)

    curves = {
        cid: {h: cif(eps, h) for h in (20, 40, 80)}
        for cid, eps in by_control.items()
    }

    for h, nxt in ((20, 40), (40, 80)):
        ok = True
        for cid, cur in curves.items():
            if not (math.isfinite(cur[h]) and math.isfinite(cur[nxt]) and math.isfinite(cur[80])):
                ok = False
                break
            if abs(cur[nxt] - cur[h]) >= 0.02:
                ok = False
                break
            if cur[80] > 0 and cur[h] / cur[80] < 0.90:
                ok = False
                break
        if ok:
            return {"horizon": h, "qualifier": None, "curves": curves}

    return {
        "horizon": 80,
        "qualifier": "HORIZON_SATURATION_NOT_ESTABLISHED",
        "curves": curves,
    }


def baseline_rank_key(x: BaselineCandidateScore) -> tuple[float, int, int]:
    class_rank = 0 if x.kind == "K1" else 1
    return (x.median_error, class_rank, x.horizon)


def metric_rank_key(x: MetricTupleScore) -> tuple[float, float, float, int]:
    return (
        x.entry_error,
        x.return_error,
        x.false_event_rate,
        0 if x.metric == "D1" else 1,
    )
