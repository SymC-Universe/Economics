import numpy as np

from market_chi.pole_stability import blockwise_pole_stability, pair_distance


def _ar2(n=8000, seed=3):
    rng = np.random.default_rng(seed)
    lam = -0.05 + 0.20j
    z = np.exp(lam)
    phi1, phi2 = 2 * z.real, -(abs(z) ** 2)
    x = np.zeros(n + 500)
    e = rng.normal(size=n + 500)
    for t in range(2, len(x)):
        x[t] = phi1 * x[t - 1] + phi2 * x[t - 2] + e[t]
    return x[500:]


def test_pair_distance_is_permutation_invariant():
    a = [0.8 + 0.2j, 0.8 - 0.2j]
    b = [0.8 - 0.2j, 0.8 + 0.2j]
    assert pair_distance(a, b) < 1e-12


def test_strong_ar2_repeats_across_blocks():
    out = blockwise_pole_stability(_ar2(), blocks=4, min_ar2_bic_gain=6.0)
    assert out.status == "COMPLETE"
    assert out.full_pole_class == "complex_conjugate"
    assert out.block_pole_class_agreement == 1.0
    assert out.block_ar2_support_fraction >= 0.75
    assert out.median_pole_distance < 0.12


def test_white_noise_does_not_gain_block_support():
    rng = np.random.default_rng(11)
    out = blockwise_pole_stability(rng.normal(size=8000), blocks=4, min_ar2_bic_gain=6.0)
    assert out.status == "COMPLETE"
    assert out.block_ar2_support_fraction <= 0.25


def test_too_short_refuses():
    out = blockwise_pole_stability(np.arange(80.0), blocks=4)
    assert out.status == "REFUSED_INSUFFICIENT_DATA"
