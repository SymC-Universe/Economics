# Q040 Metric/Event Selection Bank E2 Freeze
**Date:** 2026-10-02
**Authority:** Q040 Synthetic Estimator Implementation Closure v0.1 + Q040 Baseline Operator Plan Delta v0.2
**Execution prerequisite:** `Q040_BASELINE_SELECTION_B2_PASS`
**Real Q040 outcomes:** SEALED

## Purpose

Freeze a fresh metric/event/horizon selection bank before the B2 baseline winner is known. The B2 result supplies only the fixed global baseline class/window. It does not supply metric/event evidence.

## E2 seed bank

Use 14 replicas per required control × scale condition.

For control ordinal (o), scale (S), replica (r=0,ldots,13), and NC-R20 cell ordinal (c):

[
mathrm{SeedSequence}([20261002,o,S,1200+r,c]).
]

Single-cell controls use (c=0).

This namespace is disjoint from all original selection, confirmatory, Hawkes, baseline-repair, and exploratory namespaces.

## Required ranking controls

Use the implementation-closure ranking set:
- NC-R1 through NC-R7;
- NC-R9 through NC-R13;
- NC-R15 through NC-R20;
- all 24 NC-R20 measurement cells;
- all four scales.

NC-R8, NC-R14, and NC-R21 remain mandatory downstream controls but do not rank event thresholds.

## Frozen candidate family

Metric:
- D1;
- D2.

Entry quantile:
[
q_Ein{0.95,0.975,0.99}.
]

Return quantile:
[
q_Rin{0.50,0.60,0.70}.
]

Sustain:
[
Kin{2,3,5}.
]

Minimum separation:
[
Min{2,5,10}.
]

The global B2 baseline is fixed for every candidate.

## Required gates

A metric/event tuple is eligible only if:
- no required metric-fit fold is refused;
- overall median true-event recall >=0.80;
- every required control × scale × measurement cell has median recall >=0.60;
- overall median false-entry/true-entry ratio <=0.25;
- every required cell has median false ratio <=0.75;
- overall median terminal-state concordance >=0.75.

No threshold relaxation is allowed.

## Global ordering

Across the complete four-scale E2 bank, eligible candidates are ordered lexicographically by:
1. median normalized entry-timing error;
2. median normalized sustained-return timing error;
3. median false-entry ratio;
4. less extreme entry quantile;
5. shorter sustain duration;
6. longer minimum separation;
7. D1 before D2;
8. ascending return quantile as a final deterministic technical tie-break.

One global metric/event tuple is frozen.

If none is eligible return:
`Q040_EVENT_DEFINITION_REFUSED_E2`.

## Horizon

The horizon diagnostic is re-evaluated on E2 generator truth using the already-frozen {20,40,80} rule. It cannot rescue an event-definition refusal.

## Ceiling

E2 may execute only after B2 PASS. E2 does not authorize real Q040 outcomes or M0/M2 confirmation. After E2 freezes a pipeline, the confirmatory C bank remains separate.

`Q040_METRIC_EVENT_BANK_E2=FROZEN_PROSPECTIVELY`
