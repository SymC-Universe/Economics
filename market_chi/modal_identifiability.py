from __future__ import annotations

import math
from typing import Iterable, Mapping

import numpy as np


def canonical_depth_bases(levels: int = 10) -> dict[str, np.ndarray]:
    if levels < 2:
        raise ValueError("levels must be >= 2")
    sym = np.ones(2 * levels, dtype=float)
    imbalance = np.array([1.0, -1.0] * levels, dtype=float)
    level = np.repeat(np.linspace(-1.0, 1.0, levels), 2)
    side_gradient = level * imbalance
    bases = {
        "symmetric_depth": sym,
        "bid_ask_imbalance": imbalance,
        "depth_gradient": level,
        "side_gradient": side_gradient,
    }
    return {name: vec / np.linalg.norm(vec) for name, vec in bases.items()}


def _orthonormal_row_subspace(loadings: Iterable[Iterable[float]], k: int) -> np.ndarray:
    A = np.asarray(loadings, dtype=float)
    if A.ndim != 2:
        raise ValueError("loadings must be 2D")
    if k < 1 or k > A.shape[0]:
        raise ValueError("k outside available loading rows")
    if not np.all(np.isfinite(A[:k])):
        raise ValueError("non-finite loadings")
    Q, _ = np.linalg.qr(A[:k].T)
    return Q


def subspace_capture(
    loadings: Iterable[Iterable[float]],
    basis: Iterable[float],
    *,
    k: int,
) -> float:
    """Fraction of a unit basis direction captured by a fixed PCA subspace.

    The quantity is sign- and rotation-invariant within the selected subspace.
    It does not depend on which individual PC carries the direction.
    """
    b = np.asarray(basis, dtype=float)
    if b.ndim != 1 or not np.all(np.isfinite(b)):
        raise ValueError("basis must be a finite 1D vector")
    norm = float(np.linalg.norm(b))
    if norm <= 0:
        raise ValueError("basis must have nonzero norm")
    b = b / norm
    Q = _orthonormal_row_subspace(loadings, k)
    if Q.shape[0] != b.shape[0]:
        raise ValueError("basis and loading feature dimensions differ")
    value = float(np.sum((Q.T @ b) ** 2))
    return float(np.clip(value, 0.0, 1.0))


def semantic_capture_table(
    loadings: Iterable[Iterable[float]],
    bases: Mapping[str, Iterable[float]],
    *,
    ks: Iterable[int] = (2, 3, 4, 6, 10),
) -> dict[str, dict[str, float]]:
    A = np.asarray(loadings, dtype=float)
    out: dict[str, dict[str, float]] = {}
    for name, basis in bases.items():
        out[name] = {}
        for k in ks:
            kk = int(k)
            out[name][str(kk)] = subspace_capture(A, basis, k=kk)
    return out


def strongest_mode(
    loadings: Iterable[Iterable[float]],
    basis: Iterable[float],
) -> dict[str, float | int]:
    A = np.asarray(loadings, dtype=float)
    b = np.asarray(basis, dtype=float)
    b = b / np.linalg.norm(b)
    if A.ndim != 2 or A.shape[1] != b.shape[0]:
        raise ValueError("basis and loading dimensions differ")
    vals = np.abs(A @ b)
    i = int(np.argmax(vals))
    return {"pc": i + 1, "alignment": float(vals[i])}


def spectral_metrics(
    variance_ratio: Iterable[float],
    *,
    ks: Iterable[int] = (2, 3, 4, 6, 10),
) -> dict[str, object]:
    p = np.asarray(list(variance_ratio), dtype=float)
    if p.ndim != 1 or len(p) < 3 or not np.all(np.isfinite(p)) or np.any(p < 0):
        raise ValueError("variance ratio must be a finite nonnegative vector of length >= 3")
    total = float(p.sum())
    if total <= 0:
        raise ValueError("variance ratio must have positive mass")
    p = p / total
    positive = p[p > 0]
    entropy = float(-np.sum(positive * np.log(positive)))
    n = len(p)
    gaps = {}
    relative_gaps = {}
    for i in range(min(6, n - 1)):
        key = f"{i+1}_{i+2}"
        gap = float(p[i] - p[i + 1])
        gaps[key] = gap
        relative_gaps[key] = gap / float(p[i]) if p[i] > 0 else math.nan
    cumulative = {}
    cs = np.cumsum(p)
    for k in ks:
        kk = int(k)
        if 1 <= kk <= n:
            cumulative[str(kk)] = float(cs[kk - 1])
    return {
        "n_modes": n,
        "entropy": entropy,
        "entropy_normalized": entropy / math.log(n) if n > 1 else 0.0,
        "effective_rank": float(math.exp(entropy)),
        "gaps": gaps,
        "relative_gaps": relative_gaps,
        "cumulative_variance": cumulative,
    }
