from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Any

import numpy as np

from .q040_estimator_stage1_v01 import (
    estimate_baseline,
    fit_metric,
    apply_metric,
    _innovation_residual,
    detect_episodes,
)
from .q040_observation_episode_v01 import (
    EXPECTED,
    SCALES,
    build_observation_episode_world,
    nc20_cells,
)


@dataclass
class EpisodeRecord:
    world_index: int
    entry: int
    terminal: int
    outcome: str
    features_m0: np.ndarray
    features_m2: np.ndarray
    return_threshold: float
    detected_amplitude: float
    observed_away_samples: float


@dataclass
class SoftmaxFit:
    status: str
    beta: np.ndarray | None
    objective: float
    iterations: int
    reason: str


def selected_config_from_stage1(stage1: dict[str, Any]) -> dict[str, Any]:
    b = stage1["selected_baseline_pre_full_pipeline_gate"]
    mt = stage1["selected_metric_event_tuple_pre_full_pipeline_gate"]
    return {
        "baseline_kind": b["kind"],
        "baseline_horizon": int(b["horizon"]),
        "metric": mt["metric"],
        "entry_q": float(mt["entry_q"]),
        "return_q": float(mt["return_q"]),
        "sustain_k": int(mt["sustain_k"]),
        "min_sep": int(mt["min_sep"]),
        "horizon": int(stage1["horizon"]["horizon"]),
    }


def _world_metric_objects(world: dict[str, Any], config: dict[str, Any]):
    z = world["arrays"]["Z_observed"]
    b, vel = estimate_baseline(
        z, config["baseline_kind"], config["baseline_horizon"]
    )
    resid = z - b
    train_stop = 2048
    fit = fit_metric(config["metric"], resid[:train_stop])
    if fit is None:
        return None
    d = apply_metric(config["metric"], resid, fit, innovation=False)
    j = apply_metric(
        config["metric"], _innovation_residual(resid), fit, innovation=True
    )
    train_d = d[:train_stop]
    train_j = j[:train_stop]
    train_d = train_d[np.isfinite(train_d)]
    train_j = train_j[np.isfinite(train_j)]
    if len(train_d) < 100 or len(train_j) < 100:
        return None
    et = float(np.quantile(train_d, config["entry_q"]))
    jt = float(np.quantile(train_j, config["entry_q"]))
    rt = float(np.quantile(train_d, config["return_q"]))
    return b, vel, resid, d, j, et, jt, rt


def build_episode_records(
    world: dict[str, Any],
    config: dict[str, Any],
    *,
    world_index: int,
) -> tuple[list[EpisodeRecord], dict[str, Any]]:
    objects = _world_metric_objects(world, config)
    if objects is None:
        return [], {"status": "METRIC_REFUSED"}
    b, vel, resid, d, j, et, jt, rt = objects

    detected = detect_episodes(
        d, j,
        entry_threshold=et,
        innovation_threshold=jt,
        return_threshold=rt,
        sustain_k=config["sustain_k"],
        min_sep=config["min_sep"],
        start=1,
        stop=len(d),
        horizon=config["horizon"],
    )

    z = world["arrays"]["Z_observed"]
    phase = world["arrays"]["session_phase"]
    native = world["arrays"]["native_covariates"]

    records: list[EpisodeRecord] = []
    cum_amp = 0.0
    cum_away = 0.0
    prev_entry: int | None = None

    for ep in detected:
        e = int(ep["entry"])
        t = int(ep["terminal"])
        if not (0 <= e < len(d) and e <= t < len(d)):
            continue
        if not (
            np.all(np.isfinite(z[e]))
            and np.all(np.isfinite(b[e]))
            and np.all(np.isfinite(vel[e]))
            and np.all(np.isfinite(resid[e]))
            and np.all(np.isfinite(native[e]))
        ):
            continue

        raw = resid[e]
        norm = float(np.linalg.norm(raw))
        if not math.isfinite(norm) or norm <= 1e-12:
            continue
        direction = raw / norm
        market_sign = float(np.sign(raw[3]))
        if market_sign == 0.0:
            market_sign = 1.0

        if prev_entry is None:
            elapsed = 0.0
            has_prior = 0.0
        else:
            elapsed = float(e - prev_entry)
            has_prior = 1.0

        m0 = np.concatenate([
            z[e],
            b[e],
            vel[e],
            np.asarray([float(d[e])]),
            direction,
            np.asarray([market_sign, elapsed, has_prior]),
            phase[e],
            native[e],
        ]).astype(float)

        m2 = np.concatenate([m0, np.asarray([cum_amp, cum_away])])

        seg = d[e:t + 1]
        away = float(np.sum(np.isfinite(seg) & (seg > rt)))

        if e >= 2048:
            records.append(EpisodeRecord(
                world_index=world_index,
                entry=e,
                terminal=t,
                outcome=str(ep["outcome"]),
                features_m0=m0,
                features_m2=m2,
                return_threshold=rt,
                detected_amplitude=float(d[e]),
                observed_away_samples=away,
            ))

        cum_amp += float(d[e])
        cum_away += away
        prev_entry = e

    return records, {
        "status": "COMPLETE",
        "detected_total": len(detected),
        "eligible_records": len(records),
        "entry_threshold": et,
        "innovation_threshold": jt,
        "return_threshold": rt,
    }


def _standardize_episode_features(
    train_records: list[EpisodeRecord],
    test_records: list[EpisodeRecord],
    which: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    attr = "features_m0" if which == "M0" else "features_m2"
    tr = np.vstack([getattr(r, attr) for r in train_records])
    te = np.vstack([getattr(r, attr) for r in test_records])
    mu = np.mean(tr, axis=0)
    sd = np.std(tr, axis=0, ddof=0)
    sd = np.where(np.isfinite(sd) & (sd > 1e-8), sd, 1.0)
    return (tr - mu) / sd, (te - mu) / sd, mu, sd


def _time_basis(h: np.ndarray, horizon: int) -> np.ndarray:
    x = np.asarray(h, dtype=float)
    return np.column_stack([
        x / float(horizon),
        (x / float(horizon)) ** 2,
        np.log1p(x) / math.log1p(horizon),
    ])


def _risk_rows(
    records: list[EpisodeRecord],
    standardized_features: np.ndarray,
    horizon: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rows = []
    y = []
    episode_index = []
    for i, (rec, feat) in enumerate(zip(records, standardized_features)):
        duration = min(horizon, max(1, rec.terminal - rec.entry))
        for h in range(1, duration + 1):
            row = np.concatenate([
                np.asarray([1.0]),
                feat,
                _time_basis(np.asarray([h]), horizon)[0],
            ])
            cls = 0
            if h == duration:
                if rec.outcome == "SUSTAINED_RETURN":
                    cls = 1
                elif rec.outcome == "INTERRUPTED_BY_NEW_PERTURBATION":
                    cls = 2
            rows.append(row)
            y.append(cls)
            episode_index.append(i)
    if not rows:
        return np.empty((0, 0)), np.empty(0, dtype=int), np.empty(0, dtype=int)
    return np.vstack(rows), np.asarray(y, dtype=int), np.asarray(episode_index, dtype=int)


def _softmax_probs(X: np.ndarray, beta: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    eta = np.clip(X @ beta, -30.0, 30.0)
    e1 = np.exp(eta[:, 0])
    e2 = np.exp(eta[:, 1])
    den = 1.0 + e1 + e2
    return 1.0 / den, e1 / den, e2 / den


def _objective(X: np.ndarray, y: np.ndarray, beta: np.ndarray, ridge: float) -> float:
    p0, p1, p2 = _softmax_probs(X, beta)
    probs = np.column_stack([p0, p1, p2])
    ll = -float(np.sum(np.log(np.maximum(probs[np.arange(len(y)), y], 1e-15))))
    pen = 0.5 * ridge * float(np.sum(beta[1:] ** 2))
    return ll + pen


def fit_competing_softmax(
    X: np.ndarray,
    y: np.ndarray,
    *,
    ridge: float = 1e-4,
    max_iter: int = 50,
) -> SoftmaxFit:
    if len(X) == 0 or X.ndim != 2 or len(y) != len(X):
        return SoftmaxFit("REFUSED", None, math.inf, 0, "empty_or_mismatched")
    if np.any(~np.isfinite(X)):
        return SoftmaxFit("REFUSED", None, math.inf, 0, "nonfinite_design")

    n, d = X.shape
    beta = np.zeros((d, 2), dtype=float)
    penalty = np.eye(d, dtype=float)
    penalty[0, 0] = 0.0

    old = _objective(X, y, beta, ridge)
    for it in range(1, max_iter + 1):
        p0, p1, p2 = _softmax_probs(X, beta)
        y1 = (y == 1).astype(float)
        y2 = (y == 2).astype(float)

        g1 = X.T @ (p1 - y1) + ridge * (penalty @ beta[:, 0])
        g2 = X.T @ (p2 - y2) + ridge * (penalty @ beta[:, 1])
        grad = np.concatenate([g1, g2])

        w11 = p1 * (1.0 - p1)
        w22 = p2 * (1.0 - p2)
        w12 = -p1 * p2

        H11 = X.T @ (X * w11[:, None]) + ridge * penalty
        H22 = X.T @ (X * w22[:, None]) + ridge * penalty
        H12 = X.T @ (X * w12[:, None])
        H = np.block([[H11, H12], [H12, H22]])

        solved = False
        step = None
        for damp in (0.0, 1e-8, 1e-6, 1e-4, 1e-2, 1.0):
            try:
                Hd = H + damp * np.eye(2 * d)
                step = np.linalg.solve(Hd, grad)
                solved = np.all(np.isfinite(step))
                if solved:
                    break
            except np.linalg.LinAlgError:
                pass
        if not solved or step is None:
            return SoftmaxFit("REFUSED", None, old, it, "newton_solve_failed")

        direction = np.column_stack([step[:d], step[d:]])
        accepted = False
        scale = 1.0
        candidate = beta
        new_obj = old
        for _ in range(15):
            candidate = beta - scale * direction
            new_obj = _objective(X, y, candidate, ridge)
            if math.isfinite(new_obj) and new_obj <= old:
                accepted = True
                break
            scale *= 0.5
        if not accepted:
            return SoftmaxFit("REFUSED", None, old, it, "line_search_failed")

        beta = candidate
        if np.max(np.abs(beta)) > 30.0:
            return SoftmaxFit("REFUSED", None, new_obj, it, "coefficient_limit")
        if abs(old - new_obj) <= 1e-7 * (1.0 + abs(old)):
            return SoftmaxFit("COMPLETE", beta, new_obj, it, "converged")
        old = new_obj

    if np.any(~np.isfinite(beta)):
        return SoftmaxFit("REFUSED", None, old, max_iter, "nonfinite_beta")
    return SoftmaxFit("COMPLETE", beta, old, max_iter, "max_iter_reached")


def _predict_cif(
    feature: np.ndarray,
    beta: np.ndarray,
    horizon: int,
) -> np.ndarray:
    h = np.arange(1, horizon + 1, dtype=float)
    X = np.column_stack([
        np.ones(horizon),
        np.repeat(feature[None, :], horizon, axis=0),
        _time_basis(h, horizon),
    ])
    p0, p1, p2 = _softmax_probs(X, beta)
    cif = np.zeros(horizon, dtype=float)
    survival = 1.0
    for i in range(horizon):
        cif[i] = (cif[i - 1] if i else 0.0) + survival * p1[i]
        survival *= p0[i]
    return cif


def episode_brier(
    rec: EpisodeRecord,
    cif: np.ndarray,
    horizon: int,
) -> float:
    duration = min(horizon, max(1, rec.terminal - rec.entry))
    vals = []
    for h in range(1, horizon + 1):
        if rec.outcome == "RIGHT_CENSORED" and h > duration:
            break
        observed = 0.0
        if rec.outcome == "SUSTAINED_RETURN" and h >= duration:
            observed = 1.0
        vals.append((observed - cif[h - 1]) ** 2)
    return float(np.mean(vals)) if vals else math.nan


def score_world_records(
    records: list[EpisodeRecord],
    standardized: np.ndarray,
    beta: np.ndarray,
    horizon: int,
    *,
    burden_direction: bool = False,
) -> tuple[float, float | None]:
    scores = []
    effects = []
    for rec, feat in zip(records, standardized):
        cif = _predict_cif(feat, beta, horizon)
        b = episode_brier(rec, cif, horizon)
        if math.isfinite(b):
            scores.append(b)
        if burden_direction:
            pert = feat.copy()
            pert[-2:] += 1.0
            cif2 = _predict_cif(pert, beta, horizon)
            effects.append(float(cif2[-1] - cif[-1]))
    score = float(np.mean(scores)) if scores else math.nan
    effect = float(np.mean(effects)) if effects else None
    return score, effect


def outer_world_folds(n_worlds: int = 200) -> list[tuple[np.ndarray, np.ndarray]]:
    if n_worlds != 200:
        raise ValueError("frozen qualification requires 200 worlds")
    out = []
    all_idx = np.arange(n_worlds)
    for k in range(5):
        test = np.arange(40 * k, 40 * (k + 1))
        train = np.setdiff1d(all_idx, test, assume_unique=True)
        out.append((train, test))
    return out


def qualify_m0_m2_world_panel(
    world_records: list[list[EpisodeRecord]],
    *,
    horizon: int,
) -> dict[str, Any]:
    if len(world_records) != 200:
        raise ValueError("exactly 200 world record sets required")

    world_results = [None] * 200
    fit_summaries = []

    for fold_id, (train_idx, test_idx) in enumerate(outer_world_folds(200), start=1):
        train_records = [r for i in train_idx for r in world_records[int(i)]]
        test_records = [r for i in test_idx for r in world_records[int(i)]]
        if not train_records or not test_records:
            return {"status": "INSUFFICIENT_SUPPORT", "reason": f"fold_{fold_id}_empty"}

        tr0, te0, mu0, sd0 = _standardize_episode_features(
            train_records, test_records, "M0"
        )
        tr2, te2, mu2, sd2 = _standardize_episode_features(
            train_records, test_records, "M2"
        )

        X0, y0, _ = _risk_rows(train_records, tr0, horizon)
        X2, y2, _ = _risk_rows(train_records, tr2, horizon)
        fit0 = fit_competing_softmax(X0, y0)
        fit2 = fit_competing_softmax(X2, y2)
        fit_summaries.append({
            "fold": fold_id,
            "m0": asdict(fit0),
            "m2": asdict(fit2),
            "train_episodes": len(train_records),
            "test_episodes": len(test_records),
        })
        if fit0.status != "COMPLETE" or fit2.status != "COMPLETE":
            return {
                "status": "ESTIMATOR_REFUSED",
                "reason": f"fold_{fold_id}_fit_refused",
                "fit_summaries": fit_summaries,
            }

        # Map standardized rows back to per-world subsets.
        offset = 0
        for wi in test_idx:
            recs = world_records[int(wi)]
            n = len(recs)
            if n == 0:
                world_results[int(wi)] = {
                    "status": "INSUFFICIENT_SUPPORT",
                    "brier_m0": math.nan,
                    "brier_m2": math.nan,
                    "adds": False,
                    "burden_cif_effect": math.nan,
                }
                continue

            # Standardize directly with training-fold moments.
            raw0 = np.vstack([r.features_m0 for r in recs])
            raw2 = np.vstack([r.features_m2 for r in recs])
            z0 = (raw0 - mu0) / sd0
            z2 = (raw2 - mu2) / sd2

            b0, _ = score_world_records(
                recs, z0, fit0.beta, horizon, burden_direction=False
            )
            b2, eff = score_world_records(
                recs, z2, fit2.beta, horizon, burden_direction=True
            )
            adds = bool(math.isfinite(b0) and math.isfinite(b2) and b2 < b0)
            world_results[int(wi)] = {
                "status": "COMPLETE" if math.isfinite(b0) and math.isfinite(b2) else "INSUFFICIENT_SUPPORT",
                "brier_m0": b0,
                "brier_m2": b2,
                "adds": adds,
                "burden_cif_effect": eff,
            }
            offset += n

    complete = [x for x in world_results if x and x["status"] == "COMPLETE"]
    add_rate = float(np.mean([x["adds"] for x in complete])) if complete else math.nan
    adding = [x for x in complete if x["adds"] and math.isfinite(x["burden_cif_effect"])]
    erosion_rate = (
        float(np.mean([x["burden_cif_effect"] < 0 for x in adding]))
        if adding else math.nan
    )
    adaptation_rate = (
        float(np.mean([x["burden_cif_effect"] > 0 for x in adding]))
        if adding else math.nan
    )
    support_fraction = len(complete) / 200.0

    return {
        "status": "COMPLETE" if len(complete) == 200 else "SUPPORT_REFUSALS_PRESENT",
        "support_fraction": support_fraction,
        "add_rate": add_rate,
        "erosion_direction_rate_among_adds": erosion_rate,
        "adaptation_direction_rate_among_adds": adaptation_rate,
        "world_results": world_results,
        "fit_summaries": fit_summaries,
    }


def qualification_disposition(control_id: str, summary: dict[str, Any]) -> dict[str, Any]:
    if summary["status"] not in {"COMPLETE", "SUPPORT_REFUSALS_PRESENT"}:
        return {"pass": False, "disposition": summary["status"]}
    if summary["support_fraction"] < 1.0:
        return {"pass": False, "disposition": "INSUFFICIENT_WORLD_SUPPORT"}

    add_rate = summary["add_rate"]
    er = summary["erosion_direction_rate_among_adds"]
    ad = summary["adaptation_direction_rate_among_adds"]

    if control_id == "NC-R2":
        ok = add_rate >= 0.80 and math.isfinite(er) and er >= 0.80
        disp = "HISTORY_ADDS_EROSION_DIRECTION" if ok else "EROSION_QUALIFICATION_FAIL"
    elif control_id == "NC-R4":
        ok = add_rate >= 0.80 and math.isfinite(ad) and ad >= 0.80
        disp = "HISTORY_ADDS_ADAPTATION_DIRECTION" if ok else "ADAPTATION_QUALIFICATION_FAIL"
    elif control_id in {"NC-R1", "NC-R3", "NC-R5", "NC-R15", "NC-R16", "NC-R17", "NC-R20"}:
        ok = add_rate <= 0.05
        disp = "NULL_FALSE_ADD_CONTROL_PASS" if ok else "FALSE_HISTORY_ADD"
    elif control_id == "NC-R17b":
        ok = True
        disp = "OMITTED_NATIVE_COVARIATE_AMBIGUITY_PRESERVED"
    else:
        ok = True
        disp = "DESCRIPTIVE_SECONDARY_ADJUDICATION"
    return {"pass": bool(ok), "disposition": disp}
