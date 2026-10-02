#!/usr/bin/env python3
from __future__ import annotations

import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np

def key(x):
    return (
        0 if x["eligible"] else 1,
        float(x["median_normalized_baseline_error"]),
        0 if x["kind"]=="K1" else 1,
        int(x["window"]),
    )

def summarize(rows):
    g=defaultdict(list)
    for r in rows:
        g[(r["kind"],int(r["window"]))].append(r)
    out=[]
    for (kind,window),vals in g.items():
        refused=[x for x in vals if x["status"]!="PASS_NUMERIC_COVERAGE"]
        finite=[float(x["median_error"]) for x in vals if math.isfinite(float(x["median_error"]))]
        out.append({
            "kind":kind,"window":window,"worlds":len(vals),
            "refused_worlds":len(refused),
            "min_coverage":float(min(float(x["coverage"]) for x in vals)),
            "median_coverage":float(np.median([float(x["coverage"]) for x in vals])),
            "median_normalized_baseline_error":float(np.median(finite)) if finite else math.inf,
            "eligible":len(refused)==0,
        })
    return sorted(out,key=key)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    base=Path(args.input_dir)
    all_rows=[]; per_scale={}; faults=[]
    for scale in (15,30,60,300):
        p=base/f"scale_{scale}.json"
        if not p.exists():
            faults.append(f"missing:{scale}"); continue
        j=json.loads(p.read_text())
        rows=j["scores"]; all_rows.extend(rows)
        ranked=summarize(rows)
        per_scale[str(scale)]=ranked
    global_ranked=summarize(all_rows) if all_rows else []
    eligible=[x for x in global_ranked if x["eligible"]]
    selected=eligible[0] if eligible else None
    if selected is None:
        faults.append("no_globally_eligible_candidate")
    payload={
        "schema_version":"q040-baseline-selection-b2-combined-v1",
        "real_q040_outcomes_opened":False,
        "seed_namespace":"1100+r",
        "per_scale_ranked":per_scale,
        "global_ranked":global_ranked,
        "selected_global_baseline":selected,
        "faults":faults,
        "disposition":"Q040_BASELINE_SELECTION_B2_PASS" if not faults else "Q040_BASELINE_OPERATOR_REFUSED_V0_2",
    }
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"disposition":payload["disposition"],"selected":selected,"faults":faults},indent=2))
    return 0 if not faults else 2

if __name__=="__main__":
    raise SystemExit(main())
