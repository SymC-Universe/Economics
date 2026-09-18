from __future__ import annotations

from dataclasses import dataclass, asdict
import math

import numpy as np

from .models import fit_ar
from .chi import chi_from_discrete_poles


@dataclass(frozen=True)
class PoleStabilityResult:
    status: str
    n: int
    blocks: int
    block_size: int
    full_pole_class: str
    block_pole_class_agreement: float
    block_ar2_support_fraction: float
    block_chi_licensed_fraction: float
    median_pole_distance: float
    max_pole_distance: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def pole_class(poles, tol: float = 1e-7) -> str:
    z = np.asarray(list(poles), dtype=complex)
    if len(z) != 2 or not np.all(np.isfinite(z.real)) or not np.all(np.isfinite(z.imag)):
        return "invalid"
    if np.any(np.abs(z) >= 1.0):
        return "unstable_or_boundary"
    if np.any(np.abs(z.imag) > tol):
        if abs(z[0] - np.conj(z[1])) <= tol * max(1.0, abs(z[0]), abs(z[1])):
            return "complex_conjugate"
        return "complex_nonconjugate"
    if np.all(z.real > 0):
        return "positive_real"
    if np.any(z.real < 0):
        return "negative_real_present"
    return "zero_or_boundary_real"


def pair_distance(a, b) -> float:
    aa = np.asarray(list(a), dtype=complex)
    bb = np.asarray(list(b), dtype=complex)
    if len(aa) != 2 or len(bb) != 2:
        return math.nan
    d1 = max(abs(aa[0] - bb[0]), abs(aa[1] - bb[1]))
    d2 = max(abs(aa[0] - bb[1]), abs(aa[1] - bb[0]))
    return float(min(d1, d2))


def blockwise_pole_stability(
    series,
    *,
    blocks: int = 4,
    min_ar2_bic_gain: float = 6.0,
    dt: float = 1.0,
) -> PoleStabilityResult:
    """Report whether a full-window AR2 pole geometry recurs in contiguous blocks.

    This is a threshold-free P0-Q diagnostic. It does not alter production chi
    admission. Each block independently refits AR0/AR1/AR2; pole distances are
    computed even when the block does not independently support AR2 so that
    instability is visible rather than silently filtered away.
    """
    x = np.asarray(series, dtype=float)
    if x.ndim != 1 or not np.all(np.isfinite(x)):
        return PoleStabilityResult(
            "REFUSED_INPUT", len(x), blocks, 0, "invalid",
            math.nan, math.nan, math.nan, math.nan, math.nan,
            "series must be finite and one-dimensional",
        )
    n = len(x)
    if blocks < 2:
        return PoleStabilityResult(
            "REFUSED_INPUT", n, blocks, 0, "invalid",
            math.nan, math.nan, math.nan, math.nan, math.nan,
            "blocks must be >= 2",
        )
    block_size = n // blocks
    if block_size < 50:
        return PoleStabilityResult(
            "REFUSED_INSUFFICIENT_DATA", n, blocks, block_size, "invalid",
            math.nan, math.nan, math.nan, math.nan, math.nan,
            "blocks are too short for AR2 stability assessment",
        )

    full = fit_ar(x, 2)
    full_class = pole_class(full.roots)
    classes = []
    support = []
    licensed = []
    distances = []

    for i in range(blocks):
        lo = i * block_size
        hi = n if i == blocks - 1 else (i + 1) * block_size
        b = x[lo:hi]
        ar0, ar1, ar2 = fit_ar(b, 0), fit_ar(b, 1), fit_ar(b, 2)
        gain = min(ar0.bic, ar1.bic) - ar2.bic
        support.append(gain >= min_ar2_bic_gain)
        classes.append(pole_class(ar2.roots))
        licensed.append(chi_from_discrete_poles(ar2.roots, dt=dt).admitted)
        distances.append(pair_distance(full.roots, ar2.roots))

    dist = np.asarray(distances, dtype=float)
    finite = dist[np.isfinite(dist)]
    if len(finite) == 0:
        return PoleStabilityResult(
            "REFUSED_DEGENERATE", n, blocks, block_size, full_class,
            math.nan, math.nan, math.nan, math.nan, math.nan,
            "block pole distances are undefined",
        )
    return PoleStabilityResult(
        "COMPLETE",
        n,
        blocks,
        block_size,
        full_class,
        float(np.mean([c == full_class for c in classes])),
        float(np.mean(support)),
        float(np.mean(licensed)),
        float(np.median(finite)),
        float(np.max(finite)),
        "report-only P0-Q pole reproducibility diagnostic; no production threshold is implied",
    )
