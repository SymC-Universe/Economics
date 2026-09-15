"""Streaming Databento MBP-10 extractor v2.

Changes from v1:
- preserves signed/zero microprice offsets;
- streams chronologically instead of retaining all one-second accumulators;
- accepts .csv, .csv.gz, and .csv.zst (zstandard package required for .zst);
- retains instrument_id/symbol segmentation and snapshot/bad-book safeguards;
- does not compute lowercase χ.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Iterator, TextIO

PRICE_SCALE = 1e-9
UNDEF_PRICE = 9223372036854775807
LEVELS = 10
F_SNAPSHOT = 32
F_BAD_TS_RECV = 8
F_MAYBE_BAD_BOOK = 4

BASE_COLUMNS = (
    "ts_recv", "ts_event", "rtype", "publisher_id", "instrument_id",
    "action", "side", "depth", "price", "size", "flags",
    "ts_in_delta", "sequence", "symbol",
)
LEVEL_COLUMNS = tuple(
    name for i in range(LEVELS) for name in (
        f"bid_px_{i:02d}", f"ask_px_{i:02d}", f"bid_sz_{i:02d}",
        f"ask_sz_{i:02d}", f"bid_ct_{i:02d}", f"ask_ct_{i:02d}",
    )
)
EXPECTED_MBP10_COLUMNS = BASE_COLUMNS[:-1] + LEVEL_COLUMNS + ("symbol",)


def sha256_file(path: str | Path, block_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
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


def _scaled_positive(raw: float | int | None) -> float:
    if raw is None or not math.isfinite(float(raw)):
        return math.nan
    if int(raw) == UNDEF_PRICE or float(raw) <= 0:
        return math.nan
    return float(raw) * PRICE_SCALE


def _scaled_signed(raw: float | int | None) -> float:
    if raw is None or not math.isfinite(float(raw)):
        return math.nan
    return float(raw) * PRICE_SCALE


def validate_header(fieldnames) -> None:
    if fieldnames is None:
        raise ValueError("CSV has no header")
    missing = [c for c in EXPECTED_MBP10_COLUMNS if c not in tuple(fieldnames)]
    if missing:
        raise ValueError("MBP-10 data contract mismatch; missing columns: " + ", ".join(missing))


@contextmanager
def open_mbp10_text(path: str | Path) -> Iterator[TextIO]:
    p = Path(path)
    name = p.name.lower()
    if name.endswith(".zst"):
        try:
            import zstandard as zstd
        except ImportError as exc:
            raise RuntimeError("Reading .zst requires: python -m pip install zstandard") from exc
        raw = p.open("rb")
        reader = zstd.ZstdDecompressor().stream_reader(raw)
        text = io.TextIOWrapper(reader, encoding="utf-8", newline="")
        try:
            yield text
        finally:
            text.close()
            raw.close()
    elif name.endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8", newline="") as text:
            yield text
    else:
        with p.open("r", encoding="utf-8", newline="") as text:
            yield text


@dataclass
class BinAccumulatorV2:
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
        ts_event = _to_int(row.get("ts_event")); ts_recv = _to_int(row.get("ts_recv"))
        sequence = _to_int(row.get("sequence")); flags = _to_int(row.get("flags"))
        action = (row.get("action") or "N").strip() or "N"; side = (row.get("side") or "N").strip() or "N"
        self.rows += 1
        self.first_ts_event = ts_event if self.first_ts_event is None else min(self.first_ts_event, ts_event)
        self.last_ts_event = ts_event if self.last_ts_event is None else max(self.last_ts_event, ts_event)
        self.first_ts_recv = ts_recv if self.first_ts_recv is None else min(self.first_ts_recv, ts_recv)
        self.last_ts_recv = ts_recv if self.last_ts_recv is None else max(self.last_ts_recv, ts_recv)
        self.first_sequence = sequence if self.first_sequence is None else min(self.first_sequence, sequence)
        self.last_sequence = sequence if self.last_sequence is None else max(self.last_sequence, sequence)
        is_snapshot = bool(flags & F_SNAPSHOT); is_bad_book = bool(flags & F_MAYBE_BAD_BOOK)
        self.snapshot_rows += int(is_snapshot); self.bad_ts_recv_rows += int(bool(flags & F_BAD_TS_RECV)); self.bad_book_rows += int(is_bad_book)
        if not is_snapshot:
            self.action_counts[action] = self.action_counts.get(action, 0) + 1
            self.side_counts[side] = self.side_counts.get(side, 0) + 1
        if action == "T" and not is_snapshot:
            size = _to_int(row.get("size")); self.trade_count += 1
            if side == "B": self.buy_trade_volume += size
            elif side == "A": self.sell_trade_volume += size
            else: self.unknown_trade_volume += size
        bid_raw = [_to_int(row.get(f"bid_px_{i:02d}"), UNDEF_PRICE) for i in range(LEVELS)]
        ask_raw = [_to_int(row.get(f"ask_px_{i:02d}"), UNDEF_PRICE) for i in range(LEVELS)]
        bid_sz = [_to_int(row.get(f"bid_sz_{i:02d}")) for i in range(LEVELS)]
        ask_sz = [_to_int(row.get(f"ask_sz_{i:02d}")) for i in range(LEVELS)]
        bid_ct = [_to_int(row.get(f"bid_ct_{i:02d}")) for i in range(LEVELS)]
        ask_ct = [_to_int(row.get(f"ask_ct_{i:02d}")) for i in range(LEVELS)]
        top_valid = _valid_raw_price(bid_raw[0]) and _valid_raw_price(ask_raw[0]) and ask_raw[0] > bid_raw[0]
        if (not top_valid) or is_bad_book:
            self.invalid_top_rows += int(not top_valid); return
        self.valid_book_rows += 1
        mid_raw = (bid_raw[0] + ask_raw[0]) / 2.0; spread_raw = float(ask_raw[0] - bid_raw[0])
        l1_total = bid_sz[0] + ask_sz[0]; l1_imb = (bid_sz[0] - ask_sz[0]) / l1_total if l1_total > 0 else 0.0
        b10, a10 = sum(bid_sz), sum(ask_sz); l10_total = b10 + a10; l10_imb = (b10 - a10) / l10_total if l10_total > 0 else 0.0
        micro_offset_raw = ((ask_raw[0] * bid_sz[0] + bid_raw[0] * ask_sz[0]) / l1_total - mid_raw) if l1_total > 0 else 0.0
        self.mid_sum_raw += mid_raw; self.spread_sum_raw += spread_raw; self.l1_imbalance_sum += l1_imb; self.l10_imbalance_sum += l10_imb; self.micro_offset_sum_raw += micro_offset_raw
        self.mid_last_raw = mid_raw; self.spread_last_raw = spread_raw; self.l1_imbalance_last = l1_imb; self.l10_imbalance_last = l10_imb; self.micro_offset_last_raw = micro_offset_raw
        for i in range(LEVELS):
            self.bid_sz_sum[i] += bid_sz[i]; self.ask_sz_sum[i] += ask_sz[i]; self.bid_ct_sum[i] += bid_ct[i]; self.ask_ct_sum[i] += ask_ct[i]
            self.bid_sz_last[i] = bid_sz[i]; self.ask_sz_last[i] = ask_sz[i]; self.bid_ct_last[i] = bid_ct[i]; self.ask_ct_last[i] = ask_ct[i]
            if _valid_raw_price(bid_raw[i]): self.bid_dist_sum_raw[i] += mid_raw - bid_raw[i]; self.bid_dist_n[i] += 1
            if _valid_raw_price(ask_raw[i]): self.ask_dist_sum_raw[i] += ask_raw[i] - mid_raw; self.ask_dist_n[i] += 1

    def as_row(self) -> dict[str, object]:
        n = self.valid_book_rows; trade_volume = self.buy_trade_volume + self.sell_trade_volume + self.unknown_trade_volume; signed = self.buy_trade_volume - self.sell_trade_volume
        out = {
            "bin_start_ns": self.bin_ns, "bin_start_utc": ns_to_iso(self.bin_ns), "instrument_id": self.instrument_id, "symbol": self.symbol,
            "event_rows": self.rows, "valid_book_rows": n, "invalid_top_rows": self.invalid_top_rows, "bad_book_rows": self.bad_book_rows,
            "snapshot_rows": self.snapshot_rows, "bad_ts_recv_rows": self.bad_ts_recv_rows, "first_ts_event": self.first_ts_event,
            "last_ts_event": self.last_ts_event, "first_ts_recv": self.first_ts_recv, "last_ts_recv": self.last_ts_recv,
            "first_sequence": self.first_sequence, "last_sequence": self.last_sequence,
            "mid_mean": _scaled_positive(self.mid_sum_raw / n) if n else math.nan, "mid_last": _scaled_positive(self.mid_last_raw) if n else math.nan,
            "spread_mean": _scaled_positive(self.spread_sum_raw / n) if n else math.nan, "spread_last": _scaled_positive(self.spread_last_raw) if n else math.nan,
            "l1_imbalance_mean": self.l1_imbalance_sum / n if n else math.nan, "l1_imbalance_last": self.l1_imbalance_last if n else math.nan,
            "l10_imbalance_mean": self.l10_imbalance_sum / n if n else math.nan, "l10_imbalance_last": self.l10_imbalance_last if n else math.nan,
            "microprice_offset_mean": _scaled_signed(self.micro_offset_sum_raw / n) if n else math.nan,
            "microprice_offset_last": _scaled_signed(self.micro_offset_last_raw) if n else math.nan,
            "trade_count": self.trade_count, "trade_volume": trade_volume, "buy_trade_volume": self.buy_trade_volume,
            "sell_trade_volume": self.sell_trade_volume, "unknown_trade_volume": self.unknown_trade_volume,
            "signed_trade_volume": signed, "trade_imbalance": signed / trade_volume if trade_volume else 0.0,
        }
        for action, count in sorted(self.action_counts.items()): out[f"action_{action}_count"] = count
        for side, count in sorted(self.side_counts.items()): out[f"side_{side}_count"] = count
        for i in range(LEVELS):
            s = f"{i:02d}"; out[f"bid_sz_{s}_mean"] = self.bid_sz_sum[i] / n if n else math.nan; out[f"ask_sz_{s}_mean"] = self.ask_sz_sum[i] / n if n else math.nan
            out[f"bid_ct_{s}_mean"] = self.bid_ct_sum[i] / n if n else math.nan; out[f"ask_ct_{s}_mean"] = self.ask_ct_sum[i] / n if n else math.nan
            out[f"bid_sz_{s}_last"] = self.bid_sz_last[i] if n else 0; out[f"ask_sz_{s}_last"] = self.ask_sz_last[i] if n else 0
            out[f"bid_ct_{s}_last"] = self.bid_ct_last[i] if n else 0; out[f"ask_ct_{s}_last"] = self.ask_ct_last[i] if n else 0
            out[f"bid_dist_{s}_mean"] = _scaled_positive(self.bid_dist_sum_raw[i] / self.bid_dist_n[i]) if self.bid_dist_n[i] else math.nan
            out[f"ask_dist_{s}_mean"] = _scaled_positive(self.ask_dist_sum_raw[i] / self.ask_dist_n[i]) if self.ask_dist_n[i] else math.nan
        return out


def aggregate_mbp10_stream(input_path: str | Path, output_csv_gz: str | Path, summary_json: str | Path, interval_ms: int = 1000) -> dict[str, object]:
    src = Path(input_path); out = Path(output_csv_gz); summary_path = Path(summary_json)
    if interval_ms <= 0: raise ValueError("interval_ms must be positive")
    interval_ns = interval_ms * 1_000_000; out.parent.mkdir(parents=True, exist_ok=True); summary_path.parent.mkdir(parents=True, exist_ok=True)
    source_hash = sha256_file(src)
    rows = bins_written = out_of_order = 0; first_event = last_event = prior_event = None
    ids, symbols = set(), set(); action_counts, side_counts = {}, {}; snapshot_rows = bad_book_rows = bad_ts_recv_rows = 0
    current_bin = None; accs: dict[tuple[int, str], BinAccumulatorV2] = {}; writer = None
    with open_mbp10_text(src) as text, gzip.open(out, "wt", encoding="utf-8", newline="") as dst:
        reader = csv.DictReader(text); validate_header(reader.fieldnames)
        def flush() -> None:
            nonlocal writer, bins_written, accs
            for key in sorted(accs):
                rowout = accs[key].as_row()
                if writer is None:
                    writer = csv.DictWriter(dst, fieldnames=list(rowout.keys())); writer.writeheader()
                writer.writerow(rowout); bins_written += 1
            accs = {}
        for row in reader:
            rows += 1; ts = _to_int(row.get("ts_event")); iid = _to_int(row.get("instrument_id")); symbol = (row.get("symbol") or "").strip(); flags = _to_int(row.get("flags")); action = (row.get("action") or "N").strip() or "N"; side = (row.get("side") or "N").strip() or "N"
            if prior_event is not None and ts < prior_event: out_of_order += 1
            prior_event = ts; first_event = ts if first_event is None else min(first_event, ts); last_event = ts if last_event is None else max(last_event, ts)
            ids.add(iid); symbols.add(symbol); action_counts[action] = action_counts.get(action, 0) + 1; side_counts[side] = side_counts.get(side, 0) + 1
            snapshot_rows += int(bool(flags & F_SNAPSHOT)); bad_book_rows += int(bool(flags & F_MAYBE_BAD_BOOK)); bad_ts_recv_rows += int(bool(flags & F_BAD_TS_RECV))
            b = (ts // interval_ns) * interval_ns
            if current_bin is None: current_bin = b
            if b < current_bin: raise ValueError("Input event time is not monotone by bin; streaming extraction refused")
            if b != current_bin: flush(); current_bin = b
            key = (iid, symbol)
            if key not in accs: accs[key] = BinAccumulatorV2(b, iid, symbol)
            accs[key].add(row)
        if accs: flush()
    if rows == 0: raise ValueError("No records were read")
    summary = {
        "schema_version": "mnq-mbp10-first-pass-v2", "source_file": str(src), "source_sha256": source_hash,
        "output_file": str(out), "output_sha256": sha256_file(out), "price_encoding": "Databento fixed precision int64; physical_price = raw * 1e-9",
        "time_basis": "ts_event (nanoseconds since UNIX epoch, UTC)", "bin_interval_ms": interval_ms, "rows_read": rows, "bins_written": bins_written,
        "first_ts_event": first_event, "first_ts_event_utc": ns_to_iso(first_event), "last_ts_event": last_event, "last_ts_event_utc": ns_to_iso(last_event),
        "out_of_order_ts_event_rows": out_of_order, "instrument_ids": sorted(ids), "symbols": sorted(symbols), "multiple_instruments_detected": len(ids) > 1,
        "multiple_symbols_detected": len(symbols) > 1, "action_counts_all_rows": dict(sorted(action_counts.items())), "side_counts_all_rows": dict(sorted(side_counts.items())),
        "snapshot_rows": snapshot_rows, "bad_book_flag_rows": bad_book_rows, "bad_ts_recv_flag_rows": bad_ts_recv_rows,
        "notes": [
            "V2 preserves signed and zero microprice offsets; v1 incorrectly sent those values through a positive-price validator.",
            "Synthetic snapshot rows contribute to book-state features but are excluded from endogenous action/side flow counts.",
            "Rows carrying F_MAYBE_BAD_BOOK are excluded from book-state feature means.",
            "Continuous-contract observations are segmented by instrument_id and mapped symbol before dynamics are analyzed.",
            "Streaming extraction flushes completed event-time bins and does not retain the full raw day in memory.",
            "No lowercase chi is computed by this extraction stage.",
        ],
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
