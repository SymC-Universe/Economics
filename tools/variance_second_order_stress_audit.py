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


def coeff_complex():
    lam = -0.05 + 0.20j
    z = np.exp(lam)
    return float(2 * z.real), float(-(abs(z) ** 2))


def coeff_real():
    z1, z2 = np.exp(-0.10), np.exp(-0.40)
    return float(z1 + z2), float(-(z1 * z2))


def innovations_homoskedastic(n, rng):
    return rng.normal(size=n)


def innovations_garch(n, rng, omega=0.05, alpha=0.08, beta=0.90):
    e = np.zeros(n)
    h = np.ones(n) * omega / (1 - alpha - beta)
    z = rng.normal(size=n)
    for t in range(1, n):
        e[t] = np.sqrt(max(h[t - 1], 1e-12)) * z[t]
        h[t] = omega + alpha * e[t] ** 2 + beta * h[t - 1]
    return e


def innovations_sv(n, rng, mu=-1.0, phi=0.97, sigma=0.20):
    h = np.zeros(n)
    e = np.zeros(n)
    h[0] = mu
    for t in range(1, n):
        h[t] = mu + phi * (h[t - 1] - mu) + sigma * rng.normal()
        e[t] = np.exp(h[t] / 2) * rng.normal()
    return e


def simulate_ar2(n, rng, coeff, innovation_fn):
    burn = 400
    total = n + burn
    eps = innovation_fn(total, rng)
    x = np.zeros(total)
    phi1, phi2 = coeff
    for t in range(2, total):
        x[t] = phi1 * x[t - 1] + phi2 * x[t - 2] + eps[t]
    return x[burn:]


FAMILIES = {
    "ar2_complex_homoskedastic": (coeff_complex(), innovations_homoskedastic),
    "ar2_complex_garch_noise": (coeff_complex(), innovations_garch),
    "ar2_complex_sv_noise": (coeff_complex(), innovations_sv),
    "ar2_real_homoskedastic": (coeff_real(), innovations_homoskedastic),
    "ar2_real_garch_noise": (coeff_real(), innovations_garch),
    "ar2_real_sv_noise": (coeff_real(), innovations_sv),
}


def med(rows, key):
    vals = [r[key] for r in rows if np.isfinite(r[key])]
    return float(np.median(vals)) if vals else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicates", type=int, default=200)
    ap.add_argument("--n", type=int, default=1200)
    ap.add_argument("--bic-margin", type=float, default=6.0)
    ap.add_argument("--seed0", type=int, default=6000)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    families = []
    for name, (coeff, innovation_fn) in FAMILIES.items():
        rows = []
        for i in range(args.replicates):
            rng = np.random.default_rng(args.seed0 + i)
            x = simulate_ar2(args.n, rng, coeff, innovation_fn)
            eng = analyze_series(x, EngineConfig(min_ar2_bic_gain=args.bic_margin))
            y = (x - np.mean(x)) / np.std(x)
            fit = fit_ar(y, 2)
            vd = variance_structure_diagnostic(ar_residuals(y, fit))
            rows.append({
                "chi_admitted": eng.chi_status == "ADMITTED",
                "variance_energy": vd.squared_residual_acf_energy,
                "variance_max_abs_acf": vd.max_abs_squared_residual_acf,
                "block_variance_cv": vd.block_variance_cv,
            })
        admitted = [r for r in rows if r["chi_admitted"]]
        families.append({
            "family": name,
            "replicates": args.replicates,
            "chi_admitted": len(admitted),
            "chi_admission_rate": len(admitted) / args.replicates,
            "median_variance_energy_all": med(rows, "variance_energy"),
            "median_variance_energy_admitted": med(admitted, "variance_energy"),
            "median_max_abs_sq_acf_all": med(rows, "variance_max_abs_acf"),
            "median_max_abs_sq_acf_admitted": med(admitted, "variance_max_abs_acf"),
            "median_block_variance_cv_all": med(rows, "block_variance_cv"),
            "median_block_variance_cv_admitted": med(admitted, "block_variance_cv"),
        })

    payload = {
        "schema_version": "variance-second-order-stress-audit-v1",
        "epistemic_status": "P0-Q synthetic qualification; tests legitimate AR2 mean dynamics under heteroskedastic innovations",
        "bic_margin": args.bic_margin,
        "n": args.n,
        "seed0": args.seed0,
        "families": families,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
