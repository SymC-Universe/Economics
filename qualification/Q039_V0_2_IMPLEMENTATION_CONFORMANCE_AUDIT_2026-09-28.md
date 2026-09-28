# Q039 Temporal Hierarchy v0.2 Implementation Conformance Audit

Date: 2026-09-28  
Branch: `market-chi-architecture`  
Preregistration binding: `32efaa69879131889965d71ab799d42e7d291548`  
Status: PRE-EXECUTION / IMPLEMENTATION-QUALIFICATION ONLY / NO REAL DATA AUTHORIZED

## Purpose

Record the exact engineering delta between the preserved `temporal_hierarchy_v2` prototype and the active preregistration candidate v0.2 without opening any May 27/28/29 or June 1/2 hierarchy outcome.

This document does not qualify the preregistration, does not substitute for external-cognition APQ, and does not authorize execution. The real-data gate remains closed until the preregistration-bound external review returns `APQ_EXTERNAL_STATUS=QUALIFIED`, all BLOCKER/MATERIAL objections are resolved, and the conformant implementation passes known-truth/CI qualification.

## Frozen source contract that the conformant implementation must satisfy

1. Use only validated MBP10 v2 feature files for 2026-05-27, 2026-05-28, 2026-05-29, 2026-06-01, and 2026-06-02.
2. Segment by actual `(instrument_id, symbol)`.
3. Preserve Q037/Q038 L10 coordinate order exactly as `bid_00, ask_00, ..., bid_09, ask_09`.
4. Use the `*_last` L10 size-state fields, not within-second mean depth.
5. Carry the last finite valid state forward only within the same day; no cross-day carry and no backfill before the first valid state.
6. Apply coordinate-wise `log1p` before temporal aggregation.
7. Require a defined carried state for every second of each 15/30/60/300 s block.

## Layer R obligations missing from the preserved prototype

The preserved prototype is not v0.2-conformant because it does not implement the complete preregistered representation gate. The conformant implementation must add:

- 15, 30, 60, and 300 s non-overlapping block construction from the carried 1 s log-depth state;
- scale-local standardization of all 20 coordinates;
- full SVD/PCA with fixed `k=6`;
- `C6_sym`, `C6_imb`, `Core6=min(C6_sym,C6_imb)`;
- strongest PC rank/alignment for both canonical directions;
- adjacent-scale k=6 principal cosines;
- full eigenvalue spectrum and effective rank;
- exact Beta(3,7) q95 comparison at `0.5496416495066101`;
- coordinate-wise 1st/99th percentile winsorized sensitivity;
- the frozen 4-of-5-day plus median qualification rule;
- `SEMANTIC_REPRESENTATION_QUALIFIED` / `SEMANTIC_REPRESENTATION_NEED_MORE_INFO` classification.

No lagged result may use inheritance language when either participating scale is representation-unqualified.

## Layer L obligations missing or nonconformant in the preserved prototype

### Native comparator N

The conformant comparator must contain all of:

- current coarse D/I;
- previous coarse D/I;
- session phase sin/cos at the first and second harmonics;
- log1p event-row count;
- log1p trade volume;
- signed_log1p signed trade volume;
- mean spread state;
- mean signed microprice-offset state;
- mean native L10 imbalance state.

Training-only standardization is required for all non-cyclic continuous predictors at each refit.

### Factor-2 transitions

For 15->30 and 30->60:

- each parent has exactly two fine children;
- fine information is the signed contrast `z2-z1`;
- the comparison is `N` versus `F2=N+DeltaD+DeltaI`;
- no higher-order path-shape claim is permitted;
- no separate superiority claim over last-fast is identifiable.

### Factor-5 transition

For 60->300 the nested sequence must be:

- `N`: native comparator;
- `L`: N + last-child D/I;
- `U`: L + child D/I standard deviations;
- `S`: U + least-squares D/I slopes versus child wall-clock position.

All N-vs-S, L-vs-S, and U-vs-S contrasts must be retained.

## Evaluation and numerical obligations

The conformant implementation must:

- use OLS with intercept only;
- use NumPy Moore-Penrose least squares if rank deficient;
- report design-matrix rank and condition number rather than silently dropping predictors;
- preserve the 5 h initial training history;
- refit at 1 h wall-clock boundaries with expanding past-only data;
- enforce target-end <= first-source-time leakage protection;
- require at least 8 wall-clock hours of valid OOS evaluation per day/pair;
- standardize target errors using training-only target standard deviations;
- report component MAE, component R2, day-level mean loss contrasts, and OOS counts.

## Dependence and classification obligations

For every primary loss contrast:

- stratify by day;
- 10,000 circular moving-block bootstrap replicates;
- primary 1 h dependence block;
- 30 min and 2 h sensitivity blocks;
- seed `20260929`;
- no cross-day resampling;
- report 95% descriptive intervals;
- use 98.333% two-sided intervals for the three primary adjacent-pair classifications.

The preserved prototype's 95% primary interval logic is not v0.2-conformant.

## Frozen negative controls required before any real-data run

Known-truth/CI qualification must explicitly pass:

1. session-phase-only synthetic truth;
2. coarse-sufficiency truth;
3. factor-2 fine-contrast truth;
4. five-child ordered-path truth beyond N/L/U;
5. frozen-seed within-parent order destruction for 60->300;
6. representation robustness including ordinary versus winsorized Layer R;
7. leakage refusal;
8. insufficient-evaluation refusal;
9. rank-deficiency reporting without feature deletion;
10. scale-unqualified language firewall.

## Implementation disposition

`market_chi/temporal_hierarchy_v2.py` and `tools/mnq_temporal_hierarchy_v2.py` remain preserved engineering prototypes only.

They are NOT authorized for real data under preregistration v0.2.

The next safe engineering step after the external APQ disposition is known is to implement the above contract outcome-independently, add known-truth tests, run CI, and only then consider opening the five development-day outcomes.

## Firewalls

- June 9-11 Q038 records may not tune or rescue Q039.
- No event labels, scalar chi, trading target, price-return target, additional scale, or additional lead may be introduced.
- No real development outcome may be opened under the preserved prototype.
- No external APQ token may be self-authored or inferred.
