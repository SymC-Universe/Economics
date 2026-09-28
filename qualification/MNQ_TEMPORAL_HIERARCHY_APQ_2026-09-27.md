# MNQ Temporal-Hierarchy APQ Record

Date: 2026-09-27
APQ level: APQ-2 Substantial
Plan packet: `qualification/MNQ_TEMPORAL_HIERARCHY_PLAN_PACKET_2026-09-27.md`
Plan-packet freeze commit: `b58b95f2ec9d722e0343c4f961e849d720f8f1be`

## Qualification status

**QUALIFIED FOR SYNTHETIC IMPLEMENTATION + CI ONLY**

**REAL DEVELOPMENT-DATA EXECUTION BLOCKED PENDING EXTERNAL-COGNITION APQ ATTACK**

Reason: the current execution environment provides literature sub-agents and connector tooling but not a second general-purpose cognition that can independently attack the complete plan. The GOM v0.8.8 APQ requirement is therefore not claimed as fully satisfied. This record preserves the partial qualification rather than silently substituting self-review for external adversarial review.

## Independent attack stream A: leakage / temporal alignment

BLOCKER:
A naive walk-forward split can leak because source block t predicts target t+1; if training is selected by source time alone, a training target can overlap or occur after the first test-source timestamp.

Resolution:
For every refit chunk, training observations are eligible only when their **target block ends before the first test-source block starts**. The implementation must expose this as an audit invariant and tests must fail if violated.

Status: RESOLVED BY DISCRIMINATING IMPLEMENTATION TEST.

## Independent attack stream B: aggregation identity

MATERIAL:
Because 15/30/60/300 s states are built from the same 1 s stream, contemporaneous reconstruction can appear strong by arithmetic identity. Such a result would not establish lagged cross-scale information.

Resolution:
Primary target is always the **next non-overlapping coarse block**. Lead zero is refused. Structured terms are computed only from the current parent block.

Status: RESOLVED.

## Independent attack stream C: comparator fairness

BLOCKER:
The earlier scaffold compared a rich six-summary structured model with a much poorer last-observation baseline. Improvement could simply reflect feature count.

Resolution:
Primary comparator is now a nested **coarse-context baseline** containing current coarse symmetric-depth, current coarse imbalance, and fixed session-phase sine/cosine terms. The structured model contains the same predictors plus only four predeclared fine-organization terms: two standard deviations and two slopes. Last-fast remains a mandatory comparator but cannot rescue failure against the stronger baseline.

Status: RESOLVED.

## Independent attack stream D: session-phase confounding

MATERIAL:
Known MNQ relationships vary by session phase. Fine-scale organization could merely proxy time of day.

Resolution:
Both baseline and structured models receive identical predeclared session-phase sine/cosine terms. A synthetic known-truth test must show no spurious structured gain when future state is determined by session phase alone.

Status: RESOLVED BY REQUIRED TEST.

## Independent attack stream E: scale-dependent sample advantage

MATERIAL:
Using the same number of observations at each scale would mean very different amounts of elapsed training time.

Resolution:
Use exactly five wall-clock hours of initial training at every pair and one-hour wall-clock refit/evaluation chunks. Bootstrap dependence blocks are also one wall-clock hour at every scale.

Status: RESOLVED.

## Independent attack stream F: overfit and adaptive representation

MATERIAL:
Using the full L10 vector with many summaries, adaptive PCA, or tuned regularization would create a large search space relative to five development days.

Resolution:
Primary semantic axes are fixed canonical symmetric-depth and bid-ask-imbalance directions. No PCA is fit. Primary structured additions are exactly four terms. OLS has no tuned hyperparameter. No feature selection is allowed after outcomes.

Status: RESOLVED.

## Independent attack stream G: multiplicity

MATERIAL:
Three scale pairs, several leads, two semantic targets, multiple metrics, and possible event definitions could become a garden of forking paths.

Resolution:
Primary family is exactly three adjacent scale pairs at lead 1. Pair-level decision uses one joint standardized squared-error contrast versus the coarse-context baseline. Leads 2 and 3 are secondary only and cannot rescue a primary pair. No event threshold is tested here.

Status: RESOLVED.

## Independent attack stream H: generic novelty

BLOCKER FOR NOVELTY CLAIM:
Published work already covers multiscale market causality, multiresolution liquidity, short/meso-scale LOB predictive power, and PCA/VAR microstructure modes.

Literature collision:
- Bechler & Ludkovski 2017 analyze LOB depth/shape and order-flow predictive power at meso scales and explicitly compare aggregation regimes.
- Golub et al. 2014 construct an intrinsically multiscale market-liquidity representation and distinguish structural coarse-graining from predictive stress information.
- Elomari-Kessab et al. 2024 construct interpretable symmetric/antisymmetric microstructure modes and model their temporal predictability with VAR.
- multiscale transfer-entropy literature already formalizes directional information flow across coarse-grained scales.

Resolution:
No novelty claim may be based on "markets have multiple scales", "LOB predicts future state", "PCA modes exist", or "cross-scale information transfer exists". The residual research target is whether a **previously qualified native semantic L10 architecture** carries incremental lagged information across fixed wall-clock adjacent scales under nested comparators and explicit preservation/reorganization/loss/refusal rules.

Status: GENERIC NOVELTY REFUSED; NARROWER TARGET RETAINED FOR TESTING.

## Independent attack stream I: Q038 contamination

BLOCKER:
June 9-11 outcomes could influence scales, features, thresholds, or interpretation.

Resolution:
Q038 may motivate use of the already-frozen semantic pair only. June 9-11 are forbidden from all tuning and from this development experiment. The plan uses only May 27, May 28, May 29, June 1, June 2.

Status: RESOLVED.

## Independent attack stream J: causal overreach

MATERIAL:
Lagged incremental prediction would not establish physical substrate inheritance or causal transmission.

Resolution:
Allowed outcome language is limited to **incremental lagged information** in the fixed semantic representation. "Substrate inheritance" remains a hypothesis-level interpretation pending stronger causal/discriminating evidence.

Status: RESOLVED.

## Plan Delta

Relative to the existing `market_chi/lagged_hierarchy.py` scaffold:

1. Replace generic six-summary rich model with a nested coarse-context baseline plus four fixed fine-organization additions.
2. Fix semantic representation to symmetric-depth and bid-ask-imbalance projections; no adaptive PCA.
3. Fix primary scales to 15->30, 30->60, 60->300 s.
4. Fix primary lead to one coarse block; lead 2/3 secondary.
5. Equalize initial training, refit cadence, and bootstrap block size in wall-clock time.
6. Add explicit target-time leakage guard.
7. Add session-phase harmonics to both baseline and structured models.
8. Add pair-level ADDS / SUBTRACTS / NEED_MORE_INFO classification.
9. Add synthetic confound and leakage tests.
10. Keep all real development execution blocked until an external-cognition APQ review is recorded and all BLOCKER/MATERIAL objections are resolved.

## Required pre-real-data tests

Synthetic/known-truth suite must include:
- fine organization adds beyond current coarse state;
- no-additional-information negative control;
- session-phase-only confound negative control;
- lead-zero refusal;
- insufficient coverage refusal;
- exact wall-clock scale/factor checks;
- target-time leakage invariant;
- deterministic seeded bootstrap reproducibility;
- pair classification known truths.

## Current gate

Engineering work may proceed through:
- implementation;
- unit tests;
- synthetic fixtures;
- CI;
- code review.

Do **not** run the May 27/28/29/June 1/2 real hierarchy experiment until the external-cognition APQ attack is recorded.

