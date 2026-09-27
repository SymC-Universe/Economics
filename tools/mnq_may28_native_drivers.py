#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.modal_compare import compare_loading_subspaces
from tools.analyze_mnq_modal import (
    LEVELS, NS, basis_alignment, dense_state, forward_risk_correlations,
    load_rows, pca_depth, spearman
)


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
        s = base + timedelta(minutes=i * minutes)
        e = s + timedelta(minutes=minutes)
        out.append({
            "label": f"{minutes}m_{i+1:02d}",
            "minutes": minutes,
            "start": iso(s),
            "end": iso(e),
        })
    return out


def q(x: np.ndarray, p: float) -> float:
    return float(np.quantile(x, p))


def summarize_native(d: dict[str, np.ndarray]) -> dict[str, float]:
    bid = np.column_stack([d[f"bid_sz_{i:02d}_last"] for i in range(LEVELS)])
    ask = np.column_stack([d[f"ask_sz_{i:02d}_last"] for i in range(LEVELS)])
    total = bid.sum(axis=1) + ask.sum(axis=1)
    imb = (bid.sum(axis=1) - ask.sum(axis=1)) / np.maximum(total, 1.0)
    spread = d["spread_last"]
    events = d["event_rows"]
    tv = d["trade_volume"]
    stv = d["signed_trade_volume"]

    return {
        "total_depth_median": float(np.median(total)),
        "total_depth_mean": float(np.mean(total)),
        "total_depth_std": float(np.std(total)),
        "total_depth_iqr": q(total, .75) - q(total, .25),
        "spread_median": float(np.median(spread)),
        "spread_mean": float(np.mean(spread)),
        "spread_q90": q(spread, .90),
        "l10_imbalance_median": float(np.median(imb)),
        "l10_imbalance_iqr": q(imb, .75) - q(imb, .25),
        "event_rows_mean_per_s": float(np.mean(events)),
        "event_rows_median_per_s": float(np.median(events)),
        "event_rows_q90_per_s": q(events, .90),
        "trade_volume_total": float(np.sum(tv)),
        "active_trade_second_fraction": float(np.mean(tv > 0)),
        "signed_trade_volume_total": float(np.sum(stv)),
        "abs_signed_trade_volume_total": float(np.sum(np.abs(stv))),
        "mean_abs_signed_trade_volume_per_s": float(np.mean(np.abs(stv))),
    }


def modal_summary(d: dict[str, np.ndarray], full_loadings) -> tuple[dict[str, object], np.ndarray]:
    ratio, vt, scores, names = pca_depth(d)
    aligns = basis_alignment(vt)
    bases = ["symmetric_depth", "bid_ask_imbalance", "depth_gradient", "side_gradient"]
    strongest = {}
    for b in bases:
        row = max(aligns, key=lambda r: r[b])
        strongest[b] = {"pc": int(row["pc"]), "alignment": float(row[b])}

    bid = np.column_stack([d[f"bid_sz_{i:02d}_last"] for i in range(LEVELS)])
    ask = np.column_stack([d[f"ask_sz_{i:02d}_last"] for i in range(LEVELS)])
    total = bid.sum(axis=1) + ask.sum(axis=1)
    imb = (bid.sum(axis=1) - ask.sum(axis=1)) / np.maximum(total, 1.0)

    ref = compare_loading_subspaces(vt[:2], full_loadings[:2], k=2)
    out = {
        "variance_first6": [float(x) for x in ratio[:6]],
        "pc1_total_depth_spearman": float(spearman(scores[:, 0], total)),
        "pc1_total_depth_abs_spearman": float(abs(spearman(scores[:, 0], total))),
        "strongest_basis": strongest,
        "top2_vs_full_day": ref.to_dict(),
        "loadings_top2": [[float(v) for v in row] for row in vt[:2]],
    }
    # Secondary overlay only. It is not used in structural localization.
    risk = forward_risk_correlations(d, scores)
    out["secondary_total_depth_forward_risk"] = {
        str(r["horizon_s"]): float(r["spearman_forward_risk"])
        for r in risk if r["predictor"] == "total_depth"
    }
    return out, vt


def delta(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    return {k: float(b[k] - a[k]) for k in a.keys() if k in b}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--full-modal", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-coverage", type=float, default=0.80)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    features = Path(args.features).expanduser().resolve()
    full_path = Path(args.full_modal).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    full = json.loads(full_path.read_text(encoding="utf-8"))
    full_loadings = np.asarray(full["depth_pca_loadings_first6"], dtype=float)

    start_ns = iso_to_ns("2026-05-28T00:00:00.000000000Z")
    end_ns = iso_to_ns("2026-05-28T21:00:00.000000000Z")
    all_rows = load_rows(features, start_ns, end_ns)

    records = []
    for minutes in (60, 30):
        for w in specs(minutes):
            lo, hi = iso_to_ns(str(w["start"])), iso_to_ns(str(w["end"]))
            rr = [r for r in all_rows if lo <= int(r["bin_start_ns"]) < hi]
            observed = len({int(r["bin_start_ns"]) for r in rr})
            expected = int((hi - lo) / NS)
            coverage = observed / expected if expected else 0.0
            rec = {**w, "coverage_fraction": coverage, "observed_event_seconds": observed}
            if not rr or coverage < args.min_coverage or int(rr[0]["bin_start_ns"]) != lo:
                rec["status"] = "SKIPPED_LOW_OR_LATE_COVERAGE"
                records.append(rec)
                continue
            d = dense_state(rr, lo, hi)
            m, vt = modal_summary(d, full_loadings)
            rec["status"] = "COMPLETE"
            rec["modal"] = m
            rec["native"] = summarize_native(d)
            records.append(rec)

    adjacent = []
    for minutes in (60, 30):
        rr = [r for r in records if r.get("minutes") == minutes and r.get("status") == "COMPLETE"]
        rr.sort(key=lambda r: r["start"])
        for a, b in zip(rr, rr[1:]):
            comp = compare_loading_subspaces(
                a["modal"]["loadings_top2"],
                b["modal"]["loadings_top2"],
                k=2,
            )
            adjacent.append({
                "minutes": minutes,
                "window_a": a["label"],
                "window_b": b["label"],
                "top2_subspace": comp.to_dict(),
                "native_delta": delta(a["native"], b["native"]),
                "pc1_variance_delta": float(b["modal"]["variance_first6"][0] - a["modal"]["variance_first6"][0]),
            })

    # Remove loadings after comparisons to keep the upload compact.
    for r in records:
        if r.get("status") == "COMPLETE":
            r["modal"].pop("loadings_top2", None)

    payload = {
        "schema_version": "mnq-may28-native-driver-v1",
        "epistemic_status": "P0-D native driver localization only",
        "holdout_status": "SEALED_NOT_ACCESSED",
        "source_code_commit": args.code_commit,
        "time_rule": "ordinary UTC wall-clock",
        "primary_windows": "21 non-overlapping 60-minute windows from 00:00-21:00 UTC",
        "sensitivity_windows": "42 non-overlapping 30-minute windows over the same interval",
        "structural_localization_rule": "L10 modal geometry only; forward-risk overlay not used to select transitions",
        "records": records,
        "adjacent": adjacent,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("MAY28 NATIVE DRIVER LOCALIZATION COMPLETE")
    print("Complete windows:", sum(r.get("status") == "COMPLETE" for r in records))
    print("Skipped:", sum(str(r.get("status","")).startswith("SKIPPED") for r in records))
    print("UPLOAD ONLY:")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
