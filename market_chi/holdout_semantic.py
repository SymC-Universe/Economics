from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

import numpy as np


D = 20

# Exact isotropic random-orientation capture quantiles for d=20.
# If u is Haar-uniform on S^(d-1) and P is a fixed rank-k projector,
# ||Pu||^2 ~ Beta(k/2, (d-k)/2).
ISOTROPIC_Q95_D20 = {
    2: 0.28312883556311347,
    3: 0.36066985006432806,
    4: 0.42913554703143447,
    6: 0.5496416495066101,
    10: 0.7486323725918227,
}
ISOTROPIC_MEAN_D20 = {k: k / D for k in ISOTROPIC_Q95_D20}


@dataclass(frozen=True)
class BootstrapResult:
    point: float
    lower: float
    upper: float
    reps_requested: int
    reps_valid: int
    block_length: int
    seed: int

    def to_dict(self) -> dict[str, float | int]:
        return {
            "point": self.point,
            "lower": self.lower,
            "upper": self.upper,
            "reps_requested": self.reps_requested,
            "reps_valid": self.reps_valid,
            "block_length": self.block_length,
            "seed": self.seed,
        }


def circular_block_indices(n: int, block_length: int, rng: np.random.Generator) -> np.ndarray:
    if n < 1:
        raise ValueError("n must be positive")
    if block_length < 1 or block_length > n:
        raise ValueError("block_length must satisfy 1 <= block_length <= n")
    chunks: list[np.ndarray] = []
    total = 0
    while total < n:
        start = int(rng.integers(0, n))
        idx = (start + np.arange(block_length, dtype=int)) % n
        chunks.append(idx)
        total += block_length
    return np.concatenate(chunks)[:n]


def moving_block_bootstrap(
    arrays_by_day: Sequence[np.ndarray],
    statistic: Callable[[Sequence[np.ndarray]], float],
    *,
    block_length: int,
    reps: int = 10_000,
    seed: int = 20260927,
) -> BootstrapResult:
    if reps < 100:
        raise ValueError("reps must be >= 100")
    days = [np.asarray(x) for x in arrays_by_day]
    if not days or any(x.ndim != 1 or len(x) < block_length for x in days):
        raise ValueError("each day must be a 1D array with len >= block_length")
    if any(np.any(np.isinf(x)) for x in days):
        raise ValueError("bootstrap arrays may contain NaN for frozen missing slots but not infinity")

    point = float(statistic(days))
    rng = np.random.default_rng(seed)
    vals = np.empty(reps, dtype=float)
    valid = 0
    for _ in range(reps):
        sampled = []
        for x in days:
            idx = circular_block_indices(len(x), block_length, rng)
            sampled.append(x[idx])
        v = float(statistic(sampled))
        if np.isfinite(v):
            vals[valid] = v
            valid += 1

    if valid < int(0.95 * reps):
        raise RuntimeError("fewer than 95% bootstrap replicates produced a finite statistic")
    vals = vals[:valid]
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return BootstrapResult(
        point=point,
        lower=float(lo),
        upper=float(hi),
        reps_requested=reps,
        reps_valid=valid,
        block_length=block_length,
        seed=seed,
    )


def pooled_median(days: Sequence[np.ndarray]) -> float:
    x = np.concatenate([np.asarray(v, dtype=float) for v in days])
    x = x[np.isfinite(x)]
    return float(np.median(x)) if len(x) else float("nan")


def primary_outcome(
    primary: BootstrapResult,
    sensitivities: Iterable[BootstrapResult],
) -> str:
    sens = list(sensitivities)
    if primary.upper <= 0:
        return "EMPIRICAL_CLAIM_FALSIFIED"
    if primary.lower <= 0:
        return "INDETERMINATE"
    if any(s.lower <= 0 for s in sens):
        return "INDETERMINATE"
    return "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST"


def corridor_contrast_stat(
    values_by_day: Sequence[np.ndarray],
    flags_by_day: Sequence[np.ndarray],
) -> float:
    inside = []
    outside = []
    for values, flags in zip(values_by_day, flags_by_day):
        v = np.asarray(values, dtype=float)
        f = np.asarray(flags, dtype=bool)
        if len(v) != len(f):
            raise ValueError("values and flags length mismatch")
        inside.extend(v[f & np.isfinite(v)].tolist())
        outside.extend(v[(~f) & np.isfinite(v)].tolist())
    if not inside or not outside:
        return float("nan")
    return float(np.median(inside) - np.median(outside))


def moving_block_bootstrap_corridor(
    values_by_day: Sequence[np.ndarray],
    flags_by_day: Sequence[np.ndarray],
    *,
    block_length: int = 4,
    reps: int = 10_000,
    seed: int = 20260928,
) -> BootstrapResult:
    values = [np.asarray(x, dtype=float) for x in values_by_day]
    flags = [np.asarray(x, dtype=bool) for x in flags_by_day]
    if len(values) != len(flags) or not values:
        raise ValueError("values/flags day mismatch")
    if any(len(v) != len(f) or len(v) < block_length for v, f in zip(values, flags)):
        raise ValueError("invalid day arrays")
    point = corridor_contrast_stat(values, flags)

    rng = np.random.default_rng(seed)
    vals = np.empty(reps, dtype=float)
    valid = 0
    for _ in range(reps):
        sv = []
        sf = []
        for v, f in zip(values, flags):
            idx = circular_block_indices(len(v), block_length, rng)
            sv.append(v[idx])
            sf.append(f[idx])
        x = corridor_contrast_stat(sv, sf)
        if np.isfinite(x):
            vals[valid] = x
            valid += 1

    if valid < int(0.95 * reps):
        raise RuntimeError("fewer than 95% corridor bootstrap replicates were valid")
    vals = vals[:valid]
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return BootstrapResult(
        point=float(point),
        lower=float(lo),
        upper=float(hi),
        reps_requested=reps,
        reps_valid=valid,
        block_length=block_length,
        seed=seed,
    )


def secondary_outcome(result: BootstrapResult) -> str:
    if result.lower > 0:
        return "EMPIRICAL_SECONDARY_SURVIVES_FROZEN_TEST"
    if result.upper <= 0:
        return "EMPIRICAL_SECONDARY_FALSIFIED"
    return "INDETERMINATE"
