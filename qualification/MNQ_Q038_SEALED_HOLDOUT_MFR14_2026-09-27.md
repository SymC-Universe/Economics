# Q038 Sealed-Holdout Semantic Preservation Plan

Date frozen: 2026-09-27
Stage: P1 candidate, confirmatory empirical/system-behavior test
Claim ID: Q038-P1-v1
Holdout: MNQ 2026-06-09 through 2026-06-11
Holdout status at freeze: SEALED_NOT_ACCESSED
Time basis: ordinary UTC wall-clock
Discovery/development evidence: May 27, May 28, May 29, June 1, June 2 only

This record implements the complete MFR-14 floor before any June 9-11 holdout byte is opened.

## MFR-01 — Frozen claim

Exact claim:

> In the sealed June 9-11 MNQ mature sessions, the predeclared L10 symmetric-depth / bid-ask-imbalance semantic backbone remains jointly preferentially represented in the leading six-dimensional standardized log-depth PCA subspace relative to isotropic orientation.

Scope:
- instrument family: MNQ continuous calendar-front MBP10 data under the existing project data contract;
- interval: each eligible day 00:00-21:00 UTC;
- primary windows: non-overlapping 30-minute wall-clock windows;
- representation: 20 L10 depth coordinates only;
- fixed subspace: k=6;
- claim scope is MNQ mature-session local/modal organization only;
- no market-wide Χ universality claim;
- no scalar χ claim;
- no predictive trading claim.

Primary estimand:

For window w and semantic unit vectors b_depth and b_imb,

C6(b,w) = ||Q6(w)^T b||^2

Core6(w) = min(C6(b_depth,w), C6(b_imb,w))

M6(w) = Core6(w) - q0.95[Beta(3,7)]

because d=20 and k=6.

Frozen exact isotropic q95:
- q0.95[Beta(3,7)] = 0.5496416495066101.

Primary statistic:
- median M6 over all eligible 30-minute holdout windows.

Intended value axis:
- empirical identifiability / structural preservation;
- not incremental predictive value.

Version: Q038-P1-v1.

## MFR-02 — Hypothesis provenance

Provenance:
- DOMAIN_THEORY: bid/ask L10 depth admits symmetric-depth and bid-ask-imbalance basis directions;
- DATA_DERIVED: fixed k=6 was selected only after Q036/Q037 development results showed that individual PC rank can migrate while the semantic pair is often recovered by wider fixed subspaces;
- FRAMEWORK_DERIVED: the broader Χ interpretation asks whether modal identity is preserved under rank migration.

The holdout is required because the k=6 confirmatory claim is data-derived.

## MFR-03 — Target object / native observable

Native observable:
- Databento GLBX.MDP3 MBP10 event-stream order-book depth for MNQ;
- 1-second event-time feature states constructed from the frozen v2 streaming extractor;
- L10 bid-size and ask-size fields are the directly measured state variables used by the PCA.

The claim can be contradicted by holdout L10 depth geometry that fails to preserve the canonical semantic directions.

## MFR-04 — Representation and validity regime

Frozen representation:
1. process each holdout daily raw MBP10 .zst with the frozen v2 streaming extractor at 1000 ms;
2. preserve actual instrument_id and mapped symbol;
3. form fixed 30-minute windows from 00:00-21:00 UTC;
4. within each eligible segment/window, create the 20 columns
   [bid_sz_00, ask_sz_00, ..., bid_sz_09, ask_sz_09];
5. apply log1p elementwise;
6. standardize each column within the window by its own mean and population standard deviation;
7. refuse the window if any depth column is constant;
8. compute full SVD/PCA;
9. use the leading fixed k=6 loading subspace;
10. compute sign- and rotation-invariant semantic capture.

Coverage:
- a segment/window requires >=0.80 observed-second coverage;
- requested window start must be observed;
- missing states may only be carried forward under the existing dense-state implementation after the first observed state;
- no imputation before the first observed state.

Continuous-contract segmentation:
- group each window by (instrument_id, mapped symbol);
- exactly one segment must independently satisfy the coverage/start rule;
- zero eligible segments -> window excluded as LOW_COVERAGE_OR_LATE_START;
- more than one eligible segment -> window refused as AMBIGUOUS_MULTI_INSTRUMENT;
- no outcome-based instrument selection is permitted.

Day-level validity:
- at least 34 of 42 primary windows must be eligible on each of the three holdout days;
- otherwise the confirmatory test is INVALID_TEST for insufficient coverage/segmentation integrity.

No adaptive k, semantic-basis rotation, threshold tuning, session redefinition or post-result exclusion is permitted.

## MFR-05 — Strongest relevant native comparator

Comparator status: COMPARATOR_IDENTIFIED.

Comparator:
- standard PCA/subspace geometry with an exact isotropic-orientation null.

Principal-angle/subspace comparison is standard numerical linear algebra; Björck and Golub, Mathematics of Computation 27(123), 579-594 (1973), DOI 10.1090/S0025-5718-1973-0348991-3, establishes principal-angle methods for comparing linear subspaces.

For semantic capture, the random-orientation null is analytic rather than Monte Carlo:

Let u = z / ||z|| for z ~ N(0,I_d), and let P be any fixed rank-k orthogonal projection. Rotational invariance permits P to select the first k coordinates. Then

||Pu||^2
= [sum_{i=1}^k z_i^2] / [sum_{i=1}^d z_i^2]
= X / (X + Y),

with independent X ~ chi-square_k and Y ~ chi-square_{d-k}.

Therefore

||Pu||^2 ~ Beta(k/2, (d-k)/2).

For d=20, k=6:
- null distribution = Beta(3,7);
- mean = 0.3;
- q95 = 0.5496416495066101.

This analytic comparator supersedes the finite 256-direction Monte Carlo control for the primary P1 decision. The finite control remains a development audit only.

No claim of ADDS_OVER_STANDARD_TOOLKIT is made.

## MFR-06 — Null / competing explanations

Primary null:
- the canonical semantic directions are no more preferentially represented than isotropically oriented directions in the fixed k=6 subspace.

Operational null benchmark:
- Core6 does not reliably exceed the exact isotropic 95th-percentile capture 0.5496416495066101.

Competing explanations preserved:
- apparent development preservation was a finite-sample accident;
- widening from k=2 to k=6 alone explains the apparent recovery;
- rank migration is unstable across unseen dates;
- rollover/instrument segmentation changes invalidate the representation;
- serial dependence made development windows appear more numerous than their effective information content.

## MFR-07 — Expected response

Primary expected direction:
- median M6 > 0.

Expected uncertainty behavior:
- the 95% serial-dependence-aware confidence interval for median M6 remains entirely above 0 under the frozen primary block length;
- the conclusion must not reverse under the frozen block-length sensitivity checks.

No expectation is frozen for scalar χ.

### Hierarchical secondary claim Q038-S1-v1

Only if Q038-P1-v1 survives:

The development-defined 08:30-11:00 UTC corridor exhibits stronger rank migration than the remainder of the mature session while the broader k=6 semantic backbone remains preferentially represented.

Secondary estimand:
- G6(w) = Core6(w) - Core2(w);
- contrast = median G6 within start-times 08:30, 09:00, 09:30, 10:00, 10:30 UTC minus median G6 outside that corridor.

The secondary expected contrast is > 0.

This corridor was derived post-Q037 and therefore cannot be used to rescue the primary claim.

## MFR-08 — Decision / adjudication rule

Primary 30-minute decision:

Compute a day-stratified circular moving-block bootstrap of the primary statistic.

Frozen bootstrap:
- 10,000 replicates;
- seed = 20260927;
- primary block length = 4 consecutive 30-minute windows = 2 hours;
- resample within each day, never across day boundaries;
- preserve each day's eligible-window count;
- statistic = median M6 pooled across the three resampled days;
- percentile 95% confidence interval.

Primary outcome:
- EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST if lower 95% CI > 0 and both frozen block-length sensitivity conclusions agree;
- EMPIRICAL_CLAIM_FALSIFIED if upper 95% CI <= 0;
- INDETERMINATE if the primary CI spans 0, or if a sensitivity block length changes a surviving primary conclusion to non-surviving;
- INVALID_TEST if MFR-04 data/segmentation validity fails or frozen code cannot compute the endpoint without a scientific change.

Block-length sensitivities:
- 2 windows = 1 hour;
- 6 windows = 3 hours.

Sensitivity analyses are robustness checks, not alternate decision rules.

Hierarchical secondary Q038-S1-v1:
- evaluated only if the primary survives;
- same day-stratified circular moving-block bootstrap, block length 4, 10,000 replicates, seed 20260928;
- SURVIVES SECONDARY if lower 95% CI of the corridor-minus-outside median G6 contrast > 0;
- otherwise secondary is FALSIFIED or INDETERMINATE by the same interval logic;
- secondary failure does not reverse primary survival.

## MFR-09 — Uncertainty, tolerance, indeterminate zone

Measurement/data uncertainty:
- native order-book sizes are taken as recorded by the feed, conditional on source-file and extraction integrity;
- source and feature SHA-256 hashes are recorded;
- gzip EOF/CRC and CSV-contract validation are required.

Serial dependence:
- handled by the frozen within-day moving-block bootstrap.

Model/representation uncertainty:
- primary block length 4;
- mandatory sensitivity block lengths 2 and 6;
- 60-minute fixed-window rerun is descriptive sensitivity only and cannot rescue the 30-minute primary decision;
- k=10 is descriptive architecture-recovery sensitivity only and cannot rescue k=6 failure.

Numerical tolerance:
- semantic capture is clipped only to [0,1] for floating-point roundoff;
- no scientific threshold receives a numerical tolerance adjustment after holdout inspection.

INDETERMINATE:
- primary CI contains 0;
- block-length sensitivity changes a primary SURVIVES result to non-surviving;
- uncertainty spans incompatible outcome classes.

INVALID_TEST:
- any holdout day has fewer than 34 eligible primary windows;
- source/cache integrity fails and cannot be repaired mechanically without changing frozen science;
- multi-instrument ambiguity prevents the minimum day coverage;
- a scientific code change would be required after evidence is opened.

## MFR-10 — Evidence-independence / leakage map

Discovery/development:
- May 27, May 28, May 29, June 1, June 2.

Decisive confirmation:
- June 9, June 10, June 11 only.

At freeze:
- June 9-11 raw evidence has not been opened by the research analysis;
- no holdout feature file has been inspected;
- no holdout PCA, semantic capture, coverage, source hash or outcome has been inspected.

Shared elements:
- same native extractor;
- same L10 representation;
- same semantic basis definitions;
- same fixed wall-clock session definition.

Not shared/tuned from holdout:
- k;
- semantic bases;
- isotropic comparator;
- q95 threshold;
- bootstrap block lengths;
- corridor;
- failure rules.

Any mechanical rerun after holdout access must use the same frozen science. Scientific changes require a new claim version and new untouched decisive evidence.

## MFR-11 — Multiplicity / search-space accounting

Confirmatory family:
1. one primary claim Q038-P1-v1;
2. one hierarchical secondary claim Q038-S1-v1 evaluated only after primary survival.

Primary:
- one resolution: 30 minutes;
- one k: 6;
- one canonical pair;
- one analytic null threshold;
- one primary statistic.

Non-decision-bearing sensitivities:
- 60-minute windows;
- k=10;
- block lengths 2 and 6.

No minimum-p-value search, adaptive k search, alternate session window, semantic-basis rotation, instrument cherry-picking, or post-hoc subgroup may alter the primary outcome.

## MFR-12 — Freeze identity / untouched decisive test

Freeze record:
- this file: `qualification/MNQ_Q038_SEALED_HOLDOUT_MFR14_2026-09-27.md`;
- branch: `market-chi-architecture`;
- exact execution commit will be inserted into the runner package after CI passes;
- decisive dataset: MNQ 2026-06-09, 2026-06-10, 2026-06-11 raw MBP10 files only;
- feature extraction interval: 1000 ms;
- mature-session interval: 00:00-21:00 UTC.

The runner must print and record the frozen Git commit before opening raw holdout files.

## MFR-13 — Explicit falsifier

The primary claim is falsified if the frozen 95% block-bootstrap interval lies entirely at or below M6 = 0.

The claim is not rescued by:
- k=10;
- 60-minute windows;
- the corridor analysis;
- a favorable single day;
- a post-hoc alternative semantic basis;
- scalar χ;
- redefinition of the mature session.

An INDETERMINATE result remains indeterminate and is not converted to survival.

## MFR-14 — Precommitted failure consequence

If EMPIRICAL_CLAIM_FALSIFIED:
- retire the statement that the MNQ L10 symmetric-depth / imbalance backbone is confirmatorily preserved in the declared mature-session regime;
- Q037 remains development evidence only;
- do not promote this semantic-backbone result to P1;
- do not reinterpret the failure as a different successful Χ structure using the same holdout;
- any new representation becomes a new hypothesis requiring new untouched decisive evidence.

If INDETERMINATE:
- keep the claim at development/P0 status;
- report the holdout as unresolved;
- do not retune k, threshold, corridor or semantic bases on June 9-11;
- obtain new untouched evidence for any renewed confirmatory attempt.

If INVALID_TEST:
- repair only the mechanical/infrastructure defect when possible;
- preserve the failed run and root cause;
- rerun the same frozen science only if evidence exposure cannot bias a scientific choice;
- otherwise acquire a new untouched confirmatory dataset.

If EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST:
- promote only the bounded MNQ mature-session semantic-preservation claim;
- do not claim market-wide Χ universality;
- scalar χ remains separately licensed/refused;
- cross-market transfer remains a separate future test.

## Holdout firewall

Until the plan, executable code, known-truth tests and freeze commit all exist and CI passes:

**DO NOT OPEN JUNE 9-11.**
