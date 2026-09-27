#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi.holdout_semantic import (
    ISOTROPIC_Q95_D20,
    moving_block_bootstrap,
    moving_block_bootstrap_corridor,
    pooled_median,
    primary_outcome,
    secondary_outcome,
)
from market_chi.microstructure_v2 import (
    aggregate_mbp10_stream,
    sha256_file,
    validate_feature_gzip,
)
from market_chi.modal_identifiability import (
    canonical_depth_bases,
    spectral_metrics,
    strongest_mode,
    subspace_capture,
)
from tools.analyze_mnq_modal import LEVELS, NS, dense_state, load_rows, pca_depth


DATES = ("20260609", "20260610", "20260611")
KS = (2, 6, 10)
MIN_COVERAGE = 0.80
MIN_PRIMARY_WINDOWS_PER_DAY = 34
PRIMARY_MINUTES = 30
SENSITIVITY_MINUTES = 60
CORRIDOR_STARTS = {"08:30", "09:00", "09:30", "10:00", "10:30"}
PRIMARY_Q95 = ISOTROPIC_Q95_D20[6]


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


def iso_to_ns(text: str) -> int:
    return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp() * NS)


def base_date(date_text: str) -> datetime:
    return datetime.strptime(date_text, "%Y%m%d").replace(tzinfo=timezone.utc)


def specs(date_text: str, minutes: int) -> list[dict[str, object]]:
    if (21 * 60) % minutes:
        raise ValueError("window length must divide 21 mature-session hours")
    base = base_date(date_text)
    out = []
    for i in range((21 * 60) // minutes):
        start = base + timedelta(minutes=i * minutes)
        end = start + timedelta(minutes=minutes)
        out.append({
            "date": date_text,
            "label": f"{date_text}_{minutes}m_{i+1:02d}",
            "slot_index": i,
            "minutes": minutes,
            "start": iso(start),
            "end": iso(end),
            "start_hhmm": start.strftime("%H:%M"),
        })
    return out


def quarantine(path: Path) -> str | None:
    if not path.exists():
        return None
    i = 0
    while True:
        suffix = ".corrupt" if i == 0 else f".corrupt.{i}"
        target = path.with_name(path.name + suffix)
        if not target.exists():
            path.replace(target)
            return str(target)
        i += 1


def find_raw_file(data_root: Path, date_text: str, out_dir: Path) -> Path:
    # Same raw-data contract used by the development sweep.
    raw = (data_root / "MBR10_Data" / f"glbx-mdp3-{date_text}.mbp-10.csv.zst").resolve()
    if not raw.exists():
        raise FileNotFoundError(f"frozen holdout raw file not found: {raw}")
    return raw


def prepare_features(raw: Path, out_dir: Path, date_text: str) -> tuple[Path, Path, dict[str, object]]:
    features_dir = out_dir / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    feature = features_dir / f"glbx-mdp3-{date_text}.mbp-10.1000ms.holdout.features.v2.csv.gz"
    summary = features_dir / f"glbx-mdp3-{date_text}.mbp-10.1000ms.holdout.features.v2.summary.json"

    source_hash = sha256_file(raw)
    reuse_reason = None
    if feature.exists() and summary.exists():
        integrity = validate_feature_gzip(feature)
        try:
            meta = json.loads(summary.read_text(encoding="utf-8"))
        except Exception:
            meta = {}
        output_hash = sha256_file(feature) if feature.exists() else None
        if (
            integrity.get("valid")
            and meta.get("source_sha256") == source_hash
            and meta.get("output_sha256") == output_hash
        ):
            reuse_reason = "valid_frozen_runner_cache_reused"
            return feature, summary, {
                "raw_file": str(raw),
                "raw_sha256": source_hash,
                "feature_file": str(feature),
                "feature_sha256": output_hash,
                "cache_status": reuse_reason,
                "feature_integrity": integrity,
            }
        bad_feature = quarantine(feature)
        bad_summary = quarantine(summary)
        reuse_reason = {
            "reason": "invalid_cache_quarantined",
            "feature": bad_feature,
            "summary": bad_summary,
        }
    elif feature.exists() or summary.exists():
        bad_feature = quarantine(feature)
        bad_summary = quarantine(summary)
        reuse_reason = {
            "reason": "incomplete_cache_pair_quarantined",
            "feature": bad_feature,
            "summary": bad_summary,
        }

    meta = aggregate_mbp10_stream(raw, feature, summary, interval_ms=1000)
    integrity = validate_feature_gzip(feature)
    if not integrity.get("valid"):
        raise IOError(f"new holdout feature cache failed integrity: {integrity}")
    output_hash = sha256_file(feature)
    if meta.get("source_sha256") != source_hash or meta.get("output_sha256") != output_hash:
        raise IOError("new holdout feature hashes do not match extraction summary")
    return feature, summary, {
        "raw_file": str(raw),
        "raw_sha256": source_hash,
        "feature_file": str(feature),
        "feature_sha256": output_hash,
        "cache_status": "built_by_frozen_runner",
        "prior_cache_disposition": reuse_reason,
        "feature_integrity": integrity,
    }


def eligible_segment(
    rows: list[dict[str, str]],
    lo: int,
    hi: int,
) -> tuple[str, list[dict[str, str]] | None, dict[str, object]]:
    expected = int((hi - lo) / NS)
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        t = int(r["bin_start_ns"])
        if lo <= t < hi:
            key = ((r.get("instrument_id") or "").strip(), (r.get("symbol") or "").strip())
            groups[key].append(r)

    diagnostics = []
    eligible = []
    for key, rr in sorted(groups.items()):
        rr.sort(key=lambda x: int(x["bin_start_ns"]))
        observed = len({int(x["bin_start_ns"]) for x in rr})
        coverage = observed / expected if expected else 0.0
        first = int(rr[0]["bin_start_ns"]) if rr else None
        item = {
            "instrument_id": key[0],
            "symbol": key[1],
            "observed_event_seconds": observed,
            "coverage_fraction": coverage,
            "first_bin_start_ns": first,
            "start_observed": first == lo,
        }
        diagnostics.append(item)
        if coverage >= MIN_COVERAGE and first == lo:
            eligible.append((key, rr, item))

    info = {"segments": diagnostics, "eligible_segment_count": len(eligible)}
    if len(eligible) == 0:
        return "LOW_COVERAGE_OR_LATE_START", None, info
    if len(eligible) > 1:
        return "AMBIGUOUS_MULTI_INSTRUMENT", None, info
    key, rr, item = eligible[0]
    info["selected_segment"] = item
    return "ELIGIBLE", rr, info


def analyze_window(rows: list[dict[str, str]], spec: dict[str, object]) -> dict[str, object]:
    lo, hi = iso_to_ns(str(spec["start"])), iso_to_ns(str(spec["end"]))
    status, rr, seg = eligible_segment(rows, lo, hi)
    rec: dict[str, object] = {**spec, "segmentation": seg}
    if status != "ELIGIBLE" or rr is None:
        rec["status"] = status
        return rec
    try:
        d = dense_state(rr, lo, hi)
        ratio, vt, _, _ = pca_depth(d)
    except ValueError as exc:
        rec["status"] = "REFUSED_REPRESENTATION"
        rec["reason"] = str(exc)
        return rec

    bases = canonical_depth_bases(LEVELS)
    captures = {}
    strongest = {}
    for name in ("symmetric_depth", "bid_ask_imbalance", "depth_gradient", "side_gradient"):
        captures[name] = {
            str(k): subspace_capture(vt, bases[name], k=k)
            for k in KS
        }
        strongest[name] = strongest_mode(vt, bases[name])

    core = {
        str(k): min(
            captures["symmetric_depth"][str(k)],
            captures["bid_ask_imbalance"][str(k)],
        )
        for k in KS
    }
    rec["status"] = "COMPLETE"
    rec["metrics"] = {
        "semantic_capture": captures,
        "core_capture": core,
        "primary_margin_k6_vs_exact_isotropic_q95": core["6"] - PRIMARY_Q95,
        "rank_migration_gain_k6_minus_k2": core["6"] - core["2"],
        "strongest_mode": strongest,
        "spectral": spectral_metrics(ratio, ks=KS),
    }
    return rec


def save_checkpoint(path: Path, records: list[dict[str, object]], source_records: dict[str, object], code_commit: str | None) -> None:
    payload = {
        "schema_version": "mnq-q038-holdout-semantic-v1-checkpoint",
        "holdout_status": "OPENED_BY_FROZEN_Q038_RUNNER",
        "source_code_commit": code_commit,
        "source_records": source_records,
        "records": records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def day_slot_array(records: list[dict[str, object]], date_text: str, minutes: int, field: str) -> np.ndarray:
    n = (21 * 60) // minutes
    arr = np.full(n, np.nan, dtype=float)
    for r in records:
        if r.get("date") != date_text or r.get("minutes") != minutes:
            continue
        if r.get("status") != "COMPLETE":
            continue
        i = int(r["slot_index"])
        if field == "margin6":
            arr[i] = float(r["metrics"]["primary_margin_k6_vs_exact_isotropic_q95"])
        elif field == "gain6_2":
            arr[i] = float(r["metrics"]["rank_migration_gain_k6_minus_k2"])
        elif field == "core6":
            arr[i] = float(r["metrics"]["core_capture"]["6"])
        elif field == "core10":
            arr[i] = float(r["metrics"]["core_capture"]["10"])
        else:
            raise ValueError(field)
    return arr


def corridor_flags(date_text: str) -> np.ndarray:
    return np.array(
        [str(w["start_hhmm"]) in CORRIDOR_STARTS for w in specs(date_text, PRIMARY_MINUTES)],
        dtype=bool,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--code-commit", required=True)
    args = ap.parse_args()

    data_root = Path(args.data_root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_dir = out_path.parent
    checkpoint = out_path.with_suffix(".checkpoint.json")

    print("Q038 FROZEN HOLDOUT RUNNER", flush=True)
    print("Frozen commit:", args.code_commit, flush=True)
    print("This execution opens ONLY June 9-11 after the MFR-14 freeze.", flush=True)

    source_records: dict[str, object] = {}
    records: list[dict[str, object]] = []

    if checkpoint.exists():
        cp = json.loads(checkpoint.read_text(encoding="utf-8"))
        if (
            cp.get("schema_version") == "mnq-q038-holdout-semantic-v1-checkpoint"
            and cp.get("source_code_commit") == args.code_commit
        ):
            records = cp.get("records", [])
            source_records = cp.get("source_records", {})
            print(f"Resuming checkpoint with {len(records)} window records.", flush=True)

    done = {str(r["label"]) for r in records}

    for date_text in DATES:
        print(f"[source] locating sealed day {date_text}", flush=True)
        raw = find_raw_file(data_root, date_text, out_dir)
        feature, summary, src = prepare_features(raw, out_dir, date_text)
        source_records[date_text] = src

        day_start = base_date(date_text)
        lo = int(day_start.timestamp() * NS)
        hi = int((day_start + timedelta(hours=21)).timestamp() * NS)
        rows = load_rows(feature, lo, hi)
        if not rows:
            raise RuntimeError(f"no holdout feature rows found for {date_text} mature interval")

        for minutes in (PRIMARY_MINUTES, SENSITIVITY_MINUTES):
            for w in specs(date_text, minutes):
                if str(w["label"]) in done:
                    continue
                print(f"[{date_text} {minutes}m] {w['start_hhmm']}", flush=True)
                rec = analyze_window(rows, w)
                records.append(rec)
                done.add(str(w["label"]))
                save_checkpoint(checkpoint, records, source_records, args.code_commit)

    primary_counts = {}
    invalid_test_reasons = []
    for date_text in DATES:
        count = sum(
            r.get("date") == date_text
            and r.get("minutes") == PRIMARY_MINUTES
            and r.get("status") == "COMPLETE"
            for r in records
        )
        primary_counts[date_text] = count
        if count < MIN_PRIMARY_WINDOWS_PER_DAY:
            invalid_test_reasons.append(
                f"{date_text} has {count}/42 eligible primary windows; minimum is {MIN_PRIMARY_WINDOWS_PER_DAY}"
            )

    adjudication: dict[str, object]
    if invalid_test_reasons:
        adjudication = {
            "primary_outcome": "INVALID_TEST",
            "reasons": invalid_test_reasons,
            "primary_bootstrap": None,
            "block_sensitivities": None,
            "secondary_outcome": "NOT_TESTED",
        }
    else:
        margin_days = [
            day_slot_array(records, d, PRIMARY_MINUTES, "margin6")
            for d in DATES
        ]
        boot4 = moving_block_bootstrap(
            margin_days,
            pooled_median,
            block_length=4,
            reps=10_000,
            seed=20260927,
        )
        boot2 = moving_block_bootstrap(
            margin_days,
            pooled_median,
            block_length=2,
            reps=10_000,
            seed=20260927,
        )
        boot6 = moving_block_bootstrap(
            margin_days,
            pooled_median,
            block_length=6,
            reps=10_000,
            seed=20260927,
        )
        p_outcome = primary_outcome(boot4, [boot2, boot6])

        secondary = None
        s_outcome = "NOT_TESTED_PRIMARY_DID_NOT_SURVIVE"
        if p_outcome == "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST":
            gain_days = [
                day_slot_array(records, d, PRIMARY_MINUTES, "gain6_2")
                for d in DATES
            ]
            flags = [corridor_flags(d) for d in DATES]
            secondary = moving_block_bootstrap_corridor(
                gain_days,
                flags,
                block_length=4,
                reps=10_000,
                seed=20260928,
            )
            s_outcome = secondary_outcome(secondary)

        adjudication = {
            "primary_outcome": p_outcome,
            "exact_isotropic_null": {
                "dimension": 20,
                "k": 6,
                "distribution": "Beta(3,7)",
                "mean": 0.3,
                "q95": PRIMARY_Q95,
            },
            "primary_bootstrap": boot4.to_dict(),
            "block_sensitivities": {
                "1h_block_2_windows": boot2.to_dict(),
                "3h_block_6_windows": boot6.to_dict(),
            },
            "secondary_outcome": s_outcome,
            "secondary_bootstrap": secondary.to_dict() if secondary else None,
        }

    payload = {
        "schema_version": "mnq-q038-holdout-semantic-v1",
        "epistemic_status": "P1 frozen holdout execution",
        "claim_id": "Q038-P1-v1",
        "holdout_status": "OPENED_BY_FROZEN_Q038_RUNNER",
        "source_code_commit": args.code_commit,
        "time_rule": "ordinary UTC wall-clock",
        "dates": list(DATES),
        "primary": {
            "minutes": PRIMARY_MINUTES,
            "k": 6,
            "semantic_pair": ["symmetric_depth", "bid_ask_imbalance"],
            "core_definition": "minimum of the two fixed semantic captures",
            "margin_definition": "Core6 - exact isotropic Beta(3,7) q95",
            "minimum_complete_windows_per_day": MIN_PRIMARY_WINDOWS_PER_DAY,
        },
        "hierarchical_secondary": {
            "claim_id": "Q038-S1-v1",
            "corridor_start_times_utc": sorted(CORRIDOR_STARTS),
            "estimand": "median(Core6-Core2) in corridor minus outside corridor",
            "tested_only_if_primary_survives": True,
        },
        "source_records": source_records,
        "primary_complete_windows_by_day": primary_counts,
        "adjudication": adjudication,
        "records": records,
        "notes": [
            "Scalar chi is not computed or licensed by this runner.",
            "k=10 and 60-minute results are non-decision-bearing sensitivities only.",
            "No alternate basis, k, threshold, session window or instrument is selected from holdout outcomes.",
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if checkpoint.exists():
        checkpoint.unlink()

    print("Q038 HOLDOUT EXECUTION COMPLETE", flush=True)
    print("Primary outcome:", adjudication["primary_outcome"], flush=True)
    print("Upload only:", out_path, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
