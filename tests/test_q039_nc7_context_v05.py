import numpy as np

from market_chi.q039_intake_v04 import semantic_state
from market_chi.q039_nc7_context_v05 import (
    project_sizes_for_context,
    qualify_synthetic_context_fixture,
    recompute_nc7_native_context,
)


def test_projection_is_nonnegative_and_does_not_replace_semantic_path():
    x = np.array([
        [1.0, -1.0] * 10,
        [-0.5, 0.8] * 10,
    ], dtype=float)
    sem = semantic_state(x.copy())
    q = project_sizes_for_context(x)
    assert np.all(q >= 0.0)
    assert np.array_equal(sem, semantic_state(x))


def test_microprice_identity_uses_real_spread_and_synthetic_l1_sizes():
    x = np.zeros((1, 20), dtype=float)
    # q_bid = expm1(ln 3)=2; q_ask = expm1(ln 2)=1
    x[0, 0] = np.log(3.0)
    x[0, 1] = np.log(2.0)
    out = recompute_nc7_native_context(x, np.array([0.6]))
    # 0.5 * 0.6 * (2-1)/(2+1) = 0.1
    assert np.isclose(out["microprice_offset"][0], 0.1)


def test_zero_size_fallbacks_are_exact_zero():
    x = np.zeros((1, 20), dtype=float)
    out = recompute_nc7_native_context(x, np.array([0.5]))
    assert out["l10_imbalance"][0] == 0.0
    assert out["microprice_offset"][0] == 0.0


def test_prefirst_state_remains_nan():
    x = np.full((3, 20), np.nan)
    x[1:] = 0.0
    out = recompute_nc7_native_context(x, np.array([np.nan, 0.25, 0.25]))
    assert np.isnan(out["l10_imbalance"][0])
    assert np.isnan(out["microprice_offset"][0])
    assert out["l10_imbalance"][1] == 0.0


def test_context_fixture_passes_all_200_worlds_without_real_data():
    r = qualify_synthetic_context_fixture(worlds=200)
    assert r["disposition"] == "NC7_DERIVED_CONTEXT_IMPLEMENTATION_PREFLIGHT_PASS"
    assert r["real_data_used"] is False
    assert r["scientific_nc7_executed"] is False
