from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

from .q040_observation_episode_v02 import (
    SIGMA0,
    build_observation_episode_world,
    nc20_cells,
)


WINDOWS = (10, 20, 40)
BASELINE_CONTROLS = ("NC-R5", "NC-R15", "NC-R16", "NC-R20")
TEST_START = 2048
MIN_COVERAGE = 0.90


@dataclass(frozen=True)
class BaselineWorldScore:
    control_id: str
    scale_seconds: int
    replica: int
    cell_key: str | None
    kind: str
    window: int
    coverage: float
    median_error: float
    status: str

    def to_dict(self):
        return asdict(self)


def _valid_update_indices(
    update_mask: np.ndarray,
    t: int,
    window: int,
) -> np.ndarray:
    lo = max(0, t - window)
    rel = np.flatnonzero(update_mask[lo:t])
    return rel + lo


def estimate_k1(
    z: np.ndarray,
    update_mask: np.ndarray,
    *,
    window: int,
    start: int = TEST_START,
) -> tuple[np.ndarray, np.ndarray]:
    n, p = z.shape
    baseline = np.full((n, p), np.nan, dtype=float)
    velocity = np.full((n, p), np.nan, dtype=float)
    for t in range(max(start, 1), n):
        idx = _valid_update_indices(update_mask, t, window)
        if len(idx) < 5:
            continue
        vals = z[idx]
        if np.any(~np.isfinite(vals)):
            continue
        baseline[t] = np.median(vals, axis=0)
        velocity[t] = 0.0
    return baseline, velocity


def estimate_k2(
    z: np.ndarray,
    update_mask: np.ndarray,
    *,
    window: int,
    start: int = TEST_START,
) -> tuple[np.ndarray, np.ndarray]:
    n, p = z.shape
    baseline = np.full((n, p), np.nan, dtype=float)
    velocity = np.full((n, p), np.nan, dtype=float)
    for t in range(max(start, 1), n):
        idx = _valid_update_indices(update_mask, t, window)
        if len(idx) < 10:
            continue
        vals = z[idx]
        if np.any(~np.isfinite(vals)):
            continue
        x = idx.astype(float) - float(t)
        X = np.column_stack([np.ones(len(x)), x])
        if np.linalg.matrix_rank(X) < 2:
            continue
        beta, *_ = np.linalg.lstsq(X, vals, rcond=None)
        baseline[t] = beta[0]
        velocity[t] = beta[1]
    return baseline, velocity


def normalized_baseline_error(
    estimate: np.ndarray,
    truth: np.ndarray,
) -> np.ndarray:
    if estimate.shape != truth.shape:
        raise ValueError("baseline shape mismatch")
    scale = SIGMA0.reshape(1, -1)
    d = (estimate - truth) / scale
    return np.sqrt(np.mean(d * d, axis=1))


def score_baseline_candidate(
    world: dict,
    *,
    kind: str,
    window: int,
    replica: int,
    cell_key: str | None,
) -> BaselineWorldScore:
    a = world["arrays"]
    z = np.asarray(a["Z_observed"], dtype=float)
    update = np.asarray(a["update_mask"], dtype=bool)
    truth = np.asarray(a["baseline_true"], dtype=float)

    if kind == "K1":
        est, _ = estimate_k1(z, update, window=window)
    elif kind == "K2":
        est, _ = estimate_k2(z, update, window=window)
    else:
        raise ValueError(kind)

    valid = np.arange(len(z)) >= TEST_START
    valid &= np.all(np.isfinite(truth), axis=1)
    eligible = int(valid.sum())

    good = valid & np.all(np.isfinite(est), axis=1)
    coverage = float(good.sum() / max(1, eligible))
    if not np.any(good):
        med = math.inf
    else:
        err = normalized_baseline_error(est[good], truth[good])
        med = float(np.median(err))

    status = "PASS_NUMERIC_COVERAGE" if coverage >= MIN_COVERAGE and math.isfinite(med) else "REFUSED_COVERAGE"

    m = world["metadata"]
    return BaselineWorldScore(
        control_id=str(m["control_id"]),
        scale_seconds=int(m["scale_seconds"]),
        replica=int(replica),
        cell_key=cell_key,
        kind=kind,
        window=int(window),
        coverage=coverage,
        median_error=med,
        status=status,
    )


def summarize_candidate(scores: list[BaselineWorldScore]) -> dict[str, object]:
    if not scores:
        raise ValueError("no scores")
    refused = [s for s in scores if s.status != "PASS_NUMERIC_COVERAGE"]
    finite = [s.median_error for s in scores if math.isfinite(s.median_error)]
    return {
        "kind": scores[0].kind,
        "window": scores[0].window,
        "worlds": len(scores),
        "refused_worlds": len(refused),
        "min_coverage": float(min(s.coverage for s in scores)),
        "median_coverage": float(np.median([s.coverage for s in scores])),
        "median_normalized_baseline_error": (
            float(np.median(finite)) if finite else math.inf
        ),
        "eligible": len(refused) == 0,
    }


def rank_candidates(summary: list[dict[str, object]]) -> list[dict[str, object]]:
    def key(x):
        kind_rank = 0 if x["kind"] == "K1" else 1
        return (
            0 if x["eligible"] else 1,
            float(x["median_normalized_baseline_error"]),
            kind_rank,
            int(x["window"]),
        )
    return sorted(summary, key=key)
