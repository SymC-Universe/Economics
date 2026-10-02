# Q039 v0.5 Scientific Interpretation / Failure-Outlier Audit
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.0 + Research Continuity and Execution Protocol  
**Scope:** completed frozen P0-D development result only; Q038 June 9-11 holdout remains unused  
**Result identity:** SHA-256 `45BEF38E617C736FB3B7F4AE0B458384440FE83FC826C28112DB1C43610C89BB`

## Audit disposition

Q039 v0.5 does not support a unitary PASS/FAIL interpretation across the full 15 s -> 30 s -> 60 s -> 300 s hierarchy.

The factor-2 branches and the factor-5 branch failed for different reasons and must remain scientifically separated.

### 1. P15_30 and P30_60: structural identification refusal

Both factor-2 primary tests are `INVALID_TEST_INSUFFICIENT_IDENTIFICATION` on all five development days.

This is not evidence that fine semantic state lacks incremental information. It is an exact design-level collinearity in the preregistered comparator:
[
u_P=(u_1+u_2)/2,qquad Delta u=u_2-u_1,qquad u_P=u_2-	frac12Delta u.
]
Therefore the current v0.5 factor-2 specification cannot identify the requested contrast. No predictor may be dropped post-outcome to rescue the same test. Any repair requires a new prospective version and a fresh validation/data route.

Disposition:
`P15_30=REFUSED_IDENTIFICATION_V0_5`
`P30_60=REFUSED_IDENTIFICATION_V0_5`

### 2. Layer R: canonical capture is real, but scale-specific structural qualification is asymmetric

At every scale, real symmetric-depth and bid-ask-imbalance canonical captures are far above the 200-world NC7 q95 matched-timing null. This rejects a simple carry-forward/update-timing explanation for the observed canonical capture.

However, the adversarial structural classification is not uniform across scale. At 15 s, 30 s, and 60 s, neither canonical direction passes the frozen structure-specific criterion and both remain common-mode dominated. At 300 s, the symmetric direction remains common-mode dominated, but the imbalance lineage and imbalance functional directions become structure-specific and cease to be common-mode dominated.

Accordingly, Q039 does not qualify a uniform multiscale semantic architecture. It identifies a bounded scale-local change at 300 s in the imbalance direction that warrants prospective follow-up.

Disposition:
`LAYER_R_15_30_60=CANONICAL_CAPTURE_WITHOUT_STRUCTURE_SPECIFIC_QUALIFICATION_P0D`
`LAYER_R_300_IMBALANCE=STRUCTURE_SPECIFIC_P0D_DEVELOPMENT_SIGNAL`

This does not by itself license (Χ_S) or (Χ_{arc}) promotion.

### 3. P60_300 A->S: real signal, primary gate not passed

The frozen P60_300 primary A->S contrast is positive:
[
Delta L_{A,S}=0.0365167603.
]

The five equal-day point contrasts are:
[
[0.0181129, 0.0522682, -0.0043804, 0.00282736, 0.1137558].
]

Four of five days are positive. Pooled out-of-sample MAE improves for both semantic targets:
- D: 0.367234 -> 0.349837;
- I: 0.118706 -> 0.117982.

The real point contrast also exceeds the NC7 q95:
[
0.0365168 > 0.00825616.
]

Known-truth controls passed.

Nevertheless, the preregistered primary 98.333% one-hour moving-block interval crosses zero:
[
[-0.00259638, 0.0815603].
]

The 30-minute sensitivity is positive:
[
[0.00116828, 0.0910634],
]
while the two-hour sensitivity again crosses zero:
[
[-0.00482786, 0.0666698].
]

Therefore the correct frozen classification remains:
`P60_300=NEED_MORE_INFO_OR_MIXED_P0D`.

The signal is scientifically nontrivial but dependence-scale sensitive and cannot be promoted as a positive primary result.

### 4. Day-level heterogeneity / outlier audit

The largest positive day is 2026-06-02 with point contrast 0.113756. It is a high-leverage contributor to the pooled positive point estimate.

The June 2 measurement diagnostics do not show an obvious gross carry-forward/staleness failure: mean update fraction is 0.998347, median update fraction is 1.0, mean block staleness is approximately 0.00184 s, and maximum block staleness is 4 s. The day also retains strong 60->300 k=6 subspace continuity, with minimum principal cosine 0.95467 and median 0.99732.

June 2 therefore cannot currently be dismissed as a simple measurement-quality artifact. But because the remaining day effects range from slightly negative to moderately positive, the signal is materially heterogeneous. The high-leverage day must be treated as a regime candidate, not removed as an outlier and not used alone to promote the claim.

The correct next question is whether the gain is conditional on a measurable market state/regime that can be frozen prospectively, rather than whether the pooled point estimate can be made significant by exclusion.

### 5. Ordered-path characterization is not supported

The frozen U->S ordered-path contrast is:
[
-0.00851968,
]
with 95% interval:
[
[-0.0228095, 0.00912851].
]

Thus the data do not show that the ordered 60 s child path adds information beyond the unordered/summary comparator under the frozen test.

This matters for the recovery program: Q039 does not establish that the exact within-300 s ordering of the five 60 s states is the predictive object. The prospective recovery analysis should therefore avoid assuming that trajectory order has already been licensed by Q039.

Disposition:
`P60_300_ORDERED_PATH=NOT_SUPPORTED_P0D`.

## Recovery-program interpretation

Q039 does not test recoverability directly, and it must not be converted into a recovery claim.

What it does provide is a bounded architectural clue:
1. canonical L10 depth/imbalance directions are not explained by the matched timing/carry-forward null;
2. 300 s imbalance organization is qualitatively different under the frozen structure-specific/common-mode challenges;
3. 60 s semantic information shows a reproducible but heterogeneous and dependence-sensitive incremental relation to the next 300 s semantic state;
4. exact 60 s child ordering is not supported as the added-information mechanism.

This is consistent with, but does not prove, the hypothesis that recovery/reorganization becomes more identifiable at the 60->300 s transition than at shorter adjacent scales.

Q040 must therefore remain native-state-first and independently qualified. Q039 may be cited only as development evidence motivating explicit 60/300 stratification or diagnostics. It may not qualify a Q040 representation, recovery law, basin, threshold, or (Χ_{arc}) claim.

## Required prospective successor

The next Q039-specific work is not an automatic rerun.

A new prospective successor should contain two independent branches:

1. **Factor-2 identifiability repair:** redesign the 15->30 and 30->60 native comparator so the exact update-fraction algebraic dependence is removed prospectively, then validate on synthetic known truths and execute on a fresh data route. The opened v0.5 development outcomes cannot select which redundant term is removed.

2. **P60_300 regime/heterogeneity test:** freeze a small, native, outcome-independent set of candidate regime descriptors before looking at any new outcome data, then test whether the A->S gain is stable or conditional. June 2 is a regime candidate, not an exclusion candidate.

For the central recoverability investigation, Q040 remains the primary lane. Its next scientific gate should explicitly test recovery classes including return, delayed return, incomplete return, overshoot/rebound, baseline migration, and persistent reorganization without importing a positive Q039 conclusion that was not earned.

## Final audit status

`Q039_SCIENTIFIC_AUDIT=COMPLETE`

`Q039_V0_5_GLOBAL_DISPOSITION=MIXED_WITH_STRUCTURAL_IDENTIFICATION_FAILURES`

`Q039_RECOVERY_HANDOFF=BOUNDED_MOTIVATING_EVIDENCE_ONLY`

`Q039_AUTOMATIC_RETUNE=PROHIBITED`

`Q039_NEXT=PROSPECTIVE_SUCCESSOR_SPECIFICATION`
