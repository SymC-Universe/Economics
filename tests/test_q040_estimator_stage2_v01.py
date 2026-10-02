import numpy as np

from market_chi.q040_estimator_stage2_v01 import (
    fit_competing_softmax,
    outer_world_folds,
)


def test_outer_world_folds_cover_each_world_once():
    folds = outer_world_folds(200)
    seen = []
    for tr, te in folds:
        assert len(tr) == 160
        assert len(te) == 40
        assert len(set(tr).intersection(set(te))) == 0
        seen.extend(te.tolist())
    assert sorted(seen) == list(range(200))


def test_softmax_fit_simple_competing_risk():
    rng = np.random.default_rng(20265001)
    n = 3000
    x = rng.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    e1 = np.exp(np.clip(-1.5 + 0.8 * x, -20, 20))
    e2 = np.exp(np.clip(-2.0 - 0.4 * x, -20, 20))
    den = 1 + e1 + e2
    p = np.column_stack([1/den, e1/den, e2/den])
    u = rng.random(n)
    y = np.zeros(n, dtype=int)
    y[u > p[:,0]] = 1
    y[u > p[:,0] + p[:,1]] = 2
    fit = fit_competing_softmax(X, y)
    assert fit.status == "COMPLETE"
    assert fit.beta is not None
    assert np.all(np.isfinite(fit.beta))
