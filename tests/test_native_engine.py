import math
import numpy as np

from market_chi import EngineConfig, analyze_series, chi_from_discrete_poles


def _simulate_ar(phi, n=4000, sigma=1.0, seed=0):
    rng = np.random.default_rng(seed)
    p = len(phi)
    x = np.zeros(n + 500, dtype=float)
    eps = rng.normal(0.0, sigma, len(x))
    for t in range(p, len(x)):
        x[t] = sum(phi[j] * x[t-j-1] for j in range(p)) + eps[t]
    return x[500:]


def _phi_from_discrete_roots(z1, z2):
    return [float(np.real(z1 + z2)), float(np.real(-z1 * z2))]


def test_chi_complex_poles_known_truth():
    lam = complex(-0.05, 0.20)
    z1 = np.exp(lam); z2 = np.exp(np.conj(lam))
    out = chi_from_discrete_poles([z1, z2])
    expected = 0.05 / math.sqrt(0.05**2 + 0.20**2)
    assert out.admitted and out.regime == "underdamped"
    assert abs(out.chi - expected) < 1e-10


def test_chi_real_poles_known_truth():
    lam1, lam2 = -0.10, -0.40
    z1, z2 = np.exp(lam1), np.exp(lam2)
    out = chi_from_discrete_poles([z1, z2])
    expected = -((lam1 + lam2) / (2 * math.sqrt(lam1 * lam2)))
    assert out.admitted and out.regime == "overdamped"
    assert abs(out.chi - expected) < 1e-10


def test_white_noise_refuses_chi():
    rng = np.random.default_rng(1)
    out = analyze_series(rng.normal(size=3000))
    assert out.chi_status == "REFUSED"
    assert out.model_family in {"AR0", "AR1"}


def test_ar1_refuses_chi():
    out = analyze_series(_simulate_ar([0.80], seed=2))
    assert out.chi_status == "REFUSED"
    assert out.model_family == "AR1"


def test_complex_ar2_admits_chi_and_recovers_value():
    lam = complex(-0.05, 0.20)
    z1, z2 = np.exp(lam), np.exp(np.conj(lam))
    out = analyze_series(_simulate_ar(_phi_from_discrete_roots(z1, z2), n=8000, seed=3), EngineConfig(min_ar2_bic_gain=6.0))
    expected = 0.05 / math.sqrt(0.05**2 + 0.20**2)
    assert out.chi_status == "ADMITTED" and out.chi_regime == "underdamped"
    assert abs(out.chi - expected) < 0.06


def test_real_ar2_admits_overdamped_chi():
    lam1, lam2 = -0.10, -0.40
    z1, z2 = np.exp(lam1), np.exp(lam2)
    out = analyze_series(_simulate_ar(_phi_from_discrete_roots(z1, z2), n=8000, seed=4), EngineConfig(min_ar2_bic_gain=6.0))
    expected = -((lam1 + lam2) / (2 * math.sqrt(lam1 * lam2)))
    assert out.chi_status == "ADMITTED" and out.chi_regime == "overdamped"
    assert abs(out.chi - expected) < 0.12
