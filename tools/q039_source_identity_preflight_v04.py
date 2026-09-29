#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from market_chi.q039_source_v04 import (
    DATES,
    candidate_identity_scan,
)


def find_feature(root: Path, date_text: str) -> Path:
    matches = sorted(
        p.resolve()
        for p in root.rglob(f"*{date_text}*.features.v2.csv.gz")
        if "q038" not in str(p).lower() and "holdout" not in str(p).lower()
    )
    if len(matches) != 1:
        raise RuntimeError(
            f"{date_text}: expected exactly one non-holdout v2 feature file, "
            f"found {len(matches)}: {[str(x) for x in matches]}"
        )
    return matches[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features-root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.features_root).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()

    records = []
    for date_text in DATES:
        feature = find_feature(root, date_text)
        records.append(candidate_identity_scan(feature, date_text))

    payload = {
        "schema_version": "q039-v0.4-source-identity-candidate-scan-v1",
        "scientific_outcomes_opened": False,
        "selection_made": False,
        "dates": list(DATES),
        "records": records,
        "instructions": [
            "This file is mechanical identity/provenance only.",
            "Do not choose an instrument from Q039 outcomes.",
            "Freeze exactly one instrument_id/symbol and the recorded feature SHA-256 per date in q039-v0.4-source-freeze-v1 before production execution.",
            "Q038 June 9-11 are prohibited.",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({
        "schema_version": payload["schema_version"],
        "selection_made": False,
        "dates": list(DATES),
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
