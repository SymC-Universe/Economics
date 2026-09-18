#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_chi import EngineConfig, analyze_series
from market_chi.mean_cv import walk_forward_mean_comparison
from tools.run_adversarial_qualification import FAMILIES as ADVERSARIES
from tools.variance_second_order_stress_audit import (
    innovations_homoskedastic,
    innovations_garch,
    innovations_sv,
    simulate_ar2,
)


def complex_coeff(a: float, b: float):
    z = np.exp(complex(a, b))
    return (float(2 * z.real), float(-(abs(z) ** 2)))


def real_coeff(a: float, b: float):
    z1, z2 = np.exp(a), np.exp(b)
    return (float(z1 + z2), float(-(z1 * z2)))


def expected_complex_chi(a: float, b: float) -> float:
    return float(-a / math.sqrt(a * a + b * b))


def expected_real_chi(a: float, b: float) -> float:
    return float(-(a + b) / (2 * math.sqrt(a * b)))


SECOND_ORDER = {
    "complex_baseline": {"kind": "complex", "lam": (-0.05, 0.20)},
    "complex_low_frequency": {"kind": "complex", "lam": (-0.05, 0.05)},
    "complex_near_critical": {"kind": "complex", "lam": (-0.20, 0.05)},
    "complex_fast_decay": {"kind": "complex", "lam": (-1.00, 0.20)},
    "real_baseline": {"kind": "real", "lam": (-0.10, -0.40)},
    "real_near_repeated": {"kind": "real", "lam": (-0.20, -0.21)},
    "real_weak_second": {"kind": "real", "lam": (-0.05, -3.00)},
    "real_slow_pair": {"kind": "real", "lam": (-0.02, -0.03)},
}
NOISE = {
    "homoskedastic": innovations_homoskedastic,
    "garch": innovations_garch,
    "sv": innovations_sv,
}


def qstats(rows, key):
    vals = np.array([r[key] for r in rows if np.isfinite(r[key])], dtype=float)
    if len(vals) == 0:
        return None
    return {
        "min": float(np.min(vals)),
        "q10": float(np.quantile(vals, 0.10)),
        "median": float(np.median(vals)),
        "q90": float(np.quantile(vals, 0.90)),
        "max": float(np.max(vals)),
    }


def run_cell(name, generator, reps, n, seed0, margin, min_train, test_block, expected_chi=None):
    rows = []
    for i in range(reps):
        rng = np.random.default_rng(seed0 + i)
        x = generator(n, rng)
        eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=margin))
        cv = walk_forward_mean_comparison(x, min_train=min_train, test_block=test_block)
        rows.append({
            "admitted": eng.chi_status == "ADMITTED",
            "gain": cv.ar2_gain_vs_best_simple,
            "wins": cv.ar2_fold_win_fraction,
            "chi": eng.chi if eng.chi_status == "ADMITTED" else math.nan,
        })
    admitted = [r for r in rows if r["admitted"]]
    return {
        "case": name,
        "expected_chi": expected_chi,
        "replicates": reps,
        "chi_admitted": len(admitted),
        "chi_admission_rate": len(admitted) / reps,
        "oos_gain_all": qstats(rows, "gain"),
        "oos_gain_admitted": qstats(admitted, "gain"),
        "fold_win_all": qstats(rows, "wins"),
        "fold_win_admitted": qstats(admitted, "wins"),
        "estimated_chi_admitted": qstats(admitted, "chi"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--replicates", type=int, default=50)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--seed0", type=int, default=12000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    min_train = max(100, args.n // 3)
    test_block = max(25, args.n // 12)
    cells = []

    for j, (name, fn) in enumerate(ADVERSARIES.items()):
        cells.append(run_cell(
            f"adversary:{name}", fn, args.replicates, args.n,
            args.seed0 + 10000 * j, args.bic_margin, min_train, test_block,
        ))

    offset = 200000
    idx = 0
    for case_name, spec in SECOND_ORDER.items():
        a, b = spec["lam"]
        if spec["kind"] == "complex":
            coeff = complex_coeff(a, b)
            expected = expected_complex_chi(a, b)
        else:
            coeff = real_coeff(a, b)
            expected = expected_real_chi(a, b)
        for noise_name, innovation_fn in NOISE.items():
            def gen(n, rng, coeff=coeff, innovation_fn=innovation_fn):
                return simulate_ar2(n, rng, coeff, innovation_fn)
            cells.append(run_cell(
                f"truth:{case_name}:{noise_name}", gen, args.replicates, args.n,
                args.seed0 + offset + 10000 * idx, args.bic_margin,
                min_train, test_block, expected_chi=expected,
            ))
            idx += 1

    payload = {
        "schema_version": "mean-cv-sensitivity-map-v1",
        "epistemic_status": "P0-Q synthetic sensitivity; no production threshold",
        "n": args.n,
        "replicates_per_cell": args.replicates,
        "bic_margin": args.bic_margin,
        "min_train": min_train,
        "test_block": test_block,
        "cells": cells,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({
        "out": str(out),
        "n": args.n,
        "cells": len(cells),
        "replicates_per_cell": args.replicates,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
