# Trader Observation Lineage -> Market Χ Hypotheses

Date: 2026-09-17
Branch: `market-chi-architecture`
Epistemic status: hypothesis-generation / P0-D only

## Purpose

This file preserves the user's historical trading observations as a hypothesis source for the Market Χ program.

It is intentionally separated from:
- current empirical MNQ findings;
- assistant interpretations from the source conversation;
- the legacy oscillator-first MarketFW model;
- any claim that a trading heuristic is already a physical law or licensed χ quantity.

The source conversation is treated as a record of what the user reported observing and doing. Statements introduced by the prior assistant (for example, assertions about institutional intent, passive absorption, stop clusters, liquidity vacuums, exceptional points, χ=1, or EMA lines being physical attractors) are **not inherited as evidence**.

## User-observed trading structure

### O1. Multi-timescale baseline hierarchy

The user reports evaluating price relative to:
- 20 EMA;
- 100 EMA;
- 200 EMA;
- VWAP;
- recurring 25- and 100-point price levels;
- multiple chart resolutions: 15 s, 30 s, 1 min, and 5 min.

The 100 EMA was added later and was experienced as filling a previously perceived intermediate retest layer between shorter and longer baselines.

### O2. Baselines are not standalone entry signals

The user does not report entering merely because price touches an EMA, VWAP, or round-number level.

The decision depends on how price **tests, rejects, recovers, sustains, or fails** around those levels and on what the tape is doing at the same time.

### O3. Tape state is contextual

The user distinguishes at least:
- fast + mixed tape: generally a no-entry state;
- fast directional tape: often treated as extension/continuation;
- slow tape: treated as a precursor to exhaustion;
- slow tape followed by fast opposite-color activity: a favored exhaustion/reversal signature.

These are qualitative historical observations and require operational definitions before testing.

### O4. Indicator-price relationship matters more than indicator direction alone

The user reports that when MACD simply follows chart motion, the next cap/bottom/cycle is harder to distinguish.

A more informative condition is a mismatch or relational state, such as price recovering near/above the 15 s 20 EMA despite broader downward-looking momentum.

The user commonly waits for a clear spike/drop followed by sustained rejection rather than acting on the indicator alone.

### O5. Retest path matters

The user reports reading retests before adding the 100 EMA.

Adding the 100 EMA made an intermediate step visible in sequences involving the 20/100/200 EMA hierarchy, including cases in which price crosses one baseline, tests another, and then re-tests the first as support/resistance.

The candidate scientific object is therefore not simply distance-to-EMA; it may be the **ordered path through a hierarchy of reference states**.

### O6. Session phase changes interpretability

The user reports that time of day matters and generally avoids at least the first few minutes of the opening period.

This is consistent with treating session phase as a moderator of any Market Χ relationship rather than pooling all times indiscriminately.

### O7. Short-exhaustion preference and possible directional asymmetry

The user reports being more comfortable and more effective reading short-side exhaustion than the corresponding long-side behavior.

This is a candidate asymmetry to test rather than assuming long/short mirror symmetry.

### O8. Waiting is part of the method

The user commonly waits 2-5 minutes between trades unless a "clear wave" is present, and often deliberately passes on ambiguous setups.

This means the historical method is event-selective, not a continuously active indicator system.

### O9. News is not a primary input

The user reports historically focusing on numbers, L2/tape, and responses to levels rather than headlines.

This does **not** establish that news is irrelevant to market dynamics; it only establishes that the user's historical decision process did not condition directly on it.

### O10. Execution footprint became an explicit concern

The user recognized that simulated 80-lot market-order execution may not transfer to live trading because of depth consumption, slippage, and self-impact, and considered reducing live clip size while preserving the same rapid enter/exit style.

This provides a natural intervention/self-perturbation question for the microstructure program.

## Candidate Χ interpretation

The historical trading logic is more naturally represented as a relational state than as one scalar:

[
X_t = (B_t, F_t, R_t, C_t)
]

where, provisionally:

- (B_t): baseline/reference geometry across scales;
- (F_t): native flow/tape state;
- (R_t): response to a test/perturbation (hold, reject, recover, breach, sustain);
- (C_t): context (session phase, direction, volatility/liquidity environment, neighboring levels).

This tuple is **not** a definition of uppercase Χ. It is a hypothesis scaffold for asking what relationships must be reconstructed before a broader Χ representation becomes useful.

Lowercase χ is evaluated only later and only if an admitted dynamical factor licenses it.

## Falsifiable hypotheses generated from the trading record

### H-T01: conditional baseline-response hypothesis

The response following a baseline test is better described by the joint state

[
	ext{level geometry} + 	ext{flow state} + 	ext{session phase}
]

than by distance-to-baseline alone.

### H-T02: multiscale relationship hypothesis

The relative arrangement and crossing/retest sequence of 20/100/200 EMA and VWAP states contains information not captured by any one baseline.

Comparator requirement: each combined representation must beat its strongest single-baseline alternative or be labeled EQUIVALENT / SUBTRACTS / INDETERMINATE.

### H-T03: rejection-state hypothesis

"Rejection" can be operationalized from:
- excursion through/toward a reference level;
- dwell time near the reference;
- recovery distance/velocity;
- whether the level is subsequently re-crossed;
- contemporaneous book/tape state.

The historical visual concept must not be declared validated until this operationalization is stable under parameter perturbation.

### H-T04: flow-state moderation hypothesis

Tape/event-flow state moderates the consequence of a baseline test.

"Fast", "slow", "mixed", "green", and "red" must be translated into reproducible event-rate, aggressor-side, signed-flow, and/or book-update variables before testing.

### H-T05: session-phase moderation hypothesis

The sign and strength of depth/risk and baseline/response relationships differ by session phase.

This hypothesis is independently motivated by the trading record and is now also relevant to the current development-data result in which May 27 and May 31 showed stable depth geometry but opposite exploratory forward-risk signs.

### H-T06: directional-asymmetry hypothesis

Short-exhaustion and long-exhaustion events are not assumed to be mirror images. Separate conditional response maps will be estimated.

### H-T07: event-selection hypothesis

The user's method may derive part of its apparent edge from **refusal/abstention**, not only from signal quality.

A tool derived from this lineage must therefore be allowed to output NO-TRADE / INSUFFICIENT STRUCTURE rather than being evaluated only on forced continuous predictions.

### H-T08: self-impact hypothesis

Large aggressive orders can alter the state being measured. Any live-tool architecture must distinguish:
- passive observation of market state;
- user-generated perturbation;
- post-entry state after the user's own order has interacted with the book.

This is a direct market analogue of embedded-versus-local measurement concerns, but no general SymC mechanism is assumed.

## Current empirical collision

The current MNQ development work has already produced a useful collision with the historical observations:

- native depth geometry is reproducible across May 27 and May 31;
- scalar χ has been refused across the current modal screens;
- exploratory forward-risk relationships changed sign between different session phases.

This does not validate the trading method. It supports making **context-conditioned relationships** a first-class target instead of searching for one global depth -> risk sign.

## Claims explicitly NOT inherited from the source conversation

The following prior-assistant interpretations are quarantined unless independently established:
- "hidden volume" inferred from MACD/price behavior;
- institutional intent or participant identity;
- stop-location claims;
- "liquidity vacuum" as the unique causal explanation;
- EMA values as literal physical stiffness, damping, attractors, or exceptional points;
- χ=1 attached to an EMA test or trading entry;
- direct identity between market behavior and quantum/cosmological mechanisms;
- claims that a profitable trade validates SymC;
- claims that news is irrelevant to the data-generating process;
- claims that a particular lot size is "invisible" to algorithms.

## Missing information required for reproducible translation

Before the historical method can be encoded, the following must be specified by the user or recovered from platform records:

1. Exact instrument(s) actually traded in the historical observations (NQ, MNQ, or both).
2. Exact MACD parameters and which chart timeframe(s) displayed it.
3. EMA source and settings beyond periods 20/100/200 (e.g. close-based EMA; whether all four charts were identical).
4. VWAP definition/anchor/reset convention.
5. Exact meaning of the reported 25- and 100-dollar/point levels.
6. What the tape display showed: Time & Sales filters, color rule, size filter, aggregation, and whether "speed" meant prints/sec, subjective visual speed, or another measure.
7. L2/DOM display depth and any aggregation/filter settings.
8. Operational meaning of "sustained rejection".
9. Operational meaning of "clear wave".
10. What visual/event condition ended a winning trade.
11. What structural condition caused manual exit from a losing/invalid trade, especially because the user reported not using fixed per-trade stops at that stage.
12. How conflicts among 15 s, 30 s, 1 min, and 5 min signals were resolved.
13. Time-of-day categories beyond "avoid the first few minutes".
14. Whether long-side setups use the same criteria or a materially different logic.
15. Availability of timestamped historical trade logs/screenshots/replay markers for exploratory retrospective alignment. These may be used for P0-D reconstruction, not P1 confirmation.

## Next research use

Do not tune the current MNQ engine to reproduce this narrative.

Instead:
1. finish the independent development sweep;
2. operationalize the historical qualitative terms without looking at holdout outcomes;
3. test the generated hypotheses on development data with native comparators;
4. freeze the resulting definitions;
5. preserve the June 9-11 holdout for prospective/untouched qualification where applicable.
