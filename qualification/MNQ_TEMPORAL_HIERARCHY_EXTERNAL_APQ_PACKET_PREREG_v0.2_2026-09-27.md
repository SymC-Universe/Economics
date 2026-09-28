# External-Cognition APQ Attack Packet: MNQ Temporal Hierarchy Preregistration v0.2

Date: 2026-09-27
APQ level: APQ-2 Substantial
Candidate preregistration:
`qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.2_2026-09-27.md`
Candidate preregistration commit:
`32efaa69879131889965d71ab799d42e7d291548`
Prior-art closure commit:
`8204a340a71b9e511cc06bd6b233a93a9adb1e84`

## Reviewer instruction

Perform an isolated adversarial first-pass review of the preregistration. Do not optimize it for success and do not assume SymC, Stability Architecture, temporal inheritance, or the MNQ semantic hierarchy is correct.

Classify every objection:
- BLOCKER
- MATERIAL
- MINOR

For every BLOCKER or MATERIAL objection state:
1. exact threatened inference;
2. why the current control does not resolve it;
3. smallest discriminating change/test that would resolve it;
4. whether that change is outcome-independent and safe before real-data execution.

Attack shared premises. Do not vote with the plan.

## Literature boundary already accepted

Do not give credit for generic novelty in:
- multiscale LOB behavior;
- multi-horizon LOB prediction;
- deeper-book information;
- OFI scaling/aggregation robustness;
- interpretable PCA/microstructure modes;
- symmetric/antisymmetric mode families;
- multiscale Granger causality or transfer entropy;
- functional/factor forecasting of LOB curves;
- generic modal persistence after coarse-graining.

Closest predecessors already incorporated:
- Eisler, Kertesz & Lillo 2007, `The limit order book on different time scales`;
- Cont, Kukanov & Stoikov, `The Price Impact of Order Book Events`;
- Corradi, Zaccaria & Pietronero, `Liquidity crises on different time scales`;
- Bechler & Ludkovski, `Order Flows and Limit Order Book Resiliency on the Meso-Scale`;
- Xu, Gould & Howison, multi-level OFI;
- Cont/Cucuringu/Zhang, multi-level OFI and forecasting;
- Elomari-Kessab et al., microstructure modes;
- Golub et al., multiscale liquidity;
- Faes et al. and Zhao et al., multiscale information/causality;
- functional/factor LOB curve forecasting literature.

Residual novelty target is conditional and may still be rejected:
a previously qualified semantic L10 architecture across fixed wall-clock adjacent scales, semantic-vs-rank separation, representation qualification before inheritance language, and conditional fine->coarse lagged information beyond current/previous coarse state and native context.

## Frozen scientific skeleton to attack

Data:
- MNQ only;
- development dates May 27, May 28, May 29, June 1, June 2, 2026;
- 00:00-21:00 UTC;
- June 9-11 prohibited from tuning.

Scales:
- 15 s, 30 s, 60 s, 300 s;
- adjacent lead-1 pairs primary;
- leads 2/3 secondary.

Source representation:
- validated MBP10 v2;
- L10 last-book states;
- within-day state persistence, no backfill;
- log-depth before temporal aggregation;
- alternating bid/ask coordinate order.

Semantic coordinates:
- fixed symmetric-depth direction;
- fixed bid-ask imbalance direction.

Layer R:
- day x scale PCA after block aggregation and per-coordinate standardization;
- fixed k=6;
- exact isotropic q95 0.5496416495066101;
- ordinary + 1/99 winsorized sensitivity;
- representation qualifies only with 4/5-day and median rules in both analyses.

Layer L:
- future target = next coarse semantic block;
- native comparator includes current + previous coarse semantic state, first two session-phase harmonics, activity, trade volume, signed trade volume, spread, microprice offset, native L10 imbalance;
- OLS only;
- 5 h minimum training, hourly expanding refits, target-time leakage guard.

Factor-2 pairs:
- 15->30 and 30->60 use signed two-child semantic contrast;
- explicitly acknowledge equivalence of parent mean + last child and the full two-point path.

Factor-5 pair:
- 60->300 compares native baseline N;
- last-fast comparator L;
- unordered variability comparator U;
- ordered model S adds semantic slopes.

Inference:
- day-stratified circular block bootstrap;
- 10,000 reps;
- 1 h primary dependence blocks;
- 30 min and 2 h sensitivities;
- seed 20260929;
- 98.333% intervals across the three primary pair questions;
- all days preserved.

Interpretation:
- representation qualification and lagged-information inference separate;
- no causal language from prediction;
- no scalar chi;
- no trading claim;
- no cross-market universality.

## Mandatory attack targets

At minimum attack:

1. Whether carrying last book state through no-event seconds is scientifically valid or creates artificial persistence.
2. Whether using block means of log-depth creates an aggregation identity that undermines Layer R or L.
3. Whether direct semantic coordinates derived from Q038 directions are genuinely licensed outside Q038's standardized-PCA space.
4. Whether full-session scale-specific PCA is a fair representation-qualification test.
5. Whether exact isotropic Beta capture is an appropriate benchmark for data-estimated PCA subspaces.
6. Whether the 4-of-5 plus median representation rule is arbitrary or inadequately calibrated.
7. Whether 1/99 winsorization is an adequate heavy-tail sensitivity.
8. Whether current + previous coarse state is enough to control long memory.
9. Whether the native comparator omits an obvious stronger native variable or unfairly includes redundant variables.
10. Whether session-phase Fourier terms adequately control intraday nonstationarity.
11. Whether OLS is defensible with the predictor count and first 5 h of training, especially for 300 s blocks.
12. Whether training-only standardization and target-time guards fully prevent leakage.
13. Whether circular moving-block bootstrap is valid for strongly nonstationary intraday data and whether 1 h is defensible.
14. Whether Bonferroni 98.333% intervals correctly address the preregistered multiplicity.
15. Whether factor-2 contrast adds a scientifically meaningful test beyond simple recency.
16. Whether the 60->300 U/S nesting actually distinguishes unordered variability from ordered path.
17. Whether within-parent order-destroyed permutation is a valid noise-reduction control.
18. Whether the five development days are enough for 4/5 repeatability rules.
19. Whether prior use of these same development dates for Q023/Q036/Q037 compromises the epistemic interpretation of this new P0-D test despite the new outcomes being unviewed.
20. Whether a simpler alternative explanation, especially persistence, latent regime, activity, or scale-dependent liquidity depth, makes "inheritance" language inappropriate.
21. Whether any closer prior literature makes the residual novelty target non-novel.
22. Whether the joint structural/predictive map creates a post-hoc storytelling channel despite its non-primary status.

## Outcome discipline

The reviewer must not propose tuning to expected MNQ behavior.

A valid objection should either:
- expose invalid inference;
- force a stronger outcome-independent control;
- narrow the allowed claim;
- or demonstrate that the proposed question is already answered by prior art.

## Required response footer

End exactly with one:
- `APQ_EXTERNAL_STATUS=QUALIFIED`
- `APQ_EXTERNAL_STATUS=REVISE`
- `APQ_EXTERNAL_STATUS=BLOCKED`

Then repeat exactly:
`PREREG_COMMIT=32efaa69879131889965d71ab799d42e7d291548`
