from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from .q040_observation_episode_v04 import (
    BASE_COV,
    NC20Cell,
    SCALES,
    build_observation_episode_world,
    nc20_cells,
)

GEOM_SEED = 20261005
WINDOWS = (10, 20, 40)
ENTRY_Q = (0.95, 0.975, 0.99)
RETURN_Q = (0.50, 0.60, 0.70)
SUSTAIN = (2, 3, 5)
MIN_SEP = (2, 5, 10)
P = 8
SIGMA_TRUE = np.sqrt(np.diag(BASE_COV))

BASELINE_CONTROLS = ("NC-R5", "NC-R15", "NC-R16")
METRIC_CONTROLS = (
    "NC-R1", "NC-R2", "NC-R3", "NC-R4", "NC-R5", "NC-R6",
    "NC-R11", "NC-R12", "NC-R13", "NC-R15", "NC-R16", "NC-R17",
    "NC-R18",
)
EVENT_CONTROLS = (
    "NC-R1", "NC-R2", "NC-R3", "NC-R4", "NC-R5", "NC-R6", "NC-R7",
    "NC-R9", "NC-R10", "NC-R11", "NC-R12", "NC-R13", "NC-R15",
    "NC-R16", "NC-R17", "NC-R17b", "NC-R18", "NC-R19",
)
STABLE_HORIZON_CONTROLS = ("NC-R1", "NC-R2", "NC-R5", "NC-R15", "NC-R16")

ORDINAL = {
    "NC-R1": 1, "NC-R2": 2, "NC-R3": 3, "NC-R4": 4, "NC-R5": 5,
    "NC-R6": 6, "NC-R7": 7, "NC-R8": 8, "NC-R9": 9, "NC-R10": 10,
    "NC-R11": 11, "NC-R12": 12, "NC-R13": 13, "NC-R14": 14,
    "NC-R15": 15, "NC-R16": 16, "NC-R17": 17, "NC-R17b": 18,
    "NC-R18": 19, "NC-R19": 20, "NC-R20": 21, "NC-R21": 22,
}


def _seed(control: str, scale: int, rep: int, cell: int = -1) -> int:
    cell_code = int(cell) + 1
    if cell_code < 0:
        raise ValueError("cell index must be -1 or non-negative")
    return int(np.random.SeedSequence(
        [GEOM_SEED, ORDINAL[control], int(scale), int(rep), cell_code]
    ).generate_state(1, dtype=np.uint32)[0])


def _past_roll_sums(x: np.ndarray, h: int) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    cs = np.concatenate([[0.0], np.cumsum(a)])
    t = np.arange(len(a), dtype=int)
    lo = np.maximum(0, t - h)
    return cs[t] - cs[lo]


def baseline_k1(z: np.ndarray, update: np.ndarray, h: int) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(z, dtype=float)
    update = np.asarray(update, dtype=bool)
    n, p = z.shape
    arr = np.where(update[:, None], z, np.nan)
    pad = np.full((h, p), np.nan)
    stacked = np.vstack([pad, arr])
    win = np.lib.stride_tricks.sliding_window_view(stacked, h, axis=0)[:n]
    with np.errstate(all="ignore"):
        b = np.nanmedian(win, axis=-1)
    counts = _past_roll_sums(update.astype(float), h)
    b[counts < 3] = np.nan
    vel = np.full_like(b, np.nan)
    good = np.all(np.isfinite(b[1:]), axis=1) & np.all(np.isfinite(b[:-1]), axis=1)
    vel[1:][good] = b[1:][good] - b[:-1][good]
    return b, vel


def baseline_k2(z: np.ndarray, update: np.ndarray, h: int) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(z, dtype=float)
    update = np.asarray(update, dtype=bool)
    n, p = z.shape
    idx = np.arange(n, dtype=float)
    m = update.astype(float)
    count = _past_roll_sums(m, h)
    sx = _past_roll_sums(idx * m, h)
    sx2 = _past_roll_sums(idx * idx * m, h)

    b = np.full((n, p), np.nan)
    slope = np.full((n, p), np.nan)
    for j in range(p):
        y = np.where(update, z[:, j], 0.0)
        sy = _past_roll_sums(y, h)
        sxy = _past_roll_sums(y * idx, h)
        ok = count >= 10
        denom = sx2 - np.divide(sx * sx, count, out=np.zeros_like(sx), where=count > 0)
        ok &= denom > 1e-12
        num = sxy - np.divide(sx * sy, count, out=np.zeros_like(sx), where=count > 0)
        bj = np.full(n, np.nan)
        sj = np.full(n, np.nan)
        sj[ok] = num[ok] / denom[ok]
        ybar = np.divide(sy, count, out=np.zeros_like(sy), where=count > 0)
        xbar = np.divide(sx, count, out=np.zeros_like(sx), where=count > 0)
        bj[ok] = ybar[ok] + sj[ok] * (idx[ok] - xbar[ok])
        b[:, j] = bj
        slope[:, j] = sj
    return b, slope


def baseline_estimate(kind: str, z: np.ndarray, update: np.ndarray, h: int):
    if kind == "K1":
        return baseline_k1(z, update, h)
    if kind == "K2":
        return baseline_k2(z, update, h)
    raise ValueError(kind)


def baseline_world_score(world: dict[str, Any], kind: str, h: int) -> tuple[float, float]:
    a = world["arrays"]
    b, _ = baseline_estimate(kind, a["Z_observed"], a["update_mask"], h)
    truth = np.asarray(a["baseline_true"], dtype=float)
    idx = np.arange(len(b)) >= 2048
    finite = idx & np.all(np.isfinite(b), axis=1)
    coverage = float(np.sum(finite) / np.sum(idx))
    if not np.any(finite):
        return math.inf, coverage
    e = (b[finite] - truth[finite]) / SIGMA_TRUE[None, :]
    err = np.sqrt(np.mean(e * e, axis=1))
    return float(np.median(err)), coverage


def corner_nc20_cells() -> list[NC20Cell]:
    wanted = [
        (0.20, "IID", 0.0, 0.75),
        (0.20, "CLUSTERED", 5e-8, 1.50),
        (0.80, "IID", 5e-8, 1.50),
        (0.80, "CLUSTERED", 0.0, 0.75),
    ]
    out = []
    for w in wanted:
        for c in nc20_cells():
            if (
                abs(c.update_density - w[0]) < 1e-12
                and c.gap_structure == w[1]
                and abs(c.curvature - w[2]) < 1e-15
                and abs(c.noise_multiplier - w[3]) < 1e-12
            ):
                out.append(c)
                break
    if len(out) != 4:
        raise RuntimeError("NC-R20 corner-cell resolution failed")
    return out


def qualify_baselines() -> dict[str, Any]:
    records: dict[str, dict[int, dict[str, Any]]] = {
        k: {h: {"errors": [], "coverages": []} for h in WINDOWS}
        for k in ("K1", "K2")
    }

    for control in BASELINE_CONTROLS:
        for scale in SCALES:
            for rep in range(8):
                w = build_observation_episode_world(
                    control, seed=_seed(control, scale, rep), scale_seconds=scale
                )
                for kind in ("K1", "K2"):
                    for h in WINDOWS:
                        e, c = baseline_world_score(w, kind, h)
                        records[kind][h]["errors"].append(e)
                        records[kind][h]["coverages"].append(c)

    for j, cell in enumerate(nc20_cells()):
        for scale in SCALES:
            for rep in range(8):
                w = build_observation_episode_world(
                    "NC-R20",
                    seed=_seed("NC-R20", scale, rep, j),
                    scale_seconds=scale,
                    nc20_cell=cell,
                )
                for kind in ("K1", "K2"):
                    for h in WINDOWS:
                        e, c = baseline_world_score(w, kind, h)
                        records[kind][h]["errors"].append(e)
                        records[kind][h]["coverages"].append(c)

    classes = []
    detail = {}
    for kind in ("K1", "K2"):
        candidates = []
        for h in WINDOWS:
            errs = np.asarray(records[kind][h]["errors"], dtype=float)
            cov = np.asarray(records[kind][h]["coverages"], dtype=float)
            eligible = bool(np.all(cov >= 0.90) and np.all(np.isfinite(errs)))
            score = float(np.median(errs)) if eligible else math.inf
            item = {
                "window": h,
                "eligible": eligible,
                "median_error": score,
                "min_coverage": float(np.min(cov)),
                "median_coverage": float(np.median(cov)),
                "world_count": int(len(cov)),
            }
            candidates.append(item)
        candidates.sort(key=lambda x: (x["median_error"], x["window"]))
        best = candidates[0]
        detail[kind] = {"candidates": candidates, "best": best}
        if best["eligible"]:
            classes.append({
                "kind": kind,
                "window": best["window"],
                "median_error": best["median_error"],
            })
    classes.sort(key=lambda x: (
        x["median_error"],
        0 if x["kind"] == "K1" else 1,
    ))
    return {"ranked": classes, "detail": detail}


def fit_metric(
    world: dict[str, Any],
    baseline_kind: str,
    baseline_window: int,
    metric: str,
    train_end: int = 2048,
) -> dict[str, Any]:
    a = world["arrays"]
    z = np.asarray(a["Z_observed"], dtype=float)
    update = np.asarray(a["update_mask"], dtype=bool)
    b, vel = baseline_estimate(baseline_kind, z, update, baseline_window)
    r = z - b
    train = (
        (np.arange(len(z)) < train_end)
        & update
        & np.all(np.isfinite(r), axis=1)
    )
    X = r[train]
    if len(X) < 5 * P:
        return {"status": "REFUSED_TRAINING_SUPPORT"}

    center = np.median(X, axis=0)
    Xc = X - center

    if metric == "D1":
        mad = np.median(np.abs(X - center), axis=0) * 1.4826
        mad = np.maximum(mad, 1e-8)
        if np.any(~np.isfinite(mad)):
            return {"status": "REFUSED_D1_SCALE"}
        d = np.full(len(z), np.nan)
        good = np.all(np.isfinite(r), axis=1)
        rr = (r[good] - center) / mad
        d[good] = np.sqrt(np.sum(rr * rr, axis=1))
        return {
            "status": "OK",
            "distance": d,
            "baseline": b,
            "velocity": vel,
            "center": center,
            "scale": mad,
        }

    if metric != "D2":
        raise ValueError(metric)

    n = len(Xc)
    S = (Xc.T @ Xc) / float(n)
    mu = float(np.trace(S) / P)
    F = mu * np.eye(P)
    delta = float(np.sum((S - F) ** 2))
    outer = Xc[:, :, None] * Xc[:, None, :]
    beta = float(np.sum((outer - S[None, :, :]) ** 2) / (n * n))
    alpha = 1.0 if delta <= 1e-15 else float(np.clip(beta / delta, 0.0, 1.0))
    cov = (1.0 - alpha) * S + alpha * F

    if np.any(~np.isfinite(cov)):
        return {"status": "REFUSED_D2_NONFINITE"}
    eig = np.linalg.eigvalsh(cov)
    if np.any(eig <= 0):
        return {"status": "REFUSED_D2_NONPOSITIVE"}
    weights = eig / np.sum(eig)
    erank = float(np.exp(-np.sum(weights * np.log(weights))))
    cond = float(np.max(eig) / np.min(eig))
    if erank < 0.5 * P:
        return {"status": "REFUSED_D2_EFFECTIVE_RANK", "effective_rank": erank}
    if cond > 1e6:
        return {"status": "REFUSED_D2_CONDITION", "condition": cond}

    inv = np.linalg.inv(cov)
    d = np.full(len(z), np.nan)
    good = np.all(np.isfinite(r), axis=1)
    rr = r[good] - center
    d[good] = np.sqrt(np.maximum(0.0, np.einsum("ni,ij,nj->n", rr, inv, rr)))
    return {
        "status": "OK",
        "distance": d,
        "baseline": b,
        "velocity": vel,
        "center": center,
        "covariance": cov,
        "shrinkage": alpha,
        "effective_rank": erank,
        "condition": cond,
    }


def detect_crossings(d: np.ndarray, threshold: float, start: int, min_sep: int) -> np.ndarray:
    x = np.asarray(d, dtype=float)
    finite = np.isfinite(x)
    prev = np.concatenate([[False], finite[:-1] & (x[:-1] < threshold)])
    cross = finite & (x >= threshold) & prev
    ids = np.flatnonzero(cross & (np.arange(len(x)) >= start))
    out = []
    last = -10**9
    for i in ids:
        if i - last >= min_sep:
            out.append(int(i))
            last = int(i)
    return np.asarray(out, dtype=int)


def match_entries(truth: np.ndarray, detected: np.ndarray, tol: int = 5) -> dict[str, Any]:
    truth = np.asarray(truth, dtype=int)
    detected = np.asarray(detected, dtype=int)
    used = np.zeros(len(detected), dtype=bool)
    pairs = []
    errors = []
    for t in truth:
        cand = np.flatnonzero((~used) & (np.abs(detected - t) <= tol))
        if len(cand) == 0:
            errors.append(10.0)
            continue
        j = int(cand[np.argmin(np.abs(detected[cand] - t))])
        used[j] = True
        pairs.append((int(t), int(detected[j])))
        errors.append(float(abs(int(detected[j]) - int(t))))
    false = int(np.sum(~used))
    return {
        "pairs": pairs,
        "mean_error": float(np.mean(errors)) if errors else math.nan,
        "false_rate": float(false / max(1, len(truth))),
        "matched": len(pairs),
        "false": false,
    }


def qualify_metrics(baseline_ranked: list[dict[str, Any]]) -> dict[str, Any]:
    if not baseline_ranked:
        return {"ranked": [], "detail": {}, "status": "BASELINE_OPERATOR_REFUSED"}
    bk = baseline_ranked[0]["kind"]
    bw = int(baseline_ranked[0]["window"])
    corner = corner_nc20_cells()
    scores = {}

    for metric in ("D1", "D2"):
        errs = []
        falses = []
        valid = 0
        total = 0
        refusals: dict[str, int] = {}
        for control in METRIC_CONTROLS:
            for scale in SCALES:
                for rep in range(4):
                    w = build_observation_episode_world(
                        control, seed=_seed(control, scale, rep), scale_seconds=scale
                    )
                    total += 1
                    fit = fit_metric(w, bk, bw, metric)
                    if fit["status"] != "OK":
                        refusals[fit["status"]] = refusals.get(fit["status"], 0) + 1
                        continue
                    valid += 1
                    d = fit["distance"]
                    train = d[:2048]
                    train = train[np.isfinite(train)]
                    truth = np.flatnonzero(
                        (w["arrays"]["shock_input"] != 0)
                        & (np.arange(len(d)) >= 2048)
                    )
                    for q in ENTRY_Q:
                        thr = float(np.quantile(train, q))
                        det = detect_crossings(d, thr, 2048, 5)
                        m = match_entries(truth, det)
                        if math.isfinite(m["mean_error"]):
                            errs.append(m["mean_error"])
                            falses.append(m["false_rate"])

        for j, cell in enumerate(corner):
            for scale in SCALES:
                for rep in range(4):
                    w = build_observation_episode_world(
                        "NC-R20",
                        seed=_seed("NC-R20", scale, rep, j),
                        scale_seconds=scale,
                        nc20_cell=cell,
                    )
                    total += 1
                    fit = fit_metric(w, bk, bw, metric)
                    if fit["status"] != "OK":
                        refusals[fit["status"]] = refusals.get(fit["status"], 0) + 1
                        continue
                    valid += 1
                    d = fit["distance"]
                    train = d[:2048]
                    train = train[np.isfinite(train)]
                    truth = np.flatnonzero(
                        (w["arrays"]["shock_input"] != 0)
                        & (np.arange(len(d)) >= 2048)
                    )
                    for q in ENTRY_Q:
                        thr = float(np.quantile(train, q))
                        det = detect_crossings(d, thr, 2048, 5)
                        m = match_entries(truth, det)
                        if math.isfinite(m["mean_error"]):
                            errs.append(m["mean_error"])
                            falses.append(m["false_rate"])

        valid_fraction = valid / max(1, total)
        eligible = valid_fraction >= 0.95 and len(errs) > 0
        scores[metric] = {
            "eligible": eligible,
            "valid_fraction": float(valid_fraction),
            "median_entry_error": float(np.median(errs)) if errs else math.inf,
            "median_false_rate": float(np.median(falses)) if falses else math.inf,
            "refusals": refusals,
            "world_count": total,
        }

    ranked = []
    for metric, d in scores.items():
        if d["eligible"]:
            ranked.append({
                "metric": metric,
                "median_entry_error": d["median_entry_error"],
                "median_false_rate": d["median_false_rate"],
            })
    ranked.sort(key=lambda x: (
        x["median_entry_error"],
        x["median_false_rate"],
        0 if x["metric"] == "D1" else 1,
    ))
    return {"ranked": ranked, "detail": scores, "baseline_used": {"kind": bk, "window": bw}}


def estimated_episodes(
    d: np.ndarray,
    entry_thr: float,
    return_thr: float,
    sustain: int,
    min_sep: int,
    start: int = 2048,
    horizon: int = 80,
) -> list[dict[str, Any]]:
    entries = detect_crossings(d, entry_thr, start, min_sep)
    out = []
    n = len(d)
    for j, e in enumerate(entries):
        next_e = int(entries[j + 1]) if j + 1 < len(entries) else n
        limit = min(n, e + horizon + 1, next_e + 1)
        run = 0
        terminal = None
        outcome = None
        for t in range(e + 1, limit):
            if np.isfinite(d[t]) and d[t] <= return_thr:
                run += 1
                if run >= sustain:
                    terminal = t
                    outcome = "SUSTAINED_RETURN"
                    break
            else:
                run = 0
        if outcome is None and next_e < min(n, e + horizon + 1):
            terminal = next_e
            outcome = "INTERRUPTED_BY_NEW_PERTURBATION"
        elif outcome is None:
            terminal = min(n - 1, e + horizon)
            outcome = "RIGHT_CENSORED"
        out.append({
            "entry_index": int(e),
            "terminal_index": int(terminal),
            "outcome": outcome,
        })
    return out


def score_event_tuple(
    world: dict[str, Any],
    fit: dict[str, Any],
    entry_q: float,
    return_q: float,
    sustain: int,
    min_sep: int,
) -> tuple[float, float, float]:
    d = fit["distance"]
    train = d[:2048]
    train = train[np.isfinite(train)]
    if len(train) < 100:
        return math.inf, math.inf, math.inf
    et = float(np.quantile(train, entry_q))
    rt = float(np.quantile(train, return_q))
    est = estimated_episodes(d, et, rt, sustain, min_sep)
    detected = np.asarray([x["entry_index"] for x in est], dtype=int)

    true_eps = [
        ep for ep in world["episodes"]
        if ep["entry_index"] >= 2048
    ]
    truth = np.asarray([ep["entry_index"] for ep in true_eps], dtype=int)
    matched = match_entries(truth, detected)
    if not math.isfinite(matched["mean_error"]):
        return math.inf, math.inf, math.inf

    est_map = {x["entry_index"]: x for x in est}
    true_map = {x["entry_index"]: x for x in true_eps}
    ret_errs = []
    for te, de in matched["pairs"]:
        tr = true_map[te]
        er = est_map[de]
        if tr["outcome"] == "SUSTAINED_RETURN" and er["outcome"] == "SUSTAINED_RETURN":
            ret_errs.append(abs(int(er["terminal_index"]) - int(tr["terminal_index"])))
        elif tr["outcome"] != "SUSTAINED_RETURN" and er["outcome"] != "SUSTAINED_RETURN":
            ret_errs.append(0.0 if tr["outcome"] == er["outcome"] else 80.0)
        else:
            ret_errs.append(80.0)
    if len(matched["pairs"]) < len(true_eps):
        ret_errs.extend([80.0] * (len(true_eps) - len(matched["pairs"])))
    return (
        matched["mean_error"],
        float(np.mean(ret_errs)) if ret_errs else 80.0,
        matched["false_rate"],
    )


def qualify_event_tuple(
    baseline_ranked: list[dict[str, Any]],
    metric_ranked: list[dict[str, Any]],
) -> dict[str, Any]:
    if not baseline_ranked or not metric_ranked:
        return {"status": "REFUSED", "selected": None}
    bk = baseline_ranked[0]["kind"]
    bw = int(baseline_ranked[0]["window"])
    metric = metric_ranked[0]["metric"]
    corner = corner_nc20_cells()

    tuples = [
        (eq, rq, su, ms)
        for eq in ENTRY_Q for rq in RETURN_Q for su in SUSTAIN for ms in MIN_SEP
    ]
    accum = {t: [[], [], []] for t in tuples}

    for control in EVENT_CONTROLS:
        for scale in SCALES:
            for rep in range(4):
                w = build_observation_episode_world(
                    control, seed=_seed(control, scale, rep), scale_seconds=scale
                )
                fit = fit_metric(w, bk, bw, metric)
                if fit["status"] != "OK":
                    continue
                for t in tuples:
                    s = score_event_tuple(w, fit, *t)
                    for k in range(3):
                        if math.isfinite(s[k]):
                            accum[t][k].append(s[k])

    for j, cell in enumerate(corner):
        for scale in SCALES:
            for rep in range(4):
                w = build_observation_episode_world(
                    "NC-R20",
                    seed=_seed("NC-R20", scale, rep, j),
                    scale_seconds=scale,
                    nc20_cell=cell,
                )
                fit = fit_metric(w, bk, bw, metric)
                if fit["status"] != "OK":
                    continue
                for t in tuples:
                    s = score_event_tuple(w, fit, *t)
                    for k in range(3):
                        if math.isfinite(s[k]):
                            accum[t][k].append(s[k])

    scored = []
    for t, vals in accum.items():
        if any(len(v) == 0 for v in vals):
            continue
        item = {
            "entry_q": t[0],
            "return_q": t[1],
            "sustain": t[2],
            "min_sep": t[3],
            "median_entry_error": float(np.median(vals[0])),
            "median_return_error": float(np.median(vals[1])),
            "median_false_rate": float(np.median(vals[2])),
            "world_scores": len(vals[0]),
        }
        scored.append(item)

    scored.sort(key=lambda x: (
        x["median_entry_error"],
        x["median_return_error"],
        x["median_false_rate"],
        x["entry_q"],
        abs(x["return_q"] - 0.60),
        x["return_q"],
        x["sustain"],
        -x["min_sep"],
    ))
    return {
        "status": "PASS" if scored else "EVENT_DEFINITION_REFUSED",
        "selected": scored[0] if scored else None,
        "top10": scored[:10],
        "baseline_used": {"kind": bk, "window": bw},
        "metric_used": metric,
    }


def truth_cif(world: dict[str, Any], horizon: int) -> float:
    eps = [
        ep for ep in world["episodes"]
        if ep["entry_index"] + 80 < len(world["arrays"]["time_index"])
    ]
    if not eps:
        return math.nan
    nret = 0
    for ep in eps:
        if ep["outcome"] == "SUSTAINED_RETURN":
            lag = int(ep["terminal_index"]) - int(ep["entry_index"])
            if lag <= horizon:
                nret += 1
    return float(nret / len(eps))


def qualify_horizon() -> dict[str, Any]:
    rows = []
    for control in STABLE_HORIZON_CONTROLS:
        for scale in SCALES:
            for rep in range(4):
                w = build_observation_episode_world(
                    control, seed=_seed(control, scale, 100 + rep), scale_seconds=scale
                )
                rows.append({
                    "control": control,
                    "scale": scale,
                    "cell": None,
                    "c20": truth_cif(w, 20),
                    "c40": truth_cif(w, 40),
                    "c80": truth_cif(w, 80),
                })
    for j, cell in enumerate(nc20_cells()):
        for scale in SCALES:
            for rep in range(2):
                w = build_observation_episode_world(
                    "NC-R20",
                    seed=_seed("NC-R20", scale, 100 + rep, j),
                    scale_seconds=scale,
                    nc20_cell=cell,
                )
                rows.append({
                    "control": "NC-R20",
                    "scale": scale,
                    "cell": cell.key(),
                    "c20": truth_cif(w, 20),
                    "c40": truth_cif(w, 40),
                    "c80": truth_cif(w, 80),
                })

    finite = [r for r in rows if all(math.isfinite(r[k]) for k in ("c20","c40","c80"))]
    pass20 = all(
        abs(r["c20"] - r["c40"]) < 0.02
        and r["c20"] >= 0.90 * r["c80"]
        for r in finite
    )
    pass40 = all(
        abs(r["c40"] - r["c80"]) < 0.02
        and r["c40"] >= 0.90 * r["c80"]
        for r in finite
    )
    if pass20:
        h = 20
        qualifier = None
    elif pass40:
        h = 40
        qualifier = None
    else:
        h = 80
        qualifier = "HORIZON_SATURATION_NOT_ESTABLISHED"
    return {
        "selected_horizon": h,
        "qualifier": qualifier,
        "world_count": len(finite),
        "worst_abs_20_40": max(abs(r["c20"]-r["c40"]) for r in finite),
        "worst_abs_40_80": max(abs(r["c40"]-r["c80"]) for r in finite),
        "min_ratio_20_to_80": min(
            (r["c20"]/r["c80"]) if r["c80"] > 0 else 1.0 for r in finite
        ),
        "min_ratio_40_to_80": min(
            (r["c40"]/r["c80"]) if r["c80"] > 0 else 1.0 for r in finite
        ),
    }


def self_test() -> dict[str, Any]:
    w = build_observation_episode_world("NC-R1", seed=123456, scale_seconds=60)
    k1, _ = baseline_k1(w["arrays"]["Z_observed"], w["arrays"]["update_mask"], 20)
    k2, _ = baseline_k2(w["arrays"]["Z_observed"], w["arrays"]["update_mask"], 20)
    assert k1.shape == (4096, 8)
    assert k2.shape == (4096, 8)
    fit = fit_metric(w, "K1", 20, "D1")
    assert fit["status"] == "OK"
    d = fit["distance"]
    tr = d[:2048][np.isfinite(d[:2048])]
    thr = float(np.quantile(tr, 0.975))
    det = detect_crossings(d, thr, 2048, 5)
    truth = np.flatnonzero(
        (w["arrays"]["shock_input"] != 0)
        & (np.arange(len(d)) >= 2048)
    )
    m = match_entries(truth, det)
    assert math.isfinite(m["mean_error"])
    eps = estimated_episodes(d, thr, float(np.quantile(tr, 0.60)), 3, 5)
    assert isinstance(eps, list)
    return {
        "status": "PASS",
        "k1_finite_fraction": float(np.mean(np.all(np.isfinite(k1), axis=1))),
        "k2_finite_fraction": float(np.mean(np.all(np.isfinite(k2), axis=1))),
        "matched_entries": m["matched"],
    }


def run_all() -> dict[str, Any]:
    baseline = qualify_baselines()
    metric = qualify_metrics(baseline["ranked"])
    event = qualify_event_tuple(baseline["ranked"], metric["ranked"])
    horizon = qualify_horizon()

    passed = bool(
        baseline["ranked"]
        and metric["ranked"]
        and event["status"] == "PASS"
        and horizon["selected_horizon"] in (20, 40, 80)
    )
    return {
        "schema_version": "q040-estimator-geometry-result-v0.1",
        "real_q040_outcomes_opened": False,
        "synthetic_lineage": "v0.4",
        "geometry_freeze_commit": "bfe84c38016a62b03822120416413f9b8b9576da",
        "baseline": baseline,
        "metric": metric,
        "event_definition": event,
        "horizon": horizon,
        "disposition": (
            "Q040_SYNTHETIC_ESTIMATOR_GEOMETRY_PASS"
            if passed else
            "Q040_SYNTHETIC_ESTIMATOR_GEOMETRY_REFUSED"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output")
    args = ap.parse_args()

    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return 0

    if not args.output:
        raise SystemExit("--output is required unless --self-test is used")

    result = run_all()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "disposition": result["disposition"],
        "baseline_selected": result["baseline"]["ranked"][:1],
        "metric_selected": result["metric"]["ranked"][:1],
        "event_selected": result["event_definition"]["selected"],
        "horizon": result["horizon"],
    }, indent=2))
    return 0 if result["disposition"].endswith("_PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
