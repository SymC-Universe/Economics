"""Streaming Databento MBP-10 feature extraction for SymC market research.

This module deliberately does not compute lowercase χ. It converts native
market microstructure into time-binned state variables that can later enter
modal/vector and conglomerate analyses. χ is only evaluated downstream when
an admitted dynamical factor licenses it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

PRICE_SCALE = 1e-9
UNDEF_PRICE = 9223372036854775807
LEVELS = 10
F_LAST = 128
F_SNAPSHOT = 32
F_MBP = 16
F_BAD_TS_RECV = 8
F_MAYBE_BAD_BOOK = 4

BASE_COLUMNS = (
    "ts_recv", "ts_event", "rtype", "publisher_id", "instrument_id",
    "action", "side", "depth", "price", "size", "flags",
    "ts_in_delta", "sequence", "symbol",
)

LEVEL_COLUMNS = tuple(
    name
    for i in range(LEVELS)
    for name in (
        f"bid_px_{i:02d}", f"ask_px_{i:02d}",
        f"bid_sz_{i:02d}", f"ask_sz_{i:02d}",
        f"bid_ct_{i:02d}", f"ask_ct_{i:02d}",
    )
)
EXPECTED_MBP10_COLUMNS = BASE_COLUMNS[:-1] + LEVEL_COLUMNS + ("symbol",)


def sha256_file(path: str | Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def ns_to_iso(ns: int | None) -> str | None:
    if ns is None:
        return None
    sec, rem = divmod(int(ns), 1_000_000_000)
    dt = datetime.fromtimestamp(sec, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{rem:09d}Z"


def _to_int(value: str | None, default: int = 0) -> int:
    if value is None or value == "":
        return default
    return int(value)


def _valid_raw_price(raw: int) -> bool:
    return raw != UNDEF_PRICE and raw > 0


def _scaled_price(raw: float | int | None) -> float:
    if raw is None or not math.isfinite(float(raw)):
        return math.nan
    if int(raw) == UNDEF_PRICE or float(raw) <= 0:
        return math.nan
    return float(raw) * PRICE_SCALE


def validate_header(fieldnames: Iterable[str] | None) -> None:
    if fieldnames is None:
        raise ValueError("CSV has no header")
    got = tuple(fieldnames)
    missing = [c for c in EXPECTED_MBP10_COLUMNS if c not in got]
    if missing:
        raise ValueError("MBP-10 data contract mismatch; missing columns: " + ", ".join(missing))


@dataclass
class BinAccumulator:
    bin_ns: int
    instrument_id: int
    symbol: str
    rows: int = 0
    valid_book_rows: int = 0
    invalid_top_rows: int = 0
    bad_book_rows: int = 0
    snapshot_rows: int = 0
    bad_ts_recv_rows: int = 0
    first_ts_event: int | None = None
    last_ts_event: int | None = None
    first_ts_recv: int | None = None
    last_ts_recv: int | None = None
    first_sequence: int | None = None
    last_sequence: int | None = None
    mid_sum_raw: float = 0.0
    spread_sum_raw: float = 0.0
    l1_imbalance_sum: float = 0.0
    l10_imbalance_sum: float = 0.0
    micro_offset_sum_raw: float = 0.0
    mid_last_raw: float = math.nan
    spread_last_raw: float = math.nan
    l1_imbalance_last: float = math.nan
    l10_imbalance_last: float = math.nan
    micro_offset_last_raw: float = math.nan
    trade_count: int = 0
    buy_trade_volume: int = 0
    sell_trade_volume: int = 0
    unknown_trade_volume: int = 0
    action_counts: dict[str, int] = field(default_factory=lambda: {k: 0 for k in "AMCRTFN"})
    side_counts: dict[str, int] = field(default_factory=lambda: {k: 0 for k in ("A", "B", "N")})
    bid_sz_sum: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    ask_sz_sum: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    bid_ct_sum: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    ask_ct_sum: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    bid_dist_sum_raw: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    ask_dist_sum_raw: list[float] = field(default_factory=lambda: [0.0] * LEVELS)
    bid_dist_n: list[int] = field(default_factory=lambda: [0] * LEVELS)
    ask_dist_n: list[int] = field(default_factory=lambda: [0] * LEVELS)
    bid_sz_last: list[int] = field(default_factory=lambda: [0] * LEVELS)
    ask_sz_last: list[int] = field(default_factory=lambda: [0] * LEVELS)
    bid_ct_last: list[int] = field(default_factory=lambda: [0] * LEVELS)
    ask_ct_last: list[int] = field(default_factory=lambda: [0] * LEVELS)

    def add(self, row: dict[str, str]) -> None:
        ts_event = _to_int(row.get("ts_event"))
        ts_recv = _to_int(row.get("ts_recv"))
        sequence = _to_int(row.get("sequence"))
        flags = _to_int(row.get("flags"))
        action = (row.get("action") or "N").strip() or "N"
        side = (row.get("side") or "N").strip() or "N"

        self.rows += 1
        self.first_ts_event = ts_event if self.first_ts_event is None else min(self.first_ts_event, ts_event)
        self.last_ts_event = ts_event if self.last_ts_event is None else max(self.last_ts_event, ts_event)
        self.first_ts_recv = ts_recv if self.first_ts_recv is None else min(self.first_ts_recv, ts_recv)
        self.last_ts_recv = ts_recv if self.last_ts_recv is None else max(self.last_ts_recv, ts_recv)
        self.first_sequence = sequence if self.first_sequence is None else min(self.first_sequence, sequence)
        self.last_sequence = sequence if self.last_sequence is None else max(self.last_sequence, sequence)

        is_snapshot = bool(flags & F_SNAPSHOT)
        is_bad_book = bool(flags & F_MAYBE_BAD_BOOK)
        if is_snapshot:
            self.snapshot_rows += 1
        if flags & F_BAD_TS_RECV:
            self.bad_ts_recv_rows += 1
        if is_bad_book:
            self.bad_book_rows += 1

        # Synthetic snapshot actions initialize state but are not endogenous flow.
        if not is_snapshot:
            self.action_counts[action] = self.action_counts.get(action, 0) + 1
            self.side_counts[side] = self.side_counts.get(side, 0) + 1

        if action == "T" and not is_snapshot:
            size = _to_int(row.get("size"))
            self.trade_count += 1
            if side == "B":
                self.buy_trade_volume += size
            elif side == "A":
                self.sell_trade_volume += size
            else:
                self.unknown_trade_volume += size

        bid_raw = [_to_int(row.get(f"bid_px_{i:02d}"), UNDEF_PRICE) for i in range(LEVELS)]
        ask_raw = [_to_int(row.get(f"ask_px_{i:02d}"), UNDEF_PRICE) for i in range(LEVELS)]
        bid_sz = [_to_int(row.get(f"bid_sz_{i:02d}")) for i in range(LEVELS)]
        ask_sz = [_to_int(row.get(f"ask_sz_{i:02d}")) for i in range(LEVELS)]
        bid_ct = [_to_int(row.get(f"bid_ct_{i:02d}")) for i in range(LEVELS)]
        ask_ct = [_to_int(row.get(f"ask_ct_{i:02d}")) for i in range(LEVELS)]

        top_valid = _valid_raw_price(bid_raw[0]) and _valid_raw_price(ask_raw[0]) and ask_raw[0] > bid_raw[0]
        if (not top_valid) or is_bad_book:
            self.invalid_top_rows += int(not top_valid)
            return

        self.valid_book_rows += 1
        mid_raw = (bid_raw[0] + ask_raw[0]) / 2.0
        spread_raw = float(ask_raw[0] - bid_raw[0])
        l1_total = bid_sz[0] + ask_sz[0]
        l1_imb = (bid_sz[0] - ask_sz[0]) / l1_total if l1_total > 0 else 0.0
        b10 = sum(bid_sz)
        a10 = sum(ask_sz)
        l10_total = b10 + a10
        l10_imb = (b10 - a10) / l10_total if l10_total > 0 else 0.0
        if l1_total > 0:
            micro_raw = (ask_raw[0] * bid_sz[0] + bid_raw[0] * ask_sz[0]) / l1_total
            micro_offset_raw = micro_raw - mid_raw
        else:
            micro_offset_raw = 0.0

        self.mid_sum_raw += mid_raw
        self.spread_sum_raw += spread_raw
        self.l1_imbalance_sum += l1_imb
        self.l10_imbalance_sum += l10_imb
        self.micro_offset_sum_raw += micro_offset_raw
        self.mid_last_raw = mid_raw
        self.spread_last_raw = spread_raw
        self.l1_imbalance_last = l1_imb
        self.l10_imbalance_last = l10_imb
        self.micro_offset_last_raw = micro_offset_raw

        for i in range(LEVELS):
            self.bid_sz_sum[i] += bid_sz[i]
            self.ask_sz_sum[i] += ask_sz[i]
            self.bid_ct_sum[i] += bid_ct[i]
            self.ask_ct_sum[i] += ask_ct[i]
            self.bid_sz_last[i] = bid_sz[i]
            self.ask_sz_last[i] = ask_sz[i]
            self.bid_ct_last[i] = bid_ct[i]
            self.ask_ct_last[i] = ask_ct[i]
            if _valid_raw_price(bid_raw[i]):
                self.bid_dist_sum_raw[i] += mid_raw - bid_raw[i]
                self.bid_dist_n[i] += 1
            if _valid_raw_price(ask_raw[i]):
                self.ask_dist_sum_raw[i] += ask_raw[i] - mid_raw
                self.ask_dist_n[i] += 1

    def as_row(self) -> dict[str, object]:
        n = self.valid_book_rows
        trade_volume = self.buy_trade_volume + self.sell_trade_volume + self.unknown_trade_volume
        signed = self.buy_trade_volume - self.sell_trade_volume
        out: dict[str, object] = {
            "bin_start_ns": self.bin_ns,
            "bin_start_utc": ns_to_iso(self.bin_ns),
            "instrument_id": self.instrument_id,
            "symbol": self.symbol,
            "event_rows": self.rows,
            "valid_book_rows": n,
            "invalid_top_rows": self.invalid_top_rows,
            "bad_book_rows": self.bad_book_rows,
            "snapshot_rows": self.snapshot_rows,
            "bad_ts_recv_rows": self.bad_ts_recv_rows,
            "first_ts_event": self.first_ts_event,
            "last_ts_event": self.last_ts_event,
            "first_ts_recv": self.first_ts_recv,
            "last_ts_recv": self.last_ts_recv,
            "first_sequence": self.first_sequence,
            "last_sequence": self.last_sequence,
            "mid_mean": _scaled_price(self.mid_sum_raw / n) if n else math.nan,
            "mid_last": _scaled_price(self.mid_last_raw) if n else math.nan,
            "spread_mean": _scaled_price(self.spread_sum_raw / n) if n else math.nan,
            "spread_last": _scaled_price(self.spread_last_raw) if n else math.nan,
            "l1_imbalance_mean": self.l1_imbalance_sum / n if n else math.nan,
            "l1_imbalance_last": self.l1_imbalance_last if n else math.nan,
            "l10_imbalance_mean": self.l10_imbalance_sum / n if n else math.nan,
            "l10_imbalance_last": self.l10_imbalance_last if n else math.nan,
            "microprice_offset_mean": _scaled_price(self.micro_offset_sum_raw / n) if n else math.nan,
            "microprice_offset_last": _scaled_price(self.micro_offset_last_raw) if n else math.nan,
            "trade_count": self.trade_count,
            "trade_volume": trade_volume,
            "buy_trade_volume": self.buy_trade_volume,
            "sell_trade_volume": self.sell_trade_volume,
            "unknown_trade_volume": self.unknown_trade_volume,
            "signed_trade_volume": signed,
            "trade_imbalance": signed / trade_volume if trade_volume else 0.0,
        }
        for action, count in sorted(self.action_counts.items()):
            out[f"action_{action}_count"] = count
        for side, count in sorted(self.side_counts.items()):
            out[f"side_{side}_count"] = count
        for i in range(LEVELS):
            suffix = f"{i:02d}"
            out[f"bid_sz_{suffix}_mean"] = self.bid_sz_sum[i] / n if n else math.nan
            out[f"ask_sz_{suffix}_mean"] = self.ask_sz_sum[i] / n if n else math.nan
            out[f"bid_ct_{suffix}_mean"] = self.bid_ct_sum[i] / n if n else math.nan
            out[f"ask_ct_{suffix}_mean"] = self.ask_ct_sum[i] / n if n else math.nan
            out[f"bid_sz_{suffix}_last"] = self.bid_sz_last[i] if n else 0
            out[f"ask_sz_{suffix}_last"] = self.ask_sz_last[i] if n else 0
            out[f"bid_ct_{suffix}_last"] = self.bid_ct_last[i] if n else 0
            out[f"ask_ct_{suffix}_last"] = self.ask_ct_last[i] if n else 0
            out[f"bid_dist_{suffix}_mean"] = (
                _scaled_price(self.bid_dist_sum_raw[i] / self.bid_dist_n[i]) if self.bid_dist_n[i] else math.nan
            )
            out[f"ask_dist_{suffix}_mean"] = (
                _scaled_price(self.ask_dist_sum_raw[i] / self.ask_dist_n[i]) if self.ask_dist_n[i] else math.nan
            )
        return out


def aggregate_mbp10_csv(
    input_csv: str | Path,
    output_csv_gz: str | Path,
    summary_json: str | Path,
    interval_ms: int = 1000,
) -> dict[str, object]:
    """Aggregate one uncompressed Databento MBP-10 CSV without loading it into RAM.

    Bins are keyed by event time, actual instrument_id, and mapped symbol. This
    explicitly prevents continuous-contract rollovers from being treated as one
    physical price process.
    """
    input_csv = Path(input_csv)
    output_csv_gz = Path(output_csv_gz)
    summary_json = Path(summary_json)
    if input_csv.suffix.lower() != ".csv":
        raise ValueError("First-pass extractor intentionally accepts uncompressed .csv only")
    if interval_ms <= 0:
        raise ValueError("interval_ms must be positive")
    interval_ns = interval_ms * 1_000_000
    output_csv_gz.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)

    source_hash = sha256_file(input_csv)
    accumulators: dict[tuple[int, int, str], BinAccumulator] = {}
    rows = 0
    first_event: int | None = None
    last_event: int | None = None
    prior_event: int | None = None
    out_of_order = 0
    ids: set[int] = set()
    symbols: set[str] = set()
    action_counts: dict[str, int] = {}
    side_counts: dict[str, int] = {}
    snapshot_rows = 0
    bad_book_rows = 0
    bad_ts_recv_rows = 0

    with input_csv.open("r", encoding="utf-8", newline="") as src:
        reader = csv.DictReader(src)
        validate_header(reader.fieldnames)
        for row in reader:
            rows += 1
            ts_event = _to_int(row.get("ts_event"))
            instrument_id = _to_int(row.get("instrument_id"))
            symbol = (row.get("symbol") or "").strip()
            action = (row.get("action") or "N").strip() or "N"
            side = (row.get("side") or "N").strip() or "N"
            flags = _to_int(row.get("flags"))
            first_event = ts_event if first_event is None else min(first_event, ts_event)
            last_event = ts_event if last_event is None else max(last_event, ts_event)
            if prior_event is not None and ts_event < prior_event:
                out_of_order += 1
            prior_event = ts_event
            ids.add(instrument_id)
            symbols.add(symbol)
            action_counts[action] = action_counts.get(action, 0) + 1
            side_counts[side] = side_counts.get(side, 0) + 1
            snapshot_rows += int(bool(flags & F_SNAPSHOT))
            bad_book_rows += int(bool(flags & F_MAYBE_BAD_BOOK))
            bad_ts_recv_rows += int(bool(flags & F_BAD_TS_RECV))

            bin_ns = (ts_event // interval_ns) * interval_ns
            key = (bin_ns, instrument_id, symbol)
            acc = accumulators.get(key)
            if acc is None:
                acc = BinAccumulator(bin_ns=bin_ns, instrument_id=instrument_id, symbol=symbol)
                accumulators[key] = acc
            acc.add(row)

    rows_out = [acc.as_row() for _, acc in sorted(accumulators.items(), key=lambda kv: kv[0])]
    if not rows_out:
        raise ValueError("No records were read")
    fieldnames = list(rows_out[0].keys())
    with gzip.open(output_csv_gz, "wt", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    output_hash = sha256_file(output_csv_gz)
    summary: dict[str, object] = {
        "schema_version": "mnq-mbp10-first-pass-v1",
        "source_file": str(input_csv),
        "source_sha256": source_hash,
        "output_file": str(output_csv_gz),
        "output_sha256": output_hash,
        "price_encoding": "Databento fixed precision int64; physical_price = raw * 1e-9",
        "time_basis": "ts_event (nanoseconds since UNIX epoch, UTC)",
        "bin_interval_ms": interval_ms,
        "rows_read": rows,
        "bins_written": len(rows_out),
        "first_ts_event": first_event,
        "first_ts_event_utc": ns_to_iso(first_event),
        "last_ts_event": last_event,
        "last_ts_event_utc": ns_to_iso(last_event),
        "out_of_order_ts_event_rows": out_of_order,
        "instrument_ids": sorted(ids),
        "symbols": sorted(symbols),
        "multiple_instruments_detected": len(ids) > 1,
        "multiple_symbols_detected": len(symbols) > 1,
        "action_counts_all_rows": dict(sorted(action_counts.items())),
        "side_counts_all_rows": dict(sorted(side_counts.items())),
        "snapshot_rows": snapshot_rows,
        "bad_book_flag_rows": bad_book_rows,
        "bad_ts_recv_flag_rows": bad_ts_recv_rows,
        "notes": [
            "Synthetic snapshot rows contribute to book-state features but are excluded from endogenous action/side flow counts.",
            "Rows carrying F_MAYBE_BAD_BOOK are excluded from book-state feature means.",
            "Continuous-contract observations are segmented by instrument_id and mapped symbol before dynamics are analyzed.",
            "No lowercase chi is computed by this extraction stage.",
        ],
    }
    with summary_json.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return summary
