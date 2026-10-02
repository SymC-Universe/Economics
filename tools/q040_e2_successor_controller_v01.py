#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

SCALES=(15,30,60,300)

def now():
    return datetime.now(timezone.utc).isoformat()

def dump(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",required=True)
    ap.add_argument("--b2-run-dir",required=True)
    ap.add_argument("--run-dir",required=True)
    args=ap.parse_args()

    root=Path(args.repo_root)
    b2=Path(args.b2_run_dir)
    run=Path(args.run_dir)
    run.mkdir(parents=True,exist_ok=True)
    status_path=run/"controller_status.json"
    env=os.environ.copy()
    env["PYTHONPATH"]=str(root)+os.pathsep+env.get("PYTHONPATH","")

    status={
        "run_id":"Q040_METRIC_EVENT_E2_V01",
        "scientific_stage":"E2_METRIC_EVENT_HORIZON_SELECTION",
        "state":"EXTERNAL_BLOCK",
        "execution_substate":"WAITING_FOR_B2",
        "started_at":now(),
        "b2_status_path":str(b2/"controller_status.json"),
        "real_q040_outcomes":"SEALED",
        "cost_rule":"ZERO_COST_LOCAL_ONLY_GITHUB_NO_PAID_COMPUTE",
        "authorized_next_action":"Wait for durable B2 PASS. Do not launch E2 on refusal/failure.",
    }
    dump(status_path,status)

    while True:
        p=b2/"controller_status.json"
        if not p.exists():
            time.sleep(20); continue
        b=json.loads(p.read_text(encoding="utf-8"))
        state=b.get("state")
        disp=b.get("disposition")
        if state=="RUNNING_LOCAL":
            time.sleep(20); continue
        if state=="ADVANCED_CHECKPOINT" and disp=="Q040_BASELINE_SELECTION_B2_PASS":
            break
        status["state"]="SCIENTIFIC_GATE" if state=="SCIENTIFIC_GATE" else "EXTERNAL_BLOCK"
        status["execution_substate"]="UPSTREAM_B2_NOT_PASS"
        status["upstream_state"]=state
        status["upstream_disposition"]=disp
        status["completed_at"]=now()
        status["authorized_next_action"]="Interpret/recover B2; E2 not launched."
        dump(status_path,status)
        return 4

    baseline=b2/"combined.json"
    if not baseline.exists():
        status["state"]="EXECUTION_FAILURE"
        status["execution_substate"]="MISSING_B2_RESULT"
        status["completed_at"]=now()
        dump(status_path,status)
        return 5

    status["state"]="ACTIVE_COMPUTE"
    status["execution_substate"]="RUNNING_LOCAL"
    status["b2_disposition"]="Q040_BASELINE_SELECTION_B2_PASS"
    status["b2_combined_sha256"]=sha256(baseline)
    status["child_processes"]={}
    status["completed_scales"]=[]
    status["failed_scales"]=[]
    status["authorized_next_action"]="Combine E2 only after all four scale shards exit 0."
    dump(status_path,status)

    tool=root/"tools"/"q040_metric_event_selection_e2_v01.py"
    comb=root/"tools"/"q040_metric_event_combine_e2_v01.py"
    procs={}
    for scale in SCALES:
        prefix=run/f"scale_{scale}"
        so=(run/f"scale_{scale}.stdout.log").open("w",encoding="utf-8")
        se=(run/f"scale_{scale}.stderr.log").open("w",encoding="utf-8")
        p=subprocess.Popen(
            [sys.executable,str(tool),"--scale",str(scale),
             "--baseline-result",str(baseline),"--output-prefix",str(prefix)],
            cwd=str(root),stdout=so,stderr=se,env=env,
        )
        procs[scale]=(p,so,se)
        status["child_processes"][str(scale)]={"pid":p.pid,"output_prefix":str(prefix)}
        dump(status_path,status)

    exits={}
    for scale in SCALES:
        p,so,se=procs[scale]
        code=p.wait();so.close();se.close()
        exits[str(scale)]=code
        if code==0:
            status["completed_scales"].append(scale)
        else:
            status["failed_scales"].append(scale)
        status["exit_codes"]=exits
        dump(status_path,status)

    if status["failed_scales"]:
        status["state"]="EXECUTION_FAILURE"
        status["execution_substate"]="EXECUTION_FAILURE"
        status["completed_at"]=now()
        status["authorized_next_action"]="Inspect failed E2 shard logs; resume only failed scales."
        dump(status_path,status)
        return 2

    combined=run/"combined.json"
    so=(run/"combine.stdout.log").open("w",encoding="utf-8")
    se=(run/"combine.stderr.log").open("w",encoding="utf-8")
    c=subprocess.run(
        [sys.executable,str(comb),"--input-dir",str(run),"--output",str(combined)],
        cwd=str(root),stdout=so,stderr=se,env=env,
    )
    so.close();se.close()
    status["combine_exit_code"]=c.returncode
    if combined.exists():
        result=json.loads(combined.read_text(encoding="utf-8"))
        status["combined_output"]=str(combined)
        status["combined_sha256"]=sha256(combined)
        status["disposition"]=result.get("disposition")
        status["selected_metric_event_tuple"]=result.get("selected_metric_event_tuple")
        status["horizon"]=result.get("horizon",{}).get("horizon")
        status["horizon_qualifier"]=result.get("horizon",{}).get("qualifier")
        status["faults"]=result.get("faults",[])
    status["completed_at"]=now()

    if c.returncode==0:
        status["state"]="ADVANCED_CHECKPOINT"
        status["execution_substate"]="RESULT_VERIFIED"
        status["authorized_next_action"]="Freeze selected E2 pipeline and implement/run confirmatory C-bank successor only under the frozen v0.1 closure."
    else:
        status["state"]="SCIENTIFIC_GATE"
        status["execution_substate"]="RESULT_READY"
        status["authorized_next_action"]="Interpret E2 refusal; do not launch confirmatory C bank."
    dump(status_path,status)
    return c.returncode

if __name__=="__main__":
    raise SystemExit(main())
