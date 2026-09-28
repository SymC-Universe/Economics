# MNQ Temporal-Hierarchy Plan Packet

Date: 2026-09-27
APQ level: APQ-2 Substantial
Governance: GOM v0.8.8
Status: PRE-OUTCOME PLAN PACKET
Repository branch: `market-chi-architecture`

## Scientific question

Does fixed fine-scale organization of the already-established MNQ L10 symmetric-depth / bid-ask-imbalance semantic state contain lagged information about the next slower semantic state beyond the slower state's own current state, ordinary session phase, and the last fast state?

This is not a test of generic scale invariance, generic lead-lag, or generic LOB predictability. Those neighboring phenomena are established in prior literature. The target is incremental cross-scale information in the specific native semantic architecture already established by Q037 and independently retained by Q038.

## Scope and evidence firewall

Development data only:
- 2026-05-27
- 2026-05-28
- 2026-05-29
- 2026-06-01
- 2026-06-02

Fixed mature-session interval:
- 00:00-21:00 UTC

Q038 June 9-11 evidence is forbidden for:
- feature selection;
- scale selection;
- model selection;
- threshold selection;
- event definition;
- lead selection;
- tuning.

Q038 may be cited only as prior structural motivation: the symmetric-depth / bid-ask-imbalance semantic pair survived the frozen fixed-k=6 holdout.

## Fixed wall-clock hierarchy

Elapsed time is ordinary wall-clock time and is never rescaled.

Primary adjacent transitions:
1. 15 s -> 30 s
2. 30 s -> 60 s
3. 60 s -> 300 s

Primary lead:
- exactly one target coarse block into the future.

Secondary descriptive leads:
- 2 target blocks;
- 3 target blocks.

No other scale or lead may be added after real development outcomes are viewed under this plan.

## Native semantic state

Start from validated 1-second MBP10 v2 feature rows.

For each 1-second row, construct the 20-dimensional L10 log-depth vector:
- bid levels 0-9: `log1p(bid_sz_i_mean)`
- ask levels 0-9: `log1p(ask_sz_i_mean)`

Use two fixed canonical unit directions:
- symmetric-depth: equal positive weight on all 20 coordinates;
- bid-ask imbalance: equal positive weight on bids and equal negative weight on asks.

The 1-second semantic state is the pair of fixed projections:
`s_t = (depth_t, imbalance_t)`.

No PCA is refit for this experiment. The semantic axes are fixed before outcome exposure.

## Scale construction

For each scale S in {15, 30, 60, 300} seconds:
- partition each UTC development day into non-overlapping S-second blocks starting at 00:00 UTC;
- never cross days or the 21:00 boundary;
- current coarse semantic state is the arithmetic mean of the eligible 1-second semantic states in that S-second block;
- require at least 80% 1-second coverage within every S-second block;
- no forward fill, interpolation, or imputation;
- blocks failing coverage are missing and may invalidate parent observations.

For each adjacent fine->coarse pair, the fine blocks forming one current coarse block must all be eligible.

## Predictors

For each current coarse block t and target at t+1:

### Coarse-context baseline B
Fixed predictors:
- current coarse symmetric-depth state;
- current coarse imbalance state;
- sine of fraction through the 21-hour mature session;
- cosine of fraction through the 21-hour mature session.

### Last-fast comparator L
Fixed predictors:
- last eligible fine-block symmetric-depth state within current coarse block;
- last eligible fine-block imbalance state;
- identical session-phase sine/cosine terms.

### Structured model S
Contains every coarse-context baseline predictor plus exactly four fine-organization terms computed across the constituent fine blocks of the current coarse block:
- standard deviation of fine symmetric-depth state;
- standard deviation of fine imbalance state;
- least-squares slope of fine symmetric-depth state versus within-block wall-clock position;
- least-squares slope of fine imbalance state versus within-block wall-clock position.

No minima, maxima, adaptive PCA components, order-flow fields, volatility fields, price returns, event labels, χ values, or post-outcome selected features enter this primary test.

## Targets

The future target is the two-dimensional semantic state of the next coarse block:
- future symmetric-depth;
- future bid-ask imbalance.

Models are fitted jointly by ordinary least squares with an intercept. No hyperparameter search is permitted.

## Walk-forward rule

Each development day is evaluated separately.

For every scale pair:
- first 5 wall-clock hours form the minimum training history;
- thereafter predictions are strictly out-of-sample;
- models refit using expanding past-only data at one-hour wall-clock intervals;
- no training observation may use a target at or after the first timestamp of its test chunk;
- test predictions preserve chronological order;
- days are never concatenated across overnight boundaries for fitting.

This produces the same initial training duration and refit cadence in physical time at every scale.

## Primary loss and comparator rule

For each target component, standardize forecast errors by that component's training-only standard deviation at each refit.

Primary per-observation joint loss:
`L = 0.5 * (e_depth^2 + e_imbalance^2)`
using the standardized errors.

Primary incremental statistics:
- `Delta_B = L_B - L_S`
- `Delta_L = L_L - L_S`

Positive values favor the structured model.

Report:
- pooled mean Delta_B and Delta_L;
- per-day means;
- per-target MAE and R2 for B, L, and S.

## Dependence-aware uncertainty

For each adjacent scale pair and each primary loss contrast:
- day-stratified circular moving-block bootstrap;
- 10,000 replicates;
- one-hour wall-clock blocks, converted to the appropriate number of target blocks;
- resample within day only;
- seed 20260929.

Do not pool across days before resampling.

## Pair-level classification

For each adjacent scale pair, classify only against the coarse-context baseline:

ADDS P0-D if:
- lower 95% bootstrap bound for mean Delta_B > 0; and
- point Delta_B is positive on at least 4 of 5 development days; and
- both target-component point MAE differences favor S over B.

SUBTRACTS P0-D if:
- upper 95% bootstrap bound for mean Delta_B < 0.

Otherwise:
- NEED_MORE_INFO / EQUIVALENT-OR-MIXED.

The last-fast comparator is mandatory but cannot rescue a failure against the stronger coarse-context baseline.

No program-wide or market-wide classification is allowed from this experiment.

## Secondary analyses

Only after the primary adjacent-pair result table is frozen:
- repeat the same representation at lead 2 and lead 3;
- report, do not optimize;
- no new scales;
- no new features;
- no event threshold;
- no trading rule.

## Refusals and invalid tests

Refuse an observation when:
- required fine or coarse coverage is below 80%;
- semantic inputs are non-finite;
- a block crosses the day/session boundary;
- target lies outside the 00:00-21:00 interval.

Refuse a day/pair test if fewer than 8 wall-clock hours of eligible post-training evaluation remain.

No missing-data repair may depend on outcomes.

## Falsifiers and consequences

The cross-scale incremental-information hypothesis is weakened at a pair when S fails to add over B. It is not rescued by favorable longer leads, another scale pair, Q038, scalar χ, or a post-hoc feature.

If all three primary pairs fail to ADD, retire the current fixed semantic temporal-hierarchy representation as an incremental predictive tool and retain only the descriptive nested-scale interpretation.

If only some pairs ADD, preserve the hierarchy as scale-dependent and do not generalize across the ladder.

If all three ADD, this licenses only a development-stage claim that within-block fine semantic organization carries incremental lagged information across these MNQ scale transitions. Untouched evidence is still required for promotion beyond P0-D.

## Explicit nonclaims

This plan does not test or establish:
- universal scale invariance;
- fractality;
- scalar χ inheritance;
- market-wide Χ invariance;
- event prediction;
- profitable trading;
- cross-instrument transfer;
- causal substrate inheritance.

## Novelty boundary from prior art

Prior literature already covers:
- multiscale market causality;
- multiresolution liquidity;
- LOB predictive power at short/meso scales;
- modal order-flow dynamics;
- information transfer across time scales.

Therefore novelty, if any, must come from the joint combination of:
- a previously qualified native semantic L10 architecture;
- fixed wall-clock adjacent-scale inheritance;
- strict nested incremental comparators;
- explicit preservation/reorganization/loss/refusal outcomes;
- later prospective event mapping if separately qualified.

Generic predictive gain is not itself a novelty claim.
