# WORKING_INVESTIGATION.md

## Current State

- **Investigation:** Market Microstructure / temporal hierarchy / event mapping
- **Date:** 2026-09-27
- **Active GOM:** v0.8.8
- **Repository:** `SymC-Universe/Economics`
- **Branch:** `market-chi-architecture`
- **Stage:** Q038 P1 holdout execution + separate P0-D temporal-hierarchy development
- **Status:** OPEN
- **Scalar χ:** currently REFUSED in production MNQ screens under existing rules
- **Broader Χ:** recurrent L10 semantic architecture supported at P0-D
- **User intervention required:** NO

## Current scientific state

Across the five MNQ development sessions, the L10 symmetric-depth / bid-ask-imbalance semantic backbone is substantially more stable than individual PCA rank identity. Rank migration and localized partial semantic disturbances occur in a state-dependent manner, while wider fixed subspaces usually recover the semantic backbone well above isotropic-orientation controls.

Q038 is a separately frozen P1 structural holdout test on June 9-11. Its science may not be changed. The repository currently records decisive execution start, not a final adjudication result.

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
| recurrent L10 depth/imbalance semantic backbone | ACCEPT P0-D | cross-day development replication |
| universal PC rank identity | REFUSE | rank migration is state-dependent |
| canonical scalar χ in current MNQ production screen | REFUSE | 0 admissions under current rules |
| PC1 incremental forward-risk value over total depth | EQUIVALENT P0-D | native total depth performs equivalently |
| universal predictive sign of depth/spread | REFUSE | session/state conditioned |
| temporal hierarchy as predictive information | NEED_MORE_INFO | known-truth engine qualified; real development run pending |
| event prediction | NOT YET TESTED | event labels not frozen |
| cross-market invariance | NOT YET TESTED | separate future transfer test |
| Q038 final outcome | PENDING EXTERNAL DECISIVE RESULT | execution began locally; final artifact not yet present in repo |

## Active hold

Q038 final scientific adjudication cannot be completed until the frozen local execution result/artifact is returned or otherwise becomes accessible. This does not block development-only temporal-hierarchy work.

## Next exact action

Build and CI-qualify a development-data runner that:
1. consumes only the five development-day 1 s feature files;
2. constructs the fixed 15/30/60/300 s hierarchy;
3. tests one-block and prospectively enumerated lead relationships;
4. reports structured-vs-LAST_FAST-vs-COARSE_PERSISTENCE performance;
5. does not define a discrete event or promotion threshold;
6. emits a machine-readable result for later event-definition work.

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
