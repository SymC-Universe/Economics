from __future__ import annotations

import json
from pathlib import Path

from .q039_source_v04 import (
    PREREG_COMMIT,
    SourceSpec,
    load_source_manifest,
    verify_external_apq_text,
    verify_source_spec,
)


NC7_RULE_SCHEMA = "q039-v0.4-nc7-context-rule-v1"


def load_nc7_context_rule(path: str | Path) -> dict[str, object]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if raw.get("schema_version") != NC7_RULE_SCHEMA:
        raise ValueError("wrong NC7 context-rule schema")
    if raw.get("prereg_commit") != PREREG_COMMIT:
        raise ValueError("NC7 context rule is not bound to canonical v0.4 preregistration")
    if raw.get("status") != "FROZEN":
        raise ValueError("NC7 context rule is not frozen")
    if not str(raw.get("context_rule", "")).strip():
        raise ValueError("NC7 context rule is empty")
    if not str(raw.get("adjudication_source", "")).strip():
        raise ValueError("NC7 context rule lacks adjudication provenance")
    return raw


def production_preflight(
    *,
    external_review_text: str,
    source_manifest_path: str | Path,
    nc7_rule_path: str | Path,
    verify_hashes: bool = True,
) -> dict[str, object]:
    apq = verify_external_apq_text(external_review_text)
    sources = load_source_manifest(source_manifest_path)
    nc7 = load_nc7_context_rule(nc7_rule_path)

    verified_sources = []
    if verify_hashes:
        for date_text, spec in sorted(sources.items()):
            p = verify_source_spec(spec)
            verified_sources.append({
                "date": date_text,
                "feature_file": str(p),
                "feature_sha256": spec.feature_sha256,
                "instrument_id": spec.instrument_id,
                "symbol": spec.symbol,
            })
    else:
        verified_sources = [
            {
                "date": d,
                "feature_file": s.feature_file,
                "feature_sha256": s.feature_sha256,
                "instrument_id": s.instrument_id,
                "symbol": s.symbol,
            }
            for d, s in sorted(sources.items())
        ]

    return {
        "disposition": "Q039_V0_4_PRODUCTION_PREFLIGHT_PASS",
        "scientific_outcomes_opened": False,
        "prereg_commit": PREREG_COMMIT,
        "external_apq": apq,
        "sources": verified_sources,
        "nc7_context_rule": nc7,
        "note": (
            "This preflight validates identities and frozen gates only. "
            "It does not compute Layer R, Layer L, NC7, or any market outcome."
        ),
    }
