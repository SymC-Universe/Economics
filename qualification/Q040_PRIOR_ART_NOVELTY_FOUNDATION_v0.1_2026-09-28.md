# Q040 Prior-Art and Novelty Foundation v0.1

Date: 2026-09-28
Governance: SymC GOM v1.0
Stage: P0-N / A0
Status: RESIDUAL_DEFINED FOR PLAN CONSTRUCTION; later-literature rule remains active
Real Q040 outcome exposure: NONE

## 1. Candidate question

Q040 asks whether repeated perturbation history changes **recoverability** around a representation-licensed, scale-local baseline, and whether any such change remains local or propagates into slower-scale baseline migration.

The candidate time hierarchy begins with:

\[
15\,\mathrm{s}\rightarrow30\,\mathrm{s}\rightarrow60\,\mathrm{s}\rightarrow300\,\mathrm{s}.
\]

The candidate representation lattice is:

\[
B_S^{\chi}(t),\qquad
B_S^{Χ}(t),\qquad
B_S^{Χ_{\mathrm{arc}}}(t),
\]

but only where each representation independently earns admission.

No current Q040 plan assumes that every scale admits all three representations.

## 2. Literature search

Dedicated Undermind deep search:
- workspace: \`c9911501-f69c-401b-9658-4851eaf10682\`
- search: \`Repeated perturbation and recoverability erosion in market microstructure\`
- completed 2026-09-28/29 UTC
- 117 papers surfaced

Search result summary:

> Empirical LOB resiliency is primarily studied as recovery from individual shocks. The closest sequence-level evidence concerns recurrent liquidity droughts, spiraling shock clusters, aftershocks, and path dependence. Among retrieved studies, none jointly tests whether later perturbations around a predeclared baseline have lower sustained-recovery probability, longer recovery time, shorter reclaim dwell, or greater residual displacement while controlling shock size, spacing, time of day, volatility, liquidity/activity, and direction.

This is a literature-search result, not proof of universal novelty.

## 3. Prior art that removes broad novelty claims

### 3.1 Single-shock LOB resiliency

Already established:
- Jeremy Large, "Measuring the resiliency of an electronic limit order book" (2007), DOI 10.1016/J.FINMAR.2006.09.001.
- Xu et al., "Limit-order book resiliency after effective market orders: spread, depth and intensity" (2016), DOI 10.1088/1742-5468/aa7a3e.
- Braun et al., "Impact and recovery process of mini flash crashes: An empirical study" (2017), DOI 10.1371/journal.pone.0196920.
- Clapham et al., "Does Speed Matter? The Role of High-Frequency Trading for Order Book Resiliency" (2020), DOI 10.1111/jfir.12229.
- Panayi and Peters, "Survival models for the duration of bid-ask spread deviations" (2014), DOI 10.1109/CIFEr.2014.6924048.

Removed novelty:
- order books recover after liquidity shocks;
- recovery time, depth replenishment, spread recovery, and recovery duration are measurable;
- recovery can depend on market state and participant behavior.

### 3.2 Shock clustering, path dependence, and hysteresis

Already established or directly neighboring:
- Pelizzon, Sagade, and Vozian, "Resiliency: Cross-Venue Dynamics with Hawkes Processes" (2020), DOI 10.2139/ssrn.3711976.
- Toth et al., "Studies of the limit order book around large price changes" (2009), DOI 10.1140/epjb/e2009-00297-9.
- Eisler, Bouchaud, and Kockelkoren, "Models for the Impact of All Order Book Events" (2011), DOI 10.2139/SSRN.1888105.
- McConnell, "Liquidity Recovery and Market Hysteresis" (2026), SSRN 7190939, DOI 10.2139/ssrn.7190939.
- Lukianchenko et al., "Network Stability of Financial Markets under Cascading Shocks in an Agent-Based Model" (2026), SSRN 7005704.
- "Liquidity Recovery Dynamics Following Volatility Shocks: Evidence from an Emerging Equity Market" (2026), DOI 10.3390/ijfs14050111.

Removed novelty:
- recovery may be path-dependent;
- visible restoration need not equal structural restoration;
- shocks can cluster;
- temporally clustered/cascading shocks can differ from one equivalent-amplitude shock in simulation;
- aftershocks and incomplete restoration are plausible market phenomena.

### 3.3 Multiscale and cross-asset invariance/scaling

Already established or directly neighboring:
- Eisler, Kertesz, and Lillo, "The limit order book on different time scales" (2007), DOI 10.1117/12.724817.
- Corradi, Zaccaria, and Pietronero, "Liquidity crises on different time scales" (2015), DOI 10.1103/PhysRevE.92.062802.
- Kyle and Obizhaeva, "Market Microstructure Invariance: Empirical Hypotheses" (2016), DOI 10.3982/ECTA10486.
- Patzelt and Bouchaud, "Universal scaling and nonlinearity of aggregate price impact in financial markets" (2018), DOI 10.1103/PhysRevE.97.012304.

Removed novelty:
- market microstructure can show scaling relations;
- some normalized relations transfer across assets;
- LOB mechanisms change with timescale;
- aggregate price-impact shapes can show cross-instrument/intraday scaling.

Q040 therefore must not claim novelty from "the same pattern occurs at many scales" by itself.

## 4. Residual novelty target

The strongest currently defensible residual is a **combined empirical discrimination**, not a generic resilience or scaling claim:

> Within empirically observed LOB episodes, do later perturbations show altered recoverability relative to a representation-licensed, scale-local baseline after matching or controlling current perturbation magnitude, duration, direction, spacing, session phase, activity, liquidity, volatility, order-flow memory, and baseline motion; and does any residual recovery-history signal add information about subsequent migration/reorganization of the next slower-scale baseline beyond that slower scale's own persistence and native context?

The residual has four separable pieces:

1. **representation qualification**  
   Determine whether a usable baseline exists in scalar \(\chi\), modal/vector \(Χ\), architecture-level \(Χ_{\mathrm{arc}}\), or only a subset. Refusal is allowed.

2. **within-scale recovery-history discrimination**  
   Compare memoryless recovery against ordinal attempt, cumulative perturbation load, cumulative time displaced, and incomplete-recovery burden.

3. **cross-scale propagation discrimination**  
   Test whether fast-scale recovery degradation/adaptation adds information about future slower-baseline migration beyond slower-scale persistence and native context.

4. **later cross-instrument transport**  
   Only after development is frozen, test whether the same functional organization transports to untouched instruments/asset classes after native normalization. This is not part of the first development claim.

## 5. Representation hypotheses remain candidates

### 5.1 Scalar \(\chi\)

Trader-visible EMA/VWAP references are **candidate scalar observables**, not admitted \(\chi\).

Current MNQ production scalar \(\chi\) remains REFUSED under existing admission rules.

Any Q040 scalar coordinate must earn admission prospectively and may remain REFUSED.

### 5.2 Modal/vector \(Χ\)

The strongest currently grounded Market candidate is the existing L10 semantic/modal architecture.

Additional candidate inputs such as MACD, L2 geometry, order flow, and price behavior around trader-visible reference levels may be tested, but must not be folded into \(Χ\) merely because they are useful to a trader.

### 5.3 Architecture-level \(Χ_{\mathrm{arc}}\)

\(Χ_{\mathrm{arc}}\) must be built only from information available at time \(t\) or earlier and must be independently qualified against native alternatives.

Future rejection, rebound, continuation, or regime transition is an **outcome**, not part of the definition of \(Χ_{\mathrm{arc}}\).

### 5.4 Exogenous forcing

News or other externally arriving information is represented separately as candidate forcing/context:

\[
\xi(t).
\]

It may reorganize \(\chi\), \(Χ\), or \(Χ_{\mathrm{arc}}\), but must not be silently absorbed into an endogenous representation.

## 6. Strongest native comparators/confounds

A Q040 plan must explicitly challenge at least:

- current perturbation magnitude and duration;
- inter-perturbation spacing;
- incomplete recovery from the previous perturbation;
- session phase;
- realized volatility;
- spread/depth/liquidity state;
- event/trade intensity;
- signed trade volume and order-flow imbalance;
- L10 update/staleness state;
- baseline slope/velocity;
- order-flow self-excitation / Hawkes-like clustering;
- direction asymmetry;
- endogenous shock timing;
- identifiable scheduled or timestamped exogenous news;
- unmeasured exogenous forcing as a limitation;
- within-episode and within-day dependence.

A history term earns admission only if it adds out-of-sample information beyond an adequate native recovery model.

## 7. Falsifiers and refusal outcomes

The candidate is weakened, narrowed, or refused if:

- later perturbations recover equally well after current-state adjustment;
- apparent erosion vanishes after matching perturbation size or spacing;
- shorter shock spacing fully explains the pattern;
- baseline migration fully explains apparent recovery loss;
- order-flow self-excitation fully explains the history term;
- only one hand-selected reference or one scale produces the effect;
- the effect reverses by perturbation sign;
- repeated perturbations strengthen rather than weaken recovery;
- the faster-scale history signal adds no information about slower-scale migration;
- scalar \(\chi\) refuses while \(Χ\) remains informative;
- \(Χ_{\mathrm{arc}}\) adds no information beyond admitted native/\(Χ\) models;
- cross-instrument transport later fails.

These are results, not defects.

## 8. A0 disposition

**A0 status:** RESIDUAL_DEFINED / COMPLETE FOR PLAN CONSTRUCTION.

Broad claims of resiliency, hysteresis, repeated-shock effects, scale dependence, scale invariance, and cross-asset normalized regularity are removed from the novelty target.

The candidate residual is sufficiently narrow to enter APQ plan construction, but full-text collision review and later-literature intake remain active. No P1 claim, threshold, baseline operator, perturbation threshold, or \(Χ_{\mathrm{arc}}\) construction is frozen by this document.
