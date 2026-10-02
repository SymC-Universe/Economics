# Q040 Baseline Operator Plan Delta v0.2
**Date:** 2026-10-02
**Parent refusal:** `qualification/Q040_BASELINE_SELECTION_FAILURE_IDENTIFIABILITY_AUDIT_2026-10-02.md`
**Exploratory extensions:** `qualification/Q040_BASELINE_FAILURE_SWEEP_EXTENSION_v0.2_2026-10-02.md`
**Real Q040 outcomes:** SEALED
**Promotion eligibility of exploratory sweeps:** NO

## 1. Scientific basis

The frozen v0.1 baseline family `{10,20,40}` samples was refused because sparse clustered NC-R20 measurement cells could not meet the preregistered 90% per-world coverage floor.

Two exploratory-only failure sweeps mapped the measurement-identifiability boundary without promotion authority. The outer sweep showed that both K1 and K2 first enter an all-scale identifiable region at 480 samples, while 640 samples yields full coverage in the exploratory bank across all four scales. Moving-baseline error did not worsen over 480->640 in the exploratory bank.

These exploratory outcomes may define a new prospective candidate family but may not promote a candidate.

## 2. Prospective v0.2 baseline family

Retain both baseline classes:
- K1 causal trailing robust-location baseline;
- K2 causal local-linear moving-attractor baseline.

Freeze candidate windows to:

[
Win{480,640} 	ext{samples}.
]

No 320-sample candidate is retained because the failure-mapping bank showed that 320 remains outside the all-scale identifiability region.

All K1/K2 definitions, distinct-update counting, numerical refusal rules, normalized baseline error, and 90% per-world coverage floor from the implementation closure remain unchanged.

## 3. Fresh qualification bank B2

Use a new disjoint baseline-only qualification bank.

For control ordinal (o), scale (S), replica (r=0,ldots,13), and NC-R20 cell ordinal (c):

[
mathrm{SeedSequence}([20261002,o,S,1100+r,c]).
]

For single-cell controls set (c=0).

This namespace is disjoint from:
- original selection bank namespace (100+r);
- confirmatory history bank (200+r);
- event-history bank (300+);
- exploratory failure sweep namespaces (900+r) and (950+r).

## 4. Required controls

The full baseline qualification grid remains:
- NC-R5 moving baseline;
- NC-R15 changing noise;
- NC-R16 heteroskedastic coordinate;
- all 24 NC-R20 measurement cells;
- all four scales 15/30/60/300 s;
- 14 replicas per condition.

No failed measurement cell may be omitted.

## 5. Global selection rule

Each candidate ((K,W)) is pooled across the complete four-scale B2 bank.

A candidate is eligible only if **every required world** has:
- baseline coverage >= 0.90;
- finite normalized baseline error.

Among eligible candidates select the lowest median normalized baseline error across the complete B2 bank.

Exact ties:
1. K1 before K2;
2. shorter window.

If no candidate is eligible return:

`Q040_BASELINE_OPERATOR_REFUSED_V0_2`.

A per-scale winner is reported diagnostically but does not create four independent baseline choices.

## 6. Downstream ceiling

A B2 pass freezes one global baseline class/window for subsequent D1/D2 and event-definition qualification.

A B2 pass does **not** authorize real Q040 outcomes.

If B2 refuses all candidates, Q040 remains at a baseline-identifiability scientific gate and no D1/D2 or history qualification is authorized.

## 7. Current status

`Q040_BASELINE_PLAN_DELTA_V0_2=FROZEN_PROSPECTIVELY`

`Q040_REAL_OUTCOMES=SEALED`

`NEXT=RUN_DISJOINT_B2_BASELINE_QUALIFICATION`
