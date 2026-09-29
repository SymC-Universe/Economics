#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from market_chi.q039_nc7_v04 import qualify_synthetic_timing_fixture

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qualification" / "results" / "q039_v04_nc7_preflight"
OUT.mkdir(parents=True, exist_ok=True)

result = qualify_synthetic_timing_fixture(worlds=200, base_seed=20261001)
payload = {
    "schema_version": "q039-v0.4-nc7-implementation-preflight-v1",
    "governance": "SymC GOM v1.0",
    "preregistration_commit": "b757d0dd65a700be1bf1d2cb5233c75c83086308",
    **result,
}
(OUT / "result.json").write_text(json.dumps(payload, indent=2))
print(json.dumps(payload, indent=2))
raise SystemExit(0 if payload["disposition"] == "NC7_IMPLEMENTATION_PREFLIGHT_PASS" else 2)
