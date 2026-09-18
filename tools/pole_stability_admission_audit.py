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
from market_chi.pole_stability import blockwise_pole_stability
from tools.run_adversarial_qualification import FAMILIES as ADVERSARIES
from tools.variance_second_order_stress_audit import FAMILIES as AR2_STRESS, simulate_ar2


def qstats(rows, key):
    vals = np.asarray([r[key] for r in rows if np.isfinite(r[key])], dtype=float)
    if len(vals) == 0:
        return None
    return {
        "min": float(vals.min()),
        "q10": float(np.quantile(vals, 0.10)),
        "median": float(np.median(vals)),
        "q90": float(np.quantile(vals, 0.90)),
        "max": float(vals.max()),
    }


def audit(name, generator, reps, n, seed0, margin, blocks):
    rows = []
    for i in range(reps):
        rng = np.random.default_rng(seed0 + i)
        x = generator(n, rng)
        eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=margin))
        ps = blockwise_pole_stability(x, blocks=blocks, min_ar2_bic_gain=margin)
        rows.append({
            "admitted": eng.chi_status == "ADMITTED",
            "class_agreement": ps.block_pole_class_agreement,
            "block_support": ps.block_ar2_support_fraction,
            "block_chi_licensed": ps.block_chi_licensed_fraction,
            "median_pole_distance": ps.median_pole_distance,
            "max_pole_distance": ps.max_pole_distance,
        })
    admitted = [r for r in rows if r["admitted"]]
    return {
        "family": name,
        "replicates": reps,
        "chi_admitted": len(admitted),
        "chi_admission_rate": len(admitted) / reps,
        "class_agreement_admitted": qstats(admitted, "class_agreement"),
        "block_support_admitted": qstats(admitted, "block_support"),
        "block_chi_licensed_admitted": qstats(admitted, "block_chi_licensed"),
        "median_pole_distance_admitted": qstats(admitted, "median_pole_distance"),
        "max_pole_distance_admitted": qstats(admitted, "max_pole_distance"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicates", type=int, default=200)
    ap.add_argument("--n", type=int, default=1200)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--blocks", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=25000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    families = []
    for j, (name, fn) in enumerate(ADVERSARIES.items()):
        families.append(audit(name, fn, args.replicates, args.n, args.seed0 + 10000*j, args.bic_margin, args.blocks))

    for j, (name, (coeff, innovation_fn)) in enumerate(AR2_STRESS.items()):
        def gen(n, rng, coeff=coeff, innovation_fn=innovation_fn):
            return simulate_ar2(n, rng, coeff, innovation_fn)
        families.append(audit(name, gen, args.replicates, args.n, args.seed0 + 100000 + 10000*j, args.bic_margin, args.blocks))

    payload = {
        "schema_version": "pole-stability-admission-audit-v1",
        "epistemic_status": "P0-Q synthetic qualification; blockwise pole reproducibility",
        "n": args.n,
        "replicates": args.replicates,
        "blocks": args.blocks,
        "bic_margin": args.bic_margin,
        "families": families,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
