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
    capture_percentile_against_directions,
    fixed_isotropic_directions,
    isotropic_capture_control,
    semantic_capture_table,
    spectral_metrics,
    strongest_mode,
)
from tools.analyze_mnq_modal import LEVELS, NS, dense_state, load_rows, pca_depth

DATES = ("20260527", "20260529", "20260601", "20260602")
KS = (2, 3, 4, 6, 10)
RANDOM_COUNT = 256
RANDOM_SEED = 20260927


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


def iso_to_ns(text: str) -> int:
    return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp() * NS)


def date_base(date_text: str) -> datetime:
    return datetime.strptime(date_text, "%Y%m%d").replace(tzinfo=timezone.utc)


def specs(date_text: str, minutes: int) -> list[dict[str, object]]:
    if minutes <= 0 or (21 * 60) % minutes != 0:
        raise ValueError("window size must divide the 21-hour mature interval")
    base = date_base(date_text)
    out = []
    for i in range((21 * 60) // minutes):
        start = base + timedelta(minutes=i * minutes)
        end = start + timedelta(minutes=minutes)
        out.append({
            "date": date_text,
            "label": f"{date_text}_{minutes}m_{i+1:02d}",
            "minutes": minutes,
            "start": iso(start),
            "end": iso(end),
        })
    return out


def find_feature(root: Path, date_text: str) -> Path:
    matches = sorted(root.rglob(f"*{date_text}*.features.v2.csv.gz"))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one v2 feature file for {date_text} under {root}; found {len(matches)}"
        )
    return matches[0]


def pca_for_rows(rows, lo: int, hi: int):
    d = dense_state(rows, lo, hi)
    ratio, vt, _, _ = pca_depth(d)
    return ratio, vt


def summarize(
    ratio: np.ndarray,
    vt: np.ndarray,
    full_vt: np.ndarray,
    directions: np.ndarray,
) -> dict[str, object]:
    bases = canonical_depth_bases(LEVELS)
    captures = semantic_capture_table(vt, bases, ks=KS)
    strongest = {name: strongest_mode(vt, basis) for name, basis in bases.items()}
    comparisons = {
        str(k): compare_loading_subspaces(vt, full_vt, k=k).to_dict()
        for k in KS
    }
    controls = {}
    percentiles = {name: {} for name in bases}
    for k in KS:
        controls[str(k)] = isotropic_capture_control(vt, directions, k=k)
        for name, basis in bases.items():
            percentiles[name][str(k)] = capture_percentile_against_directions(
                vt, basis, directions, k=k
            )
    return {
        "spectral": spectral_metrics(ratio, ks=KS),
        "semantic_capture": captures,
        "semantic_capture_percentile_vs_isotropic": percentiles,
        "strongest_mode": strongest,
        "subspace_vs_day_reference": comparisons,
        "isotropic_capture_control": controls,
        "_loadings": [[float(x) for x in row] for row in vt],
        "variance_ratio": [float(x) for x in ratio],
    }


def checkpoint_path(out_path: Path) -> Path:
    return out_path.with_suffix(".checkpoint.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-coverage", type=float, default=0.80)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    features_root = Path(args.features_root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    cp_path = checkpoint_path(out_path)
    directions = fixed_isotropic_directions(
        2 * LEVELS, count=RANDOM_COUNT, seed=RANDOM_SEED
    )

    records: list[dict[str, object]] = []
    if cp_path.exists():
        cp = json.loads(cp_path.read_text(encoding="utf-8"))
        if cp.get("schema_version") == "mnq-crossday-semantic-preservation-v1-checkpoint":
            records = cp.get("records", [])
            print(f"Resuming from checkpoint with {len(records)} completed/skipped windows.", flush=True)

    done_labels = {str(r["label"]) for r in records}
    day_references: dict[str, dict[str, object]] = {}
    source_files: dict[str, str] = {}

    for date_text in DATES:
        feature = find_feature(features_root, date_text)
        source_files[date_text] = str(feature)
        day_start = date_base(date_text)
        start_ns = int(day_start.timestamp() * NS)
        end_ns = int((day_start + timedelta(hours=21)).timestamp() * NS)
        rows = load_rows(feature, start_ns, end_ns)
        if not rows:
            raise RuntimeError(f"no mature rows for {date_text}")
        full_ratio, full_vt = pca_for_rows(rows, start_ns, end_ns)
        bases = canonical_depth_bases(LEVELS)
        day_references[date_text] = {
            "spectral": spectral_metrics(full_ratio, ks=KS),
            "semantic_capture": semantic_capture_table(full_vt, bases, ks=KS),
            "semantic_capture_percentile_vs_isotropic": {
                name: {
                    str(k): capture_percentile_against_directions(
                        full_vt, basis, directions, k=k
                    )
                    for k in KS
                }
                for name, basis in bases.items()
            },
            "strongest_mode": {
                name: strongest_mode(full_vt, basis)
                for name, basis in bases.items()
            },
            "isotropic_capture_control": {
                str(k): isotropic_capture_control(full_vt, directions, k=k)
                for k in KS
            },
            "_loadings": [[float(x) for x in row] for row in full_vt],
        }

        for minutes in (60, 30):
            for w in specs(date_text, minutes):
                if w["label"] in done_labels:
                    continue
                print(f"[{date_text} {minutes}m] {w['start']} -> {w['end']}", flush=True)
                lo = iso_to_ns(str(w["start"]))
                hi = iso_to_ns(str(w["end"]))
                rr = [r for r in rows if lo <= int(r["bin_start_ns"]) < hi]
                observed = len({int(r["bin_start_ns"]) for r in rr})
                expected = int((hi - lo) / NS)
                coverage = observed / expected if expected else 0.0
                rec: dict[str, object] = {
                    **w,
                    "coverage_fraction": coverage,
                    "observed_event_seconds": observed,
                }
                if not rr or coverage < args.min_coverage or int(rr[0]["bin_start_ns"]) != lo:
                    rec["status"] = "SKIPPED_LOW_OR_LATE_COVERAGE"
                else:
                    ratio, vt = pca_for_rows(rr, lo, hi)
                    rec["status"] = "COMPLETE"
                    rec["metrics"] = summarize(ratio, vt, full_vt, directions)
                records.append(rec)
                done_labels.add(str(w["label"]))
                cp_payload = {
                    "schema_version": "mnq-crossday-semantic-preservation-v1-checkpoint",
                    "holdout_status": "SEALED_NOT_ACCESSED",
                    "source_code_commit": args.code_commit,
                    "records": records,
                }
                cp_path.parent.mkdir(parents=True, exist_ok=True)
                cp_path.write_text(json.dumps(cp_payload, indent=2), encoding="utf-8")

    adjacent = []
    for date_text in DATES:
        for minutes in (60, 30):
            ww = [
                r for r in records
                if r.get("date") == date_text
                and r.get("minutes") == minutes
                and r.get("status") == "COMPLETE"
            ]
            ww.sort(key=lambda r: str(r["start"]))
            for a, b in zip(ww, ww[1:]):
                A = a["metrics"]["_loadings"]
                B = b["metrics"]["_loadings"]
                item = {
                    "date": date_text,
                    "minutes": minutes,
                    "window_a": a["label"],
                    "window_b": b["label"],
                    "subspace": {
                        str(k): compare_loading_subspaces(A, B, k=k).to_dict()
                        for k in KS
                    },
                }
                adjacent.append(item)

    for r in records:
        if r.get("status") == "COMPLETE":
            r["metrics"].pop("_loadings", None)
    for ref in day_references.values():
        ref.pop("_loadings", None)

    payload = {
        "schema_version": "mnq-crossday-semantic-preservation-v1",
        "epistemic_status": "P0-D cross-day development replication only",
        "holdout_status": "SEALED_NOT_ACCESSED",
        "source_code_commit": args.code_commit,
        "time_rule": "ordinary UTC wall-clock",
        "dates": list(DATES),
        "fixed_subspace_k": list(KS),
        "no_adaptive_k": True,
        "isotropic_control": {
            "dimension": 2 * LEVELS,
            "direction_count": RANDOM_COUNT,
            "seed": RANDOM_SEED,
            "same_directions_reused_everywhere": True,
            "percentiles_are_descriptive_not_p_values": True,
        },
        "source_files": source_files,
        "day_references": day_references,
        "records": records,
        "adjacent": adjacent,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if cp_path.exists():
        cp_path.unlink()

    print("CROSS-DAY SEMANTIC PRESERVATION COMPLETE")
    print("Complete windows:", sum(r.get("status") == "COMPLETE" for r in records))
    print("Skipped windows:", sum(r.get("status") != "COMPLETE" for r in records))
    print("Upload only:", out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
