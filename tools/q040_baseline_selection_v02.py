#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np

from market_chi.q040_baseline_selection_v01 import (
    BASELINE_CONTROLS,
    score_baseline_candidate,
)
from market_chi.q040_observation_episode_v04 import (
    build_observation_episode_world,
    nc20_cells,
)

WINDOWS = (480, 640)
ORDINAL = {"NC-R5":5,"NC-R15":15,"NC-R16":16,"NC-R20":21}

def selection_seed(control: str, scale: int, replica: int, cell_ordinal: int = 0) -> int:
    return int(np.random.SeedSequence([
        20261002, ORDINAL[control], scale, 1100 + replica, cell_ordinal
    ]).generate_state(1, dtype=np.uint32)[0])

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--scale",type=int,required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    if args.scale not in (15,30,60,300):
        raise SystemExit("invalid scale")
    rows=[]
    for control in BASELINE_CONTROLS:
        cells=nc20_cells() if control=="NC-R20" else [None]
        for cell_ord,cell in enumerate(cells):
            key=None if cell is None else cell.key()
            for rep in range(14):
                seed=selection_seed(control,args.scale,rep,cell_ord)
                world=build_observation_episode_world(
                    control,seed=seed,scale_seconds=args.scale,nc20_cell=cell
                )
                for kind in ("K1","K2"):
                    for window in WINDOWS:
                        rows.append(score_baseline_candidate(
                            world,kind=kind,window=window,replica=rep,cell_key=key
                        ).to_dict())
    payload={
        "schema_version":"q040-baseline-selection-b2-shard-v1",
        "scale_seconds":args.scale,
        "seed_namespace":"1100+r",
        "candidate_windows":[480,640],
        "real_q040_outcomes_opened":False,
        "scores":rows,
    }
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"scale":args.scale,"rows":len(rows),"status":"COMPLETE"}))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
