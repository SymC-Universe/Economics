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
from market_chi.mean_cv import walk_forward_mean_comparison
from tools.run_adversarial_qualification import FAMILIES as ADVERSARIES
from tools.variance_second_order_stress_audit import FAMILIES as AR2_STRESS, simulate_ar2


def summarize(rows, key):
    vals = [r[key] for r in rows if np.isfinite(r[key])]
    if not vals:
        return None
    return {
        "median": float(np.median(vals)),
        "q10": float(np.quantile(vals, 0.10)),
        "q90": float(np.quantile(vals, 0.90)),
    }


def audit_family(name, generator, replicates, n, seed0, margin, min_train, test_block):
    rows = []
    for i in range(replicates):
        rng = np.random.default_rng(seed0 + i)
        x = generator(n, rng)
        eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=margin))
        cv = walk_forward_mean_comparison(x, min_train=min_train, test_block=test_block)
        rows.append({
            "chi_admitted": eng.chi_status == "ADMITTED",
            "gain": cv.ar2_gain_vs_best_simple,
            "win_fraction": cv.ar2_fold_win_fraction,
        })
    admitted = [r for r in rows if r["chi_admitted"]]
    return {
        "family": name,
        "replicates": replicates,
        "chi_admitted": len(admitted),
        "chi_admission_rate": len(admitted) / replicates,
        "ar2_oos_gain_all": summarize(rows, "gain"),
        "ar2_oos_gain_admitted": summarize(admitted, "gain"),
        "ar2_fold_win_fraction_all": summarize(rows, "win_fraction"),
        "ar2_fold_win_fraction_admitted": summarize(admitted, "win_fraction"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicates", type=int, default=200)
    ap.add_argument("--n", type=int, default=1200)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--seed0", type=int, default=9000)
    ap.add_argument("--min-train", type=int, default=400)
    ap.add_argument("--test-block", type=int, default=100)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    families = []
    for j, (name, fn) in enumerate(ADVERSARIES.items()):
        families.append(audit_family(
            name,
            fn,
            args.replicates,
            args.n,
            args.seed0 + 10000 * j,
            args.bic_margin,
            args.min_train,
            args.test_block,
        ))

    for j, (name, (coeff, innovation_fn)) in enumerate(AR2_STRESS.items()):
        def gen(n, rng, coeff=coeff, innovation_fn=innovation_fn):
            return simulate_ar2(n, rng, coeff, innovation_fn)
        families.append(audit_family(
            name,
            gen,
            args.replicates,
            args.n,
            args.seed0 + 100000 + 10000 * j,
            args.bic_margin,
            args.min_train,
            args.test_block,
        ))

    payload = {
        "schema_version": "mean-cv-admission-audit-v1",
        "epistemic_status": "P0-Q synthetic qualification; walk-forward conditional-mean persistence",
        "bic_margin": args.bic_margin,
        "n": args.n,
        "min_train": args.min_train,
        "test_block": args.test_block,
        "families": families,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
