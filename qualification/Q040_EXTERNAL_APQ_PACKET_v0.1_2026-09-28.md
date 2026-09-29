# Q040 External APQ Review Packet v0.1

Date: 2026-09-28
Governance: SymC GOM v1.0
APQ level: APQ-2 SUBSTANTIAL
Plan under review:
\`qualification/Q040_RECOVERABILITY_PLAN_PACKET_v0.1_2026-09-28.md\`

Canonical plan commit:
\`c5b095c1205109753b900d5ee7269efaad802e39\`

Prior-art foundation:
\`qualification/Q040_PRIOR_ART_NOVELTY_FOUNDATION_v0.1_2026-09-28.md\`

Prior-art foundation commit:
\`1717ead07b17c463c4bef5f25ed60a4beca053ce\`

## Reviewer role

Perform an isolated adversarial review of the Q040 plan **before any Q040 real-data outcome is opened**.

Do not decide whether the hypothesis is interesting. Attack whether the proposed design could distinguish its target from simpler market-microstructure explanations.

Do not assume that \(\chi\), \(Χ\), or \(Χ_{\mathrm{arc}}\) exists merely because the notation is available.

## Scientific target being reviewed

The residual target is:

> Within empirical LOB episodes, do later perturbations show altered recoverability relative to a representation-licensed, scale-local baseline after controlling current perturbation magnitude, duration, direction, spacing, session phase, activity, liquidity, volatility, order-flow memory, and baseline motion; and does any residual recovery-history signal add information about subsequent migration/reorganization of the next slower-scale baseline beyond that slower scale's own persistence and native context?

This is intentionally narrower than generic resiliency, hysteresis, repeated shocks, scaling, or market invariance.

## Required severity classes

For every objection use exactly one:
- BLOCKER
- MATERIAL
- MINOR

For each BLOCKER or MATERIAL objection provide:

1. threatened inference;
2. exact failure mechanism;
3. smallest discriminating fix/test;
4. whether the fix is outcome-independent;
5. whether the fix materially changes the plan;
6. required claim restriction if unresolved.

Do not vote by reviewer consensus. A single valid MATERIAL objection requires adjudication.

## Required attack domains

### 1. Prior art / novelty

Attack whether the residual still collides with:
- single-shock LOB resiliency;
- Hawkes/self-exciting liquidity shocks;
- flash-crash recovery;
- market hysteresis/path dependence;
- cascading-shock models;
- multiscale liquidity;
- market microstructure invariance;
- cross-asset/time aggregate-impact scaling.

If the novelty is only integration, say so.

### 2. Representation admission

Attack:
- candidate scalar \(\chi_S^*(t)\);
- current scalar-refusal compatibility;
- use of EMA/VWAP as candidate observables rather than assumed \(\chi\);
- existing L10 modal/vector \(Χ_S(t)\);
- whether adding MACD/L2/order-flow/reference-response objects creates an incoherent feature bundle rather than a modal representation;
- whether \(Χ_{\mathrm{arc},S}(t)\) can be defined independently of future recovery/price outcomes;
- whether REFUSED / NOT_APPLICABLE outcomes are adequately protected.

### 3. Scale-local baseline

Attack:
\[
B_S^{(r)}(t)=\mathcal{K}_S[Z_S^{(r)}(\tau<t)].
\]

Specifically:
- causal operator choice;
- averaging-window arbitrariness;
- trend leakage;
- moving-baseline versus recovery ambiguity;
- whether one operator can be used across representations;
- whether baseline motion should be treated as predictor, outcome, or both;
- whether the 15/30/60/300 s ladder is scientifically justified for Q040 rather than inherited mechanically from Q039.

Recommend the smallest non-circular baseline qualification route.

### 4. Perturbation-event construction

Attack:
- distance metric;
- threshold selection;
- event entry/exit;
- sustain definition;
- episode timeout;
- event merging/separation;
- overlapping perturbations across scales;
- endogenous event selection.

The event set must not be defined from the later recovery outcome.

### 5. Recovery object

Attack the candidate vector:

\[
R_{S,j}=
(T_{\mathrm{return}},
T_{\mathrm{sustain}},
P_{\mathrm{sustain}},
D_{\mathrm{dwell}},
E_H,
G_{\mathrm{recovery}}).
\]

Ask whether:
- components are redundant;
- censoring is handled;
- survival/hazard analysis is preferable;
- a primary outcome can be frozen without destroying the vector nature;
- fixed-horizon residuals create arbitrary tuning.

### 6. History/burden mechanism

Attack:
- perturbation ordinal count;
- cumulative absolute load;
- cumulative displaced time;
- incomplete-recovery burden.

Determine whether these are identifiable separately from:
- shock clustering;
- order-flow memory;
- current state;
- baseline drift;
- regime duration.

The researcher's descriptive "3-5 attempts" observation may not become a threshold unless independently justified.

### 7. Native comparator

Attack whether the proposed native model adequately controls:
- spread/depth;
- event/trade intensity;
- signed volume/order flow;
- volatility;
- session phase;
- update/staleness;
- current baseline velocity;
- inter-perturbation spacing;
- Hawkes-like/self-excitation history.

Identify any simpler native comparator that could absorb the proposed effect.

### 8. Cross-scale propagation

Attack whether faster-scale recovery history can be tested against future slower-baseline movement without:
- using the same data twice;
- defining the slower baseline from the outcome;
- confusing trend with propagation;
- creating mechanical overlap between nested windows;
- importing Q039 conclusions.

Demand explicit null worlds with within-scale history but no cross-scale propagation, and vice versa.

### 9. Exogenous forcing

Attack treatment of:
\[
\xi(t).
\]

Specifically:
- scheduled macro events;
- timestamped news;
- unscheduled/unobserved news;
- correlated cross-market shocks.

State whether the first test should exclude, control, stratify, or explicitly refuse event-contaminated windows.

### 10. Dependence / inference

Attack:
- within-episode dependence;
- within-day dependence;
- sparse late-attempt strata;
- survivor bias;
- day weighting;
- episode weighting;
- bootstrap/resampling unit;
- multiple scales and multiple recovery metrics;
- sign interactions.

No result should be driven by a tiny tail of repeated attempts.

### 11. Known truths

Attack NC-R1 through NC-R10.

Require additional synthetic worlds if needed to distinguish:
- true erosion;
- shock clustering;
- baseline migration;
- adaptation;
- sign asymmetry;
- exogenous common causes;
- scalar refusal;
- true/no cross-scale propagation.

### 12. Scale-invariance language

The plan does not claim universal scale invariance.

Attack the later hypothesis of functional transport across instruments/timeframes against existing scaling/invariance literature.

State exactly what evidence would be required before "scale invariant" language could be used at all.

## Shared-premise attack

At least once, challenge the possibility that the entire Stability Architecture framing adds no value beyond a strong native market-state/history model.

A valid outcome is:
- native market model sufficient;
- \(\chi\) refused;
- \(Χ\) descriptive only;
- \(Χ_{\mathrm{arc}}\) no added value.

Do not protect the framework.

## Mandatory evidence firewall

Do not request, inspect, infer, or ask for:
- Q040 real outcomes;
- Q039 real outcomes;
- Q038 June 9-11 as tuning evidence.

The review is plan-only.

## Required final section

Provide:

### BLOCKER
List all or "none."

### MATERIAL
List all or "none."

### MINOR
List all or "none."

### Minimum Plan Delta
State the smallest changes needed before preregistration.

### Claim ceiling after fixes
State exactly what the design could claim if every future gate passed.

## Required footer

End exactly with one:

\`APQ_EXTERNAL_STATUS=QUALIFIED\`

or

\`APQ_EXTERNAL_STATUS=REVISE\`

or

\`APQ_EXTERNAL_STATUS=BLOCKED\`

Then:

\`PLAN_COMMIT=c5b095c1205109753b900d5ee7269efaad802e39\`
