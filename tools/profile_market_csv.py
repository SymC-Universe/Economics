#!/usr/bin/env python3
"""Profile one local CSV without uploading market observations.

Outputs metadata only: schema, row counts, candidate timestamp/price fields,
missingness counts, timestamp range, monotonicity, and duplicate timestamp count.
No market values are copied into the report except first/last timestamps.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import math
from pathlib import Path
from typing import Optional

TIME_NAMES = {"timestamp", "datetime", "date", "time", "ts"}
PRICE_NAMES = {"adj close", "adj_close", "close", "price", "last", "settle", "mid", "midprice"}
VOLUME_NAMES = {"volume", "vol", "size", "qty", "quantity"}


def _norm(s: str) -> str:
    return s.strip().lower().replace("-", "_")


def _parse_time(s: str) -> Optional[datetime]:
    s = s.strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def profile(path: Path, delimiter: str = ",") -> dict:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("empty CSV")
        names = [_norm(h) for h in header]
        missing = [0] * len(header)
        numeric_ok = [0] * len(header)
        rows = 0
        bad_width = 0
        time_idx = next((i for i, h in enumerate(names) if h in TIME_NAMES), None)
        price_idx = [i for i, h in enumerate(names) if h in PRICE_NAMES]
        volume_idx = [i for i, h in enumerate(names) if h in VOLUME_NAMES]
        first_time = last_time = prev_time = None
        monotone_non_decreasing = True
        duplicate_timestamps = 0

        for row in reader:
            rows += 1
            if len(row) != len(header):
                bad_width += 1; continue
            for i, value in enumerate(row):
                v = value.strip()
                if v == "":
                    missing[i] += 1; continue
                try:
                    x = float(v)
                    if math.isfinite(x): numeric_ok[i] += 1
                except ValueError:
                    pass
            if time_idx is not None:
                t = _parse_time(row[time_idx])
                if t is not None:
                    if first_time is None: first_time = t
                    last_time = t
                    if prev_time is not None:
                        if t < prev_time: monotone_non_decreasing = False
                        if t == prev_time: duplicate_timestamps += 1
                    prev_time = t

    columns = []
    for i, raw in enumerate(header):
        nonmissing = max(rows - missing[i], 0)
        columns.append({"name": raw, "normalized_name": names[i], "missing": missing[i], "numeric_fraction_nonmissing": numeric_ok[i] / nonmissing if nonmissing else 0.0})
    return {
        "path": str(path.resolve()), "bytes": path.stat().st_size, "rows": rows,
        "column_count": len(header), "bad_width_rows": bad_width, "columns": columns,
        "timestamp_column": header[time_idx] if time_idx is not None else None,
        "first_timestamp": first_time.isoformat() if first_time else None,
        "last_timestamp": last_time.isoformat() if last_time else None,
        "timestamp_monotone_non_decreasing": monotone_non_decreasing if time_idx is not None else None,
        "adjacent_duplicate_timestamps": duplicate_timestamps if time_idx is not None else None,
        "candidate_price_columns": [header[i] for i in price_idx],
        "candidate_volume_columns": [header[i] for i in volume_idx],
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("--out", default=None); ap.add_argument("--delimiter", default=",")
    args = ap.parse_args(); report = profile(Path(args.csv), delimiter=args.delimiter); text = json.dumps(report, indent=2)
    if args.out: Path(args.out).write_text(text + "\n", encoding="utf-8")
    else: print(text)


if __name__ == "__main__": main()
