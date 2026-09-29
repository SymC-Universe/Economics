#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from market_chi.q039_production_gate_v04 import production_preflight


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external-review", required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--nc7-rule", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    external_text = Path(args.external_review).read_text(
        encoding="utf-8", errors="replace"
    )
    result = production_preflight(
        external_review_text=external_text,
        source_manifest_path=args.source_manifest,
        nc7_rule_path=args.nc7_rule,
        verify_hashes=True,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "disposition": result["disposition"],
        "scientific_outcomes_opened": False,
        "out": str(out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
