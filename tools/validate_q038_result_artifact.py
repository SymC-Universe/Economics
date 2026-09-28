#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

FROZEN_COMMIT = "d8a44204514a8111f524ef122d110714d9bafa29"
DATES = ["20260609", "20260610", "20260611"]
PRIMARY_OUTCOMES = {"EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST","EMPIRICAL_CLAIM_FALSIFIED","INDETERMINATE","INVALID_TEST"}

def validate(payload: dict) -> list[str]:
    errors = []
    def need(cond, msg):
        if not cond:
            errors.append(msg)
    need(payload.get("schema_version") == "mnq-q038-holdout-semantic-v1", "schema_version mismatch")
    need(payload.get("claim_id") == "Q038-P1-v1", "claim_id mismatch")
    need(payload.get("source_code_commit") == FROZEN_COMMIT, "frozen execution commit mismatch")
    need(payload.get("dates") == DATES, "holdout date set/order mismatch")
    need(payload.get("holdout_status") == "OPENED_BY_FROZEN_Q038_RUNNER", "holdout_status mismatch")
    primary = payload.get("primary") or {}
    need(primary.get("minutes") == 30, "primary window must remain 30 minutes")
    need(primary.get("k") == 6, "primary k must remain 6")
    need(primary.get("semantic_pair") == ["symmetric_depth", "bid_ask_imbalance"], "semantic pair mismatch")
    adjud = payload.get("adjudication") or {}
    need(adjud.get("primary_outcome") in PRIMARY_OUTCOMES, "primary outcome outside frozen namespace")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result_json")
    args = ap.parse_args()
    payload = json.loads(Path(args.result_json).read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        print(json.dumps({"status":"INVALID_Q038_RESULT_ARTIFACT","errors":errors}, indent=2))
        return 2
    print(json.dumps({"status":"Q038_RESULT_ARTIFACT_IDENTITY_VALID","primary_outcome":payload["adjudication"]["primary_outcome"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
