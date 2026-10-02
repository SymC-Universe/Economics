#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from market_chi.q040_baseline_selection_v01 import (
    score_baseline_candidate,
)
from market_chi.q040_observation_episode_v02 import (
    build_observation_episode_world,
    nc20_cells,
)

WINDOWS=(40,60,80,120,160,240)


def seed_for(control:str,scale:int,rep:int,cell:int=0)->int:
    ordinal={"NC-R5":5,"NC-R20":21}[control]
    return int(
        np.random.SeedSequence([20261002,ordinal,scale,900+rep,cell])
        .generate_state(1,dtype=np.uint32)[0]
    )


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--scale",type=int,required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    rows=[]
    controls=[("NC-R5",None)]
    failed_cells=[c for c in nc20_cells() if c.update_density==0.20 and c.gap_structure=="CLUSTERED"]
    controls += [("NC-R20",c) for c in failed_cells]

    for control,cell in controls:
        cell_ord=0 if cell is None else nc20_cells().index(cell)
        cell_key=None if cell is None else cell.key()
        for rep in range(14):
            world=build_observation_episode_world(
                control,
                seed=seed_for(control,args.scale,rep,cell_ord),
                scale_seconds=args.scale,
                nc20_cell=cell,
            )
            for kind in ("K1","K2"):
                for window in WINDOWS:
                    rows.append(
                        score_baseline_candidate(
                            world,
                            kind=kind,
                            window=window,
                            replica=rep,
                            cell_key=cell_key,
                        ).to_dict()
                    )

    summary=[]
    for kind in ("K1","K2"):
        for window in WINDOWS:
            vals=[x for x in rows if x["kind"]==kind and x["window"]==window]
            nc=[x for x in vals if x["control_id"]=="NC-R20"]
            mv=[x for x in vals if x["control_id"]=="NC-R5"]
            summary.append({
                "kind":kind,
                "window":window,
                "nc20_min_coverage":float(min(x["coverage"] for x in nc)),
                "nc20_median_coverage":float(np.median([x["coverage"] for x in nc])),
                "nc20_pass_fraction":float(np.mean([x["coverage"]>=0.90 for x in nc])),
                "nc20_median_error":float(np.median([x["median_error"] for x in nc if np.isfinite(x["median_error"])])),
                "moving_baseline_median_error":float(np.median([x["median_error"] for x in mv if np.isfinite(x["median_error"])])),
                "moving_baseline_min_coverage":float(min(x["coverage"] for x in mv)),
            })

    payload={
        "schema_version":"q040-baseline-failure-sweep-v1",
        "scale_seconds":args.scale,
        "promotion_eligible":False,
        "real_q040_outcomes_opened":False,
        "summary":summary,
        "rows":rows,
    }
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"scale":args.scale,"summary":summary},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
