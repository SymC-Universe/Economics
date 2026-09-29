import numpy as np

from market_chi.q039_nc7_v04 import (
    audit_timing,
    carry_forward_isotropic_world,
    qualify_synthetic_timing_fixture,
    world_seed,
)


def test_nc7_preserves_exact_update_timing_and_no_backfill():
    u = np.array([0, 0, 1, 0, 0, 1, 0, 1], dtype=bool)
    x = carry_forward_isotropic_world(u, seed=123)
    a = audit_timing(u, x)
    assert a.prefirst_all_nan
    assert a.nonupdate_state_changes == 0
    assert a.update_state_changes == 2
    assert a.finite_after_first


def test_nc7_is_deterministic_per_world_and_distinct_across_worlds():
    u = np.array([1, 0, 1, 0, 1], dtype=bool)
    s0 = world_seed(0)
    s1 = world_seed(1)
    assert s0 != s1
    a = carry_forward_isotropic_world(u, seed=s0)
    b = carry_forward_isotropic_world(u, seed=s0)
    c = carry_forward_isotropic_world(u, seed=s1)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_nc7_synthetic_timing_preflight_passes_without_real_data():
    r = qualify_synthetic_timing_fixture(worlds=200)
    assert r["disposition"] == "NC7_IMPLEMENTATION_PREFLIGHT_PASS"
    assert r["real_data_used"] is False
    assert r["scientific_nc7_executed"] is False
