#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.modal_compare import compare_loading_subspaces

NS = 1_000_000_000
DAY = "2026-05-28"


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


def iso_ns(text: str) -> int:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return int(dt.timestamp() * NS)


def window_specs(hours: int) -> list[dict[str, str | int]]:
    if hours <= 0 or 21 % hours != 0:
        raise ValueError("window size must divide the frozen 21-hour mature interval")
    base = datetime(2026, 5, 28, 0, 0, 0, tzinfo=timezone.utc)
    out = []
    for i in range(21 // hours):
        start = base + timedelta(hours=i * hours)
        end = start + timedelta(hours=hours)
        out.append({
            "label": f"{hours}h_{i+1:02d}",
            "hours": hours,
            "start": iso(start),
            "end": iso(end),
        })
    return out


def coverage_all(features: Path, windows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    info = {}
    for w in windows:
        lo, hi = iso_ns(str(w["start"])), iso_ns(str(w["end"]))
        info[str(w["label"])] = {
            "expected_seconds": int((hi - lo) / NS),
            "observed_event_seconds": 0,
            "first_observed_ns": None,
            "last_observed_ns": None,
            "_lo": lo,
            "_hi": hi,
        }

    with gzip.open(features, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row["bin_start_ns"])
            for d in info.values():
                if d["_lo"] <= t < d["_hi"]:
                    d["observed_event_seconds"] += 1
                    if d["first_observed_ns"] is None:
                        d["first_observed_ns"] = t
                    d["last_observed_ns"] = t

    for d in info.values():
        exp = int(d["expected_seconds"])
        d["coverage_fraction"] = d["observed_event_seconds"] / exp if exp else 0.0
        d["exact_start_observed"] = d["first_observed_ns"] == d["_lo"]
        d.pop("_lo")
        d.pop("_hi")
    return info


def run_modal(features: Path, start: str, end: str, out_json: Path) -> tuple[bool, str]:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "analyze_mnq_modal.py"),
        str(features),
        "--start", start,
        "--end", end,
        "--out", str(out_json),
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode == 0:
        return True, p.stdout.strip()
    return False, (p.stderr.strip() or p.stdout.strip())


def risk_map(d: dict[str, object]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for r in d.get("exploratory_forward_associations", []):
        pred = str(r["predictor"])
        if pred not in {"total_depth", "depth_pc1", "spread", "l10_imbalance"}:
            continue
        out.setdefault(pred, {})[str(r["horizon_s"])] = float(r["spearman_forward_risk"])
    return out


def compact(d: dict[str, object]) -> dict[str, object]:
    alignments = d["basis_alignment"]
    depth_grad = max(alignments, key=lambda x: x["depth_gradient"])
    side_grad = max(alignments, key=lambda x: x["side_gradient"])
    risks = risk_map(d)
    pc1_depth = float(d["mode_semantic_correlations"]["pc1_vs_total_depth_spearman"])
    sign = -1.0 if pc1_depth < 0 else 1.0
    aligned = {h: sign * float(v) for h, v in risks.get("depth_pc1", {}).items()}
    return {
        "interval_start": d["interval_start"],
        "interval_end_exclusive": d["interval_end_exclusive"],
        "coverage_fraction": d["coverage_fraction"],
        "pc1_variance": d["depth_pca_variance_ratio_first10"][0],
        "pc2_variance": d["depth_pca_variance_ratio_first10"][1],
        "pc1_pc2_cumulative": d["depth_pca_cumulative_first10"][1],
        "pc1_symmetric_alignment": d["basis_alignment"][0]["symmetric_depth"],
        "pc2_imbalance_alignment": d["basis_alignment"][1]["bid_ask_imbalance"],
        "pc1_total_depth_spearman": pc1_depth,
        "pc2_depth_imbalance_spearman": d["mode_semantic_correlations"]["pc2_vs_depth_imbalance_spearman"],
        "top2_min_principal_cosine_within_window": d["half_stability"]["top2_min_principal_cosine"],
        "best_depth_gradient_pc": depth_grad["pc"],
        "best_depth_gradient_alignment": depth_grad["depth_gradient"],
        "best_side_gradient_pc": side_grad["pc"],
        "best_side_gradient_alignment": side_grad["side_gradient"],
        "chi_admissions": sum(1 for r in d["chi_screen"] if r["chi_status"] == "ADMITTED"),
        "chi_screens": len(d["chi_screen"]),
        "forward_risk_spearman": risks,
        "depth_pc1_aligned_to_total_depth_forward_risk": aligned,
        "depth_pca_loadings_first6": d["depth_pca_loadings_first6"],
    }


def sign_label(values: dict[str, float]) -> str:
    xs = [float(v) for v in values.values()]
    if xs and all(v > 0 for v in xs):
        return "positive"
    if xs and all(v < 0 for v in xs):
        return "negative"
    return "mixed"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--full-modal", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--min-coverage", type=float, default=0.80)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    features = Path(args.features).expanduser().resolve()
    full_modal_path = Path(args.full_modal).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not features.exists():
        raise FileNotFoundError(features)
    if not full_modal_path.exists():
        raise FileNotFoundError(full_modal_path)

    full = json.loads(full_modal_path.read_text(encoding="utf-8"))
    full_loadings = full["depth_pca_loadings_first6"]

    windows = window_specs(3) + window_specs(7)
    coverage = coverage_all(features, windows)
    records = []

    for w in windows:
        label = str(w["label"])
        cov = coverage[label]
        rec: dict[str, object] = {**w, "coverage_check": cov}
        if cov["coverage_fraction"] < args.min_coverage or not cov["exact_start_observed"]:
            rec["status"] = "SKIPPED_LOW_OR_LATE_COVERAGE"
            records.append(rec)
            continue

        modal_path = out_dir / f"may28_{label}.modal.json"
        ok, msg = run_modal(features, str(w["start"]), str(w["end"]), modal_path)
        if not ok:
            rec["status"] = "ANALYSIS_FAILED"
            rec["error"] = msg
            records.append(rec)
            continue

        d = json.loads(modal_path.read_text(encoding="utf-8"))
        metrics = compact(d)
        ref = compare_loading_subspaces(
            metrics["depth_pca_loadings_first6"],
            full_loadings,
            k=2,
        )
        metrics["top2_vs_full_day"] = ref.to_dict()
        metrics["total_depth_risk_sign_all_horizons"] = sign_label(
            metrics["forward_risk_spearman"].get("total_depth", {})
        )
        metrics["spread_risk_sign_all_horizons"] = sign_label(
            metrics["forward_risk_spearman"].get("spread", {})
        )
        rec["status"] = "COMPLETE"
        rec["modal_file"] = str(modal_path)
        rec["metrics"] = metrics
        records.append(rec)

    # Adjacent-window comparisons are computed separately within each frozen scale.
    adjacent = []
    for hours in (3, 7):
        rr = [r for r in records if r.get("hours") == hours and r.get("status") == "COMPLETE"]
        rr.sort(key=lambda x: x["start"])
        for a, b in zip(rr, rr[1:]):
            comp = compare_loading_subspaces(
                a["metrics"]["depth_pca_loadings_first6"],
                b["metrics"]["depth_pca_loadings_first6"],
                k=2,
            )
            adjacent.append({
                "hours": hours,
                "window_a": a["label"],
                "window_b": b["label"],
                **comp.to_dict(),
            })

    # Remove bulky loadings from the public index after all comparisons are complete.
    for r in records:
        if r.get("status") == "COMPLETE":
            r["metrics"].pop("depth_pca_loadings_first6", None)

    payload = {
        "schema_version": "mnq-may28-reorganization-v1",
        "date": DAY,
        "epistemic_status": "P0-D outlier/reorganization follow-up only",
        "holdout_status": "SEALED_NOT_ACCESSED",
        "source_code_commit": args.code_commit,
        "time_rule": "ordinary UTC wall-clock; no market-dependent rescaling",
        "primary_windows": "seven non-overlapping 3-hour windows, 00:00-21:00 UTC",
        "sensitivity_windows": "three non-overlapping 7-hour windows, 00:00-21:00 UTC",
        "min_coverage": args.min_coverage,
        "records": records,
        "adjacent_top2_subspace": adjacent,
        "interpretation_rule": "report continuous subspace/risk trajectories first; no post-result threshold",
    }

    out_path = out_dir / "MAY28_REORGANIZATION_INDEX.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("MAY 28 REORGANIZATION FOLLOW-UP COMPLETE")
    print("Complete windows:", sum(r.get("status") == "COMPLETE" for r in records))
    print("Skipped windows:", sum(str(r.get("status", "")).startswith("SKIPPED") for r in records))
    print("Failed windows:", sum(r.get("status") == "ANALYSIS_FAILED" for r in records))
    print("UPLOAD ONLY:")
    print(out_path)
    return 0 if not any(r.get("status") == "ANALYSIS_FAILED" for r in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
