#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.modal_compare import compare_loading_subspaces
from market_chi.modal_identifiability import (
    canonical_depth_bases,
    semantic_capture_table,
    spectral_metrics,
    strongest_mode,
)
from tools.analyze_mnq_modal import LEVELS, NS, dense_state, load_rows, pca_depth


KS = (2, 3, 4, 6, 10)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


def iso_to_ns(text: str) -> int:
    return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp() * NS)


def specs(minutes: int) -> list[dict[str, object]]:
    if minutes <= 0 or (21 * 60) % minutes != 0:
        raise ValueError("window size must divide the 21-hour mature interval")
    base = datetime(2026, 5, 28, 0, 0, tzinfo=timezone.utc)
    out = []
    for i in range((21 * 60) // minutes):
        start = base + timedelta(minutes=i * minutes)
        end = start + timedelta(minutes=minutes)
        out.append({
            "label": f"{minutes}m_{i+1:02d}",
            "minutes": minutes,
            "start": iso(start),
            "end": iso(end),
        })
    return out


def pca_for_rows(rows, lo: int, hi: int):
    d = dense_state(rows, lo, hi)
    ratio, vt, _, _ = pca_depth(d)
    return ratio, vt


def summarize(ratio: np.ndarray, vt: np.ndarray, full_vt: np.ndarray) -> dict[str, object]:
    bases = canonical_depth_bases(LEVELS)
    captures = semantic_capture_table(vt, bases, ks=KS)
    strongest = {name: strongest_mode(vt, basis) for name, basis in bases.items()}
    comparisons = {}
    for k in KS:
        comparisons[str(k)] = compare_loading_subspaces(vt, full_vt, k=k).to_dict()
    return {
        "spectral": spectral_metrics(ratio, ks=KS),
        "semantic_capture": captures,
        "strongest_mode": strongest,
        "subspace_vs_full_day": comparisons,
        "loadings": [[float(x) for x in row] for row in vt],
        "variance_ratio": [float(x) for x in ratio],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-coverage", type=float, default=0.80)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    features = Path(args.features).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    start_ns = iso_to_ns("2026-05-28T00:00:00.000000000Z")
    end_ns = iso_to_ns("2026-05-28T21:00:00.000000000Z")
    rows = load_rows(features, start_ns, end_ns)
    full_ratio, full_vt = pca_for_rows(rows, start_ns, end_ns)
    bases = canonical_depth_bases(LEVELS)

    records = []
    for minutes in (60, 30):
        for w in specs(minutes):
            print(f"[{minutes}m] {w['start']} -> {w['end']}", flush=True)
            lo = iso_to_ns(str(w["start"]))
            hi = iso_to_ns(str(w["end"]))
            rr = [r for r in rows if lo <= int(r["bin_start_ns"]) < hi]
            observed = len({int(r["bin_start_ns"]) for r in rr})
            expected = int((hi - lo) / NS)
            coverage = observed / expected if expected else 0.0
            rec = {**w, "coverage_fraction": coverage, "observed_event_seconds": observed}
            if not rr or coverage < args.min_coverage or int(rr[0]["bin_start_ns"]) != lo:
                rec["status"] = "SKIPPED_LOW_OR_LATE_COVERAGE"
                records.append(rec)
                continue
            ratio, vt = pca_for_rows(rr, lo, hi)
            rec["status"] = "COMPLETE"
            rec["metrics"] = summarize(ratio, vt, full_vt)
            records.append(rec)

            cp = {
                "schema_version": "mnq-may28-modal-identifiability-v1-checkpoint",
                "holdout_status": "SEALED_NOT_ACCESSED",
                "records": records,
            }
            checkpoint = out_path.with_suffix(".checkpoint.json")
            checkpoint.parent.mkdir(parents=True, exist_ok=True)
            checkpoint.write_text(json.dumps(cp, indent=2), encoding="utf-8")

    adjacent = []
    by_key = {(r["minutes"], r["label"]): r for r in records if r.get("status") == "COMPLETE"}
    for minutes in (60, 30):
        ww = [r for r in records if r.get("minutes") == minutes and r.get("status") == "COMPLETE"]
        ww.sort(key=lambda r: r["start"])
        for a, b in zip(ww, ww[1:]):
            item = {"minutes": minutes, "window_a": a["label"], "window_b": b["label"], "subspace": {}}
            A = a["metrics"]["loadings"]
            B = b["metrics"]["loadings"]
            for k in KS:
                item["subspace"][str(k)] = compare_loading_subspaces(A, B, k=k).to_dict()
            adjacent.append(item)

    # Compact the final upload after all comparisons.
    for r in records:
        if r.get("status") == "COMPLETE":
            r["metrics"].pop("loadings", None)

    payload = {
        "schema_version": "mnq-may28-modal-identifiability-v1",
        "epistemic_status": "P0-D identifiability / rank-migration follow-up only",
        "holdout_status": "SEALED_NOT_ACCESSED",
        "source_code_commit": args.code_commit,
        "time_rule": "ordinary UTC wall-clock",
        "fixed_subspace_k": list(KS),
        "no_adaptive_k": True,
        "question": "Do apparent top-rank reorganizations preserve semantic architecture in wider fixed modal subspaces when the spectrum flattens?",
        "full_day_reference": {
            "spectral": spectral_metrics(full_ratio, ks=KS),
            "semantic_capture": semantic_capture_table(full_vt, bases, ks=KS),
            "strongest_mode": {name: strongest_mode(full_vt, basis) for name, basis in bases.items()},
        },
        "records": records,
        "adjacent": adjacent,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    checkpoint = out_path.with_suffix(".checkpoint.json")
    if checkpoint.exists():
        checkpoint.unlink()

    print("MAY28 MODAL IDENTIFIABILITY COMPLETE")
    print("Complete windows:", sum(r.get("status") == "COMPLETE" for r in records))
    print("Upload only:", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
