# Pole-Stability Sensitivity and Gate Disposition

Date: 2026-09-18
Stage: P0-Q synthetic qualification
Production chi admission changed: NO

## Purpose

Stress blockwise AR2/pole reproducibility across sample length and difficult legitimate second-order cases before considering it as a chi-admission gate.

## Design

Sample lengths: 300, 600, 1200, 2400.
Replicates: 50 per cell.
Four contiguous subblocks per realization.
Existing BIC margin: 6.

The campaign reused the same hard second-order truth families as the walk-forward mean-persistence sensitivity map, including fast-decaying complex poles and weak-second-root real poles under homoskedastic, GARCH, and stochastic-volatility innovations.

## Result

False full-window admissions among null families generally had little independent block support. Across the four sample lengths, observed false GARCH/SV/jump admissions typically had AR2 support in 0-1 of 4 blocks.

However, legitimate difficult second-order cases overlap this behavior.

Examples:
- at n=300, admitted fast-decaying complex AR2 cases had median block support only 0-0.25 depending on innovation family;
- at n=600 and n=1200, admitted fast-decaying cases typically supported AR2 in only about 0.25 of blocks;
- even at n=2400, when the fast-decaying complex case was admitted 50/50, median block support was only 0.5;
- weak-second-root real AR2 cases also showed 0-0.5 support among the rare full-window admissions.

Exact pole-class agreement is also unsuitable as a universal rule because legitimate real-pole systems can move between estimated real and nearby complex classes in finite blocks even when the full-window mapping is correct.

## Conclusion

**Blockwise support persistence and pole stability are useful identifiability diagnostics, not universal chi gates.**

The combined qualification work now rules out three tempting shortcuts:
1. residual variance clustering as a veto;
2. positive walk-forward AR2 gain as a universal veto;
3. majority blockwise AR2 support / exact pole-class replication as a universal veto.

Each can reject legitimate second-order dynamics in difficult finite-sample regimes.

The correct next direction for Q009 is therefore richer native model competition and explicit identifiability reporting, not additional single-number refusal thresholds. A true second-order process may still be honestly refused when the observed window does not identify it; finite-sample refusal is not a contradiction of the underlying truth.

No production chi rule is changed by this campaign.

## Provenance

Workflow: `pole-stability-sensitivity-map`
Workflow commit: `7e67e1ae4fef3c2ba1e8f62a21e11430178e6e48`

Artifacts:
- n=300 `sha256:f94afee5742bffcc65a18c31304e60d7db0e7b84c8a7082c4e776896d97c5eda`
- n=600 `sha256:8dd85eb91928af222af23157383e71607932a65c43fb40d0b359e653b33cf042`
- n=1200 `sha256:ccffb99051bf66ddcc6b46f3d20b20807d98955f9eb50bfa9f0541d55564ff8d`
- n=2400 `sha256:a6e7a85cbf82632aacd85fa5ec118900cdfdbefb30b4c2787fa8024ca1adb383`
