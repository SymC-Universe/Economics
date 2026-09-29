# Q040 Repeated-Perturbation Recoverability Plan Packet v0.1

Date: 2026-09-28
Governance: SymC GOM v1.0
APQ level: APQ-2 SUBSTANTIAL
Stage: P0-D plan construction after P0-N/A0 residual definition
Status: CANDIDATE PLAN / NOT PREREGISTERED / NO REAL Q040 OUTCOME AUTHORIZED
Prior-art foundation: \`qualification/Q040_PRIOR_ART_NOVELTY_FOUNDATION_v0.1_2026-09-28.md\`
Relationship to Q039: SEPARATE SCIENTIFIC LANE

## 1. Purpose

Q040 asks whether **recoverability itself is history-dependent** in market microstructure and whether any history dependence propagates across a wall-clock hierarchy.

Three questions are intentionally separated.

### Q040-R: representation-qualified baseline

At each scale \(S\), which representation, if any, supports a causal scale-local baseline:

\[
B_S^{\chi}(t),\qquad
B_S^{Χ}(t),\qquad
B_S^{Χ_{\mathrm{arc}}}(t)?
\]

A representation may be ADMITTED, REFUSED, or NOT_APPLICABLE.

### Q040-W: within-scale repeated-perturbation recovery

Conditional on current perturbation and native state, does prior perturbation/recovery history add information about the current recovery trajectory?

### Q040-H: cross-scale propagation

If a faster-scale recovery-history signal exists, does it add information about future migration/reorganization of the next slower-scale baseline beyond that slower scale's own persistence and native context?

No causal inheritance, profitable-trading, universal scale-invariance, or cross-instrument claim is tested in the first Q040 development cycle.

## 2. Candidate scale hierarchy

Initial scales:

\[
15\,\mathrm{s}
\rightarrow
30\,\mathrm{s}
\rightarrow
60\,\mathrm{s}
\rightarrow
300\,\mathrm{s}.
\]

Wall-clock time is literal.

No activity-time rescaling may silently replace these scales.

Longer scales are exploratory only until separately APQ-qualified.

## 3. Representation discipline

### 3.1 Candidate scalar \(\chi_S^*(t)\)

The asterisk denotes **candidate, not admitted**.

EMA/VWAP and other trader-visible one-dimensional references are candidate scalar observables because they compress a moving market state to scalar references. They are not automatically SymC \(\chi\).

Current canonical scalar \(\chi\) remains REFUSED in existing MNQ production screens.

A Q040 scalar representation must earn admission from native dynamics and added-value tests before the asterisk can be removed.

### 3.2 Modal/vector \(Χ_S(t)\)

The strongest currently grounded starting candidate is the existing L10 semantic/modal architecture.

Candidate additional inputs include:
- L2/L10 book geometry;
- order-flow/tape state;
- MACD or other relational price-history objects;
- price behavior relative to predeclared trader-visible reference levels.

No candidate is admitted into \(Χ\) because it was useful in discretionary trading.

### 3.3 Architecture-level \(Χ_{\mathrm{arc},S}(t)\)

\(Χ_{\mathrm{arc}}\) is not defined as "everything that predicts the price."

It must be an independently constructed conglomerate/system representation from admitted components and native context, using only information available at time \(t\) or earlier.

Schematic candidate only:

\[
Χ_{\mathrm{arc},S}(t)
=
\mathcal{A}_S
\left[
\chi_S(t),
Χ_S(t),
\xi(t),
C_S(t)
\right].
\]

Future recovery/rejection/rebound is an outcome and may not enter this definition.

### 3.4 Exogenous forcing

Use

\[
\xi(t)
\]

for timestamped exogenous forcing/context where identifiable, including scheduled macro releases and timestamped material news.

Unmeasured news remains an explicit limitation.

## 4. Evidence firewall

Q040 has no real-data outcome authorization yet.

Development evidence, once a preregistration is frozen, may use existing MNQ development data only as **P0-D**, never as untouched confirmation.

The following cannot serve as Q040 P1 confirmation:
- any dates already used in Q037/Q038/Q039 development;
- Q038 June 9-11;
- any session opened while constructing Q040.

Q039 real outcomes must not be used to select Q040 baseline operators, thresholds, recovery metrics, representations, or claims.

A future P1 test requires prospectively untouched data identities frozen before opening.

## 5. Baseline object

The baseline is not assumed to be one fixed horizontal price level.

For representation \(r\in\{\chi,Χ,Χ_{\mathrm{arc}}\}\) at scale \(S\):

\[
B_S^{(r)}(t)
=
\mathcal{K}_S
\left[
Z_S^{(r)}(\tau<t)
\right],
\]

where:
- \(Z_S^{(r)}\) is the admitted representation at scale \(S\);
- \(\mathcal{K}_S\) is a causal scale-local averaging/state-estimation operator;
- only information available before the perturbation may enter the baseline.

### 5.1 Operator remains open at APQ v0.1

Candidate operator families:
- fixed trailing block mean/centroid;
- robust trailing centroid;
- exponentially weighted causal state estimate with scale-linked time constant.

The final preregistration must choose one primary operator prospectively or provide a non-tuned qualification rule.

Outcome-based operator selection is forbidden.

### 5.2 Baseline migration is a separate outcome

A failure to recover toward a fixed pre-perturbation \(B_S^{(r)}(t_0)\) is distinct from movement of the ongoing local baseline.

Track:
- recovery relative to the pre-perturbation baseline;
- baseline velocity/drift after the perturbation;
- distance/alignment between the fast baseline and the next slower baseline.

This separates local recovery failure from genuine scale-level regime migration.

## 6. Perturbation episode

No hand-labeled chart pattern may define the decisive event set.

For an admitted representation, define a scale-normalized signed distance:

\[
d_{S}^{(r)}(t)
=
\mathcal{D}
\left(
Z_S^{(r)}(t),
B_S^{(r)}(t_0)
\right).
\]

The final preregistration must freeze:
- the distance metric \(\mathcal{D}\);
- perturbation entry threshold;
- recovery/reclaim threshold;
- sustain rule;
- episode timeout;
- minimum separation/merging rule.

Thresholds must be calibrated without Q040 outcome optimization.

For each perturbation \(j\), retain at least:
- sign;
- peak amplitude;
- integrated displacement;
- duration;
- time since prior perturbation;
- session phase;
- event/trade intensity;
- spread/depth/liquidity state;
- signed volume/order flow;
- update/staleness state;
- realized volatility/native risk state;
- baseline velocity/drift;
- prior recovery state.

## 7. Recovery object

Do not reduce recovery to one scalar unless a scalar object independently earns admission.

Candidate recovery vector for perturbation \(j\):

\[
R_{S,j}
=
\left(
T_{\mathrm{return}},
T_{\mathrm{sustain}},
P_{\mathrm{sustain}},
D_{\mathrm{dwell}},
E_H,
G_{\mathrm{recovery}}
\right).
\]

Candidate meanings:
- \(T_{\mathrm{return}}\): time to first return/reclaim;
- \(T_{\mathrm{sustain}}\): time to sustained recovery;
- \(P_{\mathrm{sustain}}\): sustained-recovery indicator/probability;
- \(D_{\mathrm{dwell}}\): post-reclaim recovered-side dwell;
- \(E_H\): residual displacement at frozen horizon \(H\);
- \(G_{\mathrm{recovery}}\): recovery excursion normalized to perturbation magnitude.

Exact primary/secondary status remains open for APQ.

## 8. History/burden hypotheses

Do not assume ordinal attempt number is the mechanism.

Candidate history variables:

\[
N_j=j-1
\]

prior perturbation count;

\[
L_j=\sum_{k<j} A_k
\]

cumulative absolute perturbation load;

\[
U_j=\sum_{k<j} T_{\mathrm{away},k}
\]

cumulative time displaced;

and an incomplete-recovery burden \(F_j\) constructed only from frozen prior-episode recovery information.

The researcher's prior observation of roughly 3-5 attempts is descriptive only and cannot become a threshold without prospective justification.

## 9. Native comparator architecture

Q040-W must compare history-bearing models against a strong memoryless/current-state native model.

Minimum native comparator families to challenge:
- current perturbation amplitude/duration;
- inter-perturbation interval;
- session harmonics/time of day;
- spread and depth;
- native L10 imbalance;
- event/trade intensity;
- trade volume and signed trade volume;
- order-flow imbalance;
- realized volatility;
- update fraction and staleness;
- current baseline slope/velocity;
- current distance between fast and next-slower baselines.

A separate clustering/self-excitation comparator must challenge the possibility that "erosion" is only closely spaced endogenous shocks. Candidate implementations include Hawkes-like recent-event intensity or another prospectively frozen native event-history model.

History earns admission only by out-of-sample added value beyond these comparators.

## 10. Candidate Q040-W model comparison

The exact estimator is not frozen at plan v0.1.

Candidate nested logic:

- **M0:** current-state/native recovery model;
- **M1:** M0 + perturbation ordinal history;
- **M2:** M0 + cumulative perturbation load/time burden;
- **M3:** M0 + incomplete-recovery burden;
- **M4:** strongest prospectively selected history model after synthetic qualification, without real-outcome feature search.

The design must distinguish:
- erosion;
- equivalence/no added history value;
- adaptation/strengthening;
- mixed/sign-dependent behavior;
- refusal/insufficient identification.

No negative coefficient may automatically be called "damage" or "fatigue."

## 11. Candidate Q040-H cross-scale propagation

For adjacent \(S<S'\), define slower-baseline future movement/reorganization without using future price direction to construct the predictor.

Candidate target family:

\[
\Delta B_{S'}^{(r)}(t,t+\Delta)
\]

or an independently defined representation-distance/reorganization measure.

Comparator must contain:
- current and lagged \(B_{S'}^{(r)}\);
- slower-scale native context;
- faster-scale current state;
- activity/volatility/session controls.

Then add frozen faster-scale recovery-history variables.

Positive interpretation is limited to:

> faster-scale recovery history adds information about future slower-scale baseline migration/reorganization beyond the frozen native comparator.

It is not causal transmission.

## 12. Direction symmetry

Primary formulation is sign-agnostic.

A direction interaction must be reported.

Allowed outcomes include:
- similar history effect in both directions;
- asymmetric magnitude;
- one-direction-only effect;
- sign reversal;
- no effect.

Pooling may not hide a strong sign interaction.

## 13. Exogenous-event handling

News cannot simply be called "noise."

Before preregistration, reviewers must attack whether the first development test should:
- exclude a predeclared window around identifiable scheduled releases;
- include event indicators in the native comparator;
- stratify scheduled-event windows;
- or use another outcome-independent rule.

Unscheduled/unidentified news remains residual exogenous forcing and limits causal interpretation.

## 14. Dependence and uncertainty

Perturbations within one episode are not independent.

Episodes within a day are not necessarily independent.

The final preregistration must define:
- clustering/resampling unit;
- day weighting;
- episode weighting;
- block or hierarchical bootstrap strategy;
- minimum number of independent episodes/days required;
- refusal conditions for sparse later-attempt strata.

No large attempt number may be interpreted from a tiny surviving tail.

## 15. Synthetic known-truth requirements before real execution

At minimum, the implementation must discriminate:

### NC-R1 memoryless recovery
Current state fully determines recovery. History must not add.

### NC-R2 clustered shocks without erosion
Closely spaced shocks generate apparent slower recovery, but spacing/self-excitation explains it. History burden must not survive the native clustering comparator.

### NC-R3 true cumulative-load erosion
Recovery worsens with cumulative burden after current-shock controls. The design must recover added history value.

### NC-R4 adaptation/strengthening
Repeated perturbation improves recovery. The design must report adaptation/opposite direction, not force erosion.

### NC-R5 baseline migration only
The baseline moves but intrinsic recovery capacity does not weaken. Baseline-motion controls must prevent a false erosion label.

### NC-R6 direction asymmetry
History effect exists in only one sign or differs materially by sign. The interaction must be detected/reported.

### NC-R7 exogenous forcing confound
A common external event drives both repeated perturbation and slower-scale migration. With frozen \(\xi(t)\)-type control present, the design must avoid a false history-propagation interpretation.

### NC-R8 representation refusal
A scalar candidate is insufficient while a modal/vector representation is adequate. The pipeline must preserve scalar REFUSED rather than force \(\chi\).

### NC-R9 true cross-scale propagation
Faster-scale recovery-history information genuinely improves future slower-baseline prediction beyond slower persistence/native context.

### NC-R10 no cross-scale propagation
Within-scale history exists but adds nothing to the slower baseline. The design must keep Q040-W positive and Q040-H null without narrative rescue.

## 16. Scale invariance / transport discipline

The user's observation that similar patterns occur in futures, gold, small caps, and blue-chip equities is hypothesis-generating.

Q040 v0.1 does **not** test a universal scale-invariance law.

The later testable form is functional transport after native normalization:

> does a frozen recovery/baseline relation retain useful structure across new scales or instruments without retuning?

Existing scaling/invariance literature is a mandatory comparator.

Cross-instrument evidence must be untouched relative to the frozen Market development model.

## 17. Failure and outlier discipline

Preserve:
- episodes that recover immediately;
- episodes with repeated failure;
- adaptation/strengthening;
- sign-reversed cases;
- baseline migration without recovery loss;
- recovery loss without slower-scale migration;
- numerical/identification failures;
- sparse later-attempt strata;
- news/event-associated outliers;
- instrument/day regimes where the representation refuses.

The majority distribution must remain visible. Failure cases are investigated without allowing rare cases to replace the overall empirical picture.

## 18. Explicit nonclaims

Q040 v0.1 does not establish:
- a universal \(\chi\);
- that EMA or VWAP is \(\chi\);
- that MACD/L2 is automatically \(Χ\);
- that a discretionary trading read is \(Χ_{\mathrm{arc}}\);
- causal Stability Inheritance;
- market "fatigue" as a biological mechanism;
- universal scale invariance;
- fractality;
- cross-asset universality;
- event prediction;
- profitable trading;
- news predictability.

## 19. External APQ questions

Reviewers should specifically attack:

1. Is the residual novelty still colliding with empirical resiliency/hysteresis literature?
2. Can a representation-qualified baseline be defined without outcome circularity?
3. Is \(B_S^{Χ}\) a better first target than attempting \(\chi\) or \(Χ_{\mathrm{arc}}\)?
4. What baseline operator is least arbitrary while remaining causal and scale-local?
5. Can perturbation episodes be detected without post-outcome selection?
6. Are the recovery-vector components sufficient and nonredundant?
7. Is a survival/hazard framework preferable to nested regression for recovery time?
8. Does the native comparator adequately absorb shock clustering/order-flow memory?
9. How should scheduled and unscheduled exogenous events be handled?
10. Can cross-scale baseline migration be distinguished from ordinary trend/regime drift?
11. Are the NC-R1 through NC-R10 known truths sufficient?
12. What design would genuinely falsify the user's cross-scale functional-homology observation?
13. Which parts, if any, are ready to freeze versus still exploratory?

## 20. Current gate

No real Q040 data execution is authorized.

Next sequence:
1. external APQ attack of this plan;
2. adjudicate BLOCKER/MATERIAL objections;
3. freeze representation/baseline and event definitions;
4. build and pass synthetic known-truth qualification;
5. issue a real-data P0-D preregistration;
6. only then expose development outcomes.
