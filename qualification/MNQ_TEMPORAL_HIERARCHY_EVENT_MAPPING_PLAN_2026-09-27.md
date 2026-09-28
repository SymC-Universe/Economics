# MNQ Temporal Hierarchy and Lagged Event-Mapping Plan

Date: 2026-09-27  
Stage: P0-D / P0-Q exploratory development  
Branch: `market-chi-architecture`  
Holdout firewall: **June 9-11 Q038 decisive data are not used by this branch.**

## Purpose

Test the user's long-standing observation that market organization appears hierarchically similar across 15 s, 30 s, 1 min, and 5 min views while the realized speed/amplitude changes by instrument and state.

This branch does **not** assume that scale recurrence is novel, causal, or predictive. It asks a stricter question:

> Does structured organization at a faster timescale contain lagged information about a future slower-timescale state beyond the slower state’s own persistence and beyond the last fast observation alone?

A positive answer would be evidence for temporal hierarchical information transfer in this market/data regime. It would not establish universal scale invariance, substrate inheritance, or a trading rule.

## Novelty boundary

Already established or active prior art includes:

- market microstructure invariance in business time and scaling-law formulations;
- multifractal/scale-dependent financial dynamics;
- multiscale price-formation models;
- high-frequency LOB regime/state-transition prediction;
- lead-lag and cross-market information transmission.

Therefore this project may **not** claim novelty for “markets are scale invariant,” “financial markets are fractal,” “LOB states predict later LOB states,” or “lead-lag exists.”

The residual research question is narrower:

1. whether the same physically interpretable L10 semantic architecture remains identifiable across fixed temporal aggregation levels;
2. whether fast-scale *within-block organization*, rather than only the terminal observation or current coarse state, adds out-of-sample information about a **future** coarser state;
3. whether transition ordering is stable enough to support event mapping with explicit refusal when hierarchy breaks;
4. whether the result transfers across instruments only after separate cross-market testing.

Key literature anchors for the novelty audit:
- Kyle & Obizhaeva (2016), *Econometrica*, market microstructure invariance in business time, DOI 10.3982/ECTA10486.
- Kyle & Obizhaeva (2022), market microstructure invariance meta-model, scaling laws in business time.
- Parent (2026), *A Three-Time-Scale Framework to Asset Price Formation*, SSRN preprint, neighboring multiscale formulation.
- Jeon (2026), *When Does Order Flow Matter? State-Dependent L2 Liquidity-State Transitions in Crypto Futures*, arXiv preprint, neighboring state-transition prediction.
- Matthews (2026), *Multifractal Price Delivery in Algorithmic Futures Markets*, SSRN preprint, neighboring nested-scale-invariance claim.

Preprints are neighboring prior art, not publication-level authority.

## Scientific firewall

Q038 is already frozen and has entered decisive holdout execution. Nothing in this temporal-hierarchy branch may:

- alter Q038;
- use June 9-11 to choose hierarchy features, scales, thresholds, labels, or events;
- reinterpret a Q038 failure as success for this branch;
- call June 9-11 untouched evidence for a later hierarchy claim after it has been opened.

The initial empirical corpus for this branch is development-only:
- 2026-05-27
- 2026-05-28
- 2026-05-29
- 2026-06-01
- 2026-06-02

May 31 remains historical discovery context and is not required for the first lagged test.

## Starting scale ladder

The first development ladder is fixed to the trader-observation lineage rather than selected from outcomes:

- 15 s
- 30 s
- 60 s
- 300 s

The 1 s MBP-10 feature stream is the native substrate from which the fixed blocks are constructed.

These scales are a P0-D starting set, not universal market timescales.

## Representation ladder

### Native

Use the existing validated 1 s MBP-10 v2 feature stream and its L10 bid/ask depth state.

### Semantic state

Preserve the already identified canonical directions where applicable:

- symmetric depth/liquidity direction;
- bid-versus-ask imbalance direction;
- depth-gradient family;
- side-gradient family.

Individual PC rank is not assumed stable.

### Structured fast-block summary

For each fine-scale feature within a block, the current generic scaffold permits:

- mean;
- standard deviation;
- minimum;
- maximum;
- last value;
- within-block linear slope.

This is deliberately broader than last-value carryover but remains transparent.

### Future coarse target

The target must occur **after** the information block used to predict it.

Current-scale reconstruction is not counted as prediction.

## Baselines

Every lagged hierarchy result must compare against at least:

1. **LAST_FAST:** a model using only the last fine-scale observation in the information block.
2. **COARSE_PERSISTENCE:** the current coarse target value carried forward to the future target.

A hierarchy claim requires incremental information beyond both for the frozen target.

A future event-classification version should additionally include a no-transition/base-rate comparator.

## First engine question

For a fixed factor and lead:

`structured fast block at t -> future coarse target at t + lead`

versus:

`last fast observation at t -> future coarse target`

and:

`current coarse state -> future coarse target`.

Primary development outputs are descriptive:

- walk-forward R²;
- MAE;
- delta R² versus LAST_FAST;
- delta R² versus COARSE_PERSISTENCE;
- refusal status;
- block count and exact alignment.

No physical/predictive promotion threshold is frozen in this P0-D stage.

## Event-mapping extension

Only after lagged incremental information is demonstrated should this branch define a discrete event.

Candidate event families include:

- semantic-backbone disturbance;
- rank migration with backbone preservation;
- partial semantic loss;
- recovery/reclaim;
- transition into a new coarse state.

The event definition must be frozen from development evidence before a new untouched test.

Price direction or profit is not the default event label.

## Substrate-Inheritance bridge

This market experiment is relevant to SI only as a **domain-specific inheritance analogue**.

Potential correspondence:

- fast block = lower-scale substrate state;
- future coarse state = higher-scale realized behavior;
- structured summary = candidate transformation information;
- last-value/persistence models = simpler native comparators;
- failure to add information = no evidence for temporal inheritance at that scale;
- success at one scale pair does not imply universal scale invariance.

The SI program remains scientifically independent and must not use market success to lower its physical evidence requirements.

## Failure consequences

If structured fast summaries do not add information beyond both baselines:
- temporal hierarchy may remain descriptive;
- no event-prediction claim is licensed;
- do not retune scale factors on the same decisive data.

If value appears only for some scale pairs:
- record a regime/scale-specific hierarchy;
- do not average into a universal hierarchy.

If hierarchy is unstable across development days:
- prioritize state-conditioned mapping or refusal rather than force invariance.

If later untouched evidence fails:
- retire or narrow the corresponding frozen claim.

## Next exact actions

1. Add known-truth lagged-hierarchy engine and refusal tests.
2. Run CI before applying it to real development data.
3. Prepare a local-data runner using only the five development days.
4. Run fixed 15/30/60/300 s development mapping.
5. Inspect whether incremental value exists beyond both baselines.
6. Only then define/freeze a discrete transition-event problem.
7. Cross-market transfer remains a later independent test.
