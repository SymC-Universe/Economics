# Q039 v0.5 Factor-2 Identification Failure Record
**Date:** 2026-09-30  
**Governance:** SymC GOM v1.0 + Research Continuity and Execution Protocol  
**Execution:** frozen Q039 v0.5 P0-D development run  
**Disposition:** SCIENTIFIC / STRUCTURAL IDENTIFICATION FAILURE, not a transport or runtime fault

## Observed failure

All five frozen development days returned:

- `P15_30 = INVALID_TEST_INSUFFICIENT_IDENTIFICATION`
- `P30_60 = INVALID_TEST_INSUFFICIENT_IDENTIFICATION`

with zero primary OOS predictions.

The frozen refit diagnostics show every hourly factor-2 A2/F2 fit refused as `RANK_DEFICIENT / RANK_DEFICIENT`. At mature training sizes the deficit is exactly one rank in both models: A2 has (p=23), rank (22); F2 has (p=25), rank (24). The same failure occurs on every development day and at both factor-2 scales.

## Root cause

This is an exact algebraic dependence created by the preregistered factor-2 native-update comparator, not a chance property of one market day.

For two equal-duration fine children with L10 update fractions (u_1,u_2), the current coarse-parent update fraction in native comparator (N) is

[
u_P=rac{u_1+u_2}{2}.
]

The frozen A2 extension also includes:

[
u_2,qquad Delta u=u_2-u_1.
]

Therefore

[
u_P=u_2-rac{1}{2}Delta u.
]

The A2 design matrix is thus exactly rank deficient whenever all three frozen update-fraction terms are present. F2 inherits the same dependence.

This is a design-level identification collision between the coarse native comparator and the factor-2 fine-native extension. It is systematic and reproducible across all five days, not an isolated outlier.

## Frozen-rule consequence

The preregistration explicitly states:

- rank deficiency is a refusal for that refit;
- predictors may not be silently dropped to rescue identification;
- fewer than eight valid OOS hours yields `INVALID_TEST_INSUFFICIENT_IDENTIFICATION`.

Accordingly, the current P15_30 and P30_60 results remain invalid under Q039 v0.5. The opened development outcomes may not be used to choose which redundant predictor to remove and then rerun the same pair as though it remained prospectively confirmatory.

Any future factor-2 repair is a new prospective design/version and requires a new data/validation route.

## Unaffected branches

The failure does **not** invalidate:

- Layer R structural summaries;
- Q039 source identity or intake;
- the P60_300 factor-5 A->S test;
- the P60_300 U->S ordered characterization;
- the NC1-NC8 synthetic qualification lineage;
- NC7 Layer-R screening;
- NC7 for P60_300.

All five real P60_300 A->S and U->S day fits completed with the frozen identification rules.

## Mechanical recovery

The production runner initially raised `ValueError("empty day")` because the aggregation wrapper attempted to bootstrap an invalid pair with no primary predictions. That wrapper behavior is an implementation failure: it should preserve the preregistered invalid disposition and continue independent valid branches.

The permitted mechanical repair is therefore limited to:

1. preserve invalid factor-2 pair statuses without bootstrapping them;
2. continue Layer R and the valid P60_300 branch;
3. skip factor-2 NC7 point-contrast aggregation because NC7 cannot rescue an invalid primary test;
4. retain all opened failure evidence and diagnostics unchanged.

No predictor is dropped, no threshold is changed, and no failed pair is converted to success.

## Current scientific status

`Q039_FACTOR2_IDENTIFICATION=REFUSED_V0_5`

`Q039_P60_300=CONTINUE_FROZEN_PIPELINE`

`Q039_LAYER_R=CONTINUE_FROZEN_PIPELINE`
