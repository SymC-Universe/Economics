# Trader Observation Lineage -> Market Χ Hypotheses

Date: 2026-09-17
Updated: 2026-09-18
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

### O1. Cross-market cycle claim

The user reports seeing the same broad test/rejection/recovery cycle across the market, not only in NQ/MNQ.

Different instruments appear to express the cycle at different speeds and amplitudes, with some markets showing the sequence more dramatically or more quickly than others.

This is a historical observation and a future cross-instrument falsification target. It is not assumed from the current MNQ evidence.

### O2. Multi-timescale baseline hierarchy

The user evaluates price relative to:
- 20 EMA;
- 100 EMA;
- 200 EMA;
- VWAP;
- multiple chart resolutions: 15 s, 30 s, 1 min, and 5 min.

EMA settings were identical across those charts. MACD, EMA, VWAP, and Time & Sales settings were not custom-tuned beyond display/window arrangement; the user used the broker/platform defaults available when selected.

The exact numerical MACD default and VWAP reset/anchor convention remain implementation metadata to recover from the broker/platform version if needed.

The previously inferred recurring "$25/$100 levels" is retracted as a misread. Absolute price denomination is not part of the user-observed mechanism unless separately demonstrated.

### O3. Baselines are not standalone entry signals

The user does not report entering merely because price touches an EMA or VWAP.

The decision depends on how price **tests, rejects, recovers, sustains, or fails** around a level and on what the tape is doing at the same time.

### O4. Tape state is contextual

The user distinguishes at least:
- fast + mixed tape: generally a no-entry state;
- fast directional tape: often treated as extension/continuation;
- slow tape: treated as a precursor to exhaustion;
- slow tape followed by fast opposite-color activity: a favored exhaustion/reversal signature.

Time & Sales was viewed using broker defaults except for the physical size/layout of the display window.

These descriptions remain qualitative until translated into reproducible event-rate, aggressor-side, signed-flow, and book-update variables.

### O5. Indicator-price relationship matters more than indicator direction alone

The user reports that when MACD simply follows chart motion, the next cap/bottom/cycle is harder to distinguish.

A more informative condition is a mismatch or relational state, such as price recovering near/above the 15 s 20 EMA despite broader downward-looking momentum.

The user commonly waits for a clear spike/drop followed by sustained rejection rather than acting on the indicator alone.

### O6. Sustained rejection has an operational historical meaning

A "sustained rejection" is not a single bounce.

The user describes it as repeated attempts to reclaim a level after that level has been broken. Roughly **3-5 reclaim attempts** are often enough for the user to judge whether the level is holding or failing.

If repeated attempts continue to reject, the user interprets that as insufficient market capacity to recover above the level and remain there.

This repeated-test sequence helps determine both entry and exit timing.

The count 3-5 is a historical heuristic, not a frozen scientific threshold. The research implementation must test sensitivity around the count, dwell time, attempt spacing, excursion depth, and definition of a successful reclaim.

### O7. Retest path matters

The user reports reading retests before adding the 100 EMA.

Adding the 100 EMA made an intermediate step visible in sequences involving the 20/100/200 EMA hierarchy, including cases in which price crosses one baseline, tests another, and then re-tests the first as support/resistance.

The candidate scientific object is therefore not simply distance-to-EMA; it may be the **ordered path through a hierarchy of reference states**.

### O8. Multi-timescale views are nested, not usually conflicting

The user reports that the 15 s, 30 s, 1 min, and 5 min views almost never meaningfully disagree.

The slower views are treated as accumulated/coarse-grained products of the faster dynamics:
- 15 s provides the fastest local structure used for scalping;
- 30 s and 1 min provide progressively slower views of the same evolving process;
- 5 min provides a broader state of the cycle;
- still longer horizons, when used, provide larger snapshots of where the instrument sits in its overall cycle.

This motivates a nested-scale representation rather than a voting/confirmation model in which each timeframe is treated as an independent signal.

### O9. Session phase changes interpretability

The user reports that time of day matters and generally avoids at least the first few minutes of the opening period.

This is consistent with treating session phase as a moderator of any Market Χ relationship rather than pooling all times indiscriminately.

### O10. Short-exhaustion preference and possible directional asymmetry

The user reports being more comfortable and more effective reading short-side exhaustion than the corresponding long-side behavior.

This is a candidate asymmetry to test rather than assuming long/short mirror symmetry.

### O11. Waiting/refusal is part of the method

The user commonly waits 2-5 minutes between trades unless a "clear wave" is present, and often deliberately passes on ambiguous setups.

This means the historical method is event-selective, not a continuously active indicator system.

A tool derived from this lineage must therefore be allowed to output NO-TRADE / INSUFFICIENT STRUCTURE.

### O12. Quick harvesting is preferred over holding through multiple levels

The user increasingly prefers making a rapid price move pay, exiting, allowing the next test/retest to occur, and re-entering if the structure is again favorable.

This preference developed from observing that cycle speed and amplitude differ substantially by market; holding through multiple structural levels can turn a favorable move into a reversal before exit.

Winning-trade termination is therefore partly relational: capture the initial move, then reset rather than assuming continuation through the next level.

### O13. News is not a primary input

The user reports historically focusing on numbers, L2/tape, and responses to levels rather than headlines.

This does **not** establish that news is irrelevant to market dynamics; it only establishes that the user's historical decision process did not condition directly on it.

### O14. Execution footprint became an explicit concern

The user recognized that simulated 80-lot market-order execution may not transfer to live trading because of depth consumption, slippage, and self-impact, and considered reducing live clip size while preserving the same rapid enter/exit style.

This provides a natural intervention/self-perturbation question for the microstructure program.

## Candidate Χ interpretation

The historical trading logic is more naturally represented as a relational state than as one scalar:

[
X_t = (B_t, F_t, R_t, C_t, H_t)
]

where, provisionally:

- (B_t): baseline/reference geometry across scales;
- (F_t): native flow/tape state;
- (R_t): response to a test/perturbation (hold, reject, recover, breach, sustain);
- (C_t): context (session phase, direction, volatility/liquidity environment);
- (H_t): hierarchical/nested scale state connecting fast local motion to slower cycle location.

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

### H-T03: repeated-reclaim rejection hypothesis

A broken level followed by repeated failed reclaim attempts has a measurably different forward response distribution from:
- a single touch/bounce;
- an immediate successful reclaim;
- a breach with no meaningful retest.

The historical "3-5 attempts" rule is a seed for sensitivity analysis, not a fixed criterion.

### H-T04: flow-state moderation hypothesis

Tape/event-flow state moderates the consequence of a baseline test.

"Fast", "slow", "mixed", "green", and "red" must be translated into reproducible event-rate, aggressor-side, signed-flow, and/or book-update variables before testing.

### H-T05: session-phase moderation hypothesis

The sign and strength of depth/risk and baseline/response relationships differ by session phase.

This hypothesis is independently motivated by the trading record and is now also relevant to the current development-data result in which May 27 and May 31 showed stable depth geometry but opposite exploratory forward-risk signs.

### H-T06: directional-asymmetry hypothesis

Short-exhaustion and long-exhaustion events are not assumed to be mirror images. Separate conditional response maps will be estimated.

### H-T07: refusal/abstention hypothesis

Part of the method's performance may derive from selective non-participation rather than signal accuracy alone.

Any diagnostic/predictive tool must therefore be evaluated on:
- action quality when it emits a state;
- refusal frequency;
- performance of refused intervals;
- whether forced prediction degrades performance.

### H-T08: nested-timescale hypothesis

The slower chart state should be modelable as a coarse-grained representation of faster dynamics rather than as an independent indicator vote.

Candidate tests include:
- state-transition consistency across 15 s -> 30 s -> 1 min -> 5 min;
- whether fast-scale events predict slower-scale phase changes;
- whether information is lost, preserved, or reorganized under temporal coarse-graining.

### H-T09: cross-market scaling hypothesis

If the same cycle exists across instruments, the geometry should persist after appropriate normalization while characteristic timescale, amplitude, liquidity, and event rate vary by market.

The research must allow this hypothesis to fail. MNQ alone cannot establish it.

### H-T10: harvest-versus-hold hypothesis

For fast event-selected setups, capturing the initial response and re-evaluating at the next structural test may outperform holding through multiple reference levels after costs and slippage.

This is an execution/use-case hypothesis, not a claim about the underlying Χ definition.

### H-T11: self-impact hypothesis

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

This does not validate the trading method. It supports making **context-conditioned relationships** and **hierarchical scale state** first-class targets instead of searching for one global depth -> risk sign.

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

## Resolved implementation details

The following previously open items are now substantially resolved from the user's clarification:

- Scope: observations are reported across the broader market, with instrument-dependent speed/amplitude.
- MACD: broker/platform default settings; not user-tuned.
- EMA: same 20/100/200 settings across 15 s, 30 s, 1 min, and 5 min charts.
- VWAP: broker/platform default; not user-adjusted.
- "$25/$100 levels": prior interpretation withdrawn as a misread.
- Time & Sales: broker defaults except display-window size/layout.
- Sustained rejection: repeated failed reclaim attempts after a break, commonly judged over roughly 3-5 attempts.
- Multi-timeframe relation: nested/coarse-grained views of the same cycle, not usually conflicting independent signals.
- Exit style: increasingly favor quick harvested moves and re-evaluation/re-entry at later tests rather than holding through multiple levels.

## Remaining information required for reproducible translation

1. Exact broker/platform used for the historical observations, so its default MACD, VWAP, Time & Sales, and L2 settings can be recovered rather than guessed.
2. Exact L2/DOM depth, aggregation, and filter defaults from that platform.
3. Operational meaning of "clear wave".
4. A more explicit rule for what ends the initial quick winning move when it is not simply a dollar/PnL target.
5. A more explicit invalidation rule for a losing trade when repeated rejection/reclaim structure is ambiguous.
6. More detailed session categories beyond "avoid the first few minutes" if the user consciously distinguished them.
7. Whether long-side setups use materially different evidence beyond the stated lower confidence/preference.
8. Recovery of timestamped personal trade-history exports, screenshots, or replay markers if they exist. Current Project/Library search did not locate an obvious personal broker execution/fill-history file. These records would be P0-D reconstruction material, not P1 confirmation.

## Next research use

Do not tune the current MNQ engine to reproduce this narrative.

Instead:
1. finish the independent development sweep;
2. operationalize repeated-reclaim rejection, flow-state labels, and nested-scale state without looking at holdout outcomes;
3. test the generated hypotheses on development data with native comparators;
4. add a cross-instrument plan before making a market-wide cycle claim;
5. freeze the resulting definitions;
6. preserve the June 9-11 holdout for prospective/untouched qualification where applicable.
