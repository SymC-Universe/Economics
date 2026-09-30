#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from market_chi.q039_production_gate_v05 import production_identity_preflight
from market_chi.q039_production_v05 import (
    DATES,
    NC7_WORLDS,
    aggregate_nc7_and_finalize,
    aggregate_real,
    process_nc7_world,
    process_real_day,
    read_json,
    write_json_atomic,
    _load_dense,
)
from market_chi.q039_source_v05 import load_source_manifest


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _status(path: Path, **kwargs) -> None:
    state = {
        "schema_version": "q039-v0.5-local-run-status-v1",
        "updated_at": _utc_now(),
        **kwargs,
    }
    write_json_atomic(path, state)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adjudication", required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--stage", choices=("real", "nc7", "all"), default="all")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    status_path = out_dir / "CONTINUITY_STATUS.json"

    adjudication_text = Path(args.adjudication).read_text(
        encoding="utf-8", errors="replace"
    )
    _status(
        status_path,
        continuity_state="ACTIVE_COMPUTE",
        current_stage="IDENTITY_PREFLIGHT",
        real_outcomes_opened=False,
        next_action="verify exact five-source hashes and recheck binding",
    )

    preflight = production_identity_preflight(
        adjudication_text=adjudication_text,
        source_manifest_path=args.source_manifest,
        verify_hashes=True,
    )
    write_json_atomic(out_dir / "identity_preflight.json", preflight)
    specs = load_source_manifest(args.source_manifest)

    real_days = []
    if args.stage in ("real", "all"):
        for i, date_text in enumerate(DATES):
            _status(
                status_path,
                continuity_state="ACTIVE_COMPUTE",
                current_stage="REAL_DAY",
                current_item=date_text,
                completed_real_days=i,
                total_real_days=len(DATES),
                real_outcomes_opened=i > 0,
                next_action="process next frozen development day without retuning",
            )
            day = process_real_day(specs[date_text], out_dir=out_dir)
            real_days.append(day)

        _status(
            status_path,
            continuity_state="ACTIVE_COMPUTE",
            current_stage="REAL_AGGREGATION",
            completed_real_days=len(DATES),
            total_real_days=len(DATES),
            real_outcomes_opened=True,
            next_action="freeze real Layer R/Layer L aggregate before NC7",
        )
        real_aggregate = aggregate_real(real_days, out_dir=out_dir)
        _status(
            status_path,
            continuity_state="ADVANCED_CHECKPOINT",
            current_stage="REAL_AGGREGATE_FROZEN",
            completed_real_days=len(DATES),
            real_outcomes_opened=True,
            next_action="execute 200-world matched-update-timing NC7",
        )
        if args.stage == "real":
            return 0
    else:
        real_aggregate = read_json(out_dir / "real" / "aggregate.json")
        for date_text in DATES:
            real_days.append(read_json(out_dir / "real" / date_text / "summary.json"))

    if args.stage in ("nc7", "all"):
        real_dense_by_day = {
            d: _load_dense(out_dir / "real" / d / "dense_state.npz")
            for d in DATES
        }
        worlds = []
        for w in range(NC7_WORLDS):
            _status(
                status_path,
                continuity_state="ACTIVE_COMPUTE",
                current_stage="NC7",
                current_item=f"world_{w:03d}",
                completed_nc7_worlds=w,
                total_nc7_worlds=NC7_WORLDS,
                real_outcomes_opened=True,
                next_action="continue frozen NC7 worlds; checkpoint each world",
            )
            worlds.append(
                process_nc7_world(
                    w,
                    out_dir=out_dir,
                    real_dense_by_day=real_dense_by_day,
                )
            )

        _status(
            status_path,
            continuity_state="ACTIVE_COMPUTE",
            current_stage="FINAL_CLASSIFICATION",
            completed_nc7_worlds=NC7_WORLDS,
            total_nc7_worlds=NC7_WORLDS,
            real_outcomes_opened=True,
            next_action="mechanically apply frozen classifications and NC7 q95 gates",
        )
        final = aggregate_nc7_and_finalize(
            worlds,
            real_aggregate=real_aggregate,
            real_days=real_days,
            out_dir=out_dir,
        )
        _status(
            status_path,
            continuity_state="ADVANCED_CHECKPOINT",
            current_stage="Q039_V0_5_P0D_COMPLETE",
            completed_nc7_worlds=NC7_WORLDS,
            total_nc7_worlds=NC7_WORLDS,
            real_outcomes_opened=True,
            final_result=str(out_dir / "Q039_V0_5_P0D_RESULT.json"),
            next_action="scientific interpretation / failure-outlier audit; do not retune automatically",
        )
        print(json.dumps({
            "disposition": final["status"],
            "result": str(out_dir / "Q039_V0_5_P0D_RESULT.json"),
            "status_file": str(status_path),
        }, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        # The wrapper intentionally does not rewrite a failed run into success.
        print(
            json.dumps({
                "disposition": "Q039_V0_5_P0D_EXECUTION_FAILED",
                "exception_type": type(exc).__name__,
                "exception": str(exc),
            }, indent=2),
            file=sys.stderr,
        )
        raise
