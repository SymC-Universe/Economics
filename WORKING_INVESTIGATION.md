# WORKING_INVESTIGATION.md

## Current State

- **Investigation:** Market Microstructure / temporal hierarchy / event mapping
- **Date:** 2026-09-27
- **Active GOM:** v1.0
- **Repository:** `SymC-Universe/Economics`
- **Branch:** `market-chi-architecture`
- **Stage:** Q038 CLOSED P1 + Q039 preregistration v0.3 external re-review
- **Status:** OPEN
- **Scalar χ:** currently REFUSED in production MNQ screens under existing rules
- **Broader Χ:** recurrent L10 semantic architecture supported at P0-D
- **User intervention required:** EXTERNAL APQ RE-REVIEW RETURN ONLY; synthetic v0.3 qualification remains internally actionable

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

Preserved lineage modules:
- `market_chi/lagged_hierarchy.py`
- `market_chi/temporal_hierarchy_v2.py`
- `tools/mnq_temporal_hierarchy_v2.py`

These are historical/prototype lineage only for Q039 v0.3 real execution. They may inform implementation comparison but are not authorized to open May 27/28/29 or June 1/2 outcomes.

Active v0.3 implementation-qualification state:
- canonical preregistration: `fde9121072694338c5c097984e6a417a993fee3a`;
- external re-review packet: `qualification/Q039_EXTERNAL_APQ_REREVIEW_PACKET_v0.3_2026-09-28.md`;
- frozen synthetic known-truth manifest: `qualification/Q039_V0_3_SYNTHETIC_KNOWN_TRUTH_MANIFEST_2026-09-28.json`, commit `26e761c970e90f9d80a68e984d5fb8f2c80f7af2`;
- NC1-NC8/null harness: NOT YET DURABLY QUALIFIED;
- real-data execution: BLOCKED.

Current governance is SymC GOM v1.0. The canonical v0.3 preregistration commit remains immutable while external review is bound to that identity; any material v0.8.8 -> v1.0 governance delta must be resolved prospectively and, if it changes the design, must produce a new preregistration identity and external re-binding rather than a silent edit.

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

Q038 is closed and remains frozen with no retuning.

### Q039

Q039 real May 27/28/29 and June 1/2 execution is BLOCKED. The late v0.3 external re-review returned a valid MATERIAL common-mode objection. The review was adjudicated at `qualification/Q039_EXTERNAL_APQ_REREVIEW_ADJUDICATION_v0.3_2026-09-28.md`, commit `c6c14a689852f68529d908dd9f8be2509bff9b52`.

The superseding candidate preregistration is v0.4:
- `qualification/MNQ_TEMPORAL_HIERARCHY_PREREGISTRATION_DRAFT_v0.4_2026-09-28.md`
- current normalized-notation commit `b757d0dd65a700be1bf1d2cb5233c75c83086308`
- Plan Delta `qualification/Q039_PLAN_DELTA_v0.3_TO_v0.4_2026-09-28.md`
- v0.4 synthetic manifest `qualification/Q039_V0_4_SYNTHETIC_KNOWN_TRUTH_MANIFEST_2026-09-28.json`.

Required before real Q039 execution:
1. external APQ re-binding to the exact v0.4 identity;
2. conformant NC1-NC8b synthetic qualification including persistent non-calendar common-mode refusal/demotion;
3. frozen implementation identity;
4. final preregistration freeze under GOM v1.0.

June 9-11 Q038 data remain prohibited for Q039 tuning.

### Q040

Q040 real-data execution is BLOCKED at P0-N/A0 and plan-construction stage.

Recovery-theory foundation is now substantial and durable:
- `qualification/Q040_RECOVERY_THEORY_FOUNDATION_v0.1_2026-09-28.md`
- latest provenance-corrected commit `4cc70f0e6fdf284ef07a80bba796442f4c7c1de7`.

The exact (chi)-collision / stability-coordinate literature search remains active. Q040 Plan Packet v0.1 and its external APQ packet are preserved as pre-theory lineage and are not final review authority. A v0.2 plan must incorporate the recovery-theory distinctions before external qualification.

The guarded Market workflow is now established at:
- `qualification/Q040_WORKFLOW_v0.1_2026-09-28.md`;
- `qualification/Q040_COMPUTE_CONVEYOR_QUEUE_v0.1.json`;
- `market_chi/q040_compute_conveyor_v0_1.py`;
- `market_chi/q040_workflow_preflight_v0_1.py`;
- `.github/workflows/q040-recovery-compute-conveyor.yml`.

The conveyor is execution plumbing only. It cannot admit (chi), define (Χ_{mathrm{arc}}), choose decisive thresholds, or open real outcomes.

## Next exact action

The exact safe next actions are:

1. complete and adjudicate the exact (chi)-collision / stability-coordinate literature search;
2. revise Q040 Plan Packet v0.1 to v0.2 using the recovery-theory foundation and collision result;
3. issue a fresh external APQ packet bound to the exact v0.2 plan commit;
4. freeze Q040 synthetic known-truth definitions/seeds after APQ and then execute them through the guarded conveyor;
5. in parallel, re-bind Q039 external APQ to v0.4 and implement/qualify NC1-NC8b without opening real Q039 outcomes;
6. freeze each lane independently before any real development exposure.

No user scientific intervention is required for mechanical workflow validation, literature bookkeeping, package assembly, synthetic implementation after definitions are frozen, or CI/reproducibility work. Scientific intervention is required at the representation/threshold/freeze gates defined in the Q040 workflow.

## Development Log

### 2026-09-28 — WATCHDOG GOVERNANCE + IMPLEMENTATION CHECKPOINT
- Definitive program governance normalized to SymC GOM v1.0 for ongoing Q039 work.
- The externally bound v0.3 preregistration commit remains immutable; no silent rewrite of its legacy governance label is permitted.
- Superseding v0.3 synthetic manifest is commit `39f25f9a4a6ea371a61298368da527521ecc76e5`; it prospectively corrects the NC7 carry-forward-null seed to the preregistered `20261001`. The earlier manifest at `26e761c970e90f9d80a68e984d5fb8f2c80f7af2` is preserved as superseded lineage and must not drive qualification.
- NC1-NC8/null qualification remains incomplete until a durable conformant harness and CI pass exist.
- External v0.3 APQ re-review remains outstanding.
- No real Q039 outcome was opened and Q038 June 9-11 remains excluded from tuning.



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


### 2026-09-28 — Q040 CANDIDATE OPENED: REPEATED-PERTURBATION RECOVERABILITY EROSION
- New hypothesis seed added without changing Q039: `qualification/Q040_RECOVERABILITY_EROSION_HYPOTHESIS_SEED_2026-09-28.md`, commit `b8d7c2ce4b8d51ae9218abc0f34ddc934b6a7ab5`.
- Motivation: researcher previously observed qualitatively that repeated excursions away from a baseline appeared to become progressively harder to recover from in markets, and later recognized a similar qualitative pattern in humans. This remains unproven.
- Stability Inheritance independently retains history-dependent changes in accessible recovery architecture and loss-of-recoverability as untouched-test targets.
- Existing market recovery primitive already distinguishes failed recovery, sustained reclaim, unresolved recovery, and no qualifying recovery without hard-coding a 3-5 attempt rule.
- Preliminary literature shows single-shock LOB resiliency is established, market hysteresis/path dependence is active prior art, and clustered/cascading shocks have been studied in simulation. Therefore novelty cannot rest on generic resiliency or repeated shocks alone.
- Residual candidate: empirical within-episode change in recoverability across successive perturbation/recovery cycles relative to a frozen baseline after controlling magnitude, spacing, direction, session phase, activity/liquidity state, baseline drift, and native order-flow memory.
- Q040 P0-N is OPEN only. No real-data execution or preregistration is authorized.
- Dedicated Undermind workspace: `c9911501-f69c-401b-9658-4851eaf10682`; prior-art deep search is active.
- Q039 evidence firewall remains unchanged.


### 2026-09-28 — Q040 BASELINE HIERARCHY CORRECTION
- User clarified that the relevant baseline is not one episode-wide fixed reference. The baseline should be averaged at each timeframe and then compared hierarchically into slower/longer times.
- Q040 hypothesis seed updated at commit `444fb2919fab296399a6fd4d98ba1ef9a0347b87`.
- Primary candidate object is now a causal scale-local native baseline (B_S(t)), initially over the existing 15 s / 30 s / 60 s / 300 s ladder.
- Perturbation/recovery is scored relative to the baseline of its own scale, while motion of that baseline is treated separately as a candidate transition object.
- New explicit distinction: (1) failed recovery around a stable fast baseline; (2) fast-baseline drift while slower baseline remains stable; (3) coordinated multiscale baseline migration; (4) slower-scale regime transition.
- Candidate hierarchy question: does repeated weakening/failure of recovery at scale S add information about subsequent migration/reorganization of the next slower baseline beyond that slower baseline's own persistence and native context?
- Exact averaging kernel remains OPEN pending prior-art/APQ. It must be causal, scale-matched, outcome-blind, and frozen before empirical scoring.
- Q039 remains unchanged and isolated.


### 2026-09-28 — Q040 GUARDED WORKFLOW ESTABLISHED FROM STABILITY INHERITANCE PATTERN
- User requested a Market workflow like Stability Inheritance.
- Established `qualification/Q040_WORKFLOW_v0.1_2026-09-28.md`, commit `68f0920d313412ba3c00d7f3f6a672b54faef7f9`.
- Added workflow-only preflight `market_chi/q040_workflow_preflight_v0_1.py`, commit `baa03de27f88c7d7a25564fbce23ffef78846b5a`.
- Added guarded compute conveyor `market_chi/q040_compute_conveyor_v0_1.py`, commit `59801b73656256b1d09d75755f8e24f918d4210b`.
- Added frozen queue `qualification/Q040_COMPUTE_CONVEYOR_QUEUE_v0.1.json`, commit `eaf4b4320cfb725b64fd9affdd845fb7af65ac55`.
- Added GitHub Actions workflow `.github/workflows/q040-recovery-compute-conveyor.yml`, commit `1033260dc339752254ea8fd6d5fc69a432e84bca`.
- Queue begins with one READY governance/workflow preflight only. All scientific and real-data tasks remain explicitly blocked.
- Conveyor stops on mechanical failure, real-data access before freeze, unlisted scientific disposition, or declared checkpoint.
- Explicit scientific stop gates include admission of (chi), construction of (Χ_{mathrm{arc}}), decisive baseline/perturbation threshold choice, exogenous-forcing rule changes, outcome-family changes, and any real-data opening.
- Workflow claim ladder now separates observed trajectory change, history-dependent recovery, changed finite-shock recoverability, and Stability-Architecture reorganization.
- Q039 remains independent and is now durably updated to v0.4 pending requalification.


### 2026-09-28 — Q040 WORKFLOW PREFLIGHT PASS + EXACT χ COLLISION SEARCH CLOSED
- Guarded Q040 conveyor first run: GitHub Actions run `36520935683`, job `109253398921`.
- Disposition: `WORKFLOW_PREFLIGHT_PASS`.
- Final state: `STOP_DECLARED_CHECKPOINT` at `Q040_WORKFLOW_PREFLIGHT_V01`.
- Real-data firewall: PASS; `real_data_enabled=false`; no READY real-data tasks.
- Workflow artifact ID: `11012581849`; SHA-256 `c766242825eebfc401bbc6410b59ea9b1f161dce1298a05d825992ec4eb07b7e`.
- Queue preflight closed at commit `ed33990e075b59ff3eb65d1d72de3814e884fb9d`.
- Exact χ/stability-coordinate collision search completed with 213 papers in Undermind workspace `c9911501-f69c-401b-9658-4851eaf10682`.
- Prior art directly includes scalar stability/phase coordinates, EP/damping thresholds, modal/non-normal coordinates, network resilience reductions, repeated-kick recovery theory, market instability thresholds, and multiscale liquidity structure.
- No retrieved work demonstrated the full conjunction of: a prospectively qualified scalar stability coordinate + modal/vector representation + system/conglomerate architecture + repeated perturbation/recovery history + cross-scale transmission. This is a bounded retrieval result, not proof of absence.
- Q040 collision-search queue item closed at commit `028c396faaa17ed03e6ea50244c6d362385ebf5f`.
- Next scientific gate: revise Q040 Plan Packet v0.1 -> v0.2 using recovery theory and exact-collision results. This is intentionally not conveyor-automated.
