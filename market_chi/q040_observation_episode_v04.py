from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
import math
from typing import Any

import numpy as np

from .q040_synthetic_generators_v0_4 import generate_control

STATE_DIM = 8
SCALES = (15, 30, 60, 300)
N_DEFAULT = 4096
BASE_SEED_Q = 20261001
BASE_SEED_DIR = 20261002

C_MODES = np.asarray([0.65, 0.78, 0.90, 1.00, 1.10, 1.22, 1.35, 1.50], dtype=float)
SIGMA0 = np.asarray([0.16, 0.18, 0.17, 0.15, 0.20, 0.18, 0.22, 0.19], dtype=float)
BASE_CORR = 0.35 ** np.abs(np.subtract.outer(np.arange(STATE_DIM), np.arange(STATE_DIM)))
BASE_COV = np.diag(SIGMA0) @ BASE_CORR @ np.diag(SIGMA0)
BASE_COV_INV = np.linalg.inv(BASE_COV)
BASE_CHOL = np.linalg.cholesky(BASE_COV)
RETURN_RADIUS_TRUE = 1.0
RETURN_SUSTAIN_TRUE = 3
SHOCK_MAGNITUDE = 4.0

V_BASELINE = np.asarray([1.0, 0.6, -0.4, 0.3, 0.2, -0.15, 0.1, 0.05], dtype=float)
V_BASELINE /= np.linalg.norm(V_BASELINE)
V_EXOG = np.asarray([0.2, -0.1, 0.4, 0.2, 0.5, -0.3, 0.15, 0.1], dtype=float)
V_EXOG /= np.linalg.norm(V_EXOG)

EXPECTED = {
    "NC-R1": "NATIVE_CURRENT_STATE_SUFFICIENT",
    "NC-R2": "CLUSTERING_EXPLAINS_APPARENT_HISTORY",
    "NC-R3": "HISTORY_ADDS_EROSION_DIRECTION",
    "NC-R4": "HISTORY_ADDS_ADAPTATION_DIRECTION",
    "NC-R5": "BASELINE_MIGRATION_EXPLAINS_APPARENT_HISTORY",
    "NC-R6": "HISTORY_MIXED_OR_DIRECTION_DEPENDENT",
    "NC-R7": "EXOGENOUS_EVENT_CONFOUNDED",
    "NC-R8": "SCALAR_REFUSAL",
    "NC-R9": "TRUE_CROSS_SCALE_PROPAGATION",
    "NC-R10": "WITHIN_SCALE_HISTORY_WITHOUT_CROSS_SCALE_PROPAGATION",
    "NC-R11": "SLOWER_RECOVERY_WITH_GREATER_RESISTANCE",
    "NC-R12": "TRANSIENT_AMPLIFICATION_WITH_STABLE_RETURN",
    "NC-R13": "INCOMPLETE_RECOVERY_EXPLAINS_APPARENT_HISTORY",
    "NC-R14": "NESTED_AGGREGATION_EXPLAINS_CROSS_SCALE_SIGNAL",
    "NC-R15": "CHANGING_NOISE_NOT_RECOVERY_LAW",
    "NC-R16": "HETEROSKEDASTIC_COORDINATE_ARTIFACT",
    "NC-R17": "LATENT_REGIME_ABSORBED_OR_EXPOSED",
    "NC-R17b": "OMITTED_NATIVE_COVARIATE_AMBIGUITY",
    "NC-R18": "RECOVERY_AND_REPERTURBATION_COMPETING_RISK",
    "NC-R19": "SHARED_REGIME_PSEUDO_PROPAGATION_REFUSED",
    "NC-R20": "MATCHED_UPDATE_TIMING_ARTIFACT_REFUSED",
    "NC-R21": "INSUFFICIENT_REPEATED_EVENTS",
}


def _fixed_orthogonal(seed: int, columns: int = STATE_DIM) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(STATE_DIM, STATE_DIM))
    q, r = np.linalg.qr(a)
    signs = np.sign(np.diag(r))
    signs[signs == 0] = 1.0
    q = q * signs
    return q[:, :columns]


Q_FIXED = _fixed_orthogonal(BASE_SEED_Q)
SHOCK_DIRS = _fixed_orthogonal(BASE_SEED_DIR, columns=4).T


@dataclass(frozen=True)
class NC20Cell:
    update_density: float
    gap_structure: str
    curvature: float
    noise_multiplier: float

    def key(self) -> str:
        return (
            f"u{self.update_density:.2f}_"
            f"{self.gap_structure.lower()}_"
            f"k{self.curvature:.1e}_"
            f"n{self.noise_multiplier:.2f}"
        )


def nc20_cells() -> list[NC20Cell]:
    out = []
    for density in (0.20, 0.50, 0.80):
        for gap in ("IID", "CLUSTERED"):
            for curvature in (0.0, 5e-8):
                for noise in (0.75, 1.50):
                    out.append(NC20Cell(density, gap, curvature, noise))
    return out


def _phase(n: int) -> np.ndarray:
    x = np.arange(n, dtype=float) / max(1, n)
    return np.column_stack([
        np.sin(2 * np.pi * x),
        np.cos(2 * np.pi * x),
        np.sin(4 * np.pi * x),
        np.cos(4 * np.pi * x),
    ])


def _default_shock(n: int) -> np.ndarray:
    shock = np.zeros(n, dtype=float)
    idx = np.arange(128, n, 64)
    shock[idx] = np.where(np.arange(len(idx)) % 2 == 0, 1.0, -1.0)
    return shock


def _shock_directions(shock: np.ndarray, control_id: str) -> np.ndarray:
    out = np.zeros((len(shock), STATE_DIM), dtype=float)
    nz = np.flatnonzero(shock != 0)
    for j, i in enumerate(nz):
        if control_id == "NC-R12":
            v = np.zeros(STATE_DIM, dtype=float)
            v[1] = np.sign(shock[i])
        else:
            v = SHOCK_DIRS[j % len(SHOCK_DIRS)] * np.sign(shock[i])
        out[i] = v / np.linalg.norm(v)
    return out


def _clustered_update_mask(n: int, density: float, rng: np.random.Generator) -> np.ndarray:
    p11 = 0.92
    p01 = density * (1.0 - p11) / max(1e-12, 1.0 - density)
    if not (0.0 <= p01 <= 1.0):
        raise ValueError("invalid Markov transition for requested density")
    x = np.zeros(n, dtype=bool)
    x[0] = bool(rng.random() < density)
    for i in range(1, n):
        p = p11 if x[i - 1] else p01
        x[i] = bool(rng.random() < p)
    return x


def _update_schedule(n: int, cell: NC20Cell | None, rng: np.random.Generator) -> np.ndarray:
    if cell is None:
        return np.ones(n, dtype=bool)
    if cell.gap_structure == "IID":
        x = rng.random(n) < cell.update_density
    elif cell.gap_structure == "CLUSTERED":
        x = _clustered_update_mask(n, cell.update_density, rng)
    else:
        raise ValueError("unknown gap structure")
    if not np.any(x):
        x[0] = True
    return x


def _staleness(mask: np.ndarray) -> np.ndarray:
    out = np.full(len(mask), -1, dtype=int)
    last = -1
    for i, flag in enumerate(mask):
        if flag:
            last = i
            out[i] = 0
        elif last >= 0:
            out[i] = i - last
    return out


def _carry_forward(z: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = np.full_like(z, np.nan, dtype=float)
    last = None
    for i in range(len(z)):
        if mask[i]:
            last = z[i].copy()
        if last is not None:
            out[i] = last
    return out


def _rate_array(data: dict[str, Any], n: int) -> np.ndarray:
    if "rate" not in data:
        return np.full(n, 0.08, dtype=float)
    r = np.asarray(data["rate"], dtype=float)
    if r.ndim == 0:
        return np.full(n, float(r), dtype=float)
    if len(r) != n:
        raise ValueError("rate length mismatch")
    return r


def _baseline_scalar(data: dict[str, Any], n: int) -> np.ndarray:
    if "baseline" not in data:
        return np.zeros(n, dtype=float)
    b = np.asarray(data["baseline"], dtype=float)
    if b.ndim == 0:
        return np.full(n, float(b), dtype=float)
    if len(b) != n:
        raise ValueError("baseline length mismatch")
    return b


def _noise_multiplier(data: dict[str, Any], control_id: str, n: int, cell: NC20Cell | None) -> np.ndarray:
    if control_id == "NC-R16" and "cov_scale" in data:
        cs = np.asarray(data["cov_scale"], dtype=float)
        return cs / float(np.median(cs))
    if "noise_scale" in data:
        ns = np.asarray(data["noise_scale"], dtype=float)
        if ns.ndim == 0:
            ns = np.full(n, float(ns))
        mult = ns / 0.05
    else:
        mult = np.ones(n, dtype=float)
    if cell is not None:
        mult = mult * cell.noise_multiplier
    return mult


def _make_covariates(
    data: dict[str, Any],
    z_observed: np.ndarray,
    shock: np.ndarray,
    update_mask: np.ndarray,
    stale: np.ndarray,
) -> tuple[np.ndarray, list[str], np.ndarray, list[str]]:
    n = len(shock)
    exog = np.asarray(data.get("exog", np.zeros(n)), dtype=float)
    regime_proxy = np.asarray(data.get("shock_intensity_proxy", np.zeros(n)), dtype=float)
    apparent_history = np.asarray(data.get("apparent_history", np.zeros(n)), dtype=float)
    noise_scale = np.asarray(data.get("noise_scale", np.full(n, 0.05)), dtype=float)
    if noise_scale.ndim == 0:
        noise_scale = np.full(n, float(noise_scale))

    ewma = np.zeros(n, dtype=float)
    state = 0.0
    for i in range(n):
        ewma[i] = state
        state = 0.96 * state + abs(float(shock[i]))

    z_norm = np.full(n, np.nan, dtype=float)
    valid = np.all(np.isfinite(z_observed), axis=1)
    z_norm[valid] = np.linalg.norm(z_observed[valid], axis=1)

    cov = np.column_stack([
        exog,
        regime_proxy,
        apparent_history,
        update_mask.astype(float),
        np.maximum(stale, 0),
        noise_scale,
        ewma,
        z_norm,
    ])
    names = [
        "exogenous_forcing",
        "observed_regime_proxy",
        "apparent_history",
        "update_indicator",
        "staleness_samples",
        "noise_scale_proxy",
        "past_event_intensity",
        "observed_state_norm",
    ]

    withheld_cols = []
    withheld_names = []
    if "omitted_covariate" in data:
        withheld_cols.append(np.asarray(data["omitted_covariate"], dtype=float))
        withheld_names.append("omitted_native_covariate")

    if withheld_cols:
        withheld = np.column_stack(withheld_cols)
    else:
        withheld = np.empty((n, 0), dtype=float)
    return cov, names, withheld, withheld_names


def _true_distance(x: np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(0.0, np.einsum("ni,ij,nj->n", x, BASE_COV_INV, x)))


def _episode_truth(
    shock: np.ndarray,
    true_distance: np.ndarray,
) -> tuple[dict[str, np.ndarray], list[dict[str, Any]]]:
    n = len(shock)
    event = shock != 0
    sustained = np.zeros(n, dtype=bool)
    interruption = np.zeros(n, dtype=bool)
    censored = np.zeros(n, dtype=bool)
    episode_id = np.full(n, -1, dtype=int)

    entries = np.flatnonzero(event)
    episodes: list[dict[str, Any]] = []
    for j, start in enumerate(entries):
        next_entry = int(entries[j + 1]) if j + 1 < len(entries) else n
        first_return = None
        terminal = None
        outcome = None
        run = 0
        sustain_start = None

        end_search = next_entry if next_entry < n else n
        for t in range(start + 1, end_search):
            if true_distance[t] <= RETURN_RADIUS_TRUE:
                if first_return is None:
                    first_return = t
                run += 1
                if run == 1:
                    sustain_start = t
                if run >= RETURN_SUSTAIN_TRUE:
                    terminal = t
                    outcome = "SUSTAINED_RETURN"
                    sustained[t] = True
                    break
            else:
                run = 0
                sustain_start = None

        if outcome is None and next_entry < n:
            terminal = next_entry
            outcome = "INTERRUPTED_BY_NEW_PERTURBATION"
            interruption[next_entry] = True
        elif outcome is None:
            terminal = n - 1
            outcome = "RIGHT_CENSORED"
            censored[n - 1] = True

        episode_id[start:terminal + 1] = j

        entry_d = float(true_distance[start])
        seg = true_distance[start:terminal + 1]
        peak_ratio = float(np.max(seg) / max(entry_d, 1e-12))
        integ = float(np.sum(seg))
        terminal_d = float(true_distance[terminal])
        away = int(np.sum(seg > RETURN_RADIUS_TRUE))

        residual = {}
        for h in (20, 40, 80):
            k = min(n - 1, start + h)
            residual[str(h)] = float(true_distance[k])

        episodes.append({
            "episode_id": j,
            "entry_index": int(start),
            "entry_amplitude": float(SHOCK_MAGNITUDE * abs(shock[start])),
            "first_return_index": None if first_return is None else int(first_return),
            "sustained_return_index": int(terminal) if outcome == "SUSTAINED_RETURN" else None,
            "terminal_index": int(terminal),
            "outcome": outcome,
            "entry_true_distance": entry_d,
            "terminal_true_distance": terminal_d,
            "away_samples": away,
            "transient_amplification": peak_ratio,
            "integrated_true_distance": integ,
            "residual_distance": residual,
        })

    burden_count = np.zeros(n, dtype=float)
    burden_amp = np.zeros(n, dtype=float)
    burden_away = np.zeros(n, dtype=float)
    burden_incomplete = np.zeros(n, dtype=float)

    n_prior = 0.0
    amp_prior = 0.0
    away_prior = 0.0
    incomplete_prior = 0.0
    for ep in episodes:
        start = ep["entry_index"]
        burden_count[start:] = n_prior
        burden_amp[start:] = amp_prior
        burden_away[start:] = away_prior
        burden_incomplete[start:] = incomplete_prior

        n_prior += 1.0
        amp_prior += ep["entry_amplitude"]
        away_prior += ep["away_samples"]
        if ep["outcome"] != "SUSTAINED_RETURN":
            incomplete_prior += ep["terminal_true_distance"]

    arrays = {
        "event_entry_true": event,
        "sustained_return_true": sustained,
        "interruption_true": interruption,
        "right_censor_true": censored,
        "episode_id": episode_id,
        "burden_count_true": burden_count,
        "burden_amplitude_true": burden_amp,
        "burden_away_time_true": burden_away,
        "incomplete_recovery_burden_true": burden_incomplete,
    }
    return arrays, episodes


def _array_hash(arrays: dict[str, np.ndarray]) -> str:
    h = hashlib.sha256()
    for key in sorted(arrays):
        a = np.asarray(arrays[key])
        h.update(key.encode("utf-8"))
        h.update(str(a.dtype).encode("utf-8"))
        h.update(np.asarray(a.shape, dtype=np.int64).tobytes())
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def build_observation_episode_world(
    control_id: str,
    *,
    seed: int,
    scale_seconds: int,
    n: int = N_DEFAULT,
    nc20_cell: NC20Cell | None = None,
) -> dict[str, Any]:
    if control_id not in EXPECTED:
        raise ValueError(f"unknown control {control_id}")
    if scale_seconds not in SCALES:
        raise ValueError("scale outside frozen Q040 ladder")
    if control_id == "NC-R20" and nc20_cell is None:
        raise ValueError("NC-R20 requires an explicit frozen measurement cell")
    if control_id != "NC-R20" and nc20_cell is not None:
        raise ValueError("measurement cell only valid for NC-R20")

    data = generate_control(control_id, seed=seed, n=n)
    shock = np.asarray(data.get("shock", _default_shock(n)), dtype=float).copy()
    if len(shock) != n:
        raise ValueError("shock length mismatch")

    rate = _rate_array(data, n)
    baseline_scalar = _baseline_scalar(data, n)

    if nc20_cell is not None and nc20_cell.curvature != 0.0:
        t = np.arange(n, dtype=float)
        center = (n - 1) / 2.0
        baseline_scalar = baseline_scalar + 0.5 * nc20_cell.curvature * (t - center) ** 2

    baseline = baseline_scalar[:, None] * V_BASELINE[None, :]
    directions = _shock_directions(shock, control_id)
    shock_vec = SHOCK_MAGNITUDE * np.abs(shock)[:, None] * directions

    exog = np.asarray(data.get("exog", np.zeros(n)), dtype=float)
    if len(exog) != n:
        raise ValueError("exogenous forcing length mismatch")

    mult = _noise_multiplier(data, control_id, n, nc20_cell)
    if np.any(~np.isfinite(mult)) or np.any(mult <= 0):
        raise ValueError("invalid noise multiplier")

    ss = np.random.SeedSequence([int(seed), int(scale_seconds), 4040])
    rng_dyn = np.random.default_rng(ss.spawn(1)[0])
    rng_meas = np.random.default_rng(ss.spawn(1)[0])

    x = np.zeros((n, STATE_DIM), dtype=float)
    background = np.zeros_like(x)

    if control_id == "NC-R16" and "x" in data:
        hx = np.asarray(data["x"], dtype=float)
        background[:, :2] = hx

    if control_id == "NC-R8":
        v1 = np.asarray(data["v1"], dtype=float)
        background[:, :2] += 0.10 * v1

    for t in range(1, n):
        if control_id == "NC-R12":
            A = np.diag(np.exp(-0.08 * C_MODES))
            A[:2, :2] = np.asarray([[0.98, 0.1375], [0.0, 0.97]])
        else:
            eig = np.exp(-C_MODES * max(1e-6, float(rate[t - 1])))
            A = Q_FIXED @ np.diag(eig) @ Q_FIXED.T

        eps = float(mult[t]) * (BASE_CHOL @ rng_dyn.normal(size=STATE_DIM))
        forcing = 0.25 * float(exog[t]) * V_EXOG
        x[t] = A @ x[t - 1] + shock_vec[t] + forcing + eps

    z_latent = baseline + x + background

    update_mask = _update_schedule(n, nc20_cell, rng_meas)
    stale = _staleness(update_mask)
    z_observed = _carry_forward(z_latent, update_mask)

    true_d = _true_distance(x)
    ep_arrays, episodes = _episode_truth(shock, true_d)

    cov_true = (mult[:, None, None] ** 2) * BASE_COV[None, :, :]
    covariates, cov_names, withheld, withheld_names = _make_covariates(
        data, z_observed, shock, update_mask, stale
    )

    cross_scale_truth: dict[str, Any] = {}
    for key in ("slow", "fast", "slow_mechanical", "fast_history_proxy", "latent_regime"):
        if key in data:
            value = np.asarray(data[key], dtype=float)
            if len(value) == n:
                cross_scale_truth[key] = value

    extras: dict[str, Any] = {}
    if control_id == "NC-R8":
        extras["scalar_refusal_v1"] = np.asarray(data["v1"], dtype=float)
        extras["scalar_refusal_v2"] = np.asarray(data["v2"], dtype=float)
        extras["scalar_refusal_scalar"] = np.asarray(data["scalar"], dtype=float)
    if control_id == "NC-R11" and "resistance" in data:
        extras["resistance_true"] = np.asarray(data["resistance"], dtype=float)
    if control_id == "NC-R12" and "eig_real" in data:
        extras["nonnormal_continuous_eig_real"] = np.asarray(data["eig_real"], dtype=float)

    arrays = {
        "time_index": np.arange(n, dtype=int),
        "time_seconds": np.arange(n, dtype=float) * float(scale_seconds),
        "Z_latent": z_latent,
        "Z_observed": z_observed,
        "baseline_true": baseline,
        "displacement_true": x,
        "noise_cov_true": cov_true,
        "update_mask": update_mask,
        "staleness_samples": stale,
        "shock_input": shock,
        "shock_direction": directions,
        "exogenous_forcing": exog,
        "session_phase": _phase(n),
        "native_covariates": covariates,
        "withheld_native_covariates": withheld,
        "true_distance": true_d,
        **ep_arrays,
    }

    metadata = {
        "schema_version": "q040-synthetic-observation-episode-v0.4",
        "control_id": control_id,
        "scale_seconds": int(scale_seconds),
        "seed": int(seed),
        "state_dim": STATE_DIM,
        "expected_disposition": EXPECTED[control_id],
        "native_covariate_names": cov_names,
        "withheld_native_covariate_names": withheld_names,
        "observed_exogenous_forcing": bool(np.any(exog != 0)),
        "intentionally_withheld_native_covariate": bool(withheld.shape[1] > 0),
        "cross_scale_truth_keys": sorted(cross_scale_truth),
        "sparse_support_refusal_world": control_id == "NC-R21",
        "nc20_cell": None if nc20_cell is None else asdict(nc20_cell),
        "array_sha256": _array_hash(arrays),
    }

    return {
        "arrays": arrays,
        "episodes": episodes,
        "cross_scale_truth": cross_scale_truth,
        "extras": extras,
        "metadata": metadata,
    }


def validate_world(world: dict[str, Any]) -> dict[str, Any]:
    a = world["arrays"]
    m = world["metadata"]
    n = len(a["time_index"])
    faults: list[str] = []

    required = [
        "time_index", "time_seconds", "Z_latent", "Z_observed",
        "baseline_true", "displacement_true", "noise_cov_true",
        "update_mask", "staleness_samples", "shock_input",
        "shock_direction", "exogenous_forcing", "session_phase",
        "native_covariates", "withheld_native_covariates",
        "true_distance", "event_entry_true", "sustained_return_true",
        "interruption_true", "right_censor_true", "episode_id",
        "burden_count_true", "burden_amplitude_true",
        "burden_away_time_true", "incomplete_recovery_burden_true",
    ]
    for key in required:
        if key not in a:
            faults.append(f"missing:{key}")

    if faults:
        return {"pass": False, "faults": faults}

    if a["Z_latent"].shape != (n, STATE_DIM):
        faults.append("Z_latent_shape")
    if a["Z_observed"].shape != (n, STATE_DIM):
        faults.append("Z_observed_shape")
    if a["baseline_true"].shape != (n, STATE_DIM):
        faults.append("baseline_shape")
    if a["displacement_true"].shape != (n, STATE_DIM):
        faults.append("displacement_shape")
    if a["noise_cov_true"].shape != (n, STATE_DIM, STATE_DIM):
        faults.append("noise_cov_shape")

    finite_keys = [
        "Z_latent", "baseline_true", "displacement_true", "noise_cov_true",
        "shock_input", "shock_direction", "exogenous_forcing",
        "session_phase", "true_distance",
    ]
    for key in finite_keys:
        if np.any(~np.isfinite(a[key])):
            faults.append(f"nonfinite:{key}")

    if not np.array_equal(a["event_entry_true"], a["shock_input"] != 0):
        faults.append("event_shock_identity")

    terminal_sum = (
        a["sustained_return_true"].astype(int)
        + a["interruption_true"].astype(int)
        + a["right_censor_true"].astype(int)
    )
    if np.any(terminal_sum > 1):
        faults.append("terminal_state_overlap")

    expected_episodes = int(np.count_nonzero(a["shock_input"]))
    if len(world["episodes"]) != expected_episodes:
        faults.append("episode_count")

    if m["control_id"] == "NC-R17b":
        if a["withheld_native_covariates"].shape[1] < 1:
            faults.append("missing_withheld_covariate")
        if "omitted_native_covariate" in m["native_covariate_names"]:
            faults.append("withheld_leaked_to_native")

    if m["control_id"] == "NC-R20":
        mask = a["update_mask"].astype(bool)
        stale = a["staleness_samples"]
        last = -1
        for i, flag in enumerate(mask):
            if flag:
                last = i
                if stale[i] != 0:
                    faults.append("staleness_update_mismatch")
                    break
            elif last >= 0 and stale[i] != i - last:
                faults.append("staleness_gap_mismatch")
                break

        z = a["Z_observed"]
        for i in range(1, n):
            if not mask[i] and np.all(np.isfinite(z[i - 1])):
                if not np.array_equal(z[i], z[i - 1]):
                    faults.append("carry_forward_mismatch")
                    break

    stable = True
    if m["control_id"] != "NC-R12":
        control_rate = 0.08
        eig = np.exp(-C_MODES * control_rate)
        stable = bool(np.all(eig < 1.0))
    else:
        eig = np.linalg.eigvals(np.asarray([[0.98, 0.1375], [0.0, 0.97]]))
        stable = bool(np.all(np.abs(eig) < 1.0))
    if not stable:
        faults.append("restoring_operator_unstable")

    return {
        "pass": len(faults) == 0,
        "faults": faults,
        "control_id": m["control_id"],
        "scale_seconds": m["scale_seconds"],
        "episode_count": len(world["episodes"]),
        "update_fraction": float(np.mean(a["update_mask"])),
        "max_staleness": int(np.max(a["staleness_samples"])),
        "array_sha256": m["array_sha256"],
    }


def determinism_check(
    control_id: str,
    *,
    seed: int,
    scale_seconds: int,
    nc20_cell: NC20Cell | None = None,
) -> bool:
    a = build_observation_episode_world(
        control_id, seed=seed, scale_seconds=scale_seconds, nc20_cell=nc20_cell
    )
    b = build_observation_episode_world(
        control_id, seed=seed, scale_seconds=scale_seconds, nc20_cell=nc20_cell
    )
    return a["metadata"]["array_sha256"] == b["metadata"]["array_sha256"]
