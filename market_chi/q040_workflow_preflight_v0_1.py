#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "qualification" / "Q040_COMPUTE_CONVEYOR_QUEUE_v0.1.json"
OUT = ROOT / "qualification" / "results" / "q040_workflow_preflight"
OUT.mkdir(parents=True, exist_ok=True)

required = [
    ROOT / "WORKING_INVESTIGATION.md",
    ROOT / "qualification" / "Q040_WORKFLOW_v0.1_2026-09-28.md",
    ROOT / "qualification" / "Q040_RECOVERABILITY_EROSION_HYPOTHESIS_SEED_2026-09-28.md",
    ROOT / "qualification" / "Q040_PRIOR_ART_NOVELTY_FOUNDATION_v0.1_2026-09-28.md",
    ROOT / "qualification" / "Q040_RECOVERY_THEORY_FOUNDATION_v0.1_2026-09-28.md",
    ROOT / "qualification" / "Q040_RECOVERABILITY_PLAN_PACKET_v0.1_2026-09-28.md",
]

missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
queue = json.loads(QUEUE.read_text()) if QUEUE.exists() else {}
governance_ok = queue.get("governance") == "SymC GOM v1.0"
real_data_enabled = bool(queue.get("real_data_enabled", False))
ready_real_tasks = [
    t.get("id") for t in queue.get("tasks", [])
    if t.get("status") == "READY" and t.get("real_data", False)
]

if missing:
    disposition = "WORKFLOW_PREFLIGHT_MISSING_ARTIFACT"
elif not governance_ok:
    disposition = "WORKFLOW_PREFLIGHT_GOVERNANCE_MISMATCH"
elif real_data_enabled or ready_real_tasks:
    disposition = "WORKFLOW_PREFLIGHT_REAL_DATA_FIREWALL_FAIL"
else:
    disposition = "WORKFLOW_PREFLIGHT_PASS"

result = {
    "disposition": disposition,
    "governance_ok": governance_ok,
    "real_data_enabled": real_data_enabled,
    "ready_real_tasks": ready_real_tasks,
    "missing_required_artifacts": missing,
    "scientific_authority": False,
    "note": "This preflight validates workflow plumbing only. It does not qualify any scientific representation, threshold, model, or claim."
}
(OUT / "result.json").write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
raise SystemExit(0 if disposition == "WORKFLOW_PREFLIGHT_PASS" else 2)
