#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from market_chi.q039_production_gate_v05 import production_identity_preflight


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--adjudication", required=True)
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()

    adj=Path(args.adjudication).read_text(encoding="utf-8",errors="replace")
    result=production_identity_preflight(
        adjudication_text=adj,
        source_manifest_path=args.source_manifest,
        verify_hashes=True,
    )
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "disposition":result["disposition"],
        "scientific_outcomes_opened":False,
        "verified_sources":len(result["sources"]),
        "out":str(out),
    },indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
