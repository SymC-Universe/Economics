# Market Χ Engine Qualification Ledger

Status: P0-Q active
Branch: `market-chi-architecture`
GOM baseline: v0.8.0

This ledger records qualification work for the native-model-first rebuild. It does not convert synthetic or previously viewed evidence into P1 confirmation.

| ID | Target | Test | Current status | Promotion consequence |
|---|---|---|---|---|
| Q001 | scalar χ licensing | derive χ from known discrete complex pole pair | implemented | required for second-order complex branch |
| Q002 | scalar χ licensing | derive χ from known positive real pole pair | implemented | required for overdamped real-pole branch |
| Q003 | refusal | white noise must not receive χ | implemented | blocks release if violated materially |
| Q004 | refusal | ordinary AR(1) must not receive χ merely from persistence | implemented | blocks release if violated materially |
| Q005 | model admission | known AR(2) complex factor should be selected against AR0/AR1 | implemented | qualifies first local modal path |
| Q006 | model admission | known AR(2) real factor should be selected against AR0/AR1 | implemented | qualifies first overdamped path |
| Q007 | legacy ACF route | correct position-versus-velocity kernel mismatch and re-test | OPEN | legacy results remain historical/P0-Q until resolved |
| Q008 | exact simulation | replace Euler known-truth oscillator with exact or production-qualified discretization | OPEN | required before oscillator known-truth campaign |
| Q009 | non-oscillator alternatives | GARCH/SV/jump/long-memory/regime-switching adversarial families | OPEN | required before broad real-data interpretation |
| Q010 | uncertainty | calibrate coverage for the exact production estimator | OPEN | required before uncertainty claim |
| Q011 | multivariate/modal | qualify correlation/factor/network layer separately from χ | OPEN | required for Χ reconstruction |
| Q012 | local-to-embedded | test whether local dynamical structure survives sector/market embedding | OPEN | substrate-inheritance target |

## Current P0-Q rule

The initial executable scaffold compares AR(0), AR(1), and AR(2) using BIC and emits χ only when AR(2) wins by a configurable qualification margin and its poles admit a canonical continuous second-order mapping.

The default BIC margin of 6 is a P0-Q qualification setting, **not** a frozen physical boundary and not a P1 decision rule. It may change during controlled qualification with the search history preserved.
