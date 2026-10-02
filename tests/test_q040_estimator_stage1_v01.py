import numpy as np

from market_chi.q040_estimator_stage1_v01 import (
    detect_episodes,
    estimate_baseline,
    shrinkage_covariance,
)
from market_chi.q040_observation_episode_v01 import build_observation_episode_world


def test_baseline_estimators_are_causal_shapes():
    w = build_observation_episode_world("NC-R5", seed=20264001, scale_seconds=60)
    z = w["arrays"]["Z_observed"]
    for kind in ("K1", "K2"):
        b, v = estimate_baseline(z, kind, 20)
        assert b.shape == z.shape
        assert v.shape == z.shape
        assert np.any(np.all(np.isfinite(b), axis=1))


def test_shrinkage_covariance_is_positive_definite():
    rng = np.random.default_rng(20264002)
    x = rng.normal(size=(500, 8))
    result = shrinkage_covariance(x)
    assert result is not None
    cov, reff, cond = result
    assert np.all(np.linalg.eigvalsh(cov) > 0)
    assert reff >= 4
    assert cond < 1e6


def test_recurrent_detector_can_interrupt_active_episode():
    d = np.zeros(100)
    j = np.zeros(100)
    d[10:60] = 5.0
    j[30] = 8.0
    eps = detect_episodes(
        d, j,
        entry_threshold=4.0,
        innovation_threshold=6.0,
        return_threshold=1.0,
        sustain_k=3,
        min_sep=2,
        start=1,
        stop=90,
        horizon=80,
    )
    assert len(eps) >= 2
    assert eps[0]["outcome"] == "INTERRUPTED_BY_NEW_PERTURBATION"
    assert eps[0]["terminal"] == 30
