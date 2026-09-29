from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

DIM = 20
K = 6
Q95 = 0.5496416495066101
COMMON_MODE_RHO1 = 0.80


@dataclass(frozen=True)
class DirectionSummary:
    capture: float
    rho1: float
    matched_percentile_lineage: float
    matched_percentile_functional: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class DayLayerRSummary:
    sym_lineage: DirectionSummary
    imb_lineage: DirectionSummary
    sym_functional: DirectionSummary
    imb_functional: DirectionSummary
    sym_winsor_lineage_capture: float
    imb_winsor_lineage_capture: float
    sym_winsor_functional_capture: float
    imb_winsor_functional_capture: float
    sym_phase_lineage: DirectionSummary
    imb_phase_lineage: DirectionSummary
    sym_phase_functional: DirectionSummary
    imb_phase_functional: DirectionSummary

    def to_dict(self):
        return {
            "sym_lineage": self.sym_lineage.to_dict(),
            "imb_lineage": self.imb_lineage.to_dict(),
            "sym_functional": self.sym_functional.to_dict(),
            "imb_functional": self.imb_functional.to_dict(),
            "sym_winsor_lineage_capture": self.sym_winsor_lineage_capture,
            "imb_winsor_lineage_capture": self.imb_winsor_lineage_capture,
            "sym_winsor_functional_capture": self.sym_winsor_functional_capture,
            "imb_winsor_functional_capture": self.imb_winsor_functional_capture,
            "sym_phase_lineage": self.sym_phase_lineage.to_dict(),
            "imb_phase_lineage": self.imb_phase_lineage.to_dict(),
            "sym_phase_functional": self.sym_phase_functional.to_dict(),
            "imb_phase_functional": self.imb_phase_functional.to_dict(),
        }


def canonical_raw_directions(dim: int = DIM) -> tuple[np.ndarray, np.ndarray]:
    if dim % 2:
        raise ValueError("dimension must be even for alternating bid/ask semantics")
    sym = np.ones(dim, dtype=float)
    imb = np.tile(np.array([1.0, -1.0]), dim // 2)
    sym /= np.linalg.norm(sym)
    imb /= np.linalg.norm(imb)
    return sym, imb


def winsorize_1_99(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    lo = np.quantile(x, 0.01, axis=0)
    hi = np.quantile(x, 0.99, axis=0)
    return np.clip(x, lo, hi)


def phase_design(n: int) -> np.ndarray:
    p = np.arange(n, dtype=float) / max(1, n)
    return np.column_stack([
        np.ones(n),
        np.sin(2 * np.pi * p),
        np.cos(2 * np.pi * p),
        np.sin(4 * np.pi * p),
        np.cos(4 * np.pi * p),
    ])


def phase_residualize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    q = phase_design(len(x))
    beta, *_ = np.linalg.lstsq(q, x, rcond=None)
    return x - q @ beta


def standardize(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or x.shape[1] != DIM:
        raise ValueError("x must have shape (n, 20)")
    mu = x.mean(axis=0)
    sigma = x.std(axis=0, ddof=0)
    if np.any(~np.isfinite(sigma)) or np.any(sigma <= 0):
        raise ValueError("constant or non-finite coordinate")
    return (x - mu) / sigma, sigma


def topk_basis(z: np.ndarray, k: int = K) -> np.ndarray:
    _, _, vh = np.linalg.svd(z, full_matrices=False)
    return vh[:k].T


def capture_and_rho1(u: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    proj = u.T @ b
    contrib = proj * proj
    capture = float(np.sum(contrib))
    if capture <= 0:
        return capture, math.nan
    return capture, float(np.max(contrib) / capture)


def _matched_raw_directions(
    rng: np.random.Generator,
    *,
    family: str,
    draws: int,
) -> np.ndarray:
    mag = rng.exponential(1.0, size=(draws, DIM))
    if family == "sym":
        raw = mag
    elif family == "imb":
        signs = np.tile(np.array([1.0, -1.0]), DIM // 2)
        raw = mag * signs[None, :]
    else:
        raise ValueError(family)
    raw /= np.linalg.norm(raw, axis=1, keepdims=True)
    return raw


def matched_percentiles(
    u: np.ndarray,
    target_lineage: np.ndarray,
    target_functional: np.ndarray,
    sigma: np.ndarray,
    *,
    family: str,
    draws: int,
    seed: int,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    raw = _matched_raw_directions(rng, family=family, draws=draws)

    # Lineage controls live directly in standardized-coordinate space.
    lineage_controls = raw
    lineage_caps = np.sum((lineage_controls @ u) ** 2, axis=1)
    target_lineage_cap = float(np.sum((u.T @ target_lineage) ** 2))
    lineage_pct = float(np.mean(lineage_caps <= target_lineage_cap))

    # Functional controls are raw covectors transported into standardized space.
    functional_controls = raw * sigma[None, :]
    functional_controls /= np.linalg.norm(functional_controls, axis=1, keepdims=True)
    functional_caps = np.sum((functional_controls @ u) ** 2, axis=1)
    target_functional_cap = float(np.sum((u.T @ target_functional) ** 2))
    functional_pct = float(np.mean(functional_caps <= target_functional_cap))
    return lineage_pct, functional_pct


def _direction_summary(
    u: np.ndarray,
    lineage: np.ndarray,
    functional: np.ndarray,
    sigma: np.ndarray,
    *,
    family: str,
    draws: int,
    seed: int,
) -> tuple[DirectionSummary, DirectionSummary]:
    c_line, r_line = capture_and_rho1(u, lineage)
    c_fun, r_fun = capture_and_rho1(u, functional)
    p_line, p_fun = matched_percentiles(
        u, lineage, functional, sigma,
        family=family, draws=draws, seed=seed
    )
    return (
        DirectionSummary(c_line, r_line, p_line, p_fun),
        DirectionSummary(c_fun, r_fun, p_line, p_fun),
    )


def analyze_layer_r_day(
    x: np.ndarray,
    *,
    scale_seconds: int,
    matched_draws: int = 5000,
) -> DayLayerRSummary:
    x = np.asarray(x, dtype=float)
    sym_raw, imb_raw = canonical_raw_directions()

    z, sigma = standardize(x)
    u = topk_basis(z)
    sym_lin = sym_raw.copy()
    imb_lin = imb_raw.copy()
    sym_fun = sigma * sym_raw
    sym_fun /= np.linalg.norm(sym_fun)
    imb_fun = sigma * imb_raw
    imb_fun /= np.linalg.norm(imb_fun)

    sym_line, sym_func = _direction_summary(
        u, sym_lin, sym_fun, sigma,
        family="sym", draws=matched_draws, seed=20260930 + scale_seconds
    )
    imb_line, imb_func = _direction_summary(
        u, imb_lin, imb_fun, sigma,
        family="imb", draws=matched_draws, seed=20260930 + scale_seconds
    )

    xw = winsorize_1_99(x)
    zw, sigmaw = standardize(xw)
    uw = topk_basis(zw)
    sym_fun_w = sigmaw * sym_raw
    sym_fun_w /= np.linalg.norm(sym_fun_w)
    imb_fun_w = sigmaw * imb_raw
    imb_fun_w /= np.linalg.norm(imb_fun_w)
    sym_w_line, _ = capture_and_rho1(uw, sym_lin)
    imb_w_line, _ = capture_and_rho1(uw, imb_lin)
    sym_w_fun, _ = capture_and_rho1(uw, sym_fun_w)
    imb_w_fun, _ = capture_and_rho1(uw, imb_fun_w)

    xr = phase_residualize(x)
    zr, sigmar = standardize(xr)
    ur = topk_basis(zr)
    sym_fun_r = sigmar * sym_raw
    sym_fun_r /= np.linalg.norm(sym_fun_r)
    imb_fun_r = sigmar * imb_raw
    imb_fun_r /= np.linalg.norm(imb_fun_r)

    sym_phase_line, sym_phase_func = _direction_summary(
        ur, sym_lin, sym_fun_r, sigmar,
        family="sym", draws=matched_draws, seed=20260930 + scale_seconds
    )
    imb_phase_line, imb_phase_func = _direction_summary(
        ur, imb_lin, imb_fun_r, sigmar,
        family="imb", draws=matched_draws, seed=20260930 + scale_seconds
    )

    return DayLayerRSummary(
        sym_lineage=sym_line,
        imb_lineage=imb_line,
        sym_functional=sym_func,
        imb_functional=imb_func,
        sym_winsor_lineage_capture=sym_w_line,
        imb_winsor_lineage_capture=imb_w_line,
        sym_winsor_functional_capture=sym_w_fun,
        imb_winsor_functional_capture=imb_w_fun,
        sym_phase_lineage=sym_phase_line,
        imb_phase_lineage=imb_phase_line,
        sym_phase_functional=sym_phase_func,
        imb_phase_functional=imb_phase_func,
    )


def _coherent(vals: list[float], threshold: float = Q95) -> bool:
    a = np.asarray(vals, dtype=float)
    return int(np.sum(a > threshold)) >= 4 and float(np.median(a)) > threshold


def classify_layer_r(days: list[DayLayerRSummary]) -> dict[str, object]:
    if len(days) != 5:
        raise ValueError("Layer-R coherence classification requires exactly five days")

    isotropic: dict[str, bool] = {}
    structure: dict[str, bool] = {}
    common_mode: dict[str, bool] = {}

    for name in ("sym", "imb"):
        for rep in ("lineage", "functional"):
            key = f"{name}_{rep}"
            ordinary = [getattr(d, key).capture for d in days]
            winsor = [getattr(d, f"{name}_winsor_{rep}_capture") for d in days]
            phase = [getattr(d, f"{name}_phase_{rep}").capture for d in days]

            iso_ok = _coherent(ordinary) and _coherent(winsor)

            if rep == "lineage":
                p_ord = [getattr(d, key).matched_percentile_lineage for d in days]
                p_phase = [
                    getattr(d, f"{name}_phase_{rep}").matched_percentile_lineage
                    for d in days
                ]
            else:
                p_ord = [getattr(d, key).matched_percentile_functional for d in days]
                p_phase = [
                    getattr(d, f"{name}_phase_{rep}").matched_percentile_functional
                    for d in days
                ]

            matched_ok = (
                sum(x > 0.95 for x in p_ord) >= 4
                and sum(x > 0.95 for x in p_phase) >= 4
            )
            phase_ok = _coherent(phase)

            rho_ord = [getattr(d, key).rho1 for d in days]
            rho_phase = [getattr(d, f"{name}_phase_{rep}").rho1 for d in days]
            cm = (
                sum(np.isfinite(x) and x > COMMON_MODE_RHO1 for x in rho_ord) >= 4
                and sum(np.isfinite(x) and x > COMMON_MODE_RHO1 for x in rho_phase) >= 4
            )

            isotropic[key] = bool(iso_ok)
            common_mode[key] = bool(cm)
            structure[key] = bool(iso_ok and phase_ok and matched_ok and not cm)

    required = ("sym_lineage", "imb_lineage", "sym_functional", "imb_functional")
    if all(structure[k] for k in required):
        status = "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D"
    elif all(isotropic[k] for k in required) and any(common_mode[k] for k in required):
        status = "CANONICAL_CAPTURE_ONLY_P0D"
    else:
        status = "STRUCTURAL_UNRESOLVED_P0D"

    return {
        "status": status,
        "isotropic": isotropic,
        "structure_specific": structure,
        "common_mode_dominated": common_mode,
    }

def _ar1(n: int, phi: float, sd: float, rng: np.random.Generator) -> np.ndarray:
    x = np.zeros(n, dtype=float)
    eps = rng.normal(scale=sd, size=n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + eps[i]
    return x


def synthetic_world(
    kind: str,
    *,
    seed: int,
    n: int = 2400,
    heavy_tail_df: float = 2.5,
    persistence: float = 0.90,
    sym_innovation_sd: float = 0.35,
    imb_innovation_sd: float = 0.30,
    isotropic_noise_sd: float = 0.30,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    sym, imb = canonical_raw_directions()

    if kind == "heavy_tail":
        return rng.standard_t(df=heavy_tail_df, size=(n, DIM))

    if kind == "calendar_common_mode":
        p = np.arange(n, dtype=float) / n
        f1 = np.sin(2 * np.pi * p) + 0.4 * np.sin(4 * np.pi * p)
        f2 = np.cos(2 * np.pi * p) + 0.35 * np.cos(4 * np.pi * p)
        noise = rng.normal(scale=0.45, size=(n, DIM))
        return 1.4 * f1[:, None] * sym + 1.1 * f2[:, None] * imb + noise

    if kind == "persistent_common_mode":
        f1 = _ar1(n, persistence, sym_innovation_sd, rng)
        f2 = _ar1(n, persistence, imb_innovation_sd, rng)
        noise = rng.normal(scale=isotropic_noise_sd, size=(n, DIM))
        return 1.2 * f1[:, None] * sym + 0.85 * f2[:, None] * imb + noise

    if kind == "isotropic":
        return rng.normal(size=(n, DIM))

    raise ValueError(kind)


def run_structural_known_truth(
    kind: str,
    *,
    base_seed: int,
    scale_seconds: int = 60,
    matched_draws: int = 5000,
    **kwargs,
) -> dict[str, object]:
    days = [
        analyze_layer_r_day(
            synthetic_world(kind, seed=base_seed + i, **kwargs),
            scale_seconds=scale_seconds,
            matched_draws=matched_draws,
        )
        for i in range(5)
    ]
    classified = classify_layer_r(days)
    return {
        "kind": kind,
        "classification": classified,
        "days": [d.to_dict() for d in days],
    }
