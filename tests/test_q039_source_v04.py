from __future__ import annotations

import json
import pytest

from market_chi.q039_source_v04 import (
    DATES,
    PREREG_COMMIT,
    load_source_manifest,
    verify_external_apq_text,
)


def test_external_apq_requires_exact_status_and_prereg_binding():
    good = (
        "APQ_EXTERNAL_STATUS=QUALIFIED\n"
        f"PREREG_COMMIT={PREREG_COMMIT}\n"
    )
    out = verify_external_apq_text(good)
    assert out["status"] == "APQ_EXTERNAL_STATUS=QUALIFIED"

    with pytest.raises(RuntimeError):
        verify_external_apq_text("APQ_EXTERNAL_STATUS=QUALIFIED\nPREREG_COMMIT=wrong")
    with pytest.raises(RuntimeError):
        verify_external_apq_text(f"APQ_EXTERNAL_STATUS=REVISE\nPREREG_COMMIT={PREREG_COMMIT}")


def test_source_manifest_requires_exact_five_dates_and_explicit_holdout_prohibition(tmp_path):
    sources = [
        {
            "date": d,
            "feature_file": f"/frozen/{d}.features.v2.csv.gz",
            "feature_sha256": "a" * 64,
            "instrument_id": str(i + 1),
            "symbol": "MNQ.c.0",
        }
        for i, d in enumerate(DATES)
    ]
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({
        "schema_version": "q039-v0.4-source-freeze-v1",
        "prereg_commit": PREREG_COMMIT,
        "q038_dates_allowed": False,
        "sources": sources,
    }))
    out = load_source_manifest(p)
    assert tuple(sorted(out)) == tuple(sorted(DATES))

    raw = json.loads(p.read_text())
    raw["q038_dates_allowed"] = True
    p.write_text(json.dumps(raw))
    with pytest.raises(ValueError):
        load_source_manifest(p)


def test_source_manifest_refuses_extra_or_missing_date(tmp_path):
    sources = [
        {
            "date": d,
            "feature_file": f"/frozen/{d}.features.v2.csv.gz",
            "feature_sha256": "b" * 64,
            "instrument_id": "1",
            "symbol": "MNQ.c.0",
        }
        for d in DATES[:-1]
    ]
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({
        "schema_version": "q039-v0.4-source-freeze-v1",
        "prereg_commit": PREREG_COMMIT,
        "q038_dates_allowed": False,
        "sources": sources,
    }))
    with pytest.raises(ValueError):
        load_source_manifest(p)
