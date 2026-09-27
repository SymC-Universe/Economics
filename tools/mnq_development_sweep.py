#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.microstructure_v2 import aggregate_mbp10_stream, validate_feature_gzip

NS = 1_000_000_000
DEFAULT_DATES = ["20260528", "20260529", "20260601", "20260602"]


def iso(day: str, hhmmss: str) -> str:
    dt = datetime.strptime(day + hhmmss, "%Y%m%d%H:%M:%S").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


def next_day(day: str) -> str:
    dt = datetime.strptime(day, "%Y%m%d") + timedelta(days=1)
    return dt.strftime("%Y%m%d")


def iso_ns(text: str) -> int:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return int(dt.timestamp() * NS)


def sha256_file(path: Path, block: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(block)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def verify_cached_features(features: Path, summary: Path | None = None) -> dict[str, object]:
    integrity = validate_feature_gzip(features)
    result: dict[str, object] = {
        "features": str(features),
        "gzip_integrity": integrity,
        "valid": bool(integrity.get("valid")),
    }
    if not result["valid"]:
        result["reason"] = "gzip_integrity_failed"
        return result
    if summary is not None:
        result["summary"] = str(summary)
        if not summary.exists():
            result["valid"] = False
            result["reason"] = "summary_missing"
            return result
        try:
            meta = json.loads(summary.read_text(encoding="utf-8"))
        except Exception as exc:
            result["valid"] = False
            result["reason"] = f"summary_unreadable:{type(exc).__name__}:{exc}"
            return result
        expected = meta.get("output_sha256")
        if expected:
            actual = sha256_file(features)
            result["expected_sha256"] = expected
            result["actual_sha256"] = actual
            if actual != expected:
                result["valid"] = False
                result["reason"] = "summary_hash_mismatch"
                return result
    result["reason"] = "cache_verified"
    return result


def quarantine(path: Path) -> str | None:
    if not path.exists():
        return None
    candidate = path.with_name(path.name + ".corrupt")
    i = 1
    while candidate.exists():
        candidate = path.with_name(path.name + f".corrupt.{i}")
        i += 1
    path.replace(candidate)
    return str(candidate)


def phase_coverage(features: Path, start: str, end: str) -> dict[str, object]:
    lo, hi = iso_ns(start), iso_ns(end)
    expected = int((hi - lo) / NS)
    observed = 0
    first = None
    last = None
    with gzip.open(features, "rt", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = int(row["bin_start_ns"])
            if t < lo:
                continue
            if t >= hi:
                break
            observed += 1
            first = t if first is None else first
            last = t
    return {
        "expected_seconds": expected,
        "observed_event_seconds": observed,
        "coverage_fraction": observed / expected if expected else 0.0,
        "first_observed_ns": first,
        "last_observed_ns": last,
        "exact_start_observed": first == lo,
    }


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


def compact_modal(path: Path) -> dict[str, object]:
    d = json.loads(path.read_text(encoding="utf-8"))
    risk = {}
    for r in d.get("exploratory_forward_associations", []):
        if r["predictor"] in {"total_depth", "depth_pc1", "spread", "l10_imbalance"}:
            risk.setdefault(r["predictor"], {})[str(r["horizon_s"])] = r["spearman_forward_risk"]
    return {
        "interval_start": d["interval_start"],
        "interval_end_exclusive": d["interval_end_exclusive"],
        "dense_seconds": d["dense_seconds"],
        "coverage_fraction": d["coverage_fraction"],
        "depth_pca_variance_ratio_first10": d["depth_pca_variance_ratio_first10"],
        "depth_pca_cumulative_first10": d["depth_pca_cumulative_first10"],
        "depth_pca_feature_names": d["depth_pca_feature_names"],
        "depth_pca_loadings_first6": d["depth_pca_loadings_first6"],
        "basis_alignment_first6": d["basis_alignment"],
        "pc1_variance": d["depth_pca_variance_ratio_first10"][0],
        "pc2_variance": d["depth_pca_variance_ratio_first10"][1],
        "pc1_pc2_cumulative": d["depth_pca_cumulative_first10"][1],
        "pc1_symmetric_alignment": d["basis_alignment"][0]["symmetric_depth"],
        "pc2_imbalance_alignment": d["basis_alignment"][1]["bid_ask_imbalance"],
        "pc1_total_depth_spearman": d["mode_semantic_correlations"]["pc1_vs_total_depth_spearman"],
        "pc2_depth_imbalance_spearman": d["mode_semantic_correlations"]["pc2_vs_depth_imbalance_spearman"],
        "top2_min_principal_cosine": d["half_stability"]["top2_min_principal_cosine"],
        "chi_admissions": sum(1 for r in d["chi_screen"] if r["chi_status"] == "ADMITTED"),
        "chi_screens": len(d["chi_screen"]),
        "chi_screen": d["chi_screen"],
        "forward_risk_spearman": risk,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--dates", nargs="*", default=DEFAULT_DATES)
    ap.add_argument("--existing-may27-features")
    ap.add_argument("--min-phase-coverage", type=float, default=0.80)
    ap.add_argument("--code-commit", default=None)
    args = ap.parse_args()

    data_root = Path(args.data_root).expanduser().resolve()
    raw_dir = data_root / "MBR10_Data"
    out = Path(args.out_dir).expanduser().resolve()
    feat_dir = out / "features"
    modal_dir = out / "modal"
    feat_dir.mkdir(parents=True, exist_ok=True)
    modal_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "schema_version": "mnq-development-sweep-v3",
        "data_root": str(data_root),
        "holdout_policy": "June 9-11 files are not referenced or opened by this script.",
        "code_commit": args.code_commit,
        "phases": {
            "mature": "00:00-21:00 UTC",
            "session_open": "22:00-24:00 UTC",
        },
        "minimum_phase_coverage": args.min_phase_coverage,
        "runs": [],
    }
    phase_index: dict[str, object] = {
        "schema_version": "mnq-development-phase-index-v3",
        "holdout_status": "SEALED_NOT_ACCESSED",
        "code_commit": args.code_commit,
        "phases": [],
    }

    jobs: list[tuple[str, Path, bool]] = []

    # May 27 may be reused from the earlier weekday pass. Reuse only after a
    # full gzip EOF/CRC check. If it is truncated, leave that external file
    # untouched and rebuild May 27 into this sweep workspace from raw data.
    if args.existing_may27_features:
        p = Path(args.existing_may27_features).expanduser().resolve()
        if p.exists():
            check = verify_cached_features(p)
            if check["valid"]:
                jobs.append(("20260527", p, True))
                manifest["runs"].append({
                    "date": "20260527",
                    "status": "EXISTING_FEATURES_VERIFIED",
                    "path": str(p),
                    "cache_check": check,
                })
            else:
                manifest["runs"].append({
                    "date": "20260527",
                    "status": "EXISTING_FEATURES_CORRUPT_REBUILD_REQUIRED",
                    "path": str(p),
                    "cache_check": check,
                    "note": "External reused file was not modified.",
                })
                raw27 = raw_dir / "glbx-mdp3-20260527.mbp-10.csv.zst"
                feat27 = feat_dir / "glbx-mdp3-20260527.mbp-10.1000ms.features.v2.csv.gz"
                sum27 = feat_dir / "glbx-mdp3-20260527.mbp-10.1000ms.summary.v2.json"
                if raw27.exists():
                    try:
                        aggregate_mbp10_stream(raw27, feat27, sum27, 1000)
                        check27 = verify_cached_features(feat27, sum27)
                        if not check27["valid"]:
                            raise IOError("rebuilt May 27 cache failed verification: " + str(check27))
                        jobs.append(("20260527", feat27, False))
                        meta27 = json.loads(sum27.read_text(encoding="utf-8"))
                        manifest["runs"].append({
                            "date": "20260527",
                            "status": "REBUILT_CORRUPT_EXTERNAL_CACHE",
                            "raw": str(raw27),
                            "raw_sha256": meta27.get("source_sha256"),
                            "features": str(feat27),
                            "features_sha256": meta27.get("output_sha256"),
                            "summary": str(sum27),
                            "cache_check": check27,
                        })
                    except Exception as exc:
                        manifest["runs"].append({
                            "date": "20260527",
                            "status": "REBUILD_FAILED",
                            "error": repr(exc),
                        })
                else:
                    manifest["runs"].append({
                        "date": "20260527",
                        "status": "RAW_NOT_FOUND_FOR_REBUILD",
                        "path": str(raw27),
                    })
        else:
            manifest["runs"].append({"date": "20260527", "status": "EXISTING_FEATURES_NOT_FOUND", "path": str(p)})

    for day in args.dates:
        raw = raw_dir / f"glbx-mdp3-{day}.mbp-10.csv.zst"
        features = feat_dir / f"glbx-mdp3-{day}.mbp-10.1000ms.features.v2.csv.gz"
        summary = feat_dir / f"glbx-mdp3-{day}.mbp-10.1000ms.summary.v2.json"
        if not raw.exists():
            manifest["runs"].append({"date": day, "status": "RAW_NOT_FOUND", "path": str(raw)})
            continue

        rebuild_reason = None
        cache_check = None
        quarantined: list[str] = []
        if features.exists() and summary.exists():
            cache_check = verify_cached_features(features, summary)
            if not cache_check["valid"]:
                rebuild_reason = str(cache_check.get("reason"))
                qf = quarantine(features)
                qs = quarantine(summary)
                quarantined = [p for p in (qf, qs) if p]
        elif features.exists() or summary.exists():
            rebuild_reason = "incomplete_cache_pair"
            qf = quarantine(features)
            qs = quarantine(summary)
            quarantined = [p for p in (qf, qs) if p]

        if not features.exists() or not summary.exists():
            try:
                aggregate_mbp10_stream(raw, features, summary, 1000)
            except Exception as exc:
                manifest["runs"].append({
                    "date": day,
                    "status": "EXTRACTION_FAILED",
                    "error": repr(exc),
                    "rebuild_reason": rebuild_reason,
                    "quarantined": quarantined,
                })
                continue

        final_check = verify_cached_features(features, summary)
        if not final_check["valid"]:
            manifest["runs"].append({
                "date": day,
                "status": "CACHE_VERIFICATION_FAILED",
                "cache_check": final_check,
                "rebuild_reason": rebuild_reason,
                "quarantined": quarantined,
            })
            continue

        jobs.append((day, features, False))
        summary_data = json.loads(summary.read_text(encoding="utf-8"))
        manifest["runs"].append({
            "date": day,
            "status": "FEATURES_READY_REBUILT" if rebuild_reason else "FEATURES_READY",
            "raw": str(raw),
            "raw_sha256": summary_data.get("source_sha256"),
            "features": str(features),
            "features_sha256": summary_data.get("output_sha256") or sha256_file(features),
            "summary": str(summary),
            "cache_check": final_check,
            "rebuild_reason": rebuild_reason,
            "quarantined": quarantined,
        })

    for day, features, reused in jobs:
        phases = {
            "mature": (iso(day, "00:00:00"), iso(day, "21:00:00")),
            "session_open": (iso(day, "22:00:00"), iso(next_day(day), "00:00:00")),
        }
        for phase, (start, end) in phases.items():
            cov = phase_coverage(features, start, end)
            record: dict[str, object] = {
                "date": day,
                "phase": phase,
                "features": str(features),
                "reused_existing_features": reused,
                "requested_start": start,
                "requested_end": end,
                "coverage_check": cov,
            }
            if cov["coverage_fraction"] < args.min_phase_coverage or not cov["exact_start_observed"]:
                record["status"] = "SKIPPED_LOW_OR_LATE_COVERAGE"
                phase_index["phases"].append(record)
                continue
            modal_out = modal_dir / f"glbx-mdp3-{day}.mbp-10.{phase}.modal.v2.json"
            ok, msg = run_modal(features, start, end, modal_out)
            if not ok:
                record["status"] = "ANALYSIS_FAILED"
                record["error"] = msg
                phase_index["phases"].append(record)
                continue
            record["status"] = "COMPLETE"
            record["modal_file"] = str(modal_out)
            record["modal_sha256"] = sha256_file(modal_out)
            record["metrics"] = compact_modal(modal_out)
            phase_index["phases"].append(record)

    manifest_path = out / "DEVELOPMENT_SWEEP_MANIFEST.json"
    index_path = out / "DEVELOPMENT_SWEEP_PHASE_INDEX.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    index_path.write_text(json.dumps(phase_index, indent=2), encoding="utf-8")

    complete = sum(1 for p in phase_index["phases"] if p.get("status") == "COMPLETE")
    skipped = sum(1 for p in phase_index["phases"] if str(p.get("status", "")).startswith("SKIPPED"))
    failed = sum(1 for p in phase_index["phases"] if p.get("status") == "ANALYSIS_FAILED")
    print("DEVELOPMENT SWEEP COMPLETE")
    print("Completed phase analyses:", complete)
    print("Skipped unavailable/low-coverage phases:", skipped)
    print("Failed phase analyses:", failed)
    print("UPLOAD ONLY:")
    print(manifest_path)
    print(index_path)
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
