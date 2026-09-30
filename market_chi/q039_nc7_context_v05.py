from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import numpy as np

from market_chi.q039_intake_v04 import semantic_state
from market_chi.q039_nc7_v04 import (
    NC7_SEED,
    NC7_WORLDS,
    carry_forward_isotropic_world,
    world_seed,
)


@dataclass(frozen=True)
class NC7DerivedContextAudit:
    worlds: int
    base_seed: int
    finite_after_first: bool
    imbalance_nonconstant: bool
    microprice_nonconstant: bool
    side_symmetric_projection: bool
    semantic_path_byte_identical: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def project_sizes_for_context(log_state: np.ndarray) -> np.ndarray:
    """Frozen v0.5 physical-cone projection for derived native context only."""
    x = np.asarray(log_state, dtype=float)
    out = np.full_like(x, np.nan, dtype=float)
    finite = np.all(np.isfinite(x), axis=1) if x.ndim == 2 else None
    if x.ndim != 2 or x.shape[1] != 20:
        raise ValueError("log_state must have shape (n,20)")
    if np.any(finite):
        out[finite] = np.expm1(np.maximum(x[finite], 0.0))
    return out


def recompute_nc7_native_context(
    log_state: np.ndarray,
    real_spread_dense: np.ndarray,
) -> dict[str, np.ndarray]:
    """Recompute the size-derived Q039 NC7 context on the frozen dense grid.

    The input log_state is the already-qualified unprojected Gaussian NC7 state,
    carried forward on the exact real update schedule. Projection is used only
    for nonnegative-size-derived native context. The semantic D/I pathway is not
    modified.

    Synthetic signed microprice offset uses the algebraically equivalent bound
    production identity:

        offset = 0.5 * spread * (bid_sz_00 - ask_sz_00)
                               / (bid_sz_00 + ask_sz_00)

    so no additional real-price field is introduced beyond the already-frozen
    real spread context.
    """
    x = np.asarray(log_state, dtype=float)
    spread = np.asarray(real_spread_dense, dtype=float)
    if x.ndim != 2 or x.shape[1] != 20:
        raise ValueError("log_state must have shape (n,20)")
    if spread.shape != (len(x),):
        raise ValueError("real_spread_dense length mismatch")

    original_bytes = x.tobytes()
    sem_before = semantic_state(x.copy())

    q = project_sizes_for_context(x)
    valid = np.all(np.isfinite(q), axis=1)

    bid10 = np.nansum(q[:, 0::2], axis=1)
    ask10 = np.nansum(q[:, 1::2], axis=1)
    total10 = bid10 + ask10
    imb10 = np.full(len(x), np.nan, dtype=float)
    imb10[valid] = 0.0
    nz10 = valid & (total10 > 0.0)
    imb10[nz10] = (bid10[nz10] - ask10[nz10]) / total10[nz10]

    bid1 = q[:, 0]
    ask1 = q[:, 1]
    total1 = bid1 + ask1
    l1imb = np.full(len(x), np.nan, dtype=float)
    l1imb[valid] = 0.0
    nz1 = valid & (total1 > 0.0)
    l1imb[nz1] = (bid1[nz1] - ask1[nz1]) / total1[nz1]

    micro = np.full(len(x), np.nan, dtype=float)
    usable = valid & np.isfinite(spread)
    micro[usable] = 0.5 * spread[usable] * l1imb[usable]

    if x.tobytes() != original_bytes:
        raise RuntimeError("derived-context recompute mutated semantic NC7 state")
    sem_after = semantic_state(x)
    semantic_identical = bool(
        np.array_equal(np.isnan(sem_before), np.isnan(sem_after))
        and np.array_equal(
            np.nan_to_num(sem_before, nan=0.0),
            np.nan_to_num(sem_after, nan=0.0),
        )
    )

    return {
        "projected_sizes20": q,
        "l10_imbalance": imb10,
        "microprice_offset": micro,
        "semantic_path_byte_identical": np.asarray([semantic_identical], dtype=bool),
    }


def qualify_synthetic_context_fixture(
    *,
    worlds: int = NC7_WORLDS,
    base_seed: int = NC7_SEED,
) -> dict[str, object]:
    """Synthetic-only implementation preflight for the v0.5 context rule."""
    n = 3600
    update = np.zeros(n, dtype=bool)
    update[[7, 8, 35, 101, 333, 334, 335, 700, 1200, 1205, 1800, 2390, 3000, 3590]] = True

    # A frozen real-context surrogate for implementation qualification only.
    # It is not market data and has no Q039 scientific outcome content.
    t = np.arange(n, dtype=float)
    spread = 0.25 + 0.03 * np.sin(2.0 * np.pi * t / 900.0)
    spread[:7] = np.nan

    imbalances = []
    micros = []
    semantic_ok = True
    finite_ok = True
    side_symmetry_ok = True

    for w in range(worlds):
        x = carry_forward_isotropic_world(
            update,
            seed=world_seed(w, base_seed=base_seed),
            dim=20,
        )
        out = recompute_nc7_native_context(x, spread)
        imbalances.append(out["l10_imbalance"])
        micros.append(out["microprice_offset"])
        semantic_ok = semantic_ok and bool(out["semantic_path_byte_identical"][0])

        first = int(np.flatnonzero(update)[0])
        finite_ok = finite_ok and bool(
            np.all(np.isfinite(out["l10_imbalance"][first:]))
            and np.all(np.isfinite(out["microprice_offset"][first:]))
        )

        q = out["projected_sizes20"]
        if np.any(q[np.isfinite(q)] < 0.0):
            side_symmetry_ok = False

    imb = np.vstack(imbalances)
    mic = np.vstack(micros)
    imbalance_nonconstant = bool(np.nanstd(imb) > 1e-12)
    microprice_nonconstant = bool(np.nanstd(mic) > 1e-12)

    audit = NC7DerivedContextAudit(
        worlds=worlds,
        base_seed=base_seed,
        finite_after_first=finite_ok,
        imbalance_nonconstant=imbalance_nonconstant,
        microprice_nonconstant=microprice_nonconstant,
        side_symmetric_projection=side_symmetry_ok,
        semantic_path_byte_identical=semantic_ok,
    )
    passed = all([
        audit.finite_after_first,
        audit.imbalance_nonconstant,
        audit.microprice_nonconstant,
        audit.side_symmetric_projection,
        audit.semantic_path_byte_identical,
    ])
    return {
        "disposition": (
            "NC7_DERIVED_CONTEXT_IMPLEMENTATION_PREFLIGHT_PASS"
            if passed
            else "NC7_DERIVED_CONTEXT_PREFLIGHT_REFUSED"
        ),
        "real_data_used": False,
        "scientific_nc7_executed": False,
        "audit": audit.to_dict(),
        "note": (
            "Implementation-only synthetic fixture. The scientific v0.5 supplemental "
            "preflight still requires the frozen five development-day update schedules "
            "after source identity is frozen."
        ),
    }
