#!/usr/bin/env python3
"""P0-Q admission/refusal sensitivity map for the market χ scaffold.

The synthetic families are qualification adversaries, not empirical market
claims. Results quantify how often the current AR0/AR1/AR2 scaffold emits χ.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from market_chi import EngineConfig, analyze_series


def white(n, rng): return rng.normal(size=n)

def ar1(n, rng, phi=0.8):
    x = np.zeros(n + 300); e = rng.normal(size=len(x))
    for t in range(1, len(x)): x[t] = phi * x[t-1] + e[t]
    return x[300:]

def garch(n, rng, omega=0.05, alpha=0.08, beta=0.90):
    x = np.zeros(n + 300); h = np.ones(n + 300) * omega / (1 - alpha - beta); z = rng.normal(size=n + 300)
    for t in range(1, n + 300):
        x[t] = np.sqrt(max(h[t-1], 1e-12)) * z[t]
        h[t] = omega + alpha * x[t]**2 + beta * h[t-1]
    return x[300:]

def stochastic_volatility(n, rng, mu=-1.0, phi=0.97, sigma=0.20):
    h = np.zeros(n + 300); x = np.zeros(n + 300); h[0] = mu
    for t in range(1, n + 300):
        h[t] = mu + phi * (h[t-1] - mu) + sigma * rng.normal()
        x[t] = np.exp(h[t] / 2) * rng.normal()
    return x[300:]

def jumps(n, rng, p=0.02, jump_sd=5.0):
    x = rng.normal(size=n); mask = rng.random(n) < p; x[mask] += rng.normal(0, jump_sd, size=mask.sum()); return x

def regime_ar1(n, rng):
    x = np.zeros(n + 300); e = rng.normal(size=n + 300); phi = 0.85
    for t in range(1, n + 300):
        if t % 250 == 0: phi = -0.35 if phi > 0 else 0.85
        x[t] = phi * x[t-1] + e[t]
    return x[300:]

def ar2_complex(n, rng):
    lam = -0.05 + 0.20j; z = np.exp(lam); phi1, phi2 = 2 * z.real, -(abs(z) ** 2)
    x = np.zeros(n + 300); e = rng.normal(size=n + 300)
    for t in range(2, n + 300): x[t] = phi1 * x[t-1] + phi2 * x[t-2] + e[t]
    return x[300:]

def ar2_real(n, rng):
    z1, z2 = np.exp(-0.10), np.exp(-0.40); phi1, phi2 = z1 + z2, -(z1 * z2)
    x = np.zeros(n + 300); e = rng.normal(size=n + 300)
    for t in range(2, n + 300): x[t] = phi1 * x[t-1] + phi2 * x[t-2] + e[t]
    return x[300:]

FAMILIES = {"white": white, "ar1": ar1, "garch": garch, "stochastic_volatility": stochastic_volatility, "jumps": jumps, "regime_ar1": regime_ar1, "ar2_complex": ar2_complex, "ar2_real": ar2_real}


def run(replicates, n, margins, seed0):
    rows = []
    for margin in margins:
        for family, fn in FAMILIES.items():
            admitted = 0; chis = []
            for i in range(replicates):
                rng = np.random.default_rng(seed0 + i)
                out = analyze_series(fn(n, rng), EngineConfig(min_ar2_bic_gain=margin))
                if out.chi_status == "ADMITTED": admitted += 1; chis.append(out.chi)
            rows.append({"bic_margin": margin, "family": family, "replicates": replicates, "n": n, "chi_admitted": admitted, "chi_refused": replicates-admitted, "chi_admission_rate": admitted/replicates, "median_chi_when_admitted": float(np.median(chis)) if chis else ""})
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--replicates", type=int, default=200); ap.add_argument("--n", type=int, default=1200); ap.add_argument("--margins", default="0,2,4,6,8,10,12"); ap.add_argument("--seed0", type=int, default=2000); ap.add_argument("--out", default="qualification/admission_sensitivity.csv")
    args = ap.parse_args(); margins = [float(v) for v in args.margins.split(",") if v.strip()]; rows = run(args.replicates, args.n, margins, args.seed0)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for r in rows: print(f"margin={r['bic_margin']:g} family={r['family']:22} chi_admission={100*r['chi_admission_rate']:5.1f}%")

if __name__ == "__main__": main()
