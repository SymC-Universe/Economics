from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class SubspaceComparison:
    status: str
    k: int
    principal_cosines: tuple[float, ...]
    min_principal_cosine: float
    mean_principal_cosine: float
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def compare_loading_subspaces(
    loadings_a: Iterable[Iterable[float]],
    loadings_b: Iterable[Iterable[float]],
    *,
    k: int = 2,
) -> SubspaceComparison:
    """Compare row-loading subspaces with principal cosines.

    PCA signs and within-subspace rotations do not affect the result. This is
    therefore preferable to comparing PC1/PC2 signs directly across days.
    """
    A = np.asarray(loadings_a, dtype=float)
    B = np.asarray(loadings_b, dtype=float)
    if A.ndim != 2 or B.ndim != 2:
        return SubspaceComparison("REFUSED_INPUT", k, (), math.nan, math.nan, "loadings must be 2D")
    if A.shape[1] != B.shape[1]:
        return SubspaceComparison("REFUSED_DIMENSION", k, (), math.nan, math.nan, "feature dimensions differ")
    if k < 1 or A.shape[0] < k or B.shape[0] < k:
        return SubspaceComparison("REFUSED_K", k, (), math.nan, math.nan, "not enough loading vectors for requested k")
    if not np.all(np.isfinite(A[:k])) or not np.all(np.isfinite(B[:k])):
        return SubspaceComparison("REFUSED_INPUT", k, (), math.nan, math.nan, "non-finite loadings")

    # Orthonormalize in case a future producer supplies numerically imperfect rows.
    Qa, _ = np.linalg.qr(A[:k].T)
    Qb, _ = np.linalg.qr(B[:k].T)
    s = np.linalg.svd(Qa.T @ Qb, compute_uv=False)
    s = np.clip(s, 0.0, 1.0)
    vals = tuple(float(x) for x in s)
    return SubspaceComparison(
        "COMPLETE",
        k,
        vals,
        float(np.min(s)),
        float(np.mean(s)),
        "principal cosines are sign- and rotation-invariant within the compared subspaces",
    )
