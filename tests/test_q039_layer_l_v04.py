from market_chi.q039_layer_l_v04 import (
    run_factor2_truth,
    run_p60_ordered_truth,
    run_order_specificity,
)


def test_nc1_phase_only_does_not_add():
    r = run_factor2_truth("phase_only", base_seed=20261011, reps=600)
    assert r["label"] != "LAST_FAST_SEMANTIC_ADDS_P0D"


def test_nc2_coarse_sufficient_does_not_add():
    r = run_factor2_truth("coarse_sufficient", base_seed=20261012, reps=600)
    assert r["label"] != "LAST_FAST_SEMANTIC_ADDS_P0D"


def test_nc2b_latent_regime_absorbed_by_native_activity():
    r = run_factor2_truth("latent_regime", base_seed=20261013, reps=600)
    assert r["label"] != "LAST_FAST_SEMANTIC_ADDS_P0D"


def test_nc3_factor2_semantic_recency_is_recovered():
    r = run_factor2_truth("semantic_recency", base_seed=20261014, reps=600)
    assert r["label"] == "LAST_FAST_SEMANTIC_ADDS_P0D"


def test_nc4_ordered_path_is_recovered():
    r = run_p60_ordered_truth(base_seed=20261015, reps=600)
    assert r["label"] == "ORDERED_SEMANTIC_PATH_ADDS_P0D"


def test_nc5_true_order_exceeds_order_destroyed_permutations():
    r = run_order_specificity(base_seed=20261015, permutations=40)
    assert r["passes"]
