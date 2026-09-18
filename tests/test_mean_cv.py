import numpy as np

from market_chi.mean_cv import walk_forward_mean_comparison


def _ar2(n=2500, seed=3):
    rng = np.random.default_rng(seed)
    lam = -0.05 + 0.20j
    z = np.exp(lam)
    phi1, phi2 = 2 * z.real, -(abs(z) ** 2)
    x = np.zeros(n + 300)
    e = rng.normal(size=n + 300)
    for t in range(2, len(x)):
        x[t] = phi1 * x[t - 1] + phi2 * x[t - 2] + e[t]
    return x[300:]


def test_true_ar2_has_persistent_oos_mean_advantage():
    out = walk_forward_mean_comparison(_ar2(), min_train=500, test_block=100)
    assert out.status == "COMPLETE"
    assert out.ar2_gain_vs_best_simple > 0.02
    assert out.ar2_fold_win_fraction > 0.80


def test_white_noise_does_not_show_persistent_ar2_advantage():
    rng = np.random.default_rng(8)
    out = walk_forward_mean_comparison(rng.normal(size=2500), min_train=500, test_block=100)
    assert out.status == "COMPLETE"
    assert out.ar2_gain_vs_best_simple < 0.01
    assert out.ar2_fold_win_fraction < 0.70


def test_short_series_refuses():
    out = walk_forward_mean_comparison(np.arange(100.0), min_train=80, test_block=50)
    assert out.status == "REFUSED_INSUFFICIENT_DATA"
