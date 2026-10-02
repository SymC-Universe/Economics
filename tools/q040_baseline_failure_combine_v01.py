#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    base=Path(args.input_dir)
    scales={}
    faults=[]
    for scale in (15,30,60,300):
        p=base/f"scale_{scale}.json"
        if not p.exists():
            faults.append(f"missing:{scale}")
            continue
        data=json.loads(p.read_text())
        rows=data["summary"]
        viable=[
            r for r in rows
            if float(r["nc20_pass_fraction"])==1.0
            and float(r["moving_baseline_min_coverage"])>=0.90
        ]
        viable=sorted(
            viable,
            key=lambda r:(
                int(r["window"]),
                float(r["moving_baseline_median_error"]),
                0 if r["kind"]=="K1" else 1,
            )
        )
        scales[str(scale)]={
            "summary":rows,
            "coverage_viable":viable,
            "minimum_coverage_viable":viable[0] if viable else None,
        }
    payload={
        "schema_version":"q040-baseline-failure-combined-v1",
        "promotion_eligible":False,
        "faults":faults,
        "scales":scales,
    }
    out=Path(args.output)
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({
        "faults":faults,
        "minimum_viable":{
            s:v["minimum_coverage_viable"] for s,v in scales.items()
        }
    },indent=2))
    return 0 if not faults else 2

if __name__=="__main__":
    raise SystemExit(main())
