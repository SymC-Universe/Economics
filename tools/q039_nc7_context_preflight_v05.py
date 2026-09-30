#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from market_chi.q039_nc7_context_v05 import qualify_synthetic_context_fixture


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qualification" / "results" / "q039_v05_nc7_context_preflight"
OUT.mkdir(parents=True, exist_ok=True)

result = qualify_synthetic_context_fixture(worlds=200)
(OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))

if result["disposition"] != "NC7_DERIVED_CONTEXT_IMPLEMENTATION_PREFLIGHT_PASS":
    raise SystemExit(2)
