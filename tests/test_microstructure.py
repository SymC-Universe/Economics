import csv
import gzip
from pathlib import Path

from market_chi.microstructure import aggregate_mbp10_csv, EXPECTED_MBP10_COLUMNS


def _row(ts, iid, symbol, action="M", side="B", flags=0, trade_size=0, bid0=20000000000000, ask0=20000250000000):
    r = {c: "0" for c in EXPECTED_MBP10_COLUMNS}
    r.update({
        "ts_recv": str(ts + 1000), "ts_event": str(ts), "rtype": "10",
        "publisher_id": "1", "instrument_id": str(iid), "action": action,
        "side": side, "depth": "0", "price": str(bid0), "size": str(trade_size),
        "flags": str(flags), "ts_in_delta": "100", "sequence": str(ts % 100000),
        "symbol": symbol,
    })
    for i in range(10):
        r[f"bid_px_{i:02d}"] = str(bid0 - i * 250000000)
        r[f"ask_px_{i:02d}"] = str(ask0 + i * 250000000)
        r[f"bid_sz_{i:02d}"] = str(10 + i)
        r[f"ask_sz_{i:02d}"] = str(6 + i)
        r[f"bid_ct_{i:02d}"] = "2"
        r[f"ask_ct_{i:02d}"] = "1"
    return r


def test_first_pass_scales_prices_segments_instruments_and_excludes_snapshot_flow(tmp_path: Path):
    src = tmp_path / "x.mbp-10.csv"
    rows = [
        _row(1_000_000_100, 11, "MNQM6", action="A", side="B", flags=32),
        _row(1_100_000_100, 11, "MNQM6", action="T", side="B", trade_size=4),
        _row(1_200_000_100, 11, "MNQM6", action="T", side="A", trade_size=1),
        _row(2_100_000_100, 22, "MNQU6", action="M", side="A"),
    ]
    with src.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(EXPECTED_MBP10_COLUMNS))
        w.writeheader()
        w.writerows(rows)
    out = tmp_path / "features.csv.gz"
    summary = tmp_path / "summary.json"
    s = aggregate_mbp10_csv(src, out, summary, interval_ms=1000)
    assert s["rows_read"] == 4
    assert s["bins_written"] == 2
    assert s["instrument_ids"] == [11, 22]
    assert s["multiple_instruments_detected"] is True
    assert s["snapshot_rows"] == 1
    with gzip.open(out, "rt", encoding="utf-8", newline="") as f:
        data = list(csv.DictReader(f))
    first = data[0]
    assert abs(float(first["mid_last"]) - 20000.125) < 1e-12
    assert abs(float(first["spread_last"]) - 0.25) < 1e-12
    assert int(first["trade_volume"]) == 5
    assert int(first["signed_trade_volume"]) == 3
    assert int(first["action_A_count"]) == 0
    assert int(first["snapshot_rows"]) == 1
