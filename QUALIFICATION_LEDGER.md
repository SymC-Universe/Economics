# Market Χ Engine Qualification Ledger

Status: P0-Q active
Branch: `market-chi-architecture`
GOM baseline: v0.8.0

This ledger records qualification work for the native-model-first rebuild. It does not convert synthetic or previously viewed evidence into P1 confirmation.

| ID | Target | Test | Current status | Promotion consequence |
|---|---|---|---|---|
| Q001 | scalar χ licensing | derive χ from known discrete complex pole pair | PASS / implemented | required for second-order complex branch |
| Q002 | scalar χ licensing | derive χ from known positive real pole pair | PASS / implemented | required for overdamped real-pole branch |
| Q003 | refusal | white noise must not receive χ | PASS in current baseline sweep | blocks release if violated materially |
| Q004 | refusal | ordinary AR(1) must not receive χ merely from persistence | PASS in current baseline sweep | blocks release if violated materially |
| Q005 | model admission | known AR(2) complex factor selected against AR0/AR1 | PASS in current baseline sweep | qualifies first local modal path |
| Q006 | model admission | known AR(2) real factor selected against AR0/AR1 | PASS in current baseline sweep | qualifies first overdamped path |
| Q007 | legacy ACF route | correct position-versus-velocity kernel mismatch and re-test | OPEN | legacy results remain historical/P0-Q until resolved |
| Q008 | exact simulation | replace Euler known-truth oscillator with exact or production-qualified discretization | OPEN | required before oscillator known-truth campaign |
| Q009 | non-oscillator alternatives | GARCH/SV/jump/regime-switching adversarial families | PARTIAL | stochastic-volatility false-admission tail remains; broader alternatives still required |
| Q010 | uncertainty | calibrate coverage for the exact production estimator | OPEN | required before uncertainty claim |
| Q011 | multivariate/modal | qualify modal layer separately from χ | PARTIAL / FIRST REAL DAY | two-axis L10 depth subspace discovered on 2026-05-31; cross-day replication required |
| Q012 | local-to-embedded | test whether local dynamical structure survives sector/market embedding | OPEN | substrate-inheritance target; current corpus is single-instrument MNQ |
| Q013 | real-data input gate | inventory and schema-profile local corpus before scale | PASS | corpus identified as MNQ trades + MBP-10; loader contract fixed |
| Q014 | MBP-10 data contract | raw price/timestamp semantics, flags, 10-level fields, continuous-symbol handling | PASS / documented | licenses native microstructure extraction |
| Q015 | MBP-10 first-pass code | synthetic fixture verifies price scale, contract segmentation, snapshot-flow exclusion | PASS | permitted first real development-file run |
| Q016 | real MBP-10 loader | run first-pass extractor on 2026-05-31 file and audit outputs | PASS | 725,631 rows -> 7,225 1-s event bins; no timestamp disorder or bad-book flags |
| Q017 | future holdout independence | freeze 2026-06-09 through 2026-06-11 MBP-10 observation files by provider hashes without inspecting rows | PASS / SEALED | preserves candidate P1 evidence |
| Q018 | contract-roll safeguard | prevent calendar continuous-contract rollover from appearing as physical return/Χ/χ transition | IMPLEMENTED; SINGLE-INSTRUMENT REAL CHECK PASS | rollover-specific real case still required before multi-contract claims |
| Q019 | signed microprice channel | detect v1 sign-loss defect; preserve negative/zero offsets in v2 and regression-test identity | PASS IN V2; V1 QUARANTINED FOR MICROPRICE | v2 required for all new raw extractions |
| Q020 | native depth geometry | recover interpretable L10 modal structure without using χ | PASS P0-D ON 2026-05-31 | PC1 liquidity + PC2 side-imbalance geometry must replicate on weekday development days |
| Q021 | χ refusal on real native modes | apply production χ gate to discovered modes across 1-60 s sampling | PASS AS REFUSAL BEHAVIOR | zero χ admissions on first day; protects against oscillator-first interpretation |
| Q022 | forward-risk discovery | compare depth modes/native scalars with future path movement | P0-D SIGNAL FOUND | dependence-aware cross-day validation and native comparator freeze required before prediction claim |

## Current P0-Q rule

The initial executable scalar scaffold compares AR(0), AR(1), and AR(2) using BIC and emits χ only when AR(2) wins by a configurable qualification margin and its poles admit a canonical continuous second-order mapping.

The default BIC margin of 6 is a P0-Q qualification setting, **not** a frozen physical boundary and not a P1 decision rule. It may change during controlled qualification with the search history preserved.

Real-market development no longer begins at that scalar scaffold. The native path starts from the Databento MNQ MBP-10 book and trade fields, preserves ten-level vector structure, separates synthetic snapshots from endogenous flow, segments actual contracts, and defers χ until downstream model admission.

The first real modal discovery supports that architecture: a stable leading two-dimensional depth subspace was recovered while the scalar χ gate correctly refused the dominant series because their admitted discrete second-order fits contained a negative real pole and therefore did not license the canonical continuous embedding.

See:

- `qualification/ADVERSARIAL_BASELINE_2026-09-14.md`
- `qualification/admission_sensitivity_2026-09-14.csv`
- `qualification/HOLDOUT_FREEZE_2026-09-14.md`
- `qualification/MNQ_2026-05-31_MODAL_DISCOVERY.md`
- `data_contract/MNQ_DATABENTO_CONTRACT_2026-09-14.md`
