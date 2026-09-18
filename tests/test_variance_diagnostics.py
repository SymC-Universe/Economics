import numpy as np

from market_chi.models import fit_ar
from market_chi.variance_diagnostics import ar_residuals, variance_structure_diagnostic


def _garch(n=5000, seed=2):
    rng = np.random.default_rng(seed)
    omega, alpha, beta = 0.05, 0.10, 0.88
    x = np.zeros(n + 300)
    h = np.ones(n + 300) * omega / (1 - alpha - beta)
    z = rng.normal(size=n + 300)
    for t in range(1, len(x)):
        x[t] = np.sqrt(max(h[t - 1], 1e-12)) * z[t]
        h[t] = omega + alpha * x[t] ** 2 + beta * h[t - 1]
    return x[300:]


def test_ar_residual_reconstruction_matches_fit_rss():
    rng = np.random.default_rng(4)
    x = rng.normal(size=1000)
    fit = fit_ar(x, 2)
    e = ar_residuals(x, fit)
    assert abs(float(np.dot(e, e)) - fit.rss) < 1e-8


def test_garch_has_more_squared_residual_structure_than_white_known_truth():
    rng = np.random.default_rng(5)
    white = rng.normal(size=5000)
    wfit = fit_ar(white, 0)
    g = _garch()
    gfit = fit_ar(g, 0)
    wd = variance_structure_diagnostic(ar_residuals(white, wfit), max_lag=20)
    gd = variance_structure_diagnostic(ar_residuals(g, gfit), max_lag=20)
    assert wd.status == gd.status == "COMPLETE"
    assert gd.squared_residual_acf_energy > wd.squared_residual_acf_energy * 5
    assert gd.max_abs_squared_residual_acf > wd.max_abs_squared_residual_acf * 2


def test_short_input_refuses():
    out = variance_structure_diagnostic(np.arange(12.0), max_lag=10)
    assert out.status == "REFUSED_INPUT"
