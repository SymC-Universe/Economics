#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi import EngineConfig, analyze_series
from market_chi.models import fit_ar
from market_chi.variance_diagnostics import ar_residuals, variance_structure_diagnostic
from tools.run_adversarial_qualification import FAMILIES


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicates", type=int, default=200)
    ap.add_argument("--n", type=int, default=1200)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--seed0", type=int, default=2000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out_rows = []
    for family, fn in FAMILIES.items():
        rows = []
        for i in range(args.replicates):
            rng = np.random.default_rng(args.seed0 + i)
            x = fn(args.n, rng)
            eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=args.bic_margin))
            order = 2 if eng.model_family in {"AR2", "AR2_SECOND_ORDER"} else (1 if eng.model_family == "AR1" else 0)
            fit = fit_ar((x - np.mean(x)) / np.std(x), order)
            vd = variance_structure_diagnostic(ar_residuals((x - np.mean(x)) / np.std(x), fit))
            rows.append({
                "chi_admitted": eng.chi_status == "ADMITTED",
                "variance_energy": vd.squared_residual_acf_energy,
                "variance_max_abs_acf": vd.max_abs_squared_residual_acf,
                "block_variance_cv": vd.block_variance_cv,
            })
        admitted = [r for r in rows if r["chi_admitted"]]
        def med(key, source):
            vals = [r[key] for r in source if np.isfinite(r[key])]
            return float(np.median(vals)) if vals else None
        out_rows.append({
            "family": family,
            "replicates": args.replicates,
            "chi_admitted": len(admitted),
            "chi_admission_rate": len(admitted) / args.replicates,
            "median_variance_energy_all": med("variance_energy", rows),
            "median_variance_energy_admitted": med("variance_energy", admitted),
            "median_max_abs_sq_acf_all": med("variance_max_abs_acf", rows),
            "median_max_abs_sq_acf_admitted": med("variance_max_abs_acf", admitted),
            "median_block_variance_cv_all": med("block_variance_cv", rows),
            "median_block_variance_cv_admitted": med("block_variance_cv", admitted),
        })

    payload = {
        "schema_version": "variance-admission-audit-v1",
        "epistemic_status": "P0-Q synthetic qualification; report-only variance diagnostic",
        "bic_margin": args.bic_margin,
        "n": args.n,
        "seed0": args.seed0,
        "families": out_rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
