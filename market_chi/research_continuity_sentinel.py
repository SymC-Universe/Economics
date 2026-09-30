#!/usr/bin/env python3
"""Repository continuity sentinel for Economics research.

This script validates continuity metadata and sealed-data firewalls only.
It is not scientific authority and does not execute or adjudicate science.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "CONTINUITY_STATE.json"
WORKING_PATH = ROOT / "WORKING_INVESTIGATION.md"
Q039_QUEUE = ROOT / "qualification" / "Q039_COMPUTE_CONVEYOR_QUEUE_v0.5.json"
Q040_QUEUE = ROOT / "qualification" / "Q040_COMPUTE_CONVEYOR_QUEUE_v0.1.json"
OUT = ROOT / "qualification" / "results" / "continuity"
OUT.mkdir(parents=True, exist_ok=True)

ALLOWED = {"ACTIVE_COMPUTE", "ADVANCED_CHECKPOINT", "SCIENTIFIC_GATE", "EXTERNAL_BLOCK"}
EXEMPT = {"SCIENTIFIC_GATE", "EXTERNAL_BLOCK"}
REQUIRED_LANES = {"Q039", "Q040"}

faults: list[str] = []
warnings: list[str] = []

def load_json(path: Path):
    if not path.exists():
        faults.append(f"missing:{path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        faults.append(f"invalid_json:{path.relative_to(ROOT)}:{type(exc).__name__}")
        return {}

state = load_json(STATE_PATH)
q39 = load_json(Q039_QUEUE)
q40 = load_json(Q040_QUEUE)

if not WORKING_PATH.exists():
    faults.append("missing:WORKING_INVESTIGATION.md")
    working = ""
else:
    working = WORKING_PATH.read_text()

overall = state.get("overall_continuity_state")
if overall not in ALLOWED:
    faults.append(f"invalid_overall_state:{overall}")

lanes = state.get("lanes", {})
if set(lanes) != REQUIRED_LANES:
    faults.append(f"lane_set_mismatch:{sorted(lanes)}")

for lane_name in sorted(REQUIRED_LANES):
    lane = lanes.get(lane_name, {})
    lane_state = lane.get("continuity_state")
    if lane_state not in ALLOWED:
        faults.append(f"{lane_name}:invalid_state:{lane_state}")
    if not lane.get("last_verified_checkpoint"):
        faults.append(f"{lane_name}:missing_last_verified_checkpoint")
    if not lane.get("next_exact_authorized_action"):
        faults.append(f"{lane_name}:missing_next_exact_authorized_action")
    if not lane.get("execution_ceiling"):
        faults.append(f"{lane_name}:missing_execution_ceiling")
    if lane_state == "EXTERNAL_BLOCK" and not lane.get("external_block"):
        faults.append(f"{lane_name}:external_block_without_reason")
    if lane_state == "SCIENTIFIC_GATE" and not lane.get("scientific_gate"):
        faults.append(f"{lane_name}:scientific_gate_without_reason")
    if lane_state == "ACTIVE_COMPUTE" and not lane.get("active_execution"):
        faults.append(f"{lane_name}:active_compute_without_execution_id")

last = state.get("last_productive_advancement")
if last:
    try:
        ts = datetime.fromisoformat(last.replace("Z", "+00:00"))
        age_min = (datetime.now(timezone.utc) - ts).total_seconds() / 60.0
        threshold = float(state.get("continuity_controls", {}).get("stagnation_audit_minutes", 90))
        if overall not in EXEMPT and age_min > threshold:
            faults.append(f"stagnation:{age_min:.1f}min>{threshold:.1f}min")
    except Exception:
        faults.append("invalid_last_productive_advancement")
else:
    faults.append("missing_last_productive_advancement")

if state.get("protected_inputs", {}).get("q039_real_development_outcomes") != "SEALED":
    faults.append("q039_real_outcomes_not_sealed")
if state.get("protected_inputs", {}).get("q040_real_outcomes") != "SEALED":
    faults.append("q040_real_outcomes_not_sealed")
if state.get("protected_inputs", {}).get("q040_real_data_enabled") is not False:
    faults.append("q040_state_real_data_firewall_not_false")
if q039.get("real_data_enabled") is not False:
    faults.append("q039_queue_real_data_enabled")
if q040.get("real_data_enabled") is not False:
    faults.append("q040_queue_real_data_enabled")

for label, queue in (("Q039", q39), ("Q040", q40)):
    for task in queue.get("tasks", []):
        if task.get("real_data") and task.get("status") == "READY":
            faults.append(f"{label}:real_data_task_ready:{task.get('id')}")

for token in (
    "ECON_Q039_Q040_RECHECK_20260930_A",
    "Q039 v0.5",
    "Q040 v0.6",
    "EXTERNAL_BLOCK",
):
    if token not in working:
        faults.append(f"working_record_missing_token:{token}")

report = {
    "sentinel": "ECONOMICS_RESEARCH_CONTINUITY_SENTINEL_V1",
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "scientific_authority": False,
    "overall_state": overall,
    "active_execution_id": state.get("active_execution_id"),
    "faults": faults,
    "warnings": warnings,
    "result": "PASS" if not faults else "FAIL",
}
(OUT / "sentinel_summary.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
raise SystemExit(0 if not faults else 2)
