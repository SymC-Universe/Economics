#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from market_chi.q040_synthetic_generators_v0_1 import audit_generator, generate_control

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"qualification"/"Q040_SYNTHETIC_KNOWN_TRUTH_MANIFEST_v0.1_2026-09-30.json"
OUT=ROOT/"qualification"/"results"/"q040_synthetic_generator_contract"
OUT.mkdir(parents=True, exist_ok=True)

m=json.loads(MANIFEST.read_text())
base=int(m["base_seed"])
audits=[]
for item in m["controls"]:
    ordinal=int(item["ordinal"])
    seed=int(np.random.SeedSequence([base,ordinal]).generate_state(1,dtype=np.uint32)[0])
    data=generate_control(item["id"],seed=seed,n=int(m["generator_contract_points"]))
    audits.append(audit_generator(item["id"],data).to_dict())

faults=[a["control_id"] for a in audits if not a["pass_invariant"]]
result={
  "disposition":"Q040_SYNTHETIC_GENERATOR_CONTRACT_PASS" if not faults else "Q040_SYNTHETIC_GENERATOR_CONTRACT_FAIL",
  "scientific_authority":False,
  "real_data_used":False,
  "estimator_qualified":False,
  "control_count":len(audits),
  "failed_controls":faults,
  "audits":audits,
  "note":"Generator-contract stage only. A pass does not qualify Q040 estimators, thresholds, K1/K2, representations, or real-data execution."
}
(OUT/"result.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if not faults else 2)
