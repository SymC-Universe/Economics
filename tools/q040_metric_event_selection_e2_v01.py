#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict
import numpy as np

from market_chi.q040_metric_event_selection_v01 import (
    ENTRY_Q, RETURN_Q, SUSTAIN, MIN_SEP, FOLDS,
    fit_fold_distance, evaluate_event_grid_for_fold,
)
from market_chi.q040_observation_episode_v04 import (
    build_observation_episode_world, nc20_cells,
)

CONTROLS = (
    "NC-R1","NC-R2","NC-R3","NC-R4","NC-R5","NC-R6","NC-R7",
    "NC-R9","NC-R10","NC-R11","NC-R12","NC-R13",
    "NC-R15","NC-R16","NC-R17","NC-R17b","NC-R18","NC-R19","NC-R20",
)
ORDINAL = {
    "NC-R1":1,"NC-R2":2,"NC-R3":3,"NC-R4":4,"NC-R5":5,"NC-R6":6,"NC-R7":7,
    "NC-R9":9,"NC-R10":10,"NC-R11":11,"NC-R12":12,"NC-R13":13,
    "NC-R15":15,"NC-R16":16,"NC-R17":17,"NC-R17b":18,"NC-R18":19,"NC-R19":20,"NC-R20":21,
}
HORIZON_CONTROLS = {"NC-R1","NC-R3","NC-R4","NC-R6","NC-R7","NC-R10","NC-R15","NC-R17","NC-R20"}

def seed_for(control: str, scale: int, replica: int, cell_ordinal: int=0) -> int:
    return int(np.random.SeedSequence([
        20261002, ORDINAL[control], scale, 1200 + replica, cell_ordinal
    ]).generate_state(1, dtype=np.uint32)[0])

def candidate_table():
    out=[]
    idx=0
    for metric in ("D1","D2"):
        for qe in ENTRY_Q:
            for qr in RETURN_Q:
                for sustain in SUSTAIN:
                    for sep in MIN_SEP:
                        out.append({
                            "index":idx,"metric":metric,"entry_q":float(qe),
                            "return_q":float(qr),"sustain":int(sustain),
                            "min_separation":int(sep),
                        })
                        idx+=1
    return out

def candidate_index_map():
    return {
        (x["metric"],x["entry_q"],x["return_q"],x["sustain"],x["min_separation"]):x["index"]
        for x in candidate_table()
    }

def load_baseline(path: Path) -> tuple[str,int]:
    j=json.loads(path.read_text(encoding="utf-8"))
    if j.get("disposition")!="Q040_BASELINE_SELECTION_B2_PASS":
        raise RuntimeError("B2 baseline result is not PASS")
    b=j.get("selected_global_baseline")
    if not b:
        raise RuntimeError("B2 baseline selection missing")
    return str(b["kind"]), int(b["window"])

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--scale",type=int,required=True)
    ap.add_argument("--baseline-result",required=True)
    ap.add_argument("--output-prefix",required=True)
    args=ap.parse_args()
    if args.scale not in (15,30,60,300):
        raise SystemExit("invalid scale")

    baseline_kind,baseline_window=load_baseline(Path(args.baseline_result))
    ctable=candidate_table()
    cmap=candidate_index_map()

    cand=[]; cell=[]; ntrue=[]; nest=[]; recall=[]; entry=[]; ret=[]; false=[]; terminal=[]
    cell_names=[]; cell_to_idx={}
    fit_refused=defaultdict(int)
    horizon_counts=defaultdict(lambda:{"episodes":0,"sr20":0,"sr40":0,"sr80":0})

    def cell_id(name: str) -> int:
        if name not in cell_to_idx:
            cell_to_idx[name]=len(cell_names); cell_names.append(name)
        return cell_to_idx[name]

    for control in CONTROLS:
        cells=nc20_cells() if control=="NC-R20" else [None]
        for cell_ord,nc in enumerate(cells):
            name=control if nc is None else f"{control}:{nc.key()}"
            ci=cell_id(name)
            for rep in range(14):
                world=build_observation_episode_world(
                    control,
                    seed=seed_for(control,args.scale,rep,cell_ord),
                    scale_seconds=args.scale,
                    nc20_cell=nc,
                )
                if control in HORIZON_CONTROLS:
                    hc=horizon_counts[name]
                    for ep in world["episodes"]:
                        hc["episodes"]+=1
                        if ep["outcome"]=="SUSTAINED_RETURN":
                            dt=int(ep["sustained_return_index"])-int(ep["entry_index"])
                            if dt<=20: hc["sr20"]+=1
                            if dt<=40: hc["sr40"]+=1
                            if dt<=80: hc["sr80"]+=1

                for fold_start,fold_stop in FOLDS:
                    for metric in ("D1","D2"):
                        fit=fit_fold_distance(
                            world,
                            baseline_kind=baseline_kind,
                            baseline_window=baseline_window,
                            metric_kind=metric,
                            fold_start=fold_start,
                            fold_stop=fold_stop,
                        )
                        if fit is None:
                            fit_refused[f"{metric}|{name}"]+=1
                            continue
                        distance,_=fit
                        rows=evaluate_event_grid_for_fold(
                            world,distance,fold_start=fold_start,fold_stop=fold_stop
                        )
                        for row in rows:
                            key=(metric,float(row["entry_q"]),float(row["return_q"]),
                                 int(row["sustain"]),int(row["min_separation"]))
                            ix=cmap[key]
                            nt=int(row["n_true"]); ne=int(row["n_estimated"])
                            cand.append(ix); cell.append(ci); ntrue.append(nt); nest.append(ne)
                            if nt>0:
                                recall.append(float(row["recall"]))
                                entry.append(float(row["entry_error"]))
                                false.append(float(row["false_ratio"]))
                            else:
                                recall.append(np.nan); entry.append(np.nan); false.append(float(ne))
                            ret.append(float(row["return_error"]) if np.isfinite(row["return_error"]) else np.nan)
                            terminal.append(float(row["terminal_concordance"]) if np.isfinite(row["terminal_concordance"]) else np.nan)

    prefix=Path(args.output_prefix)
    prefix.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(
        str(prefix)+".npz",
        candidate=np.asarray(cand,dtype=np.int16),
        cell=np.asarray(cell,dtype=np.int16),
        n_true=np.asarray(ntrue,dtype=np.int16),
        n_estimated=np.asarray(nest,dtype=np.int16),
        recall=np.asarray(recall,dtype=np.float32),
        entry_error=np.asarray(entry,dtype=np.float32),
        return_error=np.asarray(ret,dtype=np.float32),
        false_ratio=np.asarray(false,dtype=np.float32),
        terminal_concordance=np.asarray(terminal,dtype=np.float32),
    )
    meta={
        "schema_version":"q040-e2-metric-event-shard-v1",
        "scale_seconds":args.scale,
        "real_q040_outcomes_opened":False,
        "baseline":{"kind":baseline_kind,"window":baseline_window},
        "seed_namespace":"1200+r",
        "candidate_table":ctable,
        "cell_names":cell_names,
        "fit_refused":dict(fit_refused),
        "horizon_counts":dict(horizon_counts),
        "records":len(cand),
        "status":"COMPLETE",
    }
    Path(str(prefix)+".json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"scale":args.scale,"records":len(cand),"status":"COMPLETE"}))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
