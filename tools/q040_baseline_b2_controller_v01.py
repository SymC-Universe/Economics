#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

SCALES = (15, 30, 60, 300)

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--run-dir", required=True)
    args=ap.parse_args()

    root=Path(args.repo_root)
    run=Path(args.run_dir)
    run.mkdir(parents=True, exist_ok=True)
    status_path=run/"controller_status.json"
    shard_tool=root/"tools"/"q040_baseline_selection_v02.py"
    combiner=root/"tools"/"q040_baseline_combine_v02.py"
    python=Path(sys.executable)

    status={
        "run_id":"Q040_BASELINE_B2_V02",
        "scientific_stage":"DISJOINT_B2_BASELINE_QUALIFICATION",
        "state":"RUNNING_LOCAL",
        "execution_substate":"RUNNING_LOCAL",
        "started_at":now(),
        "repo_root":str(root),
        "run_dir":str(run),
        "python":str(python),
        "candidate_windows":[480,640],
        "seed_namespace":"1100+r",
        "real_q040_outcomes":"SEALED",
        "cost_rule":"ZERO_COST_LOCAL_ONLY_GITHUB_NO_PAID_COMPUTE",
        "child_processes":{},
        "completed_scales":[],
        "failed_scales":[],
        "authorized_next_action":"Combine B2 only after all four shards exit 0.",
    }
    dump(status_path,status)

    procs={}
    logs={}
    for scale in SCALES:
        out=run/f"scale_{scale}.json"
        stdout=run/f"scale_{scale}.stdout.log"
        stderr=run/f"scale_{scale}.stderr.log"
        so=stdout.open("w", encoding="utf-8")
        se=stderr.open("w", encoding="utf-8")
        p=subprocess.Popen(
            [str(python), str(shard_tool), "--scale", str(scale), "--output", str(out)],
            cwd=str(root), stdout=so, stderr=se,
        )
        procs[scale]=(p,so,se,out)
        logs[scale]=(stdout,stderr)
        status["child_processes"][str(scale)]={
            "pid":p.pid,"output":str(out),"stdout":str(stdout),"stderr":str(stderr)
        }
        dump(status_path,status)

    exit_codes={}
    for scale in SCALES:
        p,so,se,out=procs[scale]
        code=p.wait()
        so.close(); se.close()
        exit_codes[str(scale)]=code
        if code==0 and out.exists():
            status["completed_scales"].append(scale)
        else:
            status["failed_scales"].append(scale)
        status["exit_codes"]=exit_codes
        dump(status_path,status)

    if status["failed_scales"]:
        status["state"]="EXECUTION_FAILURE"
        status["execution_substate"]="EXECUTION_FAILURE"
        status["completed_at"]=now()
        status["authorized_next_action"]="Inspect failed shard logs; resume only failed scale(s)."
        dump(status_path,status)
        return 2

    combined=run/"combined.json"
    co=(run/"combine.stdout.log").open("w", encoding="utf-8")
    ce=(run/"combine.stderr.log").open("w", encoding="utf-8")
    c=subprocess.run(
        [str(python), str(combiner), "--input-dir", str(run), "--output", str(combined)],
        cwd=str(root), stdout=co, stderr=ce,
    )
    co.close(); ce.close()
    status["combine_exit_code"]=c.returncode
    if not combined.exists():
        status["state"]="EXECUTION_FAILURE"
        status["execution_substate"]="EXECUTION_FAILURE"
        status["completed_at"]=now()
        status["authorized_next_action"]="Inspect combine logs; do not rerun completed shards."
        dump(status_path,status)
        return 3

    result=json.loads(combined.read_text(encoding="utf-8"))
    status["combined_output"]=str(combined)
    status["combined_sha256"]=sha256(combined)
    status["disposition"]=result.get("disposition")
    status["selected_global_baseline"]=result.get("selected_global_baseline")
    status["faults"]=result.get("faults",[])
    status["completed_at"]=now()
    if c.returncode==0:
        status["state"]="ADVANCED_CHECKPOINT"
        status["execution_substate"]="RESULT_VERIFIED"
        status["authorized_next_action"]="Freeze selected global baseline and proceed to D1/D2 only if B2 disposition is PASS."
    else:
        status["state"]="SCIENTIFIC_GATE"
        status["execution_substate"]="RESULT_READY"
        status["authorized_next_action"]="Interpret B2 refusal; do not open D1/D2 or real Q040 outcomes."
    dump(status_path,status)
    return c.returncode

if __name__=="__main__":
    raise SystemExit(main())
