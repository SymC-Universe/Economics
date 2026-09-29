from __future__ import annotations

import numpy as np

from market_chi.q039_blocks_v04 import (
    SESSION_SECONDS,
    build_scale_blocks,
    coarse_native_N,
    factor2_models,
    factor5_models,
    session_phase_features,
)


NS = 1_000_000_000


def _dense():
    n = SESSION_SECONDS
    depth = np.tile(np.arange(1, 21, dtype=float), (n, 1))
    return {
        "times_ns": np.arange(n, dtype=np.int64) * NS,
        "depth20_log1p": np.log1p(depth),
        "event_rows": np.ones(n),
        "trade_volume": np.full(n, 2.0),
        "signed_trade_volume": np.where(np.arange(n) % 2 == 0, 1.0, -1.0),
        "spread": np.full(n, 0.25),
        "microprice_offset": np.full(n, 0.01),
        "l10_imbalance": np.full(n, -0.1),
        "staleness_age_s": np.zeros(n),
        "l10_update_indicator": np.ones(n),
    }


def test_fixed_scale_block_aggregation_and_native_predictor_dimension():
    d = _dense()
    b30 = build_scale_blocks(d, scale_seconds=30, session_start_ns=0)
    assert len(b30) == SESSION_SECONDS // 30
    assert b30[0].status == "COMPLETE"
    assert b30[0].valid_state_seconds == 30
    assert b30[0].log_event_rows == np.log1p(30)
    assert b30[0].log_trade_volume == np.log1p(60)
    assert b30[0].l10_update_fraction == 1.0
    N = coarse_native_N(b30[1], b30[0])
    assert N.shape == (17,)


def test_prefirst_block_is_refused_without_invented_coverage_threshold():
    d = _dense()
    d["depth20_log1p"][:20] = np.nan
    d["staleness_age_s"][:20] = np.nan
    d["spread"][:20] = np.nan
    d["microprice_offset"][:20] = np.nan
    d["l10_imbalance"][:20] = np.nan
    d["l10_update_indicator"][:20] = 0

    b15 = build_scale_blocks(d, scale_seconds=15, session_start_ns=0)
    assert b15[0].status == "REFUSED_NO_VALID_STATE_YET"
    assert b15[1].status == "COMPLETE"
    assert b15[1].valid_state_seconds == 10


def test_factor2_dimensions_and_semantic_delta():
    d = _dense()
    b15 = build_scale_blocks(d, scale_seconds=15, session_start_ns=0)
    b30 = build_scale_blocks(d, scale_seconds=30, session_start_ns=0)
    A2, F2 = factor2_models(b30[1], b30[0], [b15[2], b15[3]])
    assert A2.shape == (22,)
    assert F2.shape == (24,)
    assert np.allclose(F2[-2:], [0.0, 0.0])


def test_factor5_dimensions():
    d = _dense()
    b60 = build_scale_blocks(d, scale_seconds=60, session_start_ns=0)
    b300 = build_scale_blocks(d, scale_seconds=300, session_start_ns=0)
    A, L, U, S = factor5_models(
        b300[1], b300[0],
        [b60[i] for i in range(5, 10)],
    )
    assert A.shape == (23,)
    assert L.shape == (25,)
    assert U.shape == (27,)
    assert S.shape == (29,)


def test_phase_features_are_literal_session_phase():
    p0 = session_phase_features(0, 60)
    assert np.allclose(p0, [0.0, 1.0, 0.0, 1.0])
    p1 = session_phase_features(1, 60)
    assert not np.allclose(p0, p1)
