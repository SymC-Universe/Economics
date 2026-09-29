from __future__ import annotations

import numpy as np

from market_chi.q039_intake_v04 import dense_q039_state, semantic_state


NS = 1_000_000_000


def _row(sec: int, *, valid: int, base: float = 1.0, event_rows: int = 1):
    r = {
        "bin_start_ns": str(sec * NS),
        "valid_book_rows": str(valid),
        "event_rows": str(event_rows),
        "trade_volume": "10",
        "signed_trade_volume": "2",
        "spread_last": "0.25",
        "microprice_offset_last": "0.01",
        "l10_imbalance_last": "0.2",
    }
    for i in range(10):
        r[f"bid_sz_{i:02d}_last"] = str(base + 2 * i)
        r[f"ask_sz_{i:02d}_last"] = str(base + 2 * i + 1)
    return r


def test_no_backfill_and_exact_valid_update_timing():
    rows = [_row(2, valid=1, base=10), _row(5, valid=1, base=20)]
    d, a = dense_q039_state(rows, 0, 8 * NS)

    assert a.first_valid_update_index == 2
    assert a.prefirst_state_all_nan
    assert np.all(np.isnan(d["depth20_raw"][:2]))
    assert d["l10_update_indicator"].tolist() == [0, 0, 1, 0, 0, 1, 0, 0]
    assert np.isnan(d["staleness_age_s"][0])
    assert d["staleness_age_s"][2:8].tolist() == [0, 1, 2, 0, 1, 2]


def test_zero_valid_book_rows_do_not_overwrite_carried_state():
    good = _row(1, valid=1, base=5)
    placeholder = _row(3, valid=0, base=999)
    rows = [good, placeholder]
    d, _ = dense_q039_state(rows, 0, 5 * NS)

    assert d["l10_update_indicator"][3] == 0
    assert np.allclose(d["depth20_raw"][1], d["depth20_raw"][3])
    assert not np.any(d["depth20_raw"][3] == 999)


def test_invalid_positive_valid_row_is_ignored_not_carried_as_new_state():
    good = _row(0, valid=1, base=5)
    bad = _row(2, valid=1, base=7)
    bad["bid_sz_04_last"] = "nan"
    d, a = dense_q039_state([good, bad], 0, 4 * NS)

    assert a.bad_or_invalid_rows_ignored == 1
    assert d["l10_update_indicator"].tolist() == [1, 0, 0, 0]
    assert np.allclose(d["depth20_raw"][0], d["depth20_raw"][2])


def test_coordinate_order_is_alternating_bid_ask_and_semantics_are_finite_after_update():
    d, _ = dense_q039_state([_row(0, valid=1, base=1)], 0, 2 * NS)
    x = d["depth20_raw"][0]
    assert x[:6].tolist() == [1, 2, 3, 4, 5, 6]

    s = semantic_state(d["depth20_log1p"])
    assert s.shape == (2, 2)
    assert np.all(np.isfinite(s))
    assert s[0, 1] < 0


def test_no_updates_refuses_by_remaining_nan_not_zero_state():
    d, a = dense_q039_state([_row(1, valid=0, base=99)], 0, 3 * NS)
    assert a.first_valid_update_index is None
    assert a.prefirst_state_all_nan
    assert np.all(np.isnan(d["depth20_raw"]))
    assert np.all(np.isnan(d["staleness_age_s"]))
