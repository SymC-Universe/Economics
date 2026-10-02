#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
import numpy as np


def candidate_key(x: dict) -> tuple:
    return (
        0 if x["eligible"] else 1,
        float(x["median_normalized_baseline_error"]),
        0 if x["kind"] == "K1" else 1,
        int(x["window"]),
    )


def summarize(rows: list[dict]) -> list[dict]:
    grouped=defaultdict(list)
    for r in rows:
        grouped[(r["kind"],int(r["window"]))].append(r)
    out=[]
    for (kind,window), vals in grouped.items():
        refusals=[x for x in vals if x["status"]!="PASS_NUMERIC_COVERAGE"]
        finite=[float(x["median_error"]) for x in vals if math.isfinite(float(x["median_error"]))]
        out.append({
            "kind":kind,
            "window":window,
            "worlds":len(vals),
            "refused_worlds":len(refusals),
            "min_coverage":float(min(float(x["coverage"]) for x in vals)),
            "median_coverage":float(np.median([float(x["coverage"]) for x in vals])),
            "median_normalized_baseline_error":float(np.median(finite)) if finite else math.inf,
            "eligible":len(refusals)==0,
        })
    return sorted(out,key=candidate_key)


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    base=Path(args.input_dir)
    result={
        "schema_version":"q040-baseline-selection-combined-v1",
        "real_q040_outcomes_opened":False,
        "scales":{},
    }
    faults=[]
    for scale in (15,30,60,300):
        p=base/f"scale_{scale}.json"
        if not p.exists():
            faults.append(f"missing:{p}")
            continue
        data=json.loads(p.read_text())
        ranked=summarize(data["scores"])
        result["scales"][str(scale)]={
            "ranked_candidates":ranked,
            "provisional_top":ranked[0] if ranked else None,
            "eligible_count":sum(bool(x["eligible"]) for x in ranked),
        }
        if not any(bool(x["eligible"]) for x in ranked):
            faults.append(f"no_eligible_baseline:{scale}")
    result["faults"]=faults
    result["disposition"]=(
        "Q040_BASELINE_SELECTION_BANK_PASS"
        if not faults else
        "Q040_BASELINE_OPERATOR_REFUSED_OR_INCOMPLETE"
    )
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
        "disposition":result["disposition"],
        "faults":faults,
        "provisional_top":{
            k:v["provisional_top"] for k,v in result["scales"].items()
        },
    },indent=2))
    return 0 if not faults else 2

if __name__=="__main__":
    raise SystemExit(main())
