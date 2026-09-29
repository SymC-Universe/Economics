#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from market_chi.q039_layer_l_v04 import (
    run_factor2_truth,
    run_p60_ordered_truth,
    run_order_specificity,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qualification" / "results" / "q039_v04_synthetic_layer_l"
OUT.mkdir(parents=True, exist_ok=True)

tests = {
    "NC1": run_factor2_truth("phase_only", base_seed=20261011, reps=10_000),
    "NC2": run_factor2_truth("coarse_sufficient", base_seed=20261012, reps=10_000),
    "NC2B": run_factor2_truth("latent_regime", base_seed=20261013, reps=10_000),
    "NC3": run_factor2_truth("semantic_recency", base_seed=20261014, reps=10_000),
    "NC4": run_p60_ordered_truth(base_seed=20261015, reps=10_000),
    "NC5": run_order_specificity(base_seed=20261015, permutation_seed=20261002, permutations=200),
}

passes = {
    "NC1": tests["NC1"].get("label") != "LAST_FAST_SEMANTIC_ADDS_P0D",
    "NC2": tests["NC2"].get("label") != "LAST_FAST_SEMANTIC_ADDS_P0D",
    "NC2B": tests["NC2B"].get("label") != "LAST_FAST_SEMANTIC_ADDS_P0D",
    "NC3": tests["NC3"].get("label") == "LAST_FAST_SEMANTIC_ADDS_P0D",
    "NC4": tests["NC4"].get("label") == "ORDERED_SEMANTIC_PATH_ADDS_P0D",
    "NC5": bool(tests["NC5"].get("passes")),
}

payload = {
    "schema_version": "q039-v0.4-layer-l-known-truth-v1",
    "governance": "SymC GOM v1.0",
    "real_data_used": False,
    "preregistration_commit": "b757d0dd65a700be1bf1d2cb5233c75c83086308",
    "tests": tests,
    "passes": passes,
    "disposition": "LAYER_L_KNOWN_TRUTHS_PASS" if all(passes.values()) else "LAYER_L_KNOWN_TRUTHS_FAIL",
}
(OUT / "result.json").write_text(json.dumps(payload, indent=2))
print(json.dumps({"disposition": payload["disposition"], "passes": passes}, indent=2))
raise SystemExit(0 if all(passes.values()) else 2)
