from __future__ import annotations

import math
from typing import Sequence


def _finite_positive_count(values: Sequence[float]) -> int:
    return sum(math.isfinite(float(x)) and float(x) > 0 for x in values)


def factor2_label(
    *,
    primary_ci: dict[str, float],
    day_points: Sequence[float],
    pooled_mae_small_d: float,
    pooled_mae_large_d: float,
    pooled_mae_small_i: float,
    pooled_mae_large_i: float,
    nc7_exceeded_95: bool,
    known_truths_passed: bool,
) -> dict[str, object]:
    lower = float(primary_ci["lower"])
    upper = float(primary_ci["upper"])
    positive_days = _finite_positive_count(day_points)
    mae_both = (
        pooled_mae_large_d < pooled_mae_small_d
        and pooled_mae_large_i < pooled_mae_small_i
    )
    positive_gate = bool(
        lower > 0
        and positive_days >= 4
        and mae_both
        and nc7_exceeded_95
        and known_truths_passed
    )

    if positive_gate:
        label = "LAST_FAST_SEMANTIC_ADDS_P0D"
    elif upper <= 0:
        label = "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D"
    else:
        label = "NEED_MORE_INFO_OR_MIXED_P0D"

    qualifiers = []
    if lower > 0 and not nc7_exceeded_95:
        qualifiers.append("CARRY_FORWARD_ARTIFACT_NOT_EXCLUDED")
    if not known_truths_passed:
        qualifiers.append("KNOWN_TRUTH_QUALIFICATION_NOT_SATISFIED")

    return {
        "label": label,
        "positive_primary_gate": positive_gate,
        "positive_days": positive_days,
        "pooled_mae_both_improve": mae_both,
        "nc7_exceeded_95": bool(nc7_exceeded_95),
        "known_truths_passed": bool(known_truths_passed),
        "qualifiers": qualifiers,
    }


def p60_label(
    *,
    primary_ci: dict[str, float],
    ordered_ci_95: dict[str, float] | None,
    day_points: Sequence[float],
    pooled_mae_small_d: float,
    pooled_mae_large_d: float,
    pooled_mae_small_i: float,
    pooled_mae_large_i: float,
    nc7_exceeded_95: bool,
    known_truths_passed: bool,
    order_specificity_resolved: bool,
) -> dict[str, object]:
    lower = float(primary_ci["lower"])
    upper = float(primary_ci["upper"])
    positive_days = _finite_positive_count(day_points)
    mae_both = (
        pooled_mae_large_d < pooled_mae_small_d
        and pooled_mae_large_i < pooled_mae_small_i
    )
    primary_pass = bool(
        lower > 0
        and positive_days >= 4
        and mae_both
        and nc7_exceeded_95
        and known_truths_passed
    )

    qualifiers = []
    if lower > 0 and not nc7_exceeded_95:
        qualifiers.append("CARRY_FORWARD_ARTIFACT_NOT_EXCLUDED")
    if not known_truths_passed:
        qualifiers.append("KNOWN_TRUTH_QUALIFICATION_NOT_SATISFIED")

    if primary_pass:
        if ordered_ci_95 is None:
            label = "FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D"
            qualifiers.append("ORDERED_CHARACTERIZATION_NOT_RUN")
        elif float(ordered_ci_95["lower"]) > 0 and order_specificity_resolved:
            label = "ORDERED_SEMANTIC_PATH_ADDS_P0D"
        else:
            label = "FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D"
            if not order_specificity_resolved:
                qualifiers.append("ORDER_SPECIFICITY_NOT_RESOLVED")
    elif upper <= 0:
        label = "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D"
    else:
        label = "NEED_MORE_INFO_OR_MIXED_P0D"

    return {
        "label": label,
        "positive_primary_gate": primary_pass,
        "positive_days": positive_days,
        "pooled_mae_both_improve": mae_both,
        "nc7_exceeded_95": bool(nc7_exceeded_95),
        "known_truths_passed": bool(known_truths_passed),
        "order_specificity_resolved": bool(order_specificity_resolved),
        "qualifiers": qualifiers,
    }


def joint_status_map(layer_r_status: str, layer_l_status: str) -> dict[str, str]:
    allowed_r = {
        "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D",
        "CANONICAL_CAPTURE_ONLY_P0D",
        "STRUCTURAL_UNRESOLVED_P0D",
    }
    if layer_r_status not in allowed_r:
        raise ValueError("unexpected Layer R status")
    return {
        "layer_r": layer_r_status,
        "layer_l": layer_l_status,
        "rule": "mechanical Cartesian status map; no inheritance classification",
    }
