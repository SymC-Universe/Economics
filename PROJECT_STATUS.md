Active governance baseline: GOM v0.8.6.

# Market Χ Project Status

Date: 2026-09-27
Branch: `market-chi-architecture`
Stage: P0-D / P0-Q

## Scientific direction

The project no longer begins by assuming a damped oscillator. Uppercase Χ is the broader reconstructed market stability architecture. Lowercase χ is emitted only when a licensed local or modal second-order factor supports it.

## Current executable paths

Local scalar qualification scaffold:

`native series -> AR0/AR1/AR2 qualification scaffold -> pole inspection -> χ if licensed -> otherwise refusal`

Preferred real-market path:

`Databento MBP-10 -> validated native fields -> contract segmentation -> quality/snapshot handling -> 10-level book vectors + trade/order-flow features -> modal/vector Χ analysis -> χ only if later licensed`

The native microstructure path is operational. Extractor v2 streams `.csv.zst` directly and preserves signed microprice offsets.

## Real data locked

The user corpus is CME Globex `GLBX.MDP3` for Databento continuous calendar-front `MNQ.c.0`:

- trades: `[2026-04-03, 2026-06-03)` with 52 returned daily files;
- development MBP-10: `[2026-05-27, 2026-06-03)` with returned files on May 27, 28, 29, 31 and June 1, 2;
- sealed MBP-10 holdout: `[2026-06-09, 2026-06-12)` with returned files June 9, 10 and 11.

The June 9-11 block remains sealed at observation level in `qualification/HOLDOUT_FREEZE_2026-09-14.md`.

## Real-data qualification now completed across the development sweep

### May 31 discovery

The May 31 first pass identified a stable two-axis L10 depth geometry in the 22:00-24:00 UTC Sunday/opening block:

- PC1: 39.16% variance, symmetric liquidity/depth mode;
- PC2: 9.55% variance, bid-versus-ask imbalance mode;
- PC1+PC2: 48.71%;
- minimum top-2 within-block principal cosine: 0.9797;
- canonical χ admissions across screened native series/resolutions: 0.

### May 27 weekday replication

Extractor v2 read 37,491,279 raw rows and emitted 82,713 one-second bins with zero event-time disorder, one actual instrument, no bad-book flags, one bad-receive-time flag and one synthetic snapshot row.

The frozen high-coverage rule selected 00:00-21:00 UTC:

- 75,600 dense seconds;
- 75,523 event-bearing seconds;
- 99.8981% coverage.

The modal geometry replicated:

- PC1: 29.64% variance, symmetric-depth alignment 0.9843;
- PC2: 7.84% variance, bid/ask-imbalance alignment 0.9782;
- PC1+PC2: 37.49%;
- minimum top-2 half-block principal cosine: 0.9209;
- PC3 additionally aligns with a depth-gradient basis (0.7845);
- PC4 additionally aligns with a side-gradient basis (0.7082).

The sign of PCA modes is arbitrary; May 27 PC1 is negatively oriented relative to total depth but represents the same liquidity/depth axis.

## Replicated Χ versus χ result

The May 27 production χ screen evaluated six native series across seven sampling resolutions (1, 2, 5, 10, 15, 30, 60 s): 42 screens total.

**χ admissions: 0 of 42.**

Thirty-five cases strongly admitted a discrete AR(2) structure but were refused canonical χ because one propagation pole was negative, retaining alias ambiguity under the continuous logarithmic embedding. Seven coarser cases preferred AR(0) or AR(1).

This reproduces the May 31 conclusion: native modal/vector Χ structure can be strong and repeatable even where canonical scalar χ is not licensed.

## Forward-risk interpretation revised

The May 31 discovery associated greater depth with smaller subsequent path movement and wider spread with larger path movement.

May 27 does not reproduce those signs. Across its automatically selected 00:00-21:00 UTC block:

- greater total depth is associated with *larger* subsequent path movement;
- wider spread is associated with *smaller* subsequent path movement;
- directional associations remain weak relative to capacity/risk associations.

Therefore the first May 31 sign pattern is not a portable rule and has been explicitly demoted.

The two analyses cover different Globex session phases. CME equity-index futures trade approximately 22:00-21:00 UTC during Central Daylight Time with a 21:00-22:00 UTC maintenance interval. May 31 sampled the first two hours after the weekly open; May 27's automatic block sampled the later 21 hours of a regular session. Session phase, liquidity state and event environment must be controlled before any predictive sign is frozen.

## Current scientific interpretation

The strongest development result is structural rather than predictive:

`native MBP-10 -> repeated liquidity/depth + bid/ask-imbalance modal geometry -> Χ structure -> χ refused where not licensed`.

The v3 fixed-session sweep produced 9 complete phase windows. Same-phase cross-day top-2 minimum principal cosines range 0.9686-0.9937, while production χ is refused in all 378 screens.

Forward-risk behavior is phase/state conditioned rather than universal. Total-depth association is negative at all five horizons in all four available session-open windows, but mature windows are positive on four of five days. May 28 mature is the retained exception and also has the weakest within-window top-2 half-subspace cosine (0.6480).

PC1 versus native total depth is EQUIVALENT at P0-D for forward-risk use. PC1 remains structurally interpretable but has not shown incremental predictive information beyond native total depth.


## Historical trader-observation lineage added

The user's trading observations are now preserved separately as hypothesis-generation evidence in `hypotheses/TRADER_OBSERVATION_LINEAGE_2026-09-17.md`.

Key corrections from the user:
- the perceived test/rejection/recovery cycle is reported across markets, with instrument-dependent speed and amplitude; MNQ is not an upper-speed market, with small-cap/daily-high movers often substantially faster and instruments such as GLD slower;
- 15 s, 30 s, 1 min and 5 min charts are better treated as a temporal substrate-inheritance/reorganization problem than as independent signals or merely statistical coarse-graining;
- sustained rejection means an active recovery/reclaim attempt can partially recover and still fail to sustain the level; roughly 3-5 attempts is a common personal decision horizon, not a fixed market threshold;
- EMA settings were identical across timeframes; MACD, VWAP and Time & Sales were broker/platform defaults rather than tuned research parameters;
- preserving defaults is intentional because the user wants to observe conventional/shared reference constructions; whether shared visibility causes stronger responses is now a separate default-versus-perturbed hypothesis;
- the prior "$25/$100 level" interpretation was a misread and is removed;
- the user increasingly favors harvesting the initial move and re-evaluating at the next structural test rather than assuming continuation through multiple levels.

These observations do not validate SymC or any trading rule. They generate independent P0-D questions about conditional response, failed recovery trajectories, temporal substrate inheritance, shared-reference effects, cross-market scaling, refusal/abstention, and self-impact.

Current Project/Library search did not locate an obvious personal broker execution/fill-history export, so personal trade logs remain a recover-if-available input rather than an assumed part of the corpus.

## New qualification scaffolds

Two lineage-derived components are now executable without touching the sealed holdout.

`market_chi/recovery.py` treats failed recovery as a trajectory after a known break, not as repeated line touches. It distinguishes no qualifying recovery, failed recovery, sustained reclaim, unresolved recovery, and input/break refusal. A recovery may cross the reference and still fail if it cannot sustain the recovered side. The user's typical 3-5-attempt decision horizon is not an admission rule.

`market_chi/temporal_inheritance.py` treats temporal substrate inheritance as an incremental reconstruction question. It compares walk-forward reconstruction of a slower target from structured summaries of the faster substrate against a last-fast-observation baseline. Success would be P0-Q evidence that faster-state organization contains additional information about the slower state, not proof of a universal inheritance law.

The new known-truth tests passed locally before commit: 5 recovery tests + 4 inheritance tests = 9/9. Market-data application remains pending the development sweep and frozen definitions for scale, reference construction, and event segmentation.

## GitHub-side work completed while local data are unavailable

The branch now has GitHub Actions CI, explicit setuptools package discovery, a sign/rotation-invariant cross-day modal subspace comparator, and an enriched development sweep index that preserves PCA loadings, basis alignments and detailed chi screens. The remaining development comparison plan was frozen before May 28/29 and June 1/2 outcomes are inspected.

The scalar chi scaffold was also adversarially hardened while local data were unavailable. Residual-variance, walk-forward mean-persistence, and blockwise pole-stability diagnostics were implemented and stress-tested. All three add useful identifiability information, but hard legitimate second-order cases falsified simple universal veto thresholds. Production chi admission therefore remains unchanged; future Q009 work should expand native model competition rather than stack brittle gates.

Two additional pre-outcome plans are frozen:
- `qualification/SHARED_REFERENCE_TEST_DESIGN_2026-09-18.md`;
- `qualification/CROSS_MARKET_EXTENSION_PLAN_2026-09-18.md`.

The development sweep output now records the exact frozen code commit. This closes the earlier provenance gap in which the BAT knew the commit but the uploaded JSON did not.

## Immediate development sequence

1. **COMPLETE:** fixed same-phase development sweep across May 27, May 28, May 29, June 1 and June 2.
2. **COMPLETE:** cross-day PC1/PC2 subspace replication and PC3/PC4 gradient-family check.
3. **COMPLETE:** PC1 versus native total-depth comparator. Outcome: EQUIVALENT at P0-D.
4. **COMPLETE:** session-phase control Q023. Phase conditions the risk map, but May 28 mature prevents a simple two-regime law.
5. **NEXT:** run the frozen May 28 mature reorganization follow-up using 3-hour primary and 7-hour sensitivity wall-clock windows.
6. Freeze development-only market-data definitions for failed-recovery trajectories and temporal substrate-inheritance tests after the May 28 localization result.
7. Add broker-default versus nearby-perturbed reference controls before interpreting EMA/MACD/VWAP response as a shared-reference effect.
8. Integrate the April 3-June 2 trade history as the longer execution-flow baseline.
9. Expand native model competition beyond AR0/AR1/AR2 without adding unsupported scalar veto thresholds.
10. Freeze the first holdout-facing diagnostic/predictive question, comparator, endpoint, exclusions, uncertainty method and failure criteria.
11. Keep June 9-11 sealed until that freeze is complete.


## Current road-state

The development sweep outputs have been received and the fixed same-phase gate is closed at P0-D.

Recorded results:
- `qualification/MNQ_DEVELOPMENT_SWEEP_V3_RESULT_2026-09-27.md`
- `qualification/mnq_development_sweep_v3_cross_day_result.json`

The current empirical dependency is the targeted May 28 mature reorganization follow-up. A frozen CI-passing runner is recorded in `qualification/MNQ_MAY28_REORGANIZATION_V1_PACKAGE_2026-09-27.md`.

The June 9-11 holdout remains sealed.

## GOM v0.8.6 interpretation status

Under GOM v0.8.3, the relationship between any admitted local chi and the broader market Chi architecture is itself an explicit research question. Current viewed development evidence does not require a scalar, and scalar refusal remains a supported outcome.

The existing recovery primitive is not promoted to a market-stability definition. Future empirical recovery work must distinguish immediate resistance/response, first reclaim, sustained recovery, reorganization, and repeated-event behavior under prospectively frozen event/reference rules.

The sealed June 9-11 block remains untouched by this migration.


## May 28 reorganization follow-up

The fixed 3-hour/7-hour follow-up rejects the earlier whole-session characterization of May 28 as a single outlier state. The day contains a sequence of native modal reorganizations while scalar chi remains refused throughout.

Development sequence:
- 00:00-06:00 UTC: canonical stable liquidity/imbalance architecture;
- 06:00-12:00 UTC: leading-subspace reorganization with the strongest disruption at 06:00-09:00;
- 12:00-15:00 UTC: canonical reconstruction and positive total-depth forward-risk sign;
- 15:00-18:00 UTC: canonical semantics retained but strong internal top-two instability;
- 18:00-21:00 UTC: modal-rank reorganization, with liquidity retained as PC1 while imbalance moves to PC3.

The coarser 7-hour sensitivity windows reproduce the existence of internal reorganization and the late-session rank shift. This result is recorded in `qualification/MNQ_MAY28_REORGANIZATION_RESULT_2026-09-27.md`.

The next frozen P0-D experiment is `qualification/MNQ_MAY28_NATIVE_DRIVER_PLAN_2026-09-27.md`: 60-minute primary windows plus 30-minute sensitivity windows will test which native depth, spread, imbalance, event-activity and trade-flow changes accompany the structural transitions. Structural localization is independent of forward-risk outcome. June 9-11 remains sealed.
