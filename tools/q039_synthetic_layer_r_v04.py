#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from market_chi.q039_layer_r_v04 import run_structural_known_truth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qualification" / "results" / "q039_v04_synthetic_layer_r"
OUT.mkdir(parents=True, exist_ok=True)

results = {
    "schema_version": "q039-v0.4-layer-r-known-truth-v1",
    "governance": "SymC GOM v1.0",
    "real_data_used": False,
    "preregistration_commit": "b757d0dd65a700be1bf1d2cb5233c75c83086308",
    "tests": {}
}

results["tests"]["NC6"] = run_structural_known_truth(
    "heavy_tail", base_seed=20261016, matched_draws=5000
)
results["tests"]["NC8"] = run_structural_known_truth(
    "calendar_common_mode", base_seed=20261018, matched_draws=5000
)
results["tests"]["NC8B"] = run_structural_known_truth(
    "persistent_common_mode",
    base_seed=20261019,
    matched_draws=5000,
    persistence=0.90,
    sym_innovation_sd=0.35,
    imb_innovation_sd=0.30,
    isotropic_noise_sd=0.30,
)

passes = {
    "NC6": results["tests"]["NC6"]["classification"]["status"] != "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D",
    "NC8": results["tests"]["NC8"]["classification"]["status"] != "STRUCTURE_SPECIFIC_PAIR_COHERENT_P0D",
    "NC8B": results["tests"]["NC8B"]["classification"]["status"] in {
        "CANONICAL_CAPTURE_ONLY_P0D", "STRUCTURAL_UNRESOLVED_P0D"
    },
}
results["passes"] = passes
results["disposition"] = (
    "LAYER_R_KNOWN_TRUTHS_PASS"
    if all(passes.values())
    else "LAYER_R_KNOWN_TRUTHS_FAIL"
)

(OUT / "result.json").write_text(json.dumps(results, indent=2))
print(json.dumps({"disposition": results["disposition"], "passes": passes}, indent=2))
raise SystemExit(0 if all(passes.values()) else 2)
