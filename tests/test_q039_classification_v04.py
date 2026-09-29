from market_chi.q039_classification_v04 import (
    factor2_label,
    joint_status_map,
    p60_label,
)


def test_factor2_positive_requires_all_gates():
    base = dict(
        primary_ci={"lower": 0.1, "upper": 0.3},
        day_points=[0.2, 0.1, 0.05, 0.08, -0.01],
        pooled_mae_small_d=1.0,
        pooled_mae_large_d=0.8,
        pooled_mae_small_i=1.1,
        pooled_mae_large_i=0.9,
        nc7_exceeded_95=True,
        known_truths_passed=True,
    )
    r = factor2_label(**base)
    assert r["label"] == "LAST_FAST_SEMANTIC_ADDS_P0D"

    base["nc7_exceeded_95"] = False
    r2 = factor2_label(**base)
    assert r2["label"] == "NEED_MORE_INFO_OR_MIXED_P0D"
    assert "CARRY_FORWARD_ARTIFACT_NOT_EXCLUDED" in r2["qualifiers"]


def test_negative_upper_is_no_gain_not_subtracts():
    r = factor2_label(
        primary_ci={"lower": -0.3, "upper": -0.1},
        day_points=[-0.2] * 5,
        pooled_mae_small_d=1.0,
        pooled_mae_large_d=1.1,
        pooled_mae_small_i=1.0,
        pooled_mae_large_i=1.1,
        nc7_exceeded_95=True,
        known_truths_passed=True,
    )
    assert r["label"] == "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D"


def test_p60_ordered_label_requires_primary_and_order_specificity():
    kw = dict(
        primary_ci={"lower": 0.1, "upper": 0.3},
        ordered_ci_95={"lower": 0.02, "upper": 0.2},
        day_points=[0.2, 0.1, 0.08, 0.07, -0.01],
        pooled_mae_small_d=1.0,
        pooled_mae_large_d=0.8,
        pooled_mae_small_i=1.0,
        pooled_mae_large_i=0.9,
        nc7_exceeded_95=True,
        known_truths_passed=True,
        order_specificity_resolved=True,
    )
    r = p60_label(**kw)
    assert r["label"] == "ORDERED_SEMANTIC_PATH_ADDS_P0D"

    kw["order_specificity_resolved"] = False
    r2 = p60_label(**kw)
    assert r2["label"] == "FINE_SEMANTIC_INFO_ADDS_ORDER_NOT_RESOLVED_P0D"


def test_joint_map_refuses_inheritance_wording():
    r = joint_status_map(
        "CANONICAL_CAPTURE_ONLY_P0D",
        "NO_INCREMENTAL_SEMANTIC_GAIN_DETECTED_P0D",
    )
    assert r["layer_r"] == "CANONICAL_CAPTURE_ONLY_P0D"
    assert "inheritance classification" in r["rule"]
