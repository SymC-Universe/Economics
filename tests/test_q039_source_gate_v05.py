from __future__ import annotations

import json
import pytest

from market_chi.q039_source_v05 import (
    DATES,
    PLAN_DOCUMENTATION_CLOSURE_COMMIT,
    PLAN_REVIEWED_COMMIT,
    RECHECK_ADJUDICATION_COMMIT,
    SOURCE_SCHEMA,
    load_source_manifest,
)
from market_chi.q039_production_gate_v05 import verify_recheck_adjudication


def _manifest():
    return {
        "schema_version": SOURCE_SCHEMA,
        "reviewed_plan_commit": PLAN_REVIEWED_COMMIT,
        "documentation_closure_commit": PLAN_DOCUMENTATION_CLOSURE_COMMIT,
        "recheck_adjudication_commit": RECHECK_ADJUDICATION_COMMIT,
        "q038_dates_allowed": False,
        "real_outcomes_opened": False,
        "sources": [
            {
                "date": d,
                "feature_file": f"/frozen/{d}.features.v2.csv.gz",
                "feature_sha256": "a" * 64,
                "instrument_id": "42004936",
                "symbol": "MNQ.c.0",
            }
            for d in DATES
        ],
    }


def test_v05_source_manifest_binds_exact_plan_chain(tmp_path):
    p=tmp_path/"manifest.json"
    p.write_text(json.dumps(_manifest()))
    out=load_source_manifest(p)
    assert tuple(sorted(out)) == tuple(sorted(DATES))

    raw=_manifest()
    raw["documentation_closure_commit"]="wrong"
    p.write_text(json.dumps(raw))
    with pytest.raises(ValueError):
        load_source_manifest(p)


def test_v05_recheck_adjudication_must_bind_closed_status():
    text=(
        "Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION_CLOSED\n"
        + PLAN_REVIEWED_COMMIT + "\n"
        + PLAN_DOCUMENTATION_CLOSURE_COMMIT + "\n"
    )
    out=verify_recheck_adjudication(text)
    assert out["status"] == "Q039_V0_5_RECHECK=PASS_WITH_MINOR_DOCUMENTATION_CLOSED"

    with pytest.raises(RuntimeError):
        verify_recheck_adjudication("Q039_V0_5_RECHECK=REVISE")
