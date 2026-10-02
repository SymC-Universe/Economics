#!/usr/bin/env python3
from __future__ import annotations

import argparse,json,math
from pathlib import Path
import numpy as np

def finite_median(x):
    a=np.asarray(x,dtype=float)
    a=a[np.isfinite(a)]
    return float(np.median(a)) if len(a) else math.inf

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    base=Path(args.input_dir)

    metas=[]; arrays=[]
    for scale in (15,30,60,300):
        prefix=base/f"scale_{scale}"
        metas.append(json.loads(Path(str(prefix)+".json").read_text()))
        arrays.append(np.load(str(prefix)+".npz"))

    ctable=metas[0]["candidate_table"]
    all_summaries=[]
    global_fit_refused={}
    for m in metas:
        for k,v in m["fit_refused"].items():
            global_fit_refused[k]=global_fit_refused.get(k,0)+int(v)

    for c in ctable:
        ix=int(c["index"])
        metric=c["metric"]
        vals={k:[] for k in ("recall","entry","return","false","terminal")}
        cell_stats=[]
        fit_refusal_count=sum(v for k,v in global_fit_refused.items() if k.startswith(metric+"|"))

        for meta,arr in zip(metas,arrays):
            mask=arr["candidate"]==ix
            vals["recall"].extend(arr["recall"][mask].tolist())
            vals["entry"].extend(arr["entry_error"][mask].tolist())
            vals["return"].extend(arr["return_error"][mask].tolist())
            vals["false"].extend(arr["false_ratio"][mask].tolist())
            vals["terminal"].extend(arr["terminal_concordance"][mask].tolist())

            for ci,name in enumerate(meta["cell_names"]):
                cmask=mask & (arr["cell"]==ci)
                nt=arr["n_true"][cmask]
                support=int(np.sum(nt>0))
                r=arr["recall"][cmask]
                f=arr["false_ratio"][cmask]
                r=r[np.isfinite(r)]; f=f[np.isfinite(f)]
                cell_stats.append({
                    "scale":meta["scale_seconds"],"cell":name,"support_units":support,
                    "median_recall":float(np.median(r)) if len(r) else math.nan,
                    "median_false_ratio":float(np.median(f)) if len(f) else math.nan,
                })

        overall_recall=finite_median(vals["recall"])
        entry=finite_median(vals["entry"])
        ret=finite_median(vals["return"])
        false=finite_median(vals["false"])
        terminal=finite_median(vals["terminal"])
        support_ok=all(x["support_units"]>=20 for x in cell_stats)
        min_cell_recall=min((x["median_recall"] for x in cell_stats if math.isfinite(x["median_recall"])),default=-math.inf)
        max_cell_false=max((x["median_false_ratio"] for x in cell_stats if math.isfinite(x["median_false_ratio"])),default=math.inf)
        eligible=(
            fit_refusal_count==0 and support_ok and
            overall_recall>=0.80 and min_cell_recall>=0.60 and
            false<=0.25 and max_cell_false<=0.75 and
            terminal>=0.75
        )
        all_summaries.append({
            **c,
            "fit_refused_folds":fit_refusal_count,
            "support_ok":support_ok,
            "overall_median_recall":overall_recall,
            "min_cell_median_recall":min_cell_recall,
            "median_entry_error":entry,
            "median_return_error":ret,
            "median_false_ratio":false,
            "max_cell_median_false_ratio":max_cell_false,
            "median_terminal_concordance":terminal,
            "eligible":bool(eligible),
        })

    def order(x):
        return (
            0 if x["eligible"] else 1,
            float(x["median_entry_error"]),
            float(x["median_return_error"]),
            float(x["median_false_ratio"]),
            (0.95,0.975,0.99).index(float(x["entry_q"])),
            (2,3,5).index(int(x["sustain"])),
            -int(x["min_separation"]),
            0 if x["metric"]=="D1" else 1,
            float(x["return_q"]),
        )

    ranked=sorted(all_summaries,key=order)
    eligible=[x for x in ranked if x["eligible"]]
    selected=eligible[0] if eligible else None

    horizon_units=[]
    for meta in metas:
        for name,h in meta["horizon_counts"].items():
            n=int(h["episodes"])
            c20=h["sr20"]/n if n else math.nan
            c40=h["sr40"]/n if n else math.nan
            c80=h["sr80"]/n if n else math.nan
            horizon_units.append({"scale":meta["scale_seconds"],"cell":name,"cif20":c20,"cif40":c40,"cif80":c80})

    horizon=80; qualifier="HORIZON_SATURATION_NOT_ESTABLISHED"
    for h,nxt in ((20,40),(40,80)):
        ok=True
        for u in horizon_units:
            ch=u[f"cif{h}"]; cn=u[f"cif{nxt}"]; c80=u["cif80"]
            if not (math.isfinite(ch) and math.isfinite(cn) and math.isfinite(c80)):
                ok=False; break
            if abs(cn-ch)>=0.02:
                ok=False; break
            if c80>0 and ch/c80<0.90:
                ok=False; break
        if ok:
            horizon=h; qualifier=None; break

    faults=[]
    if selected is None: faults.append("no_eligible_metric_event_tuple")
    payload={
        "schema_version":"q040-e2-metric-event-combined-v1",
        "real_q040_outcomes_opened":False,
        "selected_metric_event_tuple":selected,
        "ranked_candidates":ranked,
        "horizon":{"horizon":horizon,"qualifier":qualifier,"units":horizon_units},
        "faults":faults,
        "disposition":"Q040_METRIC_EVENT_E2_PASS" if not faults else "Q040_EVENT_DEFINITION_REFUSED_E2",
    }
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"disposition":payload["disposition"],"selected":selected,"horizon":payload["horizon"]["horizon"],"qualifier":qualifier},indent=2))
    return 0 if not faults else 2

if __name__=="__main__":
    raise SystemExit(main())
