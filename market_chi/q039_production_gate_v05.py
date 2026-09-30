from __future__ import annotations

import json
from pathlib import Path

from .q039_source_v05 import (
    PLAN_DOCUMENTATION_CLOSURE_COMMIT,
    PLAN_REVIEWED_COMMIT,
    RECHECK_ADJUDICATION_COMMIT,
    load_source_manifest,
    verify_source_spec,
)

REQUIRED_RECHECK_TOKEN = "Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION_CLOSED"


def verify_recheck_adjudication(text: str) -> dict[str, str]:
    required = [
        REQUIRED_RECHECK_TOKEN,
        PLAN_REVIEWED_COMMIT,
        PLAN_DOCUMENTATION_CLOSURE_COMMIT,
    ]
    missing = [x for x in required if x not in text]
    if missing:
        raise RuntimeError("Q039 v0.5 recheck adjudication binding missing: " + ",".join(missing))
    return {
        "status": REQUIRED_RECHECK_TOKEN,
        "reviewed_plan_commit": PLAN_REVIEWED_COMMIT,
        "documentation_closure_commit": PLAN_DOCUMENTATION_CLOSURE_COMMIT,
        "recheck_adjudication_commit": RECHECK_ADJUDICATION_COMMIT,
    }


def production_identity_preflight(
    *,
    adjudication_text: str,
    source_manifest_path: str | Path,
    verify_hashes: bool = True,
) -> dict[str, object]:
    recheck = verify_recheck_adjudication(adjudication_text)
    sources = load_source_manifest(source_manifest_path)
    verified = []
    for date_text, spec in sorted(sources.items()):
        p = verify_source_spec(spec) if verify_hashes else Path(spec.feature_file)
        verified.append({
            "date": date_text,
            "feature_file": str(p),
            "feature_sha256": spec.feature_sha256,
            "instrument_id": spec.instrument_id,
            "symbol": spec.symbol,
        })

    return {
        "disposition": "Q039_V0_5_PRODUCTION_IDENTITY_PREFLIGHT_PASS",
        "scientific_outcomes_opened": False,
        "recheck": recheck,
        "sources": verified,
        "note": (
            "Identity/provenance preflight only. It does not compute Layer R, "
            "Layer L, scientific NC7, or any market outcome."
        ),
    }
