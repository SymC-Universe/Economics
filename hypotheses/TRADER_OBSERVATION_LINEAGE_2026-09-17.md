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

Different instruments appear to express the cycle at different characteristic speeds and amplitudes. MNQ is **not** treated as a uniquely high-speed laboratory. In the user's experience, small-cap / daily-high-gainer equities can cycle substantially faster and more violently than MNQ, whereas slower instruments such as GLD can express analogous sequences over longer timescales.

MNQ is therefore the current high-resolution data testbed, not the upper-speed endpoint of the market-wide hypothesis.

This is a historical observation and a future cross-instrument falsification target. It is not assumed from the current MNQ evidence.

### O2. Multi-timescale baseline hierarchy

The user evaluates price relative to:
- 20 EMA;
- 100 EMA;
- 200 EMA;
- VWAP;
- multiple chart resolutions: 15 s, 30 s, 1 min, and 5 min.

EMA settings were identical across those charts. MACD, EMA, VWAP, and Time & Sales settings were not custom-tuned beyond display/window arrangement; the user used the broker/platform defaults available when selected.

The user's reason for preserving broker defaults is methodological: the user wants to observe the same conventional reference constructions that many other traders may also see, rather than creating idiosyncratic levels by custom-tuning parameters. The proposition that these defaults are widely shared, and that shared visibility contributes causally to market response, is **not yet established** and becomes a testable shared-reference hypothesis.

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

The user describes it as repeated attempts to recover/reclaim a level after that level has been broken. A rejection does **not** mean price merely touches the level. Price may actively recover toward or through the level, appear to begin reclaiming it, and then fail to sustain the recovery.

Those failed recoveries are especially important to the user's short entries. The user reports that short-side opportunities of this type appear more frequently in practice than equivalent long-side opportunities.

Roughly **3-5 attempts** is a common personal observation/decision limit, not a claimed fixed property of the market. It reflects how many recovery/reclaim attempts the user will often watch before deciding that the attempted recovery is repeatedly failing.

If repeated attempts recover and then fail to hold, the user interprets that as insufficient market capacity to push price higher and keep it there.

This repeated recovery-failure sequence helps determine both entry and exit timing.

The research implementation must therefore model the *trajectory of each reclaim attempt* (approach, penetration/recovery, dwell, loss of the level, and subsequent response), not count line touches. Attempt count, dwell time, spacing, excursion depth, recovery velocity, hold duration, and successful-reclaim definition all require sensitivity analysis.

### O7. Retest path matters

The user reports reading retests before adding the 100 EMA.

Adding the 100 EMA made an intermediate step visible in sequences involving the 20/100/200 EMA hierarchy, including cases in which price crosses one baseline, tests another, and then re-tests the first as support/resistance.

The candidate scientific object is therefore not simply distance-to-EMA; it may be the **ordered path through a hierarchy of reference states**.

### O8. Multi-timescale views are nested and may reflect temporal substrate inheritance

The user reports that the 15 s, 30 s, 1 min, and 5 min views almost never meaningfully disagree.

The user's interpretation is closer to **substrate inheritance across temporal representation** than to independent confirmation signals:
- 15 s expresses the fastest local dynamics used for scalping;
- 30 s and 1 min are built from those faster observations and show the same process at progressively slower temporal resolution;
- 5 min is a product of the faster evolution and reveals a broader location within the cycle;
- still longer horizons provide larger snapshots of what the instrument is doing and where it sits in the larger cycle.

The research question is therefore not merely whether slower charts are statistical coarse-grainings. It is whether dynamical structure is **inherited, reorganized, preserved, or lost** as faster market activity becomes the substrate of slower-timescale states.

This motivates a hierarchical inheritance/reorganization representation rather than a voting model in which each timeframe is treated as an independent signal.

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

### H-T03: repeated recovery-failure rejection hypothesis

A broken level followed by one or more **active recovery/reclaim attempts that subsequently fail to sustain the level** has a measurably different forward response distribution from:
- a mere touch of the level;
- an immediate clean rejection without meaningful recovery;
- a successful reclaim that holds;
- a breach with no meaningful retest.

The historical "3-5 attempts" observation is a personal decision horizon and seed for sensitivity analysis, not a fixed structural criterion. The primary event object is the recovery-and-failure trajectory, not the attempt count alone.

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

### H-T08: temporal substrate-inheritance hypothesis

Slower-timescale market states are hypothesized to arise from faster dynamics as an inherited/reorganized temporal substrate rather than as independent indicator votes.

Candidate tests include:
- state-transition consistency across 15 s -> 30 s -> 1 min -> 5 min;
- whether fast-scale state sequences reconstruct the slower-scale state without adding ad hoc variables;
- which features are preserved, transformed, amplified, cancelled, or lost as timescale increases;
- whether modal organization changes rank or composition across timescales;
- whether any scalar χ admitted at one scale is inherited, transformed, or refused at another.

"Substrate inheritance" here is a research hypothesis to test, not a foregone conclusion.

### H-T09: cross-market timing and cycle-expression hypothesis

Physical elapsed time is not rescaled across markets: 15 s, 30 s, 1 min, and 5 min remain the same wall-clock durations for every instrument.

If the same broad cycle exists across instruments, different markets may traverse different fractions of that cycle during the same elapsed time because their characteristic dynamics differ. That does **not** make time itself market-dependent.

Primary analyses therefore remain in ordinary clock time. A dimensionless phase or cycle-position coordinate may be explored secondarily when justified, but it must never replace or reinterpret the actual elapsed seconds.

The research must allow the cross-market cycle hypothesis to fail. MNQ alone cannot establish it.

### H-T10: harvest-versus-hold hypothesis

For fast event-selected setups, capturing the initial response and re-evaluating at the next structural test may outperform holding through multiple reference levels after costs and slippage.

This is an execution/use-case hypothesis, not a claim about the underlying Χ definition.

### H-T11: shared-reference hypothesis

The user's deliberate use of broker-default EMA/MACD/VWAP/T&S settings generates a testable social-measurement hypothesis: widely shared default reference constructions may coincide with stronger or more repeatable market responses because multiple participants observe similar levels.

This mechanism is **not assumed**. Competing explanations include ordinary smoothing geometry, trend persistence, microstructure, and chance.

Required controls should include:
- default parameters versus nearby perturbed parameters;
- multiple alternative EMA lengths with matched effective timescales;
- placebo/reference levels;
- broker/platform differences where defaults differ;
- reaction strength before/after controlling for native book/flow state.

A default setting only "adds" if it outperforms suitably matched alternatives without circular selection.

### H-T12: self-impact hypothesis

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
- Sustained rejection: active recovery/reclaim attempts after a break that repeatedly fail to sustain the recovered level; ~3-5 is a common personal decision horizon, not a fixed market threshold.
- Multi-timeframe relation: nested inherited/reorganized views of the same cycle, closer to a temporal substrate-inheritance question than independent confirmation or simple coarse-graining.
- Default indicator rationale: broker defaults are intentionally preserved to overlap with conventional/shared trader reference frames; whether this produces any measurable coordination effect remains unverified.
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
2. operationalize active recovery-failure rejection trajectories, flow-state labels, and temporal inheritance states without looking at holdout outcomes;
3. add default-versus-perturbed reference tests before attributing any reaction to shared indicator visibility;
4. test the generated hypotheses on development data with native comparators;
5. add a cross-instrument plan spanning faster small-cap/daily-high-gainer behavior through intermediate MNQ and slower instruments such as GLD, while preserving identical wall-clock units across all markets; any phase-normalized comparison is secondary only;
6. freeze the resulting definitions;
7. preserve the June 9-11 holdout for prospective/untouched qualification where applicable.
