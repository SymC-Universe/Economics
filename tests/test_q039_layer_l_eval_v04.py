from __future__ import annotations

import numpy as np

from market_chi.q039_layer_l_eval_v04 import (
    _contiguous_block_starts,
    equal_day_noncircular_bootstrap,
    evaluate_nested_day,
)


NS = 1_000_000_000


def _obs(n=2500, p_small=4, p_large=6, seed=7):
    rng = np.random.default_rng(seed)
    # Columns 0..3 are treated as cyclic in this fixture so no constant-scaling
    # refusal is triggered. Larger-model extra columns are genuine continuous
    # predictors.
    small = rng.normal(size=(n, p_small))
    large = np.column_stack([small, rng.normal(size=(n, p_large - p_small))])
    beta = rng.normal(size=(p_large, 2))
    y = large @ beta + rng.normal(scale=0.2, size=(n, 2))
    source = np.arange(n, dtype=np.int64) * 30 * NS
    target_end = source + 60 * NS
    return {
        "A2": small,
        "F2": large,
        "y": y,
        "source_start_ns": source,
        "target_end_ns": target_end,
        "source_block": np.arange(n, dtype=int),
    }


def test_walkforward_uses_dynamic_np_and_produces_valid_oos():
    obs = _obs()
    s, extra = evaluate_nested_day(
        obs,
        small_name="A2",
        large_name="F2",
        fine_seconds=15,
        coarse_seconds=30,
        day_start_ns=0,
        cyclic_columns=(0, 1, 2, 3),
    )
    assert s.status == "COMPLETE"
    assert s.p_max == 7
    assert s.valid_oos_hours >= 8
    assert s.point_contrast > 0
    assert s.mae_large_d < s.mae_small_d
    assert np.sum(extra["primary_mask"]) == s.n_primary_predictions


def test_constant_noncyclic_predictor_refuses_instead_of_dropping_column():
    obs = _obs()
    obs["F2"][:, -1] = 1.0
    s, extra = evaluate_nested_day(
        obs,
        small_name="A2",
        large_name="F2",
        fine_seconds=15,
        coarse_seconds=30,
        day_start_ns=0,
        cyclic_columns=(0, 1, 2, 3),
    )
    assert s.status == "INVALID_TEST_INSUFFICIENT_IDENTIFICATION"
    assert any(r["status"] == "REFUSED_REFIT" for r in extra["refits"])


def test_train_target_must_end_before_test_source():
    obs = _obs(n=2000)
    # Make target endpoints much later, reducing the eligible training set.
    obs["target_end_ns"] = obs["source_start_ns"] + 4 * 3600 * NS
    s, _ = evaluate_nested_day(
        obs,
        small_name="A2",
        large_name="F2",
        fine_seconds=15,
        coarse_seconds=30,
        day_start_ns=0,
        cyclic_columns=(0, 1, 2, 3),
    )
    # Either complete after enough delayed history or refuse, but it must never
    # use future target endpoints. With this fixture, less than eight valid
    # hourly chunks remain.
    assert s.status == "INVALID_TEST_INSUFFICIENT_IDENTIFICATION"


def test_non_circular_bootstrap_uses_only_contiguous_starts():
    ids = np.array([10, 11, 12, 20, 21, 22, 23])
    starts = _contiguous_block_starts(ids, 3)
    assert starts.tolist() == [0, 3, 4]


def test_equal_day_bootstrap_is_seeded_and_equal_weighted():
    vals = [np.linspace(0.1, 0.2, 40) for _ in range(5)]
    ids = [np.arange(40) for _ in range(5)]
    a = equal_day_noncircular_bootstrap(
        vals, ids, coarse_seconds=300, block_seconds=1800,
        reps=1000, seed=20260929,
    )
    b = equal_day_noncircular_bootstrap(
        vals, ids, coarse_seconds=300, block_seconds=1800,
        reps=1000, seed=20260929,
    )
    assert a == b
    assert a["lower"] > 0
    assert a["circular"] is False
