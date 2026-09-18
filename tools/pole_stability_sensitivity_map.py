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
from tools.mean_cv_sensitivity_map import SECOND_ORDER, NOISE, complex_coeff, real_coeff
from tools.variance_second_order_stress_audit import simulate_ar2


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


def run_cell(name, generator, reps, n, seed0, margin, blocks):
    rows = []
    for i in range(reps):
        rng = np.random.default_rng(seed0 + i)
        x = generator(n, rng)
        eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=margin))
        ps = blockwise_pole_stability(x, blocks=blocks, min_ar2_bic_gain=margin)
        rows.append({
            "admitted": eng.chi_status == "ADMITTED",
            "block_support": ps.block_ar2_support_fraction,
            "block_licensed": ps.block_chi_licensed_fraction,
            "class_agreement": ps.block_pole_class_agreement,
            "median_distance": ps.median_pole_distance,
        })
    admitted = [r for r in rows if r["admitted"]]
    return {
        "case": name,
        "replicates": reps,
        "chi_admitted": len(admitted),
        "chi_admission_rate": len(admitted) / reps,
        "block_support_admitted": qstats(admitted, "block_support"),
        "block_chi_licensed_admitted": qstats(admitted, "block_licensed"),
        "class_agreement_admitted": qstats(admitted, "class_agreement"),
        "median_pole_distance_admitted": qstats(admitted, "median_distance"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--replicates", type=int, default=50)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--blocks", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=40000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cells = []
    for j, (name, fn) in enumerate(ADVERSARIES.items()):
        cells.append(run_cell(
            f"adversary:{name}", fn, args.replicates, args.n,
            args.seed0 + 10000*j, args.bic_margin, args.blocks
        ))

    idx = 0
    for case_name, spec in SECOND_ORDER.items():
        a, b = spec["lam"]
        coeff = complex_coeff(a, b) if spec["kind"] == "complex" else real_coeff(a, b)
        for noise_name, innovation_fn in NOISE.items():
            def gen(n, rng, coeff=coeff, innovation_fn=innovation_fn):
                return simulate_ar2(n, rng, coeff, innovation_fn)
            cells.append(run_cell(
                f"truth:{case_name}:{noise_name}", gen, args.replicates, args.n,
                args.seed0 + 200000 + 10000*idx, args.bic_margin, args.blocks
            ))
            idx += 1

    payload = {
        "schema_version": "pole-stability-sensitivity-map-v1",
        "epistemic_status": "P0-Q synthetic sensitivity; no production threshold",
        "n": args.n,
        "replicates_per_cell": args.replicates,
        "blocks": args.blocks,
        "bic_margin": args.bic_margin,
        "cells": cells,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"out": str(out), "n": args.n, "cells": len(cells)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
