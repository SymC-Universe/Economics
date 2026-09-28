# WORKING_INVESTIGATION.md

## Current State

- **Investigation:** Market Microstructure / temporal hierarchy / event mapping
- **Date:** 2026-09-27
- **Active GOM:** v0.8.8
- **Repository:** `SymC-Universe/Economics`
- **Branch:** `market-chi-architecture`
- **Stage:** Q038 CLOSED P1 + Q039 preregistration v0.3 external re-review
- **Status:** OPEN
- **Scalar χ:** currently REFUSED in production MNQ screens under existing rules
- **Broader Χ:** recurrent L10 semantic architecture supported at P0-D
- **User intervention required:** EXTERNAL APQ RE-REVIEW RETURN ONLY

## Current scientific state

Across the five MNQ development sessions, the L10 symmetric-depth / bid-ask-imbalance semantic backbone is substantially more stable than individual PCA rank identity. Rank migration and localized partial semantic disturbances occur in a state-dependent manner, while wider fixed subspaces usually recover the semantic backbone well above isotropic-orientation controls.

Q038 is now closed at P1. The frozen June 9-11 test returned `EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST`: all 42 primary windows completed on each day, the pooled fixed-k=6 margin above the exact Beta(3,7) isotropic q95 was 0.411995 with 95% block-bootstrap interval [0.399033, 0.427259], and both mandatory block sensitivities agreed. The hierarchical corridor secondary also survived. This promotes only the bounded MNQ mature-session semantic-preservation claim; scalar χ remains refused and market-wide universality remains untested.

A new development-only branch now tests the user's cross-timescale observation in a stricter form:

> Does structured fast-scale organization at time t contain information about a future coarse-scale state beyond the last fast observation and the coarse state's own persistence?

Current-scale reconstruction is explicitly not counted as prediction.

## Frozen / protected objects

### Q038
- Claim ID: Q038-P1-v1
- Holdout: 2026-06-09 through 2026-06-11
- Frozen execution commit: `d8a44204514a8111f524ef122d110714d9bafa29`
- No retuning after holdout opening.
- Allowed outcomes only: EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST / EMPIRICAL_CLAIM_FALSIFIED / INDETERMINATE / INVALID_TEST.

### Development temporal hierarchy
Initial scale ladder fixed from pre-existing trader-observation lineage:
- 15 s
- 30 s
- 60 s
- 300 s

Development data only:
- May 27
- May 28
- May 29
- June 1
- June 2

June 9-11 may not select hierarchy variables, scales, event definitions, thresholds, or models.

## Prior-art / novelty state

Established neighboring prior art includes market microstructure invariance in business time, multifractal/scale-dependent market behavior, multiscale price formation, LOB regime prediction, and lead-lag structure.

Therefore no novelty claim may rest on:
- markets being scale invariant;
- fractal/multifractal market behavior;
- generic LOB state prediction;
- generic lead-lag.

Residual question:
- whether a physically interpretable semantic architecture is inherited across fixed time aggregation levels;
- whether fast within-block organization has **lagged incremental information** about future coarse states;
- whether transition ordering/event structure is stable enough for prospectively frozen event mapping;
- whether the result later transfers across instruments without retuning.

## Engine state

New module:
- `market_chi/lagged_hierarchy.py`

Known-truth tests:
- structured fast shape predicts future coarse state where last-fast and coarse persistence do not;
- no artificial gain where fast block contains no additional information;
- insufficient-data refusal;
- zero-lead refusal.

Latest known-truth CI:
- run `36361848216`
- conclusion: SUCCESS
- commit: `6234f9be05bbc436c81279f9003e09aff13391be`

## ACCEPT / REFUSE / NEED_MORE_INFO

| Object | Status | Basis |
|---|---|---|
| recurrent L10 depth/imbalance semantic backbone | ACCEPT P1 BOUNDED | June 9-11 frozen holdout survived at fixed k=6; scope limited to MNQ mature-session regime |
| universal PC rank identity | REFUSE | rank migration is state-dependent |
| canonical scalar χ in current MNQ production screen | REFUSE | 0 admissions under current rules |
| PC1 incremental forward-risk value over total depth | EQUIVALENT P0-D | native total depth performs equivalently |
| universal predictive sign of depth/spread | REFUSE | session/state conditioned |
| temporal hierarchy as predictive information | NEED_MORE_INFO | known-truth engine qualified; real development run pending |
| event prediction | NOT YET TESTED | event labels not frozen |
| cross-market invariance | NOT YET TESTED | separate future transfer test |
| Q038 final outcome | PASS P1 | frozen primary and hierarchical secondary both survived; no retuning or rescue |

## Active hold

No Q038 hold remains. The decisive result is recorded and the bounded promotion consequence is active. The temporal-hierarchy branch remains development-only and must not use June 9-11 to select variables, scales, event definitions, thresholds, or models.

## Next exact action

Q039 v0.2 external APQ is complete and adjudicated. Material objections were accepted where scientifically valid, one hash-ambiguity blocker was rejected as a reviewer transcription error, and preregistration v0.3 is now the active candidate.

Canonical v0.3 preregistration commit:
`fde9121072694338c5c097984e6a417a993fee3a`

External re-review packet:
`qualification/Q039_EXTERNAL_APQ_REREVIEW_PACKET_v0.3_2026-09-28.md`

Real May 27/28/29 and June 1/2 Q039 execution remains blocked. The next authorized actions are:
1. send v0.3 to external cognitions for isolated APQ re-review;
2. build/requalify only synthetic/known-truth v0.3 machinery;
3. resolve any remaining BLOCKER/MATERIAL objections;
4. freeze preregistration + implementation;
5. only then open development outcomes.

The old v0.2 implementation and runner remain preserved lineage and are not authorized for real execution.

## Development Log

### 2026-09-27 — TEMPORAL HIERARCHY REOPENING
- User prioritized Market + SI before further geophysics.
- Motivation: market hierarchy may help formulate event mapping across timescales.
- Prior art narrows the target: generic scale invariance is not novel.
- Scientific correction: contemporaneous coarse reconstruction is not event prediction.
- Added lagged future-state scaffold and known-truth tests.
- CI PASS.
- Q038 firewall preserved.

### 2026-09-27 — CROSS-PROJECT SI LINK
- Market semantic-backbone preservation under rank migration resembles, but does not establish equivalence to, SI subspace preservation under carrier-rank/basis instability.
- Shared question promoted only at hypothesis level: what information survives scale/representation/embedding, and what is lost or reordered?


### 2026-09-27 — Q038 P1 HOLDOUT CLOSED
- Uploaded decisive result SHA-256: `fb13ae917955c1a32200105226d4edd7881aa1bb630abed29b7519c3a5bf207c`.
- Frozen execution commit: `d8a44204514a8111f524ef122d110714d9bafa29`.
- Primary outcome: `EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST`.
- All three days: 42/42 primary windows COMPLETE.
- Frozen 2 h block-bootstrap margin: 0.411995, 95% CI [0.399033, 0.427259].
- Mandatory 1 h and 3 h sensitivities agree.
- Hierarchical corridor secondary survives: contrast 0.059272, 95% CI [0.022142, 0.157405].
- Descriptively, all 126 primary windows individually remain above the exact k=6 isotropic q95, while five windows show severe top-two rank migration. Failures remain active evidence, not exclusions.
- Promotion is bounded to MNQ mature-session semantic preservation. No scalar χ, market-wide universality, cross-market transfer, or trading claim is promoted.
- Result record: `qualification/MNQ_Q038_SEALED_HOLDOUT_RESULT_2026-09-27.md`.


### 2026-09-27 — TEMPORAL-HIERARCHY APQ PARTIAL QUALIFICATION
- APQ level: APQ-2 Substantial.
- Frozen Plan Packet: `qualification/MNQ_TEMPORAL_HIERARCHY_PLAN_PACKET_2026-09-27.md`, commit `b58b95f2ec9d722e0343c4f961e849d720f8f1be`.
- Internal/literature attack record: `qualification/MNQ_TEMPORAL_HIERARCHY_APQ_2026-09-27.md`, commit `2d417ea3333a05da17830a479d4c6c0d305d0b5a`.
- Generic novelty explicitly refused for multiscale causality, generic LOB prediction, multiresolution liquidity, microstructure modes, and generic cross-scale information flow.
- Plan Delta replaces the older rich-summary scaffold with a nested incremental design: current coarse semantic state + session phase for both models; only fixed fine-scale SD/slope terms are added to the structured model.
- Fixed adjacent primary ladder: 15->30 s, 30->60 s, 60->300 s; primary lead 1; leads 2/3 secondary.
- Physical-time parity: 5 h initial training, hourly refit/evaluation, one-hour dependence bootstrap at every scale.
- New core: `market_chi/temporal_hierarchy_v2.py`.
- Known-truth tests: `tests/test_temporal_hierarchy_v2.py`.
- Known-truth CI: run `36371753558`, SUCCESS.
- External attack packet: `qualification/MNQ_TEMPORAL_HIERARCHY_EXTERNAL_APQ_PACKET_2026-09-27.md`, commit `327825bd1b6f67b337895492fd3841be2e40b1b7`.
- APQ-gated runner: `tools/mnq_temporal_hierarchy_v2.py`, commit `35babe2f7405d5d63e176855b5ddfa385faac267`.
- The runner refuses real development execution unless the external review contains both `APQ_EXTERNAL_STATUS=QUALIFIED` and the exact frozen Plan Packet commit.
- May 27/28/29 and June 1/2 outcomes have not been exposed to this new hierarchy analysis.
- June 9-11 remain prohibited for tuning this branch.


### 2026-09-27 — TEMPORAL-HIERARCHY PRIOR-ART FOUNDATION + PREREGISTRATION v0.2
- Comprehensive Undermind prior-art search completed: 131 papers surfaced.
- Closest collisions include Eisler/Kertesz/Lillo on LOB time scales, Cont/Kukanov/Stoikov on OFI aggregation robustness, Corradi/Zaccaria/Pietronero on scale-specific liquidity mechanisms, functional/factor LOB forecasts, multiscale causality, and microstructure modes.
- Literature/hypothesis foundation: `qualification/MNQ_TEMPORAL_HIERARCHY_LITERATURE_HYPOTHESIS_FOUNDATION_2026-09-27.md`, closure commit `8204a340a71b9e511cc06bd6b233a93a9adb1e84`.
- Active preregistration candidate: `qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.2_2026-09-27.md`, commit `32efaa69879131889965d71ab799d42e7d291548`.
- External APQ packet bound to v0.2: `qualification/MNQ_TEMPORAL_HIERARCHY_EXTERNAL_APQ_PACKET_PREREG_v0.2_2026-09-27.md`, commit `6a51a9898f310fceaa9a6d605bfa0872dc997aa6`.
- Pre-outcome Plan Delta from the early scaffold: `qualification/MNQ_TEMPORAL_HIERARCHY_PLAN_DELTA_TO_PREREG_v0.2_2026-09-27.md`, commit `4431b0649725428e7f26890900d336d2d69bb0d7`.
- Representation continuity correction: use Q037/Q038 L10 last-book state lineage, not 1-second mean-depth representation.
- Layer R now qualifies semantic representation separately at 15/30/60/300 s before inheritance language.
- Layer L uses stronger current+previous coarse state, session harmonics, and native flow/context comparators.
- Factor-2 transitions are treated as two-child contrast tests with algebraic equivalence to last-fast information.
- 60->300 is the first ordered five-child path test beyond last-fast and unordered variability.
- Existing `temporal_hierarchy_v2.py` and its runner remain preserved engineering prototypes but are NOT authorized for real-data execution under preregistration v0.2.
- No real temporal-hierarchy outcome from May27/28/29 or Jun1/2 has been opened under the new definitions.


### 2026-09-28 — Q039 EXTERNAL APQ ADJUDICATED / v0.3 ISSUED
- External review set returned REVISE, BLOCKED, and REVISE dispositions plus one non-adjudicative tool response.
- Independent Kimi known-truth harness was rerun locally and exited 0, reproducing NC1-NC5 and null calibrations without market data.
- External adjudication record: `qualification/Q039_EXTERNAL_APQ_ADJUDICATION_v0.2_2026-09-28.md`, commit `2c2771ebc20b2cbd72529b84ee8976636e75452c`.
- Active preregistration: `qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.3_2026-09-28.md`, canonical commit `fde9121072694338c5c097984e6a417a993fee3a`.
- Plan Delta: `qualification/Q039_PLAN_DELTA_v0.2_TO_v0.3_2026-09-28.md`, commit `d452ea0820f54853eabcb2c199fb6452abc7dd5f`.
- Re-review packet: `qualification/Q039_EXTERNAL_APQ_REREVIEW_PACKET_v0.3_2026-09-28.md`, commit `5008dd151b34fbdea76d5631d99d2fe73f5bb928`.
- v0.3 resolves Layer-R coordinate/null ambiguity, generic calendar/common-mode confounding, carry-forward/staleness, 300 s identification, circular bootstrap, ambiguous SUBTRACTS semantics, factor-2 wording, P60_300 nesting, and prior-art delta.
- Layer R and Layer L are now independent result objects. No inheritance classification exists.
- Real Q039 outcomes remain unopened.
