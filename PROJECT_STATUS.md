# Market Χ Project Status

Date: 2026-09-18
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

## Real-data qualification now completed on two development days

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

The strongest replicated result is structural rather than predictive:

`native MBP-10 -> repeated liquidity/depth + bid/ask-imbalance modal geometry -> Χ structure -> χ refused where not licensed`.

This is currently more robust than any claim about the sign of forward risk.


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

Two additional pre-outcome plans are frozen:
- `qualification/SHARED_REFERENCE_TEST_DESIGN_2026-09-18.md`;
- `qualification/CROSS_MARKET_EXTENSION_PLAN_2026-09-18.md`.

The development sweep output now records the exact frozen code commit. This closes the earlier provenance gap in which the BAT knew the commit but the uploaded JSON did not.

## Immediate development sequence

1. Complete the already-packaged fixed-session-phase development sweep so 22:00-24:00 UTC opening blocks are compared with opening blocks and 00:00-21:00 UTC mature blocks are compared separately.
2. Process May 28, May 29, June 1 and June 2 under the same frozen v2 extractor and modal analysis rules; use May 27 and May 31 as already-viewed development evidence.
3. Determine whether PC1 and PC2 remain stable across days and whether PC3/PC4 gradient modes repeat.
4. Evaluate PC1 against total depth under ADDS / EQUIVALENT / SUBTRACTS / INDETERMINATE; do not award modal novelty when a scalar comparator carries the same information.
5. Characterize the repeated negative discrete pole as a native microstructure/sampling phenomenon rather than relabeling it as damping.
6. Freeze development-only definitions for failed-recovery trajectories and temporal substrate-inheritance tests, then apply them without consulting June 9-11.
7. Add broker-default versus nearby-perturbed reference controls before interpreting EMA/MACD/VWAP response as a shared-reference effect.
8. Integrate the April 3-June 2 trade history as the longer execution-flow baseline.
9. Expand candidate dynamics beyond AR0/AR1/AR2 to heteroskedastic, stochastic-volatility, state-space, jump and regime-switching alternatives.
10. Freeze the first diagnostic/predictive question, comparator, endpoint, exclusions, uncertainty method and failure criteria only after the development session-phase map is complete.
11. Keep June 9-11 sealed until that gate is passed.
