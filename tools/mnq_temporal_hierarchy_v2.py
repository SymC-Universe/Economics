#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.temporal_hierarchy_v2 import (
    PRIMARY_PAIRS,
    bootstrap_delta_by_day,
    classify_pair,
    evaluate_pair_day,
    semantic_scores_from_depth,
)

NS = 1_000_000_000
DATES = ("20260527", "20260528", "20260529", "20260601", "20260602")
PLAN_COMMIT = "b58b95f2ec9d722e0343c4f961e849d720f8f1be"
CLEARANCE_STATUS = "APQ_EXTERNAL_STATUS=QUALIFIED"
CLEARANCE_COMMIT = f"PLAN_PACKET_COMMIT={PLAN_COMMIT}"


def date_start_ns(date_text: str) -> int:
    dt = datetime.strptime(date_text, "%Y%m%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * NS)


def verify_external_clearance(path: Path) -> dict[str, object]:
    if not path.exists():
        raise RuntimeError(
            "external-cognition APQ clearance file is required before real development execution"
        )
    text = path.read_text(encoding="utf-8", errors="replace")
    if CLEARANCE_STATUS not in text:
        raise RuntimeError("APQ external review is not QUALIFIED")
    if CLEARANCE_COMMIT not in text:
        raise RuntimeError("APQ review is not bound to the frozen plan commit")
    return {
        "clearance_file": str(path.resolve()),
        "required_status": CLEARANCE_STATUS,
        "required_plan_binding": CLEARANCE_COMMIT,
    }


def find_feature(root: Path, date_text: str) -> Path:
    matches = sorted(
        p for p in root.rglob(f"*{date_text}*.features.v2.csv.gz")
        if "q038" not in str(p).lower() and "holdout" not in str(p).lower()
    )
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one development v2 feature file for {date_text}; found {len(matches)}"
        )
    return matches[0]


def load_day_segment(feature: Path, date_text: str) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    lo = date_start_ns(date_text)
    hi = lo + 21 * 60 * 60 * NS
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    with gzip.open(feature, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row["bin_start_ns"])
            if not (lo <= t < hi):
                continue
            key = ((row.get("instrument_id") or "").strip(), (row.get("symbol") or "").strip())
            groups.setdefault(key, []).append(row)

    diagnostics = []
    eligible = []
    for key, rows in groups.items():
        unique_seconds = len({int(r["bin_start_ns"]) for r in rows})
        coverage = unique_seconds / (21 * 60 * 60)
        diagnostics.append(
            {
                "instrument_id": key[0],
                "symbol": key[1],
                "rows": len(rows),
                "unique_seconds": unique_seconds,
                "coverage_fraction": coverage,
            }
        )
        if coverage >= 0.80:
            eligible.append((key, rows, coverage))

    if len(eligible) != 1:
        raise RuntimeError(
            f"{date_text}: expected exactly one >=80% mature-session segment; found {len(eligible)}"
        )

    key, rows, coverage = eligible[0]
    rows.sort(key=lambda r: int(r["bin_start_ns"]))
    times = np.array([int(r["bin_start_ns"]) for r in rows], dtype=np.int64)

    names = [f"bid_sz_{i:02d}_mean" for i in range(10)] + [
        f"ask_sz_{i:02d}_mean" for i in range(10)
    ]
    depth = np.empty((len(rows), 20), dtype=float)
    for j, r in enumerate(rows):
        for k, name in enumerate(names):
            v = r.get(name)
            depth[j, k] = float(v) if v not in ("", None) else math.nan

    finite = np.all(np.isfinite(depth), axis=1) & np.all(depth >= 0, axis=1)
    times = times[finite]
    depth = depth[finite]
    semantic = semantic_scores_from_depth(depth)

    return times, semantic, {
        "feature_file": str(feature.resolve()),
        "selected_segment": {
            "instrument_id": key[0],
            "symbol": key[1],
            "coverage_fraction_before_depth_filter": coverage,
            "finite_depth_seconds": int(len(times)),
            "finite_depth_fraction": float(len(times) / (21 * 60 * 60)),
        },
        "segment_diagnostics": diagnostics,
    }


def finite_values(x: np.ndarray) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    return a[np.isfinite(a)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--apq-clearance", required=True)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    clearance = verify_external_clearance(Path(args.apq_clearance).expanduser().resolve())
    root = Path(args.features_root).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    primary_checkpoint = out.with_suffix(".primary_frozen.json")

    source_records = {}
    day_data = {}
    for date_text in DATES:
        feature = find_feature(root, date_text)
        times, semantic, meta = load_day_segment(feature, date_text)
        source_records[date_text] = meta
        day_data[date_text] = (times, semantic, date_start_ns(date_text))

    primary_pairs = {}
    for fine_s, coarse_s in PRIMARY_PAIRS:
        key = f"{fine_s}_to_{coarse_s}"
        day_results = {}
        day_extras = {}
        for date_text in DATES:
            times, semantic, start = day_data[date_text]
            print(f"[PRIMARY {key}] {date_text}", flush=True)
            result, extra = evaluate_pair_day(
                times,
                semantic,
                fine_seconds=fine_s,
                coarse_seconds=coarse_s,
                day_start_ns=start,
                lead_blocks=1,
            )
            day_results[date_text] = result.to_dict()
            day_extras[date_text] = extra

        complete = [d for d in DATES if day_results[d]["status"] == "COMPLETE"]
        if len(complete) != len(DATES):
            primary_pairs[key] = {
                "status": "INVALID_PAIR",
                "day_results": day_results,
                "reason": "all five development days must complete the frozen primary pair",
            }
            continue

        delta_b_by_day = []
        delta_l_by_day = []
        day_deltas = []
        for d in DATES:
            ex = day_extras[d]
            mask = ex["pred_mask"]
            db = finite_values(ex["delta_b"][mask])
            dl = finite_values(ex["delta_l"][mask])
            delta_b_by_day.append(db)
            delta_l_by_day.append(dl)
            day_deltas.append(float(np.mean(db)))

        boot_b = bootstrap_delta_by_day(
            delta_b_by_day, coarse_seconds=coarse_s, reps=10_000, seed=20260929
        )
        boot_l = bootstrap_delta_by_day(
            delta_l_by_day, coarse_seconds=coarse_s, reps=10_000, seed=20260929
        )

        depth_mae_b = float(np.mean([day_results[d]["depth_mae_baseline"] for d in DATES]))
        depth_mae_s = float(np.mean([day_results[d]["depth_mae_structured"] for d in DATES]))
        imb_mae_b = float(np.mean([day_results[d]["imbalance_mae_baseline"] for d in DATES]))
        imb_mae_s = float(np.mean([day_results[d]["imbalance_mae_structured"] for d in DATES]))

        classification = classify_pair(
            boot_b,
            day_deltas,
            depth_mae_baseline=depth_mae_b,
            depth_mae_structured=depth_mae_s,
            imbalance_mae_baseline=imb_mae_b,
            imbalance_mae_structured=imb_mae_s,
        )

        primary_pairs[key] = {
            "status": "COMPLETE",
            "classification": classification,
            "bootstrap_vs_coarse_context": boot_b.to_dict(),
            "bootstrap_vs_last_fast": boot_l.to_dict(),
            "day_delta_b": {d: day_deltas[i] for i, d in enumerate(DATES)},
            "mean_mae": {
                "depth_baseline": depth_mae_b,
                "depth_structured": depth_mae_s,
                "imbalance_baseline": imb_mae_b,
                "imbalance_structured": imb_mae_s,
            },
            "day_results": day_results,
        }

    primary_payload = {
        "schema_version": "mnq-temporal-hierarchy-v2-primary-freeze",
        "epistemic_status": "P0-D development only",
        "plan_packet_commit": PLAN_COMMIT,
        "source_code_commit": args.code_commit,
        "external_apq_clearance": clearance,
        "dates": list(DATES),
        "session_utc": "00:00-21:00",
        "time_rule": "ordinary wall-clock; never rescaled",
        "primary_pairs": primary_pairs,
    }
    primary_checkpoint.parent.mkdir(parents=True, exist_ok=True)
    primary_checkpoint.write_text(json.dumps(primary_payload, indent=2), encoding="utf-8")

    secondary = {}
    for lead in (2, 3):
        lead_results = {}
        for fine_s, coarse_s in PRIMARY_PAIRS:
            key = f"{fine_s}_to_{coarse_s}"
            day_results = {}
            for date_text in DATES:
                times, semantic, start = day_data[date_text]
                print(f"[SECONDARY lead={lead} {key}] {date_text}", flush=True)
                result, _ = evaluate_pair_day(
                    times,
                    semantic,
                    fine_seconds=fine_s,
                    coarse_seconds=coarse_s,
                    day_start_ns=start,
                    lead_blocks=lead,
                )
                day_results[date_text] = result.to_dict()
            lead_results[key] = day_results
        secondary[f"lead_{lead}"] = lead_results

    payload = {
        "schema_version": "mnq-temporal-hierarchy-v2",
        "epistemic_status": "P0-D development only",
        "plan_packet_commit": PLAN_COMMIT,
        "source_code_commit": args.code_commit,
        "external_apq_clearance": clearance,
        "dates": list(DATES),
        "session_utc": "00:00-21:00",
        "time_rule": "ordinary wall-clock; never rescaled",
        "primary_pairs": primary_pairs,
        "secondary": secondary,
        "source_records": source_records,
        "nonclaims": [
            "no event prediction claim",
            "no trading claim",
            "no scalar chi claim",
            "no causal substrate-inheritance claim",
            "no cross-market claim",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("MNQ TEMPORAL HIERARCHY V2 COMPLETE")
    print("Primary checkpoint:", primary_checkpoint)
    print("Final result:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
