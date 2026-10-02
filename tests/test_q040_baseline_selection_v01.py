import numpy as np

from market_chi.q040_baseline_selection_v01 import (
    estimate_k1,
    estimate_k2,
    normalized_baseline_error,
)


def test_k1_tracks_constant_baseline():
    z = np.tile(np.arange(8, dtype=float), (128, 1))
    update = np.ones(128, dtype=bool)
    b, v = estimate_k1(z, update, window=20, start=20)
    assert np.allclose(b[40], np.arange(8, dtype=float))
    assert np.allclose(v[40], 0.0)


def test_k2_tracks_linear_baseline():
    t = np.arange(128, dtype=float)
    z = np.column_stack([(0.1 + 0.01 * (k + 1) * t) for k in range(8)])
    update = np.ones(128, dtype=bool)
    b, v = estimate_k2(z, update, window=20, start=20)
    assert np.allclose(b[80], z[80], atol=1e-10)
    expected = np.asarray([0.01 * (k + 1) for k in range(8)])
    assert np.allclose(v[80], expected, atol=1e-10)


def test_error_is_zero_for_truth():
    x = np.zeros((10, 8))
    e = normalized_baseline_error(x, x)
    assert np.allclose(e, 0)
