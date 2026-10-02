from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

from .q040_baseline_selection_v01 import estimate_k1, estimate_k2


ENTRY_Q = (0.95, 0.975, 0.99)
RETURN_Q = (0.50, 0.60, 0.70)
SUSTAIN = (2, 3, 5)
MIN_SEP = (2, 5, 10)
FOLDS = ((2048, 2560), (2560, 3072), (3072, 3584), (3584, 4096))


@dataclass(frozen=True)
class MetricFit:
    kind: str
    scale: np.ndarray | None
    covariance: np.ndarray | None
    inverse_covariance: np.ndarray | None
    shrinkage: float | None
    effective_rank: float | None
    condition_number: float | None
    status: str


@dataclass(frozen=True)
class EstimatedEpisode:
    entry: int
    terminal: int
    outcome: str


def fit_baseline_full(world: dict, kind: str, window: int) -> tuple[np.ndarray, np.ndarray]:
    z = np.asarray(world["arrays"]["Z_observed"], dtype=float)
    update = np.asarray(world["arrays"]["update_mask"], dtype=bool)
    if kind == "K1":
        return estimate_k1(z, update, window=window, start=1)
    if kind == "K2":
        return estimate_k2(z, update, window=window, start=1)
    raise ValueError(kind)


def _residuals(z: np.ndarray, baseline: np.ndarray) -> np.ndarray:
    if z.shape != baseline.shape:
        raise ValueError("shape mismatch")
    return z - baseline


def _mad_scale(x: np.ndarray) -> np.ndarray:
    med = np.median(x, axis=0)
    mad = np.median(np.abs(x - med), axis=0)
    return np.maximum(1e-8, 1.4826 * mad)


def _ledoit_wolf_linear(x: np.ndarray) -> tuple[np.ndarray, float, float]:
    xc = x - np.mean(x, axis=0, keepdims=True)
    n, p = xc.shape
    S = (xc.T @ xc) / float(n)
    mu = float(np.trace(S) / p)
    F = np.eye(p) * mu
    delta = float(np.sum((S - F) ** 2) / p)

    if delta <= 0.0:
        lam = 0.0
        shrunk = S.copy()
    else:
        acc = 0.0
        for row in xc:
            outer = np.outer(row, row)
            acc += float(np.sum((outer - S) ** 2))
        beta_raw = acc / float(p * n * n)
        beta = min(beta_raw, delta)
        lam = float(beta / delta)
        shrunk = (1.0 - lam) * S + lam * F

    tr = float(np.trace(S))
    denom = float(np.trace(S @ S))
    eff = (tr * tr / denom) if denom > 0 else 0.0
    return shrunk, lam, eff


def fit_metric(train_resid: np.ndarray, kind: str) -> MetricFit:
    x = np.asarray(train_resid, dtype=float)
    good = np.all(np.isfinite(x), axis=1)
    x = x[good]
    if len(x) < 20:
        return MetricFit(kind, None, None, None, None, None, None, "REFUSED_INSUFFICIENT_TRAINING")

    if kind == "D1":
        scale = _mad_scale(x)
        return MetricFit("D1", scale, None, None, None, None, None, "OK")

    if kind != "D2":
        raise ValueError(kind)

    cov, lam, eff = _ledoit_wolf_linear(x)
    if np.any(~np.isfinite(cov)):
        return MetricFit("D2", None, cov, None, lam, eff, math.inf, "REFUSED_NONFINITE_COVARIANCE")
    if eff < 0.5 * x.shape[1]:
        return MetricFit("D2", None, cov, None, lam, eff, math.inf, "REFUSED_EFFECTIVE_RANK")
    cond = float(np.linalg.cond(cov))
    if not math.isfinite(cond) or cond > 1e6:
        return MetricFit("D2", None, cov, None, lam, eff, cond, "REFUSED_CONDITION")
    try:
        inv = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        return MetricFit("D2", None, cov, None, lam, eff, cond, "REFUSED_INVERSION")
    return MetricFit("D2", None, cov, inv, lam, eff, cond, "OK")


def metric_distance(resid: np.ndarray, fit: MetricFit) -> np.ndarray:
    r = np.asarray(resid, dtype=float)
    out = np.full(len(r), np.nan, dtype=float)
    good = np.all(np.isfinite(r), axis=1)
    if fit.status != "OK":
        return out
    if fit.kind == "D1":
        d = r[good] / fit.scale.reshape(1, -1)
        out[good] = np.sqrt(np.sum(d * d, axis=1))
    else:
        out[good] = np.sqrt(np.maximum(
            0.0,
            np.einsum("ni,ij,nj->n", r[good], fit.inverse_covariance, r[good]),
        ))
    return out


def detect_episodes(
    distance: np.ndarray,
    *,
    start: int,
    stop: int,
    entry_threshold: float,
    return_threshold: float,
    sustain: int,
    min_separation: int,
) -> list[EstimatedEpisode]:
    d = np.asarray(distance, dtype=float)
    eps: list[EstimatedEpisode] = []
    active_entry: int | None = None
    last_entry = -10**9
    return_run = 0

    def upcross(t: int) -> bool:
        if not math.isfinite(float(d[t])):
            return False
        p = t - 1
        if p < 0 or not math.isfinite(float(d[p])):
            return False
        return bool(d[p] < entry_threshold and d[t] >= entry_threshold)

    for t in range(start, stop):
        if active_entry is None:
            if upcross(t) and t - last_entry >= min_separation:
                active_entry = t
                last_entry = t
                return_run = 0
            continue

        if upcross(t) and t - last_entry >= min_separation:
            eps.append(EstimatedEpisode(active_entry, t, "INTERRUPTED_BY_NEW_PERTURBATION"))
            active_entry = t
            last_entry = t
            return_run = 0
            continue

        if math.isfinite(float(d[t])) and d[t] <= return_threshold:
            return_run += 1
            if return_run >= sustain:
                eps.append(EstimatedEpisode(active_entry, t, "SUSTAINED_RETURN"))
                active_entry = None
                return_run = 0
        else:
            return_run = 0

    if active_entry is not None:
        eps.append(EstimatedEpisode(active_entry, stop - 1, "RIGHT_CENSORED"))
    return eps


def _true_episodes_in_fold(world: dict, start: int, stop: int) -> list[dict]:
    out = []
    for ep in world["episodes"]:
        if start <= int(ep["entry_index"]) < stop:
            out.append(ep)
    return out


def score_detected_episodes(
    world: dict,
    estimated: list[EstimatedEpisode],
    *,
    start: int,
    stop: int,
    horizon: int = 80,
) -> dict[str, float | int]:
    true_eps = _true_episodes_in_fold(world, start, stop)
    est_entries = np.asarray([e.entry for e in estimated], dtype=int)

    entry_errors = []
    matched = 0
    false_entries = 0
    return_errors = []
    terminal_correct = 0
    terminal_total = 0

    used = set()
    for j, ep in enumerate(true_eps):
        t0 = int(ep["entry_index"])
        if j + 1 < len(true_eps):
            next_t = int(true_eps[j + 1]["entry_index"])
        else:
            next_t = stop
        candidates = [
            k for k, e in enumerate(estimated)
            if k not in used and t0 <= e.entry < next_t
        ]
        denom = max(1, next_t - t0)
        if not candidates:
            entry_errors.append(1.0)
            continue
        k = min(candidates, key=lambda q: estimated[q].entry)
        used.add(k)
        ee = estimated[k]
        matched += 1
        entry_errors.append(min(1.0, (ee.entry - t0) / denom))

        true_outcome = str(ep["outcome"])
        if true_outcome in {"SUSTAINED_RETURN", "INTERRUPTED_BY_NEW_PERTURBATION"}:
            terminal_total += 1
            if ee.outcome == true_outcome:
                terminal_correct += 1

        true_sr = ep.get("sustained_return_index")
        if true_sr is not None and t0 + horizon < stop:
            if ee.outcome == "SUSTAINED_RETURN":
                norm = max(1, min(horizon, denom))
                return_errors.append(min(1.0, abs(ee.terminal - int(true_sr)) / norm))
            else:
                return_errors.append(1.0)

    false_entries = max(0, len(estimated) - len(used))
    n_true = len(true_eps)
    return {
        "n_true": n_true,
        "n_estimated": len(estimated),
        "matched": matched,
        "recall": float(matched / n_true) if n_true else math.nan,
        "entry_error": float(np.mean(entry_errors)) if entry_errors else math.nan,
        "return_error": float(np.mean(return_errors)) if return_errors else math.nan,
        "false_ratio": float(false_entries / n_true) if n_true else math.nan,
        "terminal_concordance": (
            float(terminal_correct / terminal_total) if terminal_total else math.nan
        ),
    }


def fit_fold_distance(
    world: dict,
    *,
    baseline_kind: str,
    baseline_window: int,
    metric_kind: str,
    fold_start: int,
    fold_stop: int,
) -> tuple[np.ndarray, MetricFit] | None:
    z = np.asarray(world["arrays"]["Z_observed"], dtype=float)
    baseline, _ = fit_baseline_full(world, baseline_kind, baseline_window)
    resid = _residuals(z, baseline)
    train = resid[:fold_start]
    fit = fit_metric(train, metric_kind)
    if fit.status != "OK":
        return None
    return metric_distance(resid, fit), fit


def evaluate_event_grid_for_fold(
    world: dict,
    distance: np.ndarray,
    *,
    fold_start: int,
    fold_stop: int,
) -> list[dict[str, object]]:
    train_d = distance[:fold_start]
    finite_train = train_d[np.isfinite(train_d)]
    if len(finite_train) < 100:
        return []

    rows = []
    for qe in ENTRY_Q:
        entry = float(np.quantile(finite_train, qe))
        for sep in MIN_SEP:
            # Entry detections are reused across return/sustain combinations.
            for qr in RETURN_Q:
                ret = float(np.quantile(finite_train, qr))
                if not ret < entry:
                    continue
                for sustain in SUSTAIN:
                    estimated = detect_episodes(
                        distance,
                        start=fold_start,
                        stop=fold_stop,
                        entry_threshold=entry,
                        return_threshold=ret,
                        sustain=sustain,
                        min_separation=sep,
                    )
                    score = score_detected_episodes(
                        world,
                        estimated,
                        start=fold_start,
                        stop=fold_stop,
                        horizon=80,
                    )
                    rows.append({
                        "entry_q": qe,
                        "return_q": qr,
                        "sustain": sustain,
                        "min_separation": sep,
                        **score,
                    })
    return rows
