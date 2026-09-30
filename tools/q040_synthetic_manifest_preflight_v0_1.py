#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "qualification" / "Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.1_2026-09-30.json"
OUT = ROOT / "qualification" / "results" / "q040_synthetic_manifest_preflight"
OUT.mkdir(parents=True, exist_ok=True)

m = json.loads(MANIFEST.read_text())
faults = []

expected = [
    "NC-R1","NC-R2","NC-R3","NC-R4","NC-R5","NC-R6","NC-R7","NC-R8",
    "NC-R9","NC-R10","NC-R11","NC-R12","NC-R13","NC-R14","NC-R15",
    "NC-R16","NC-R17","NC-R17b","NC-R18","NC-R19","NC-R20","NC-R21"
]
ids = [x.get("id") for x in m.get("controls", [])]
if ids != expected:
    faults.append("control_identity_or_order_mismatch")
if m.get("real_data_used") is not False:
    faults.append("real_data_used_must_be_false")
if m.get("real_outcomes_authorized") is not False:
    faults.append("real_outcomes_authorized_must_be_false")
if m.get("scales_seconds") != [15,30,60,300]:
    faults.append("scale_ladder_mismatch")
if m.get("primary_history_extension") != "M2_CUMULATIVE_BURDEN":
    faults.append("primary_history_extension_mismatch")
if m.get("primary_score") != "COMPETING_RISK_INTEGRATED_BRIER_SUSTAINED_RETURN_CIF":
    faults.append("primary_score_mismatch")
if m.get("primary_family_control", {}).get("method") != "HOLM_STEP_DOWN":
    faults.append("primary_family_method_mismatch")
if float(m.get("primary_family_control", {}).get("two_sided_familywise_alpha", -1)) != 0.05:
    faults.append("primary_family_alpha_mismatch")
if int(m.get("sparse_tail_min_qualifying_episodes_per_stratum", -1)) != 10:
    faults.append("sparse_tail_threshold_not_frozen")

base = int(m.get("base_seed", -1))
seeds = []
for item in m.get("controls", []):
    ordinal = int(item.get("ordinal", -1))
    if ordinal < 1:
        faults.append(f"invalid_ordinal:{item.get('id')}")
        continue
    ss = np.random.SeedSequence([base, ordinal])
    seeds.append(int(ss.generate_state(1, dtype=np.uint32)[0]))
if len(set(seeds)) != len(seeds):
    faults.append("nonunique_control_seeds")

result = {
    "disposition": "Q040_SYNTHETIC_MANIFEST_PREFLIGHT_PASS" if not faults else "Q040_SYNTHETIC_MANIFEST_PREFLIGHT_FAIL",
    "scientific_authority": False,
    "real_data_used": False,
    "control_count": len(ids),
    "seed_count": len(seeds),
    "unique_seed_count": len(set(seeds)),
    "faults": faults,
}
(OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if not faults else 2)
