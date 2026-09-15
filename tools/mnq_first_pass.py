#!/usr/bin/env python3
"""First real-data pass for the uncompressed MNQ MBP-10 development file."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from market_chi.microstructure import aggregate_mbp10_csv


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to one uncompressed Databento *.mbp-10.csv file")
    p.add_argument("--out-dir", required=True, help="Directory for small derived outputs")
    p.add_argument("--interval-ms", type=int, default=1000)
    args = p.parse_args()

    src = Path(args.input).expanduser().resolve()
    out = Path(args.out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    stem = src.name.replace(".csv", "")
    features = out / f"{stem}.{args.interval_ms}ms.features.csv.gz"
    summary = out / f"{stem}.{args.interval_ms}ms.summary.json"

    result = aggregate_mbp10_csv(src, features, summary, interval_ms=args.interval_ms)
    print("DONE")
    print(f"Rows read: {result['rows_read']}")
    print(f"Bins written: {result['bins_written']}")
    print(f"Instrument IDs: {result['instrument_ids']}")
    print(f"Symbols: {result['symbols']}")
    print(f"Summary: {summary}")
    print(f"Features: {features}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
