from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

import numpy as np

OUTCOME_CENSOR = 0
OUTCOME_RETURN = 1
OUTCOME_INTERRUPT = 2

TIME_BINS = 8
MAX_ITER = 100
GRAD_TOL = 1e-8
HESSIAN_COND_MAX = 1e10
CENSORING_G_MIN = 0.05


@dataclass(frozen=True)
class Standardizer:
    mean: np.ndarray
    scale: np.ndarray
    active_columns: np.ndarray


@dataclass(frozen=True)
class CompetingRiskFit:
    status: str
    beta: np.ndarray | None
    standardizer: Standardizer | None
    iterations: int
    gradient_max_norm: float
    hessian_condition: float
    log_likelihood: float
    reason: str


@dataclass(frozen=True)
class CensoringKM:
    status: str
    g_after: np.ndarray
    g_left: np.ndarray
    minimum_g: float
    reason: str


@dataclass(frozen=True)
class BootstrapSummary:
    point: float
    ci_low: float
    ci_high: float
    p_two_sided: float
    positive_count: int
    n_boot: int


def grouped_confirmatory_folds() -> list[tuple[np.ndarray, np.ndarray]]:
    reps = np.arange(30, dtype=int)
    out = []
    for fold in range(5):
        test = reps[reps % 5 == fold]
        train = reps[reps % 5 != fold]
        out.append((train, test))
    return out


def time_bin_index(k: int, horizon: int) -> int:
    if horizon < 8:
        raise ValueError("horizon must support eight frozen time bins")
    if not 1 <= int(k) <= int(horizon):
        raise ValueError("time outside scoring horizon")
    return min(7, int(((int(k) - 1) * 8) // int(horizon)))


def time_bin_dummies(k: int, horizon: int) -> np.ndarray:
    b = time_bin_index(k, horizon)
    out = np.zeros(7, dtype=float)
    if b > 0:
        out[b - 1] = 1.0
    return out


def fit_standardizer(features: np.ndarray) -> Standardizer:
    x = np.asarray(features, dtype=float)
    if x.ndim != 2 or len(x) == 0:
        raise ValueError("features must be nonempty 2D")
    if np.any(~np.isfinite(x)):
        raise ValueError("nonfinite training feature")
    mean = np.mean(x, axis=0)
    scale = np.std(x, axis=0, ddof=0)
    active = np.isfinite(scale) & (scale > 1e-12)
    return Standardizer(mean=mean, scale=scale, active_columns=active)


def transform_features(features: np.ndarray, standardizer: Standardizer) -> np.ndarray:
    x = np.asarray(features, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(standardizer.mean):
        raise ValueError("feature shape mismatch")
    if np.any(~np.isfinite(x)):
        raise ValueError("nonfinite feature")
    if not np.any(standardizer.active_columns):
        return np.empty((len(x), 0), dtype=float)
    cols = standardizer.active_columns
    return (x[:, cols] - standardizer.mean[cols]) / standardizer.scale[cols]


def build_risk_design(
    features: np.ndarray,
    durations: np.ndarray,
    outcomes: np.ndarray,
    horizon: int,
    *,
    standardizer: Standardizer | None = None,
) -> tuple[np.ndarray, np.ndarray, Standardizer]:
    x = np.asarray(features, dtype=float)
    d = np.asarray(durations, dtype=int)
    y_episode = np.asarray(outcomes, dtype=int)
    if len(x) != len(d) or len(x) != len(y_episode):
        raise ValueError("episode arrays differ in length")
    if np.any(d < 1):
        raise ValueError("durations must be positive")
    if np.any(~np.isin(y_episode, [OUTCOME_CENSOR, OUTCOME_RETURN, OUTCOME_INTERRUPT])):
        raise ValueError("invalid outcome code")
    std = fit_standardizer(x) if standardizer is None else standardizer
    z = transform_features(x, std)

    rows: list[np.ndarray] = []
    cls: list[int] = []
    for i in range(len(x)):
        raw_duration = int(d[i])
        stop = min(raw_duration, int(horizon))
        for k in range(1, stop + 1):
            row = np.concatenate(([1.0], z[i], time_bin_dummies(k, horizon)))
            terminal_inside = raw_duration <= horizon and k == raw_duration
            code = int(y_episode[i]) if terminal_inside and y_episode[i] in (1, 2) else 0
            rows.append(row)
            cls.append(code)
    if not rows:
        raise ValueError("empty risk design")
    return np.vstack(rows), np.asarray(cls, dtype=int), std


def _probabilities(X: np.ndarray, beta: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    eta = np.asarray(X, dtype=float) @ np.asarray(beta, dtype=float)
    m = np.maximum(0.0, np.max(eta, axis=1))
    e0 = np.exp(-m)
    e1 = np.exp(eta[:, 0] - m)
    e2 = np.exp(eta[:, 1] - m)
    den = e0 + e1 + e2
    return e0 / den, e1 / den, e2 / den


def _log_likelihood(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> float:
    eta = X @ beta
    m = np.maximum(0.0, np.max(eta, axis=1))
    logden = m + np.log(np.exp(-m) + np.exp(eta[:, 0] - m) + np.exp(eta[:, 1] - m))
    ll = -np.sum(logden)
    ll += float(np.sum(eta[y == 1, 0]))
    ll += float(np.sum(eta[y == 2, 1]))
    return float(ll)


def _information_and_gradient(
    X: np.ndarray,
    y: np.ndarray,
    beta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    _, p1, p2 = _probabilities(X, beta)
    y1 = (y == 1).astype(float)
    y2 = (y == 2).astype(float)
    g1 = X.T @ (y1 - p1)
    g2 = X.T @ (y2 - p2)
    grad = np.concatenate([g1, g2])

    w11 = p1 * (1.0 - p1)
    w22 = p2 * (1.0 - p2)
    w12 = -p1 * p2
    i11 = X.T @ (X * w11[:, None])
    i22 = X.T @ (X * w22[:, None])
    i12 = X.T @ (X * w12[:, None])
    info = np.block([[i11, i12], [i12, i22]])
    cond = float(np.linalg.cond(info))
    return info, grad, cond


def fit_competing_risk_hazard(
    features: np.ndarray,
    durations: np.ndarray,
    outcomes: np.ndarray,
    horizon: int,
) -> CompetingRiskFit:
    try:
        X, y, std = build_risk_design(features, durations, outcomes, horizon)
    except Exception as exc:
        return CompetingRiskFit(
            "REFUSED", None, None, 0, math.inf, math.inf, -math.inf,
            f"design_error:{exc}",
        )

    if np.linalg.matrix_rank(X) < X.shape[1]:
        return CompetingRiskFit(
            "REFUSED", None, std, 0, math.inf, math.inf, -math.inf,
            "rank_deficient_after_zero_variance_removal",
        )

    d = X.shape[1]
    beta = np.zeros((d, 2), dtype=float)
    ll = _log_likelihood(X, y, beta)
    last_cond = math.inf
    last_grad = math.inf

    for iteration in range(1, MAX_ITER + 1):
        info, grad, cond = _information_and_gradient(X, y, beta)
        last_cond = cond
        last_grad = float(np.max(np.abs(grad)))
        if not math.isfinite(cond) or cond > HESSIAN_COND_MAX:
            return CompetingRiskFit(
                "REFUSED", None, std, iteration, last_grad, cond, ll,
                "hessian_condition",
            )
        if last_grad <= GRAD_TOL:
            return CompetingRiskFit(
                "COMPLETE", beta, std, iteration, last_grad, cond, ll,
                "converged",
            )
        try:
            step = np.linalg.solve(info, grad)
        except np.linalg.LinAlgError:
            return CompetingRiskFit(
                "REFUSED", None, std, iteration, last_grad, cond, ll,
                "newton_solve_failed",
            )
        direction = np.column_stack([step[:d], step[d:]])
        accepted = False
        factor = 1.0
        candidate = beta
        candidate_ll = ll
        for _ in range(40):
            candidate = beta + factor * direction
            candidate_ll = _log_likelihood(X, y, candidate)
            if math.isfinite(candidate_ll) and candidate_ll >= ll - 1e-12:
                accepted = True
                break
            factor *= 0.5
        if not accepted:
            return CompetingRiskFit(
                "REFUSED", None, std, iteration, last_grad, cond, ll,
                "no_finite_improving_newton_step",
            )
        beta = candidate
        ll = candidate_ll

    info, grad, cond = _information_and_gradient(X, y, beta)
    return CompetingRiskFit(
        "REFUSED", None, std, MAX_ITER,
        float(np.max(np.abs(grad))), float(cond), float(ll),
        "convergence_not_reached",
    )


def predict_hazards(
    fit: CompetingRiskFit,
    features: np.ndarray,
    horizon: int,
) -> np.ndarray:
    if fit.status != "COMPLETE" or fit.beta is None or fit.standardizer is None:
        raise ValueError("fit is not qualified")
    z = transform_features(features, fit.standardizer)
    n = len(z)
    out = np.empty((n, horizon, 2), dtype=float)
    for k in range(1, horizon + 1):
        dummies = time_bin_dummies(k, horizon)
        X = np.column_stack([
            np.ones(n, dtype=float),
            z,
            np.repeat(dummies[None, :], n, axis=0),
        ])
        p0, p1, p2 = _probabilities(X, fit.beta)
        if np.any(~np.isfinite(p0)) or np.any(~np.isfinite(p1)) or np.any(~np.isfinite(p2)):
            raise FloatingPointError("nonfinite predicted probability")
        if np.any(p1 < 0.0) or np.any(p2 < 0.0) or np.any(p1 + p2 > 1.0 + 1e-12):
            raise FloatingPointError("invalid predicted probability")
        out[:, k - 1, 0] = p1
        out[:, k - 1, 1] = p2
    return out


def sustained_return_cif(hazards: np.ndarray) -> np.ndarray:
    h = np.asarray(hazards, dtype=float)
    if h.ndim != 3 or h.shape[2] != 2:
        raise ValueError("hazards must be n x H x 2")
    n, horizon, _ = h.shape
    cif = np.zeros((n, horizon), dtype=float)
    survival = np.ones(n, dtype=float)
    cumulative = np.zeros(n, dtype=float)
    for k in range(horizon):
        hr = h[:, k, 0]
        hi = h[:, k, 1]
        if np.any(hr < 0.0) or np.any(hi < 0.0) or np.any(hr + hi > 1.0 + 1e-12):
            raise FloatingPointError("invalid hazards")
        cumulative = cumulative + survival * hr
        cif[:, k] = cumulative
        survival = survival * np.maximum(0.0, 1.0 - hr - hi)
    return cif


def estimate_censoring_km(
    durations: np.ndarray,
    outcomes: np.ndarray,
    horizon: int,
) -> CensoringKM:
    d = np.asarray(durations, dtype=int)
    o = np.asarray(outcomes, dtype=int)
    if len(d) == 0 or len(d) != len(o):
        return CensoringKM("REFUSED", np.array([]), np.array([]), 0.0, "invalid_input")
    survival = 1.0
    g_after = np.ones(horizon, dtype=float)
    g_left = np.ones(horizon, dtype=float)
    for k in range(1, horizon + 1):
        g_left[k - 1] = survival
        risk = int(np.sum(d >= k))
        censored = int(np.sum((d == k) & (o == OUTCOME_CENSOR)))
        if risk > 0:
            survival *= 1.0 - censored / float(risk)
        g_after[k - 1] = survival
    min_g = float(np.min(g_after)) if len(g_after) else 0.0
    if not math.isfinite(min_g) or min_g < CENSORING_G_MIN:
        return CensoringKM(
            "REFUSED", g_after, g_left, min_g,
            "CENSORING_WEIGHT_NOT_QUALIFIED",
        )
    return CensoringKM("COMPLETE", g_after, g_left, min_g, "qualified")


def ipcw_integrated_brier(
    cif: np.ndarray,
    durations: np.ndarray,
    outcomes: np.ndarray,
    km: CensoringKM,
) -> tuple[float, np.ndarray]:
    pred = np.asarray(cif, dtype=float)
    d = np.asarray(durations, dtype=int)
    o = np.asarray(outcomes, dtype=int)
    if km.status != "COMPLETE":
        raise ValueError("censoring weights not qualified")
    if pred.ndim != 2 or pred.shape[0] != len(d) or len(d) != len(o):
        raise ValueError("score shape mismatch")
    n, horizon = pred.shape
    if horizon != len(km.g_after):
        raise ValueError("KM horizon mismatch")
    bs = np.zeros(horizon, dtype=float)
    for k in range(1, horizon + 1):
        total = 0.0
        for i in range(n):
            t = int(d[i])
            outcome = int(o[i])
            if outcome == OUTCOME_CENSOR and t <= k:
                continue
            if outcome in (OUTCOME_RETURN, OUTCOME_INTERRUPT) and t <= k:
                y = 1.0 if outcome == OUTCOME_RETURN else 0.0
                g = float(km.g_left[max(0, t - 1)])
            else:
                y = 0.0
                g = float(km.g_after[k - 1])
            if g < CENSORING_G_MIN or not math.isfinite(g):
                raise ValueError("unqualified censoring weight")
            err = y - float(pred[i, k - 1])
            total += (err * err) / g
        bs[k - 1] = total / float(n)
    return float(np.mean(bs)), bs


def paired_bootstrap_summary(
    deltas: np.ndarray,
    scale_seconds: int,
    *,
    namespace: int = 400,
    n_boot: int = 10_000,
) -> BootstrapSummary:
    x = np.asarray(deltas, dtype=float)
    if x.shape != (30,) or np.any(~np.isfinite(x)):
        raise ValueError("paired bootstrap requires 30 finite replica differences")
    rng = np.random.default_rng(
        np.random.SeedSequence([20261002, int(namespace), int(scale_seconds)])
    )
    indices = rng.integers(0, 30, size=(n_boot, 30))
    boot = np.mean(x[indices], axis=1)
    ci_low, ci_high = np.quantile(boot, [0.025, 0.975], method="linear")
    left = (int(np.sum(boot <= 0.0)) + 1) / float(n_boot + 1)
    right = (int(np.sum(boot >= 0.0)) + 1) / float(n_boot + 1)
    p = min(1.0, 2.0 * min(left, right))
    return BootstrapSummary(
        point=float(np.mean(x)),
        ci_low=float(ci_low),
        ci_high=float(ci_high),
        p_two_sided=float(p),
        positive_count=int(np.sum(x > 0.0)),
        n_boot=int(n_boot),
    )


def holm_adjust(pvalues: Mapping[int, float]) -> dict[int, float]:
    if len(pvalues) != 4:
        raise ValueError("Holm family requires four scale p-values")
    ordered = sorted(
        ((int(scale), float(p)) for scale, p in pvalues.items()),
        key=lambda x: (x[1], x[0]),
    )
    m = len(ordered)
    adjusted: dict[int, float] = {}
    running = 0.0
    for i, (scale, p) in enumerate(ordered):
        raw = min(1.0, (m - i) * p)
        running = max(running, raw)
        adjusted[scale] = min(1.0, running)
    return adjusted

