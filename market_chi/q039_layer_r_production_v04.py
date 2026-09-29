from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import numpy as np

from .modal_identifiability import spectral_metrics
from .q039_blocks_v04 import BlockRecord, SESSION_SECONDS
from .q039_layer_r_v04 import (
    K,
    DayLayerRSummary,
    DirectionSummary,
    canonical_raw_directions,
    capture_and_rho1,
    matched_percentiles,
    standardize,
    topk_basis,
    winsorize_1_99,
)


@dataclass(frozen=True)
class FullDirectionDiagnostic:
    capture: float
    rho1: float
    strongest_pc_rank: int
    strongest_pc_alignment: float
    contributions_pc1_to_pc6: tuple[float, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def phase_design_from_block_indices(
    block_indices: np.ndarray,
    *,
    scale_seconds: int,
) -> np.ndarray:
    idx = np.asarray(block_indices, dtype=float)
    seconds = idx * float(scale_seconds)
    phase = seconds / float(SESSION_SECONDS)
    return np.column_stack([
        np.ones(len(idx)),
        np.sin(2 * np.pi * phase),
        np.cos(2 * np.pi * phase),
        np.sin(4 * np.pi * phase),
        np.cos(4 * np.pi * phase),
    ])


def phase_residualize_actual(
    x: np.ndarray,
    block_indices: np.ndarray,
    *,
    scale_seconds: int,
) -> np.ndarray:
    q = phase_design_from_block_indices(block_indices, scale_seconds=scale_seconds)
    beta, *_ = np.linalg.lstsq(q, np.asarray(x, dtype=float), rcond=None)
    return np.asarray(x, dtype=float) - q @ beta


def _functional_direction(sigma: np.ndarray, raw: np.ndarray) -> np.ndarray:
    b = np.asarray(sigma, dtype=float) * np.asarray(raw, dtype=float)
    n = float(np.linalg.norm(b))
    if not math.isfinite(n) or n <= 0:
        raise ValueError("functional direction is degenerate")
    return b / n


def _summary_pair(
    u: np.ndarray,
    lineage: np.ndarray,
    functional: np.ndarray,
    sigma: np.ndarray,
    *,
    family: str,
    matched_draws: int,
    seed: int,
) -> tuple[DirectionSummary, DirectionSummary]:
    c_line, r_line = capture_and_rho1(u, lineage)
    c_fun, r_fun = capture_and_rho1(u, functional)
    p_line, p_fun = matched_percentiles(
        u,
        lineage,
        functional,
        sigma,
        family=family,
        draws=matched_draws,
        seed=seed,
    )
    return (
        DirectionSummary(c_line, r_line, p_line, p_fun),
        DirectionSummary(c_fun, r_fun, p_line, p_fun),
    )


def _full_direction(u: np.ndarray, b: np.ndarray) -> FullDirectionDiagnostic:
    proj = np.asarray(u.T @ b, dtype=float)
    contrib = proj * proj
    capture = float(np.sum(contrib))
    rho1 = float(np.max(contrib) / capture) if capture > 0 else math.nan
    rank = int(np.argmax(np.abs(proj)) + 1)
    align = float(np.max(np.abs(proj)))
    return FullDirectionDiagnostic(
        capture,
        rho1,
        rank,
        align,
        tuple(float(x) for x in contrib[:K]),
    )


def analyze_layer_r_blocks(
    blocks: list[BlockRecord],
    *,
    scale_seconds: int,
    matched_draws: int = 5000,
) -> dict[str, object]:
    complete = [b for b in blocks if b.status == "COMPLETE" and b.depth20_mean is not None]
    if len(complete) < 20:
        return {
            "status": "REFUSED_INSUFFICIENT_COMPLETE_BLOCKS",
            "scale_seconds": scale_seconds,
            "complete_blocks": len(complete),
        }

    idx = np.asarray([b.block_index for b in complete], dtype=int)
    x = np.asarray([b.depth20_mean for b in complete], dtype=float)
    if x.ndim != 2 or x.shape[1] != 20 or np.any(~np.isfinite(x)):
        return {
            "status": "REFUSED_REPRESENTATION",
            "scale_seconds": scale_seconds,
            "reason": "complete Layer-R block matrix is non-finite or wrong dimension",
        }

    sym_raw, imb_raw = canonical_raw_directions()

    try:
        z, sigma = standardize(x)
        _, s, vh = np.linalg.svd(z, full_matrices=False)
        u = vh[:K].T
        ratio = s * s
        ratio = ratio / ratio.sum()

        sym_fun = _functional_direction(sigma, sym_raw)
        imb_fun = _functional_direction(sigma, imb_raw)

        seed = 20260930 + scale_seconds
        sym_line, sym_func = _summary_pair(
            u, sym_raw, sym_fun, sigma,
            family="sym", matched_draws=matched_draws, seed=seed,
        )
        imb_line, imb_func = _summary_pair(
            u, imb_raw, imb_fun, sigma,
            family="imb", matched_draws=matched_draws, seed=seed,
        )

        xw = winsorize_1_99(x)
        zw, sigmaw = standardize(xw)
        uw = topk_basis(zw)
        sym_fun_w = _functional_direction(sigmaw, sym_raw)
        imb_fun_w = _functional_direction(sigmaw, imb_raw)
        sym_w_line, _ = capture_and_rho1(uw, sym_raw)
        imb_w_line, _ = capture_and_rho1(uw, imb_raw)
        sym_w_fun, _ = capture_and_rho1(uw, sym_fun_w)
        imb_w_fun, _ = capture_and_rho1(uw, imb_fun_w)

        xr = phase_residualize_actual(x, idx, scale_seconds=scale_seconds)
        zr, sigmar = standardize(xr)
        ur = topk_basis(zr)
        sym_fun_r = _functional_direction(sigmar, sym_raw)
        imb_fun_r = _functional_direction(sigmar, imb_raw)
        sym_phase_line, sym_phase_func = _summary_pair(
            ur, sym_raw, sym_fun_r, sigmar,
            family="sym", matched_draws=matched_draws, seed=seed,
        )
        imb_phase_line, imb_phase_func = _summary_pair(
            ur, imb_raw, imb_fun_r, sigmar,
            family="imb", matched_draws=matched_draws, seed=seed,
        )
    except (ValueError, np.linalg.LinAlgError) as exc:
        return {
            "status": "REFUSED_REPRESENTATION",
            "scale_seconds": scale_seconds,
            "reason": str(exc),
        }

    summary = DayLayerRSummary(
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

    staleness_mean = np.asarray([b.mean_staleness_age_s for b in complete], dtype=float)
    staleness_max = np.asarray([b.max_staleness_age_s for b in complete], dtype=float)
    updates = np.asarray([b.l10_update_fraction for b in complete], dtype=float)

    directions = {
        "sym_lineage": _full_direction(u, sym_raw).to_dict(),
        "imb_lineage": _full_direction(u, imb_raw).to_dict(),
        "sym_functional": _full_direction(u, sym_fun).to_dict(),
        "imb_functional": _full_direction(u, imb_fun).to_dict(),
    }

    return {
        "status": "COMPLETE",
        "scale_seconds": scale_seconds,
        "complete_blocks": len(complete),
        "first_complete_block_index": int(idx[0]),
        "last_complete_block_index": int(idx[-1]),
        "day_summary": summary,
        "day_summary_json": summary.to_dict(),
        "ordinary_top6_basis": u,
        "ordinary_variance_ratio": ratio,
        "spectral": spectral_metrics(ratio, ks=(2, 3, 4, 6, 10)),
        "direction_diagnostics": directions,
        "measurement_diagnostics": {
            "mean_update_fraction": float(np.mean(updates)),
            "median_update_fraction": float(np.median(updates)),
            "mean_block_staleness_s": float(np.mean(staleness_mean)),
            "max_block_staleness_s": float(np.max(staleness_max)),
        },
        "phase_design_uses_actual_block_indices": True,
        "matched_draws": matched_draws,
        "matched_seed": seed,
    }


def adjacent_k6_principal_cosines(
    fine_result: dict[str, object],
    coarse_result: dict[str, object],
) -> dict[str, object]:
    if fine_result.get("status") != "COMPLETE" or coarse_result.get("status") != "COMPLETE":
        return {"status": "REFUSED_INCOMPLETE_LAYER_R"}
    uf = np.asarray(fine_result["ordinary_top6_basis"], dtype=float)
    uc = np.asarray(coarse_result["ordinary_top6_basis"], dtype=float)
    if uf.shape != (20, K) or uc.shape != (20, K):
        return {"status": "REFUSED_BASIS_SHAPE"}
    s = np.linalg.svd(uf.T @ uc, compute_uv=False)
    return {
        "status": "COMPLETE",
        "principal_cosines": [float(x) for x in s],
        "min_principal_cosine": float(np.min(s)),
        "median_principal_cosine": float(np.median(s)),
    }
