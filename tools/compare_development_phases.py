#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

from market_chi.modal_compare import compare_loading_subspaces


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase_index")
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=2)
    args = ap.parse_args()

    src = Path(args.phase_index)
    data = json.loads(src.read_text(encoding="utf-8"))
    complete = [p for p in data.get("phases", []) if p.get("status") == "COMPLETE"]

    result: dict[str, object] = {
        "schema_version": "mnq-development-cross-day-compare-v1",
        "source_phase_index": str(src),
        "source_schema_version": data.get("schema_version"),
        "holdout_status": data.get("holdout_status"),
        "k": args.k,
        "phases": {},
        "epistemic_status": "P0-D/P0-Q development comparison only; no holdout claim",
    }

    for phase in sorted({p.get("phase") for p in complete}):
        rows = [p for p in complete if p.get("phase") == phase]
        phase_out: dict[str, object] = {
            "n_days": len(rows),
            "days": [],
            "pairwise_subspace": [],
        }
        for r in rows:
            m = r.get("metrics", {})
            phase_out["days"].append({
                "date": r.get("date"),
                "pc1_variance": m.get("pc1_variance"),
                "pc2_variance": m.get("pc2_variance"),
                "pc1_pc2_cumulative": m.get("pc1_pc2_cumulative"),
                "pc1_symmetric_alignment": m.get("pc1_symmetric_alignment"),
                "pc2_imbalance_alignment": m.get("pc2_imbalance_alignment"),
                "top2_min_principal_cosine_within_day": m.get("top2_min_principal_cosine"),
                "chi_admissions": m.get("chi_admissions"),
                "chi_screens": m.get("chi_screens"),
                "forward_risk_spearman": m.get("forward_risk_spearman"),
            })

        for a, b in itertools.combinations(rows, 2):
            ma, mb = a.get("metrics", {}), b.get("metrics", {})
            names_a = ma.get("depth_pca_feature_names")
            names_b = mb.get("depth_pca_feature_names")
            if names_a != names_b:
                comp = {
                    "status": "REFUSED_FEATURE_MISMATCH",
                    "k": args.k,
                    "principal_cosines": [],
                    "min_principal_cosine": None,
                    "mean_principal_cosine": None,
                    "reason": "depth feature names differ",
                }
            else:
                out = compare_loading_subspaces(
                    ma.get("depth_pca_loadings_first6", []),
                    mb.get("depth_pca_loadings_first6", []),
                    k=args.k,
                )
                comp = out.to_dict()
                for key in ("min_principal_cosine", "mean_principal_cosine"):
                    if isinstance(comp.get(key), float) and not math.isfinite(comp[key]):
                        comp[key] = None
            phase_out["pairwise_subspace"].append({
                "date_a": a.get("date"),
                "date_b": b.get("date"),
                **comp,
            })
        result["phases"][phase] = phase_out

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "complete_phase_records": len(complete),
        "phase_groups": {k: v["n_days"] for k, v in result["phases"].items()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
