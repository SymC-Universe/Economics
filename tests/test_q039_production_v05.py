import numpy as np

from market_chi.q039_production_v05 import (
    nc7_day_seed,
    _nc7_dense,
)


def test_nc7_world_day_streams_are_deterministic_and_unique():
    seeds = [nc7_day_seed(w, d) for w in range(4) for d in range(5)]
    assert len(seeds) == len(set(seeds))
    assert nc7_day_seed(0, 0) == nc7_day_seed(0, 0)


def test_nc7_dense_preserves_timing_context_and_replaces_size_semantics():
    n = 12
    real = {
        "times_ns": np.arange(n, dtype=np.int64) * 1_000_000_000,
        "l10_update_indicator": np.array([0,1,0,0,1,0,0,1,0,0,0,1], dtype=float),
        "staleness_age_s": np.array([np.nan,0,1,2,0,1,2,0,1,2,3,0], dtype=float),
        "event_rows": np.arange(n, dtype=float),
        "trade_volume": np.arange(n, dtype=float) + 2,
        "signed_trade_volume": np.linspace(-2,2,n),
        "spread": np.full(n, 0.5),
    }
    null = _nc7_dense(real, seed=123)
    assert np.array_equal(null["times_ns"], real["times_ns"])
    assert np.array_equal(null["l10_update_indicator"], real["l10_update_indicator"])
    assert np.array_equal(null["event_rows"], real["event_rows"])
    assert np.array_equal(null["spread"], real["spread"])
    assert null["depth20_log1p"].shape == (n,20)
    assert np.all(np.isnan(null["depth20_log1p"][0]))
    assert np.all(np.isfinite(null["depth20_log1p"][1:]))
    assert np.all(np.isfinite(null["microprice_offset"][1:]))
    assert np.all(np.isfinite(null["l10_imbalance"][1:]))
