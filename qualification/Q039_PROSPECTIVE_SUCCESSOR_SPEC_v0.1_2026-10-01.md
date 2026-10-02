# Q039 Prospective Successor Specification v0.1
**Date:** 2026-10-01
**Governance:** SymC GOM v1.0 + Research Continuity and Execution Protocol
**Predecessor:** Q039 v0.5 scientific audit at commit `c4a273a07747b53de98269baec965c67d7df06f2`
**Status:** PROSPECTIVE SPECIFICATION; NO SUCCESSOR REAL OUTCOMES OPENED
**Cost rule:** zero-cost execution only; paid GitHub compute is prohibited

## 1. Purpose and firewall

Q039 v0.5 produced two different unresolved objects and they remain separated:
1. exact factor-2 identification failure at 15->30 s and 30->60 s;
2. a mixed, dependence-sensitive 60->300 s incremental-information signal with scale-local 300 s imbalance structure.

This successor may not reinterpret v0.5 invalid factor-2 tests as null results, may not delete June 2 as an outlier, and may not use any opened v0.5 outcome to choose a rescue predictor, threshold, date, or regime definition.

The Q038 June 9-11 holdout remains prohibited.

## 2. Branch A: factor-2 identifiability repair

### A1. Canonical algebraic repair

For two equal-duration children, the parent update fraction is already in N:
[
u_P=(u_1+u_2)/2.
]

Conditional on (u_P), there is only one independent within-parent update-timing degree of freedom. Freeze it as:
[
Delta u=u_2-u_1.
]

Therefore successor comparator (A2^*) is identical to v0.5 A2 except that **last-child L10 update fraction is removed** and (Delta u) is retained. No alternative equivalent parameterization may be chosen after this freeze.

This choice is made from the exact algebraic dependency, not from observed predictive performance.

All other v0.5 N/A2/F2 fields, transforms, walk-forward rules, minimum-training rule, loss, bootstrap, multiplicity, and claim labels remain unchanged unless a separate prospective APQ objection requires a documented Plan Delta.

### A2. Pre-real qualification

Before any fresh real session is opened:
- prove full column rank symbolically for the frozen factor-2 update-timing block conditional on N;
- run numerical rank/condition preflights over known-truth synthetic worlds;
- rerun the factor-2 known-truth family, including coarse-sufficient, latent-regime, and semantic-recency worlds;
- require the semantic-recency known truth to recover ADD and the null worlds not to manufacture ADD;
- preserve refusal if the revised design remains unidentified.

No opened May 27/28/29 or June 1/2 outcome may be used for this qualification.

## 3. Branch B: P60_300 regime/heterogeneity test

### B1. Question

Does the out-of-sample incremental gain of the frozen v0.5 60->300 semantic model vary systematically with prospectively frozen native market regime descriptors?

This is a heterogeneity question, not an outlier-removal procedure.

### B2. Frozen regime descriptors

Use only current-parent variables already present in the v0.5 native comparator N. No new chart-selected indicator is admitted.

Four primary regime descriptors are frozen:
1. activity: (log(1+	ext{event rows}));
2. liquidity: mean spread;
3. book-pressure magnitude: (|	ext{mean native L10 imbalance}|);
4. directional-flow magnitude: (|	ext{signed-log1p signed trade volume}|).

All are standardized using training data only within each walk-forward refit.

June 2 does not define any threshold, sign, or descriptor.

### B3. Observation-level gain

For each eligible OOS 300 s target observation, retain the already-defined joint normalized losses:
[
L_A(t),qquad L_S(t),
]
and define:
[
g(t)=L_A(t)-L_S(t).
]

Positive (g) means the semantic extension improves that observation relative to the strong fine-native comparator.

### B4. Primary heterogeneity test

For each frozen descriptor separately, classify each test observation as LOW or HIGH using the **training-only median** of that descriptor at the current refit. Ties are assigned LOW.

Compute:
[
H_r=ar g_{mathrm{HIGH},r}-ar g_{mathrm{LOW},r}.
]

Inference uses the same non-circular within-day moving-block bootstrap discipline as Q039 v0.5, with one-hour primary blocks and equal day weighting.

The four descriptor-level tests form one family controlled by Holm step-down at two-sided familywise (alpha=0.05).

A regime descriptor is called heterogeneous only if:
- the Holm-adjusted primary interval excludes zero;
- both LOW and HIGH strata satisfy the frozen minimum-support rule;
- the sign of (H_r) is the same on at least 4/5 fresh sessions.

Otherwise it is reported quantitatively without a regime claim.

### B5. Minimum support / refusal

Each LOW/HIGH stratum must contain at least 20 eligible OOS 300 s observations pooled across the fresh five-session set and must be represented on at least 4/5 sessions.

Otherwise return:
`REGIME_HETEROGENEITY_INSUFFICIENT_SUPPORT`.

No stratum may be dropped because its result is inconvenient.

### B6. Interpretation ceiling

A positive heterogeneity result means only that semantic incremental information is state-conditioned under the frozen comparator class.

It does not establish:
- causal regime switching;
- recovery erosion or adaptation;
- basin change;
- (Χ_S) or (Χ_{arc});
- trading profitability.

Those remain Q040 or later questions.

## 4. Fresh-data route

Successor real execution requires a genuinely fresh MNQ MBP10 route.

Freeze the selection rule as:
- choose the first five chronologically available eligible regular MNQ MBP10 sessions **after 2026-06-02**;
- exclude 2026-06-09, 2026-06-10, and 2026-06-11 permanently because they are the protected Q038 holdout;
- exclude any session already opened for Q039 successor development or threshold selection;
- resolve source identity before feature extraction and record exact SHA-256, instrument ID, symbol, schema, and session bounds;
- no session may be substituted based on outcome behavior.

Current local inventory contains no eligible fresh post-June-2 MBP10 five-session set outside the protected Q038 dates.

Therefore:
`Q039_SUCCESSOR_REAL_EXECUTION=EXTERNAL_BLOCK_FRESH_MBP10_REQUIRED`.

No paid acquisition or paid GitHub compute is authorized. Kaggle or another free source may be used for synthetic/methodological qualification, but a different instrument/data product may not be silently substituted for the frozen MNQ-MBP10 fresh-route test.

## 5. Relationship to Q040

Q039 successor work does not gate Q040 within-scale recovery qualification.

The completed Q039 v0.5 audit is motivating evidence only. Q040 remains native-state-first and may not import a positive 60->300 recovery, inheritance, or architecture claim from Q039.

If Q040 independently finds a 60/300 recovery transition, the two lines may later be compared prospectively. Neither line may retroactively qualify the other.

## 6. Allowed outcomes

Branch A:
- `FACTOR2_REPAIRED_AND_QUALIFIED_FOR_FRESH_TEST`
- `FACTOR2_REPAIR_NOT_QUALIFIED`
- `FACTOR2_IDENTIFICATION_REFUSED_AGAIN`

Fresh factor-2 real test:
- existing v0.5 ADD / NO_GAIN / NEED_MORE_INFO labels, under the revised prospective identity;
- `INVALID_TEST` remains allowed.

Branch B:
- `REGIME_HETEROGENEITY_DETECTED_P0D`
- `NO_REGIME_HETEROGENEITY_DETECTED_P0D`
- `REGIME_HETEROGENEITY_MIXED_P0D`
- `REGIME_HETEROGENEITY_INSUFFICIENT_SUPPORT`
- `INVALID_TEST`

## 7. Current gate and next action

Mechanical/synthetic implementation of Branch A and Branch B is authorized only after this specification is source-reviewed for internal consistency.

Real successor execution remains blocked on the frozen fresh-data route.

No v0.5 real computation is to be rerun.
