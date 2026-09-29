from __future__ import annotations

from dataclasses import dataclass, asdict
import numpy as np

DIM = 20
NC7_SEED = 20261001
NC7_WORLDS = 200


@dataclass(frozen=True)
class NC7TimingAudit:
    n: int
    update_count: int
    first_update_index: int | None
    prefirst_all_nan: bool
    nonupdate_state_changes: int
    update_state_changes: int
    finite_after_first: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def carry_forward_isotropic_world(
    update_indicator,
    *,
    seed: int,
    dim: int = DIM,
) -> np.ndarray:
    """Generate one NC7 world with exact supplied update timing.

    New valid states are iid isotropic N(0, I) at update times. The last valid
    state is carried forward between updates. Samples before the first update
    remain NaN. The function contains no market values or targets.
    """
    u = np.asarray(update_indicator, dtype=bool)
    if u.ndim != 1:
        raise ValueError("update_indicator must be one-dimensional")
    if dim < 1:
        raise ValueError("dim must be positive")

    out = np.full((len(u), dim), np.nan, dtype=float)
    rng = np.random.default_rng(seed)
    last = None
    for i, is_update in enumerate(u):
        if is_update:
            last = rng.normal(size=dim)
        if last is not None:
            out[i] = last
    return out


def audit_timing(update_indicator, states: np.ndarray) -> NC7TimingAudit:
    u = np.asarray(update_indicator, dtype=bool)
    x = np.asarray(states, dtype=float)
    if x.ndim != 2 or len(x) != len(u):
        raise ValueError("state/update length mismatch")

    idx = np.flatnonzero(u)
    first = int(idx[0]) if len(idx) else None

    if first is None:
        prefirst = bool(np.all(np.isnan(x)))
        finite_after = False
        return NC7TimingAudit(
            len(u), 0, None, prefirst, 0, 0, finite_after
        )

    prefirst = bool(np.all(np.isnan(x[:first])))
    finite_after = bool(np.all(np.isfinite(x[first:])))

    nonupdate_changes = 0
    update_changes = 0
    for i in range(first + 1, len(u)):
        changed = not np.array_equal(x[i], x[i - 1])
        if u[i]:
            update_changes += int(changed)
        else:
            nonupdate_changes += int(changed)

    return NC7TimingAudit(
        len(u),
        int(len(idx)),
        first,
        prefirst,
        nonupdate_changes,
        update_changes,
        finite_after,
    )


def world_seed(world_index: int, *, base_seed: int = NC7_SEED) -> int:
    if world_index < 0:
        raise ValueError("world_index must be nonnegative")
    # Deterministic independent stream identity, frozen from the preregistered base seed.
    ss = np.random.SeedSequence([base_seed, world_index])
    return int(ss.generate_state(1, dtype=np.uint32)[0])


def qualify_synthetic_timing_fixture(
    *,
    worlds: int = NC7_WORLDS,
    base_seed: int = NC7_SEED,
    dim: int = DIM,
) -> dict[str, object]:
    """Pre-real-data NC7 plumbing qualification on a synthetic update schedule.

    This validates timing preservation and isotropic-state generation only.
    It does NOT execute the scientific NC7 null, which requires the frozen real
    development-day update timestamps during P0-D execution.
    """
    n = 2400
    u = np.zeros(n, dtype=bool)
    # Delayed first update, irregular gaps, and a denser segment.
    u[[7, 8, 35, 101, 333, 334, 335, 700, 1200, 1205, 1800, 2390]] = True

    audits = []
    update_samples = []
    for w in range(worlds):
        x = carry_forward_isotropic_world(u, seed=world_seed(w, base_seed=base_seed), dim=dim)
        a = audit_timing(u, x)
        audits.append(a)
        update_samples.append(x[u])

    timing_pass = all(
        a.prefirst_all_nan
        and a.nonupdate_state_changes == 0
        and a.update_state_changes == max(0, a.update_count - 1)
        and a.finite_after_first
        for a in audits
    )

    updates = np.vstack(update_samples)
    mean_abs_max = float(np.max(np.abs(updates.mean(axis=0))))
    var = updates.var(axis=0, ddof=0)
    var_min = float(np.min(var))
    var_max = float(np.max(var))

    # Broad implementation sanity bounds only, not scientific acceptance thresholds.
    isotropy_sanity = bool(mean_abs_max < 0.10 and var_min > 0.80 and var_max < 1.20)

    disposition = (
        "NC7_IMPLEMENTATION_PREFLIGHT_PASS"
        if timing_pass and isotropy_sanity
        else "NC7_IMPLEMENTATION_PREFLIGHT_FAIL"
    )
    return {
        "disposition": disposition,
        "real_data_used": False,
        "scientific_nc7_executed": False,
        "base_seed": base_seed,
        "worlds": worlds,
        "timing_pass": timing_pass,
        "isotropy_sanity": isotropy_sanity,
        "mean_abs_max": mean_abs_max,
        "variance_min": var_min,
        "variance_max": var_max,
        "note": (
            "Plumbing-only qualification. Real NC7 must preserve actual development-day "
            "update timestamps and is executed only inside the frozen P0-D pipeline."
        ),
    }
