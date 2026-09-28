#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.lagged_hierarchy import _fit_predict, _r2
from market_chi.temporal_inheritance import summarize_fine_blocks
from market_chi.microstructure_v2 import validate_feature_gzip

DATES = ["20260527", "20260528", "20260529", "20260601", "20260602"]
FACTORS = [15, 30, 60, 300]
TARGETS = ["log_depth_capacity", "log_side_contrast"]


def _day_start_ns(day: str) -> int:
    dt = datetime.strptime(day, "%Y%m%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1_000_000_000)


def _semantic_row(row: dict[str, str]) -> tuple[float, float] | None:
    bids, asks = [], []
    try:
        for i in range(10):
            b = float(row[f"bid_sz_{i:02d}_mean"])
            a = float(row[f"ask_sz_{i:02d}_mean"])
            if not (math.isfinite(b) and math.isfinite(a) and b >= 0 and a >= 0):
                return None
            bids.append(math.log1p(b))
            asks.append(math.log1p(a))
    except (KeyError, ValueError):
        return None
    allv = bids + asks
    depth = float(np.mean(allv))
    side = float(np.mean(bids) - np.mean(asks))
    return depth, side


def load_mature_semantics(path: Path, day: str) -> dict[int, np.ndarray]:
    start = _day_start_ns(day)
    end = start + 21 * 3600 * 1_000_000_000
    out: dict[int, np.ndarray] = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            t = int(row["bin_start_ns"])
            if t < start:
                continue
            if t >= end:
                break
            sem = _semantic_row(row)
            if sem is not None:
                out[t] = np.asarray(sem, dtype=float)
    return out


def build_blocks(series: dict[int, np.ndarray], day: str, factor: int):
    start = _day_start_ns(day)
    ns = 1_000_000_000
    blocks = {}
    for b in range((21 * 3600) // factor):
        times = [start + (b * factor + j) * ns for j in range(factor)]
        if not all(t in series for t in times):
            continue
        arr = np.vstack([series[t] for t in times])
        structured, last = summarize_fine_blocks(arr, factor)
        if len(structured) != 1:
            raise RuntimeError("one complete wall-clock block should yield one summary")
        blocks[b] = {
            "structured": structured[0],
            "last": last[0],
            "coarse": arr.mean(axis=0),
        }
    return blocks


def evaluate(blocks, target_idx: int, factor: int, *, lead_blocks: int = 1,
             min_train_blocks: int = 30, test_block_size: int = 10):
    pairs = []
    for b in sorted(blocks):
        fb = b + lead_blocks
        if fb not in blocks:
            continue
        cur, fut = blocks[b], blocks[fb]
        pairs.append((b, cur["structured"], cur["last"], cur["coarse"][target_idx], fut["coarse"][target_idx]))

    if len(pairs) < min_train_blocks + test_block_size:
        return {
            "status": "REFUSED_INSUFFICIENT_BLOCKS",
            "factor_s": factor,
            "lead_blocks": lead_blocks,
            "n_pairs": len(pairs),
        }

    x_struct = np.vstack([p[1] for p in pairs])
    x_last = np.vstack([p[2] for p in pairs])
    cur_y = np.asarray([p[3] for p in pairs])
    fut_y = np.asarray([p[4] for p in pairs])
    block_ids = np.asarray([p[0] for p in pairs])

    n = len(fut_y)
    ps = np.full(n, np.nan)
    pl = np.full(n, np.nan)
    pp = np.full(n, np.nan)
    start = min_train_blocks
    while start < n:
        stop = min(n, start + test_block_size)
        ps[start:stop] = _fit_predict(x_struct[:start], fut_y[:start], x_struct[start:stop])
        pl[start:stop] = _fit_predict(x_last[:start], fut_y[:start], x_last[start:stop])
        pp[start:stop] = cur_y[start:stop]
        start = stop

    mask = np.isfinite(ps) & np.isfinite(pl) & np.isfinite(pp)
    yy, a, b, c = fut_y[mask], ps[mask], pl[mask], pp[mask]
    return {
        "status": "COMPLETE",
        "factor_s": factor,
        "lead_blocks": lead_blocks,
        "lead_seconds": factor * lead_blocks,
        "n_pairs": int(n),
        "n_test": int(mask.sum()),
        "first_test_block": int(block_ids[np.where(mask)[0][0]]) if mask.any() else None,
        "structured_r2": _r2(yy, a),
        "last_fast_r2": _r2(yy, b),
        "coarse_persistence_r2": _r2(yy, c),
        "delta_r2_vs_last": _r2(yy, a) - _r2(yy, b),
        "delta_r2_vs_persistence": _r2(yy, a) - _r2(yy, c),
        "structured_mae": float(np.mean(np.abs(yy - a))),
        "last_fast_mae": float(np.mean(np.abs(yy - b))),
        "coarse_persistence_mae": float(np.mean(np.abs(yy - c))),
    }


def locate_feature(root: Path, day: str) -> Path:
    names = [
        root / "_symc_development_sweep_v1" / "features" / f"glbx-mdp3-{day}.mbp-10.1000ms.features.v2.csv.gz",
        root / "_symc_weekday_pass_v2" / f"glbx-mdp3-{day}.mbp-10.1000ms.features.v2.csv.gz",
    ]
    for p in names:
        if p.exists() and validate_feature_gzip(p).get("valid"):
            return p
    raise FileNotFoundError(f"no valid frozen-development feature file found for {day}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dates", nargs="*", default=DATES)
    args = ap.parse_args()

    root = Path(args.data_root).expanduser().resolve()
    results = {
        "schema": "mnq-temporal-hierarchy-development-v1",
        "stage": "P0-D",
        "holdout_policy": "June 9-11 are forbidden inputs for this runner.",
        "scales_s": FACTORS,
        "lead_blocks": 1,
        "targets": TARGETS,
        "semantic_coordinates": {
            "log_depth_capacity": "mean log1p depth across 10 bid + 10 ask levels",
            "log_side_contrast": "mean log1p bid depth minus mean log1p ask depth",
        },
        "baselines": ["LAST_FAST", "COARSE_PERSISTENCE"],
        "days": [],
    }

    forbidden = {"20260609", "20260610", "20260611"}
    if forbidden.intersection(args.dates):
        raise SystemExit("holdout date requested; runner refuses June 9-11")

    for day in args.dates:
        path = locate_feature(root, day)
        series = load_mature_semantics(path, day)
        d = {"date": day, "feature_file": str(path), "observed_mature_seconds": len(series), "maps": []}
        for factor in FACTORS:
            blocks = build_blocks(series, day, factor)
            for ti, target in enumerate(TARGETS):
                rec = evaluate(blocks, ti, factor)
                rec["target"] = target
                rec["complete_blocks"] = len(blocks)
                d["maps"].append(rec)
        results["days"].append(d)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({
        "schema": results["schema"],
        "dates": [d["date"] for d in results["days"]],
        "scales_s": FACTORS,
        "records": sum(len(d["maps"]) for d in results["days"]),
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
