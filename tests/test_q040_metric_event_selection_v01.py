import numpy as np

from market_chi.q040_metric_event_selection_v01 import (
    MetricFit,
    detect_episodes,
    fit_metric,
    metric_distance,
)


def test_d1_distance_finite():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(500, 8))
    fit = fit_metric(x, "D1")
    assert fit.status == "OK"
    d = metric_distance(x, fit)
    assert np.all(np.isfinite(d))


def test_d2_distance_finite_and_conditioned():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(500, 8))
    fit = fit_metric(x, "D2")
    assert fit.status == "OK"
    assert fit.effective_rank >= 4
    assert fit.condition_number < 1e6
    d = metric_distance(x, fit)
    assert np.all(np.isfinite(d))


def test_episode_detection_return_and_interrupt():
    d = np.zeros(80)
    d[10] = 5
    d[11:15] = 3
    d[15:18] = 0.2
    d[30] = 5
    d[31:35] = 3
    d[36] = 0.2
    d[37] = 5
    eps = detect_episodes(
        d,
        start=1,
        stop=len(d),
        entry_threshold=2,
        return_threshold=0.5,
        sustain=3,
        min_separation=2,
    )
    assert eps[0].outcome == "SUSTAINED_RETURN"
    assert eps[1].outcome == "INTERRUPTED_BY_NEW_PERTURBATION"
