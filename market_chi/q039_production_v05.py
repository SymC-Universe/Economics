from __future__ import annotations

from dataclasses import asdict
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from .q039_blocks_v04 import SESSION_SECONDS, SCALES, build_scale_blocks
from .q039_classification_v04 import factor2_label, p60_label, joint_status_map
from .q039_intake_v04 import dense_q039_state
from .q039_layer_l_eval_v04 import (
    build_pair_observations,
    equal_day_noncircular_bootstrap,
    evaluate_nested_day,
)
from .q039_layer_r_production_v04 import (
    adjacent_k6_principal_cosines,
    analyze_layer_r_blocks,
)
from .q039_layer_r_v04 import (
    DayLayerRSummary,
    DirectionSummary,
    classify_layer_r,
)
from .q039_nc7_context_v05 import recompute_nc7_native_context
from .q039_nc7_v04 import NC7_SEED, NC7_WORLDS, carry_forward_isotropic_world
from .q039_source_v05 import (
    DATES,
    NS,
    SourceSpec,
    date_start_ns,
    load_selected_session_rows,
    load_source_manifest,
)

PAIR_SPECS = {
    "P15_30": {
        "fine_seconds": 15,
        "coarse_seconds": 30,
        "small": "A2",
        "large": "F2",
    },
    "P30_60": {
        "fine_seconds": 30,
        "coarse_seconds": 60,
        "small": "A2",
        "large": "F2",
    },
    "P60_300": {
        "fine_seconds": 60,
        "coarse_seconds": 300,
        "small": "A",
        "large": "S",
    },
}
ORDERED_SPEC = {
    "fine_seconds": 60,
    "coarse_seconds": 300,
    "small": "U",
    "large": "S",
}
PRIMARY_CI = 0.98333
KNOWN_TRUTHS_PASSED = True
ORDER_SPECIFICITY_RESOLVED = True

R_DIRS = ("sym_lineage", "imb_lineage", "sym_functional", "imb_functional")


def valid_primary_pairs(real_aggregate: dict[str, object]) -> tuple[str, ...]:
    """Return only primary pairs whose frozen real test is COMPLETE.

    Invalid primary tests are preserved and may not be rescued by NC7.
    """
    return tuple(
        pair
        for pair in PAIR_SPECS
        if real_aggregate["layer_l"][pair].get("status") == "COMPLETE"
    )


def _json_default(x: Any):
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if hasattr(x, "to_dict"):
        return x.to_dict()
    if hasattr(x, "__dataclass_fields__"):
        return asdict(x)
    raise TypeError(type(x).__name__)


def write_json_atomic(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=_json_default) + "\n", encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _direction_from_dict(d: dict[str, object]) -> DirectionSummary:
    return DirectionSummary(
        capture=float(d["capture"]),
        rho1=float(d["rho1"]),
        matched_percentile_lineage=float(d["matched_percentile_lineage"]),
        matched_percentile_functional=float(d["matched_percentile_functional"]),
    )


def day_r_summary_from_dict(d: dict[str, object]) -> DayLayerRSummary:
    return DayLayerRSummary(
        sym_lineage=_direction_from_dict(d["sym_lineage"]),
        imb_lineage=_direction_from_dict(d["imb_lineage"]),
        sym_functional=_direction_from_dict(d["sym_functional"]),
        imb_functional=_direction_from_dict(d["imb_functional"]),
        sym_winsor_lineage_capture=float(d["sym_winsor_lineage_capture"]),
        imb_winsor_lineage_capture=float(d["imb_winsor_lineage_capture"]),
        sym_winsor_functional_capture=float(d["sym_winsor_functional_capture"]),
        imb_winsor_functional_capture=float(d["imb_winsor_functional_capture"]),
        sym_phase_lineage=_direction_from_dict(d["sym_phase_lineage"]),
        imb_phase_lineage=_direction_from_dict(d["imb_phase_lineage"]),
        sym_phase_functional=_direction_from_dict(d["sym_phase_functional"]),
        imb_phase_functional=_direction_from_dict(d["imb_phase_functional"]),
    )


def nc7_day_seed(world_index: int, day_index: int) -> int:
    if not (0 <= world_index < NC7_WORLDS):
        raise ValueError("world_index outside frozen 0..199 range")
    if not (0 <= day_index < len(DATES)):
        raise ValueError("day_index outside frozen development-day range")
    ss = np.random.SeedSequence([NC7_SEED, world_index, day_index])
    return int(ss.generate_state(1, dtype=np.uint32)[0])


def _save_dense(path: Path, dense: dict[str, np.ndarray]) -> None:
    keys = (
        "times_ns", "feature_present", "l10_update_indicator",
        "staleness_age_s", "depth20_raw", "depth20_log1p",
        "event_rows", "trade_volume", "signed_trade_volume",
        "spread", "microprice_offset", "l10_imbalance",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".npz.tmp")
    with tmp.open("wb") as f:
        np.savez(f, **{k: np.asarray(dense[k]) for k in keys})
    tmp.replace(path)


def _load_dense(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _pair_eval(
    blocks_by_scale: dict[int, list],
    spec: dict[str, object],
    *,
    day_start_ns: int,
):
    fine = int(spec["fine_seconds"])
    coarse = int(spec["coarse_seconds"])
    obs = build_pair_observations(
        blocks_by_scale[fine],
        blocks_by_scale[coarse],
        fine_seconds=fine,
        coarse_seconds=coarse,
    )
    return evaluate_nested_day(
        obs,
        small_name=str(spec["small"]),
        large_name=str(spec["large"]),
        fine_seconds=fine,
        coarse_seconds=coarse,
        day_start_ns=day_start_ns,
    )


def _save_pair_aux(path: Path, aux: dict[str, object]) -> None:
    wanted = (
        "source_block", "source_start_ns", "target_end_ns",
        "primary_mask", "descriptive_mask", "raw_delta",
        "clark_west_delta", "pred_small", "pred_large", "y",
    )
    arrays = {k: np.asarray(aux[k]) for k in wanted if k in aux}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".npz.tmp")
    with tmp.open("wb") as f:
        np.savez(f, **arrays)
    tmp.replace(path)


def process_real_day(
    spec: SourceSpec,
    *,
    out_dir: Path,
    matched_draws: int = 5000,
) -> dict[str, object]:
    date_text = spec.date
    day_dir = out_dir / "real" / date_text
    summary_path = day_dir / "summary.json"
    dense_path = day_dir / "dense_state.npz"

    if summary_path.exists() and dense_path.exists():
        saved = read_json(summary_path)
        if saved.get("feature_sha256") == spec.feature_sha256:
            return saved

    rows = load_selected_session_rows(spec)
    start_ns = date_start_ns(date_text)
    end_ns = start_ns + SESSION_SECONDS * NS
    dense, intake_audit = dense_q039_state(rows, start_ns, end_ns)
    _save_dense(dense_path, dense)

    blocks = {
        scale: build_scale_blocks(dense, scale_seconds=scale, session_start_ns=start_ns)
        for scale in SCALES
    }

    r_raw = {
        scale: analyze_layer_r_blocks(
            blocks[scale],
            scale_seconds=scale,
            matched_draws=matched_draws,
        )
        for scale in SCALES
    }
    if any(v.get("status") != "COMPLETE" for v in r_raw.values()):
        bad = {str(k): v.get("status") for k, v in r_raw.items() if v.get("status") != "COMPLETE"}
        raise RuntimeError(f"Layer R real-day refusal {date_text}: {bad}")

    adjacent = {}
    for fine, coarse in ((15, 30), (30, 60), (60, 300)):
        adjacent[f"{fine}_{coarse}"] = adjacent_k6_principal_cosines(
            r_raw[fine], r_raw[coarse]
        )

    layer_l = {}
    for pair, pair_spec in PAIR_SPECS.items():
        summary, aux = _pair_eval(blocks, pair_spec, day_start_ns=start_ns)
        layer_l[pair] = summary.to_dict()
        _save_pair_aux(day_dir / f"{pair}_primary_aux.npz", aux)

    ordered_summary, ordered_aux = _pair_eval(
        blocks, ORDERED_SPEC, day_start_ns=start_ns
    )
    layer_l["P60_300_U_to_S"] = ordered_summary.to_dict()
    _save_pair_aux(day_dir / "P60_300_U_to_S_aux.npz", ordered_aux)

    result = {
        "date": date_text,
        "feature_sha256": spec.feature_sha256,
        "instrument_id": spec.instrument_id,
        "symbol": spec.symbol,
        "intake_audit": intake_audit.to_dict(),
        "layer_r": {
            str(scale): {
                "status": r_raw[scale]["status"],
                "day_summary": r_raw[scale]["day_summary_json"],
                "spectral": r_raw[scale]["spectral"],
                "direction_diagnostics": r_raw[scale]["direction_diagnostics"],
                "measurement_diagnostics": r_raw[scale]["measurement_diagnostics"],
                "matched_draws": r_raw[scale]["matched_draws"],
                "matched_seed": r_raw[scale]["matched_seed"],
            }
            for scale in SCALES
        },
        "adjacent_k6_principal_cosines": adjacent,
        "layer_l": layer_l,
        "real_q039_outcomes_opened": True,
    }
    write_json_atomic(summary_path, result)
    return result


def _load_pair_aux(out_dir: Path, date_text: str, pair: str) -> dict[str, np.ndarray]:
    p = out_dir / "real" / date_text / (
        f"{pair}_primary_aux.npz" if pair != "P60_300_U_to_S"
        else "P60_300_U_to_S_aux.npz"
    )
    with np.load(p, allow_pickle=False) as z:
        return {k: z[k] for k in z.files}


def _pooled_mae(aux_by_day: list[dict[str, np.ndarray]]) -> dict[str, float]:
    ys, ps, pl = [], [], []
    for a in aux_by_day:
        mask = np.asarray(a["primary_mask"], dtype=bool)
        if not np.any(mask):
            continue
        ys.append(np.asarray(a["y"])[mask])
        ps.append(np.asarray(a["pred_small"])[mask])
        pl.append(np.asarray(a["pred_large"])[mask])
    if not ys:
        return {
            "small_d": math.nan, "large_d": math.nan,
            "small_i": math.nan, "large_i": math.nan,
        }
    y = np.vstack(ys)
    psmall = np.vstack(ps)
    plarge = np.vstack(pl)
    ms = np.mean(np.abs(y - psmall), axis=0)
    ml = np.mean(np.abs(y - plarge), axis=0)
    return {
        "small_d": float(ms[0]), "large_d": float(ml[0]),
        "small_i": float(ms[1]), "large_i": float(ml[1]),
    }


def aggregate_real(
    real_days: list[dict[str, object]],
    *,
    out_dir: Path,
) -> dict[str, object]:
    layer_r = {}
    for scale in SCALES:
        summaries = [
            day_r_summary_from_dict(day["layer_r"][str(scale)]["day_summary"])
            for day in real_days
        ]
        layer_r[str(scale)] = classify_layer_r(summaries)

    layer_l = {}
    for pair, spec in PAIR_SPECS.items():
        day_summaries = [day["layer_l"][pair] for day in real_days]
        invalid_days = [
            DATES[i]
            for i, summary in enumerate(day_summaries)
            if summary.get("status") != "COMPLETE"
        ]
        if invalid_days:
            layer_l[pair] = {
                "status": "INVALID_TEST_INSUFFICIENT_IDENTIFICATION",
                "invalid_days": invalid_days,
                "day_statuses": {
                    DATES[i]: summary.get("status")
                    for i, summary in enumerate(day_summaries)
                },
                "day_reasons": {
                    DATES[i]: summary.get("reason")
                    for i, summary in enumerate(day_summaries)
                },
                "primary_ci": None,
                "day_points": [
                    summary.get("point_contrast")
                    for summary in day_summaries
                ],
                "nc7_required": False,
                "reason": (
                    "Frozen pair/day identification refusal preserved. "
                    "No bootstrap or NC7 rescue is permitted for an invalid primary pair."
                ),
            }
            continue

        auxs = [_load_pair_aux(out_dir, d, pair) for d in DATES]
        values_by_day = []
        blocks_by_day = []
        for a in auxs:
            mask = np.asarray(a["primary_mask"], dtype=bool)
            values_by_day.append(np.asarray(a["raw_delta"], dtype=float)[mask])
            blocks_by_day.append(np.asarray(a["source_block"], dtype=int)[mask])

        primary = equal_day_noncircular_bootstrap(
            values_by_day,
            blocks_by_day,
            coarse_seconds=int(spec["coarse_seconds"]),
            block_seconds=3600,
            reps=10_000,
            seed=20260929,
            ci_level=PRIMARY_CI,
        )
        sens30 = equal_day_noncircular_bootstrap(
            values_by_day,
            blocks_by_day,
            coarse_seconds=int(spec["coarse_seconds"]),
            block_seconds=1800,
            reps=10_000,
            seed=20260929,
            ci_level=PRIMARY_CI,
        )
        sens120 = equal_day_noncircular_bootstrap(
            values_by_day,
            blocks_by_day,
            coarse_seconds=int(spec["coarse_seconds"]),
            block_seconds=7200,
            reps=10_000,
            seed=20260929,
            ci_level=PRIMARY_CI,
        )
        day_points = [
            float(day["layer_l"][pair]["point_contrast"])
            for day in real_days
        ]
        layer_l[pair] = {
            "status": "COMPLETE",
            "primary_ci": primary,
            "sensitivity_30m": sens30,
            "sensitivity_2h": sens120,
            "day_points": day_points,
            "pooled_mae": _pooled_mae(auxs),
            "nc7_required": True,
        }

    ordered_day_summaries = [
        day["layer_l"]["P60_300_U_to_S"] for day in real_days
    ]
    ordered_invalid = [
        DATES[i]
        for i, summary in enumerate(ordered_day_summaries)
        if summary.get("status") != "COMPLETE"
    ]
    if ordered_invalid:
        layer_l["P60_300_U_to_S"] = {
            "status": "INVALID_TEST_INSUFFICIENT_IDENTIFICATION",
            "invalid_days": ordered_invalid,
            "ci_95": None,
            "day_points": [
                summary.get("point_contrast")
                for summary in ordered_day_summaries
            ],
        }
    else:
        ordered_auxs = [_load_pair_aux(out_dir, d, "P60_300_U_to_S") for d in DATES]
        ov, ob = [], []
        for a in ordered_auxs:
            mask = np.asarray(a["primary_mask"], dtype=bool)
            ov.append(np.asarray(a["raw_delta"], dtype=float)[mask])
            ob.append(np.asarray(a["source_block"], dtype=int)[mask])
        ordered_ci = equal_day_noncircular_bootstrap(
            ov, ob,
            coarse_seconds=300,
            block_seconds=3600,
            reps=10_000,
            seed=20260929,
            ci_level=0.95,
        )
        layer_l["P60_300_U_to_S"] = {
            "status": "COMPLETE",
            "ci_95": ordered_ci,
            "day_points": [
                float(day["layer_l"]["P60_300_U_to_S"]["point_contrast"])
                for day in real_days
            ],
        }

    out = {
        "layer_r": layer_r,
        "layer_l": layer_l,
        "known_truths_passed": KNOWN_TRUTHS_PASSED,
        "order_specificity_resolved": ORDER_SPECIFICITY_RESOLVED,
        "q038_holdout_used": False,
    }
    write_json_atomic(out_dir / "real" / "aggregate.json", out)
    return out


def _nc7_dense(real_dense: dict[str, np.ndarray], *, seed: int) -> dict[str, np.ndarray]:
    update = np.asarray(real_dense["l10_update_indicator"], dtype=bool)
    x = carry_forward_isotropic_world(update, seed=seed, dim=20)
    ctx = recompute_nc7_native_context(x, np.asarray(real_dense["spread"], dtype=float))
    return {
        "times_ns": np.asarray(real_dense["times_ns"]),
        "depth20_log1p": x,
        "event_rows": np.asarray(real_dense["event_rows"]),
        "trade_volume": np.asarray(real_dense["trade_volume"]),
        "signed_trade_volume": np.asarray(real_dense["signed_trade_volume"]),
        "spread": np.asarray(real_dense["spread"]),
        "microprice_offset": np.asarray(ctx["microprice_offset"]),
        "l10_imbalance": np.asarray(ctx["l10_imbalance"]),
        "staleness_age_s": np.asarray(real_dense["staleness_age_s"]),
        "l10_update_indicator": np.asarray(real_dense["l10_update_indicator"]),
    }


def _r_day_metrics(day_summary: DayLayerRSummary) -> dict[str, dict[str, float]]:
    out = {}
    for key in R_DIRS:
        ordinary = getattr(day_summary, key)
        phase = getattr(day_summary, key.replace("_lineage", "_phase_lineage").replace("_functional", "_phase_functional"))
        out[key] = {
            "ordinary_capture": float(ordinary.capture),
            "phase_capture": float(phase.capture),
            "ordinary_rho1": float(ordinary.rho1),
            "phase_rho1": float(phase.rho1),
        }
    return out


def process_nc7_world(
    world_index: int,
    *,
    out_dir: Path,
    real_dense_by_day: dict[str, dict[str, np.ndarray]],
    active_pairs: tuple[str, ...] | None = None,
    matched_draws: int = 5000,
) -> dict[str, object]:
    world_path = out_dir / "nc7" / "worlds" / f"world_{world_index:03d}.json"
    if world_path.exists():
        saved = read_json(world_path)
        if saved.get("world_index") == world_index:
            return saved

    if active_pairs is None:
        active_pairs = tuple(PAIR_SPECS)
    unknown = set(active_pairs) - set(PAIR_SPECS)
    if unknown:
        raise ValueError(f"unknown NC7 active pairs: {sorted(unknown)}")
    pair_day_points = {p: [] for p in active_pairs}
    r_day = {str(scale): [] for scale in SCALES}
    seeds = {}

    for day_index, date_text in enumerate(DATES):
        seed = nc7_day_seed(world_index, day_index)
        seeds[date_text] = seed
        dense = _nc7_dense(real_dense_by_day[date_text], seed=seed)
        start_ns = date_start_ns(date_text)
        blocks = {
            scale: build_scale_blocks(dense, scale_seconds=scale, session_start_ns=start_ns)
            for scale in SCALES
        }

        for pair in active_pairs:
            spec = PAIR_SPECS[pair]
            summary, _ = _pair_eval(blocks, spec, day_start_ns=start_ns)
            if summary.status != "COMPLETE":
                raise RuntimeError(
                    f"NC7 Layer-L invalid world={world_index} day={date_text} pair={pair} status={summary.status}"
                )
            pair_day_points[pair].append(float(summary.point_contrast))

        for scale in SCALES:
            rr = analyze_layer_r_blocks(
                blocks[scale],
                scale_seconds=scale,
                matched_draws=matched_draws,
            )
            if rr.get("status") != "COMPLETE":
                raise RuntimeError(
                    f"NC7 Layer-R invalid world={world_index} day={date_text} scale={scale} status={rr.get('status')}"
                )
            r_day[str(scale)].append(
                _r_day_metrics(rr["day_summary"])
            )

    pair_points = {
        p: float(np.mean(v))
        for p, v in pair_day_points.items()
    }
    r_world = {}
    for scale in SCALES:
        skey = str(scale)
        r_world[skey] = {}
        for direction in R_DIRS:
            r_world[skey][direction] = {}
            for metric in ("ordinary_capture", "phase_capture", "ordinary_rho1", "phase_rho1"):
                vals = [d[direction][metric] for d in r_day[skey]]
                r_world[skey][direction][metric] = float(np.median(vals))

    result = {
        "world_index": world_index,
        "base_seed": NC7_SEED,
        "day_seeds": seeds,
        "pair_equal_day_point_contrasts": pair_points,
        "layer_r_median_across_days": r_world,
        "real_semantic_values_used": False,
        "real_update_timing_preserved": True,
    }
    write_json_atomic(world_path, result)
    return result


def _real_r_medians(real_days: list[dict[str, object]]) -> dict[str, object]:
    out = {}
    for scale in SCALES:
        skey = str(scale)
        out[skey] = {}
        ds = [
            day_r_summary_from_dict(day["layer_r"][skey]["day_summary"])
            for day in real_days
        ]
        for direction in R_DIRS:
            ordinary = [float(getattr(d, direction).capture) for d in ds]
            phase_name = direction.replace("_lineage", "_phase_lineage").replace("_functional", "_phase_functional")
            phase = [float(getattr(d, phase_name).capture) for d in ds]
            out[skey][direction] = {
                "ordinary_capture_median": float(np.median(ordinary)),
                "phase_capture_median": float(np.median(phase)),
            }
    return out


def aggregate_nc7_and_finalize(
    worlds: list[dict[str, object]],
    *,
    real_aggregate: dict[str, object],
    real_days: list[dict[str, object]],
    out_dir: Path,
) -> dict[str, object]:
    if len(worlds) != NC7_WORLDS:
        raise ValueError("NC7 finalization requires exactly 200 worlds")

    pair_nc7 = {}
    labels = {}
    for pair, spec in PAIR_SPECS.items():
        real_pair = real_aggregate["layer_l"][pair]
        if real_pair.get("status") != "COMPLETE":
            pair_nc7[pair] = {
                "status": "NOT_RUN_REAL_PAIR_INVALID",
                "worlds": 0,
                "reason": (
                    "The frozen real primary pair is invalid for identification; "
                    "NC7 cannot rescue a failed primary test."
                ),
            }
            labels[pair] = "INVALID_TEST_INSUFFICIENT_IDENTIFICATION"
            continue

        vals = np.asarray([
            float(w["pair_equal_day_point_contrasts"][pair])
            for w in worlds
        ], dtype=float)
        q95 = float(np.quantile(vals, 0.95))
        real_point = float(real_pair["primary_ci"]["point"])
        exceeded = bool(real_point > q95)
        pair_nc7[pair] = {
            "status": "COMPLETE",
            "real_point": real_point,
            "nc7_q95": q95,
            "exceeded_q95": exceeded,
            "null_mean": float(np.mean(vals)),
            "null_sd": float(np.std(vals, ddof=0)),
            "worlds": NC7_WORLDS,
        }

        pm = real_pair["pooled_mae"]
        if pair in ("P15_30", "P30_60"):
            labels[pair] = factor2_label(
                primary_ci=real_pair["primary_ci"],
                day_points=real_pair["day_points"],
                pooled_mae_small_d=pm["small_d"],
                pooled_mae_large_d=pm["large_d"],
                pooled_mae_small_i=pm["small_i"],
                pooled_mae_large_i=pm["large_i"],
                nc7_exceeded_95=exceeded,
                known_truths_passed=KNOWN_TRUTHS_PASSED,
            )
        else:
            ordered = real_aggregate["layer_l"]["P60_300_U_to_S"]
            ordered_ci = ordered.get("ci_95") if ordered.get("status") == "COMPLETE" else None
            if ordered_ci is None:
                labels[pair] = "NEED_MORE_INFO_OR_MIXED_P0D"
            else:
                labels[pair] = p60_label(
                    primary_ci=real_pair["primary_ci"],
                    ordered_ci_95=ordered_ci,
                    day_points=real_pair["day_points"],
                    pooled_mae_small_d=pm["small_d"],
                    pooled_mae_large_d=pm["large_d"],
                    pooled_mae_small_i=pm["small_i"],
                    pooled_mae_large_i=pm["large_i"],
                    nc7_exceeded_95=exceeded,
                    known_truths_passed=KNOWN_TRUTHS_PASSED,
                    order_specificity_resolved=ORDER_SPECIFICITY_RESOLVED,
                )

    real_r = _real_r_medians(real_days)
    r_nc7 = {}
    for scale in SCALES:
        skey = str(scale)
        r_nc7[skey] = {}
        for direction in R_DIRS:
            r_nc7[skey][direction] = {}
            for metric in ("ordinary_capture", "phase_capture"):
                vals = np.asarray([
                    float(w["layer_r_median_across_days"][skey][direction][metric])
                    for w in worlds
                ], dtype=float)
                q95 = float(np.quantile(vals, 0.95))
                real_key = metric + "_median"
                real_value = float(real_r[skey][direction][real_key])
                r_nc7[skey][direction][metric] = {
                    "real_median": real_value,
                    "nc7_q95": q95,
                    "exceeded_q95": bool(real_value > q95),
                }

    final = {
        "schema_version": "q039-v0.5-p0d-result-v1",
        "real_data_scope": list(DATES),
        "q038_holdout_used": False,
        "layer_r": real_aggregate["layer_r"],
        "layer_r_nc7": r_nc7,
        "layer_l": real_aggregate["layer_l"],
        "layer_l_nc7": pair_nc7,
        "pair_labels": labels,
        "known_truths_passed": KNOWN_TRUTHS_PASSED,
        "order_specificity_resolved": ORDER_SPECIFICITY_RESOLVED,
        "nc7_worlds": NC7_WORLDS,
        "nc7_base_seed": NC7_SEED,
        "nc7_stream_rule": "SeedSequence([20261001, world_index, day_index])",
        "status": "Q039_V0_5_P0D_EXECUTION_COMPLETE",
        "invalid_primary_pairs": [
            pair for pair in PAIR_SPECS
            if real_aggregate["layer_l"][pair].get("status") != "COMPLETE"
        ],
        "nonclaims": [
            "No Q038 June 9-11 holdout data used for tuning or execution.",
            "No causal substrate-inheritance claim is licensed by Q039 alone.",
            "NC7 is a matched-update-timing carry-forward artifact screen and may be lenient against empirical amplitude persistence.",
        ],
    }
    write_json_atomic(out_dir / "Q039_V0_5_P0D_RESULT.json", final)
    return final
