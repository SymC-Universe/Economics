# Q040 Repeated-Perturbation Recoverability Plan Packet v0.2

Date: 2026-09-29
Governance: SymC General Operations Manual v1.0
APQ level: APQ-2 SUBSTANTIAL
Stage: P0-D plan construction after P0-N/A0 theory and collision closure
Status: APQ CANDIDATE / NOT PREREGISTERED / NO REAL Q040 OUTCOME AUTHORIZED
Supersedes: Q040 Plan Packet v0.1
Prior-art foundation: \`qualification/Q040_PRIOR_ART_NOVELTY_FOUNDATION_v0.1_2026-09-28.md\`
Recovery-theory foundation: \`qualification/Q040_RECOVERY_THEORY_FOUNDATION_v0.1_2026-09-28.md\`
χ-collision foundation: \`qualification/Q040_CHI_COLLISION_FOUNDATION_v0.1_2026-09-29.md\`
Workflow: \`qualification/Q040_WORKFLOW_v0.1_2026-09-28.md\`
Relationship to Q039: SEPARATE SCIENTIFIC LANE / NO MUTUAL QUALIFICATION

## 1. Purpose

Q040 tests whether repeated perturbation changes **finite-time recoverability** in market microstructure, whether any such change survives strong native-state/history controls, and whether a supported faster-scale history signal adds information about later reorganization at the next slower scale.

The design explicitly separates four claim levels:

\[
R_0:
\text{finite-time recovery trajectories differ},
\]

\[
R_1:
\text{recovery is history-dependent under the frozen model class},
\]

\[
R_2:
\text{finite-shock recoverability changes},
\]

\[
R_3:
\text{Stability Architecture reorganizes}.
\]

A result at one level does not automatically promote the next.

Repeated slower recovery alone cannot establish a smaller basin, lower transition threshold, reduced resistance, or \(R_3\).

## 2. Core scientific questions

### Q040-R: representation qualification

At scale \(S\), which representation, if any, is scientifically admissible for recovery analysis?

Candidate objects are:

\[
Z_S(t),
\qquad
\chi_S^{*}(t),
\qquad
Χ_S(t),
\qquad
Χ_{\mathrm{arc},S}(t).
\]

Here:

- \(Z_S(t)\) is the native pre-interpretive market state;
- \(\chi_S^{*}(t)\) is a candidate scalar coordinate only;
- \(Χ_S(t)\) is a candidate/admitted modal-vector representation where independently qualified;
- \(Χ_{\mathrm{arc},S}(t)\) is a later architecture/conglomerate representation where independently qualified.

REFUSED and NOT_APPLICABLE are valid outcomes.

### Q040-W: within-scale history dependence

Conditional on current perturbation, current native state, baseline motion, clustering/self-excitation, activity, liquidity, volatility, direction, and identifiable exogenous forcing, does prior perturbation/recovery history add out-of-sample information about the current finite-time recovery trajectory?

### Q040-H: cross-scale propagation

If Q040-W is supported at a faster scale, do frozen faster-scale recovery-history variables add information about future slower-scale baseline migration/reorganization beyond the slower scale's own persistence, nested-window mechanics, and native context?

No causal transmission is inferred from predictive ordering alone.

## 3. Q039 isolation rule

Q040 does not assume that the 15 s / 30 s / 60 s / 300 s representations have already been qualified as \(Χ_S\).

Q039 is designed to test cross-scale semantic representation and remains independently gated.

Therefore Q040 v0.2 begins from native states \(Z_S(t)\), not from predeclared \(Χ_S(t)\), at every scale.

If Q039 later supplies independently qualified cross-scale representation evidence before the Q040 preregistration freeze, that evidence may be entered as external prior architecture only through an explicit Plan Delta. It may not silently alter Q040 definitions.

Q040 outcomes cannot qualify Q039.

## 4. Candidate wall-clock hierarchy

Initial scales remain:

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

This ladder is candidate structure inherited from prior Market work, not a universal law.

Longer scales are outside the first Q040 cycle.

Cross-instrument transport is outside the first Q040 cycle.

## 5. Native state \(Z_S(t)\)

The first-cycle recovery analysis starts from a native state rather than from an assumed SymC representation.

Candidate state ingredients include only prospectively defined market observables available by time \(t\), for example:

- L10 bid/ask depth coordinates;
- spread;
- microprice offset;
- event/trade intensity;
- trade volume and signed trade volume;
- order-flow imbalance;
- update fraction;
- staleness;
- realized volatility/native risk context.

The exact state vector for decisive execution must be frozen before real Q040 outcomes.

Any standardization is training-only and causal.

No feature is admitted because it is useful in discretionary trading.

## 6. Scalar \(\chi_S^{*}(t)\) qualification lane

The canonical physical coordinate remains:

\[
\chi
=
\frac{\gamma}{2|\omega|}.
\]

Market \(\chi\) is not created by analogy.

The existing production rule in \`market_chi/chi.py\` remains the canonical admission route for an AR2-like second-order factor:

- two finite poles;
- stable discrete poles;
- admissible continuous embedding;
- conjugacy/real-pole requirements;
- negative-real discrete-pole alias ambiguity refused;
- canonical underdamped/overdamped mapping only where licensed.

The existing Q038/Q039 production evidence currently REFUSES canonical scalar \(\chi\) for the tested MNQ windows.

Q040 v0.2 therefore treats scalar \(\chi\) as an independent qualification lane, not as the primary baseline.

EMA, VWAP, MACD, ATR, price displacement, L2 imbalance, or another market observable may not be renamed \(\chi\), \(\gamma\), or \(\omega\).

A generalized noncanonical scalar coordinate requires:
1. explicit derivation;
2. a new symbol until equivalence is proven;
3. native-comparator qualification;
4. a separate APQ decision.

## 7. Modal/vector \(Χ_S(t)\) qualification lane

Recovery theory shows that finite-time recovery can depend on perturbation direction and modal composition even when asymptotic return is unchanged.

A candidate \(Χ_S(t)\) may therefore be admitted only if a reduced modal/subspace representation preserves recovery-relevant structure relative to \(Z_S(t)\) without unacceptable information loss.

Candidate qualification comparisons include:

- full native vector \(Z_S\);
- predeclared semantic directions where independently supported;
- fixed-\(k\) subspace representation;
- scalar summaries;
- shuffled/permuted semantic controls;
- native low-rank alternatives.

Required refusal states include:

- \`MODAL_NOT_IDENTIFIABLE\`;
- \`MODAL_INFORMATION_LOSS\`;
- \`NATIVE_VECTOR_REQUIRED\`;
- \`SCALAR_SUFFICIENT_FOR_TASK\`;
- \`MODAL_EQUIVALENT_TO_NATIVE\`.

Q040 may proceed scientifically with \(Z_S\) even if \(Χ_S\) refuses.

## 8. Architecture \(Χ_{\mathrm{arc},S}(t)\) lane

\(Χ_{\mathrm{arc},S}(t)\) is **not** defined during the first within-scale recovery qualification.

It is deferred until:
1. native recovery is operational;
2. scalar/modal admission states are frozen;
3. Q040-W is closed or formally null;
4. an architecture construction can be specified using only information available by time \(t\);
5. added value can be tested against the strongest native/\(Χ\) alternatives.

Future rejection, rebound, continuation, collapse, or recovery is always an outcome:

\[
Y_S(t+\Delta),
\]

not part of the definition of \(Χ_{\mathrm{arc},S}(t)\).

This deferral is intentional anti-circularity.

## 9. Baseline object

The baseline is a scale-local causal state, not one fixed horizontal level.

For the native state:

\[
B_S^{Z}(t)
=
\mathcal{K}_S
\left[
Z_S(\tau<t)
\right].
\]

Only after a representation is admitted may one write:

\[
B_S^{\chi}(t),
\qquad
B_S^{Χ}(t),
\qquad
B_S^{Χ_{\mathrm{arc}}}(t).
\]

### 9.1 Candidate baseline operator families

Two operator classes enter APQ:

**K1. Causal trailing location**
- fixed scale-linked trailing window;
- coordinate-wise mean or robust location;
- no future samples;
- no outcome-dependent bandwidth.

**K2. Moving-attractor local-dynamics model**
- local regression/state-space form that estimates baseline motion and recovery jointly;
- inspired by non-stationary resilience formulations in which baseline \(\mu(t)\) and restoring rate are separate estimands;
- must be identifiable on synthetic known truths before real use.

The final preregistration must either:
- freeze one primary operator, or
- freeze an outcome-independent qualification rule that can return \`BASELINE_OPERATOR_REFUSED\`.

Real Q040 outcomes may not select the operator.

### 9.2 Baseline motion is not recovery

Track separately:

\[
\dot B_S^{Z}(t),
\]

or the discrete equivalent, and recovery relative to the pre-perturbation baseline:

\[
B_S^{Z}(t_0).
\]

Allowed distinctions include:
- recovery toward a stable baseline;
- incomplete recovery with stable baseline;
- baseline migration with unchanged local recovery law;
- recovery-law change with little baseline migration;
- coordinated multiscale baseline migration.

## 10. Perturbation definition

No chart-selected or outcome-selected event may enter decisive analysis.

For each scale, define the pre-perturbation residual:

\[
r_S(t)
=
Z_S(t)-B_S^{Z}(t).
\]

A candidate scale-normalized distance is:

\[
d_S(t)
=
\sqrt{
r_S(t)^\top
\Sigma_{S,\mathrm{train}}^{-1}
r_S(t)
},
\]

with regularization/conditioning rules frozen before use.

This is a candidate event-coordinate only. APQ may replace it with a better native metric before freeze.

The decisive preregistration must freeze:

- entry threshold;
- return-set threshold;
- sustain rule;
- timeout/censoring horizon;
- minimum event separation;
- overlap/merge rule;
- conditioning/refusal rule.

Threshold selection may use synthetic known truths and outcome-blind input-distribution adequacy rules only. It may not optimize recovery-history results.

## 11. Perturbation direction

Vector perturbations do not have a universal scalar sign.

Preserve:

\[
u_{S,j}
=
\frac{r_S(t_j)}
{\|r_S(t_j)\|}
\]

as a perturbation-direction object where defined.

Separately record market-direction label from a prospectively frozen price displacement measure:

\[
s_j
\in
\{-1,+1\}.
\]

The sign interaction is descriptive/secondary unless independently elevated before freeze.

"Up" and "down" are therefore tested without pretending the entire vector perturbation is one-dimensional.

## 12. Recovery object

The first-cycle primary scientific object is the finite-time trajectory back toward a predeclared return set.

Candidate vector:

\[
R_{S,j}
=
\left(
T_{\mathrm{return}},
T_{\mathrm{sustain}},
P_{\mathrm{return}}(T),
A_{\mathrm{transient}},
I_{\mathrm{loss}},
D_{\mathrm{dwell}},
E_H
\right).
\]

Where:

- \(T_{\mathrm{return}}\): time to first return;
- \(T_{\mathrm{sustain}}\): time to sustained return;
- \(P_{\mathrm{return}}(T)\): finite-time return probability;
- \(A_{\mathrm{transient}}\): maximum transient amplification relative to entry displacement;
- \(I_{\mathrm{loss}}\): integrated normalized displacement/recovery burden;
- \(D_{\mathrm{dwell}}\): recovered-side dwell after return;
- \(E_H\): residual displacement at a frozen horizon.

Exact primary/secondary ordering remains an APQ target.

A survival/hazard formulation is preferred for return time because censoring is intrinsic, but this is not frozen until external APQ.

## 13. Resistance is separate from recovery

Q040 must not infer "resistance" merely from fast recovery.

If a valid shock/input magnitude \(Q_j\) can be defined prospectively, a response-per-input resistance-like quantity may be tested.

If no defensible input magnitude exists for endogenous market perturbations, return:

\`RESISTANCE_NOT_IDENTIFIED_FROM_OBSERVATIONAL_EVENT\`.

No basin-size or global-resistance claim is allowed from return time alone.

## 14. Independence time and incomplete recovery

Repeated perturbations arriving before recovery is dynamically independent are a primary competing explanation.

Let:

\[
\beta_S(T)
=
P(\text{return to declared set within }T).
\]

A training-only empirical/synthetic analogue of independence time is:

\[
T_{\mathrm{ind},S}(\epsilon,\delta),
\]

the time at which finite-time return behavior is sufficiently close to its longer-horizon value under the frozen return definition.

For each event, record:

\[
I_{j}^{\mathrm{preind}}
=
\mathbf{1}
\left[
\Delta t_j<T_{\mathrm{ind},S}
\right].
\]

Q040 must distinguish:
- genuine history-dependent change in recovery law;
- a new shock arriving before ordinary recovery was complete.

## 15. History/burden variables

Do not assume attempt number is the mechanism.

Candidate frozen history variables are:

\[
N_j=j-1
\]

prior event count;

\[
L_j
=
\sum_{k<j} A_k
\]

cumulative perturbation amplitude/load;

\[
U_j
=
\sum_{k<j} T_{\mathrm{away},k}
\]

cumulative time outside the return set;

\[
F_j
\]

incomplete-recovery burden constructed only from prior frozen recovery outcomes;

\[
C_j
\]

native clustering/self-excitation burden;

and, if required by APQ,

\[
M_j
\]

a distributed-lag/history-kernel summary that does not presuppose "damage."

The researcher's historical "3-5 attempts" observation remains descriptive only.

## 16. Native comparator stack

The strongest current-state/history comparator must be available before a history effect earns admission.

Minimum candidate covariate families:

- current perturbation amplitude and duration;
- perturbation direction;
- inter-perturbation interval;
- prior incomplete-recovery indicator;
- session phase;
- spread and depth;
- native L10 imbalance;
- event/trade intensity;
- trade volume and signed trade volume;
- order-flow imbalance;
- realized volatility;
- update fraction and staleness;
- baseline position and velocity;
- distance/alignment to next-slower baseline;
- recent event/self-excitation intensity;
- scheduled exogenous-event indicator where available.

A Hawkes-like or equivalent native event-history comparator must challenge the possibility that apparent recovery erosion is merely clustered endogenous order flow.

## 17. Candidate within-scale estimator

The exact estimator remains subject to APQ, but the preferred v0.2 structure is:

### M0: native current-state model
Current perturbation + current native state + baseline motion + session/activity/liquidity/volatility + clustering + exogenous-event controls.

### M1: ordinal-history extension
M0 + \(N_j\).

### M2: cumulative-burden extension
M0 + \(L_j+U_j\).

### M3: incomplete-recovery extension
M0 + \(F_j+I_j^{\mathrm{preind}}\).

### M4: memory/history-kernel extension
M0 + frozen distributed-lag/history representation \(M_j\), only if independently justified.

History is supported only when an extension improves frozen out-of-sample scoring beyond M0.

Coefficient sign alone is insufficient.

Candidate scoring for recovery-time models:
- out-of-sample survival log loss / partial likelihood as appropriate;
- integrated Brier score;
- calibration;
- finite-time return discrimination.

Candidate scoring for continuous secondary outcomes:
- MAE / squared error;
- calibration where probabilistic.

## 18. Allowed within-scale dispositions

At each scale:

- \`HISTORY_ADDS_EROSION_DIRECTION_P0D\`;
- \`HISTORY_ADDS_ADAPTATION_DIRECTION_P0D\`;
- \`HISTORY_ADDS_MIXED_OR_DIRECTION_DEPENDENT_P0D\`;
- \`NATIVE_CURRENT_STATE_SUFFICIENT_P0D\`;
- \`INCOMPLETE_RECOVERY_EXPLAINS_APPARENT_HISTORY_P0D\`;
- \`CLUSTERING_EXPLAINS_APPARENT_HISTORY_P0D\`;
- \`BASELINE_MIGRATION_EXPLAINS_APPARENT_HISTORY_P0D\`;
- \`EXOGENOUS_EVENT_CONFOUNDED_P0D\`;
- \`RECOVERY_NOT_IDENTIFIABLE\`;
- \`INSUFFICIENT_REPEATED_EVENTS\`.

No "fatigue" label is used in the statistical result object.

## 19. Cross-scale target

Q040-H is tested only after a faster-scale Q040-W result is frozen.

For adjacent scales \(S<S'\), candidate slower-scale outcome is a representation-appropriate baseline migration/reorganization measure:

\[
\Delta B_{S'}(t,t+\Delta).
\]

The predictor block contains only information available at or before \(t\).

The native slower-scale comparator must include:

- \(B_{S'}(t)\);
- lagged slower baseline motion;
- slower native state/context;
- current faster-scale state;
- session/activity/volatility controls;
- nested-window mechanical-overlap controls.

Only then are frozen faster-scale history variables added.

## 20. Mechanical-overlap firewall for cross-scale claims

Because wall-clock scales are nested, a fast perturbation can mechanically enter the slower aggregation.

Q040-H must therefore include at least one of:

- a non-overlapping future target window;
- leave-child-out slower-baseline sensitivity;
- synthetic null preserving nested aggregation but removing true propagation;
- equivalent outcome-independent control.

If a cross-scale signal disappears under the mechanical-overlap control, classify:

\`NESTED_AGGREGATION_EXPLAINS_CROSS_SCALE_SIGNAL\`.

## 21. Exogenous forcing \(\xi(t)\)

Identifiable scheduled releases and timestamped material events are not called noise.

At minimum, event metadata must be retained as:

\[
\xi(t).
\]

The external APQ must decide among:
- primary inclusion with event indicator;
- stratified event/non-event analysis;
- prospectively excluded narrow windows plus reported event-window sensitivity.

The rule must be frozen before real Q040 outcomes.

Unscheduled/unobserved news remains an explicit residual confound.

## 22. Dependence and uncertainty

Perturbations within one episode are dependent.

Episodes within a day may be dependent.

The final preregistration must freeze:

- episode identity;
- clustering unit;
- day weighting;
- episode weighting;
- survival censoring;
- hierarchical/block bootstrap or equivalent;
- minimum independent days;
- minimum events per history stratum;
- sparse-tail refusal rules.

No large attempt-number effect may be interpreted from a tiny surviving tail.

## 23. Synthetic known truths required before real execution

The implementation must discriminate at least the following.

### NC-R1 memoryless recovery
Current state fully determines recovery. History must not add.

### NC-R2 clustered shocks without recovery-law change
Short spacing/self-excitation produces apparent slower recovery. Native clustering controls must absorb it.

### NC-R3 true cumulative-load degradation
Recovery worsens with prior load after current-state controls. History must add in the erosion direction.

### NC-R4 adaptation/strengthening
Repeated perturbation improves recovery. The design must return adaptation, not force erosion.

### NC-R5 moving baseline only
The baseline migrates while intrinsic return law remains unchanged. The design must not label recovery-law erosion.

### NC-R6 direction asymmetry
History effect differs by market-direction sign. The interaction must remain visible.

### NC-R7 exogenous common cause
A common forcing drives repeated perturbations and later slower-scale movement. With observed \(\xi(t)\), the design must avoid a false propagation claim.

### NC-R8 scalar refusal / vector adequacy
A scalar reduction is insufficient while the native/modal vector is adequate. Scalar \(\chi\) must remain REFUSED.

### NC-R9 true cross-scale propagation
Faster-scale history genuinely improves future slower-baseline prediction beyond slower persistence/native context.

### NC-R10 no cross-scale propagation
Within-scale history exists, but no slower-scale added information exists. Q040-W may pass while Q040-H remains null.

### NC-R11 slower recovery with greater transition resistance
Memory slows local return while increasing the perturbation threshold for regime change. The design must not equate slower recovery with reduced resistance.

### NC-R12 transient amplification with stable asymptotic recovery
A non-normal stable system initially amplifies displacement before returning. The design must record reactivity/transient amplification without falsely classifying instability.

### NC-R13 pre-independence repeated shocks
Identical memoryless recovery laws receive new shocks before \(T_{\mathrm{ind}}\). The design must attribute apparent cumulative degradation to incomplete recovery when appropriate.

### NC-R14 nested-aggregation false propagation
Fast events mechanically influence the next slower aggregation, but no true cross-scale state law exists. Mechanical-overlap controls must refuse propagation.

### NC-R15 changing-noise false slowing
Noise amplitude/color changes create rising variance/autocorrelation without a change in the restoring law. The design must not label a recovery-law transition from those indicators alone.

## 24. Shared-reference extension

EMA, VWAP, MACD, price behavior around trader-visible levels, tape, and L2 remain scientifically interesting because they may represent shared-reference and relational market structure.

They are **not** part of the first native Q040 baseline definition.

After the native recovery model is frozen, a separate extension may test:

- whether trader-visible references improve scalar/reference representation;
- whether response around them adds to \(Χ\);
- whether shared-reference behavior transports across scales/instruments;
- whether matched nearby placebo references perform equivalently.

This extension cannot redefine the native baseline after seeing Q040-W outcomes.

## 25. Scale-invariance discipline

Q040 v0.2 does not test or claim universal scale invariance.

The later transport hypothesis is:

> after native normalization and without retuning, does a frozen recovery/representation relation retain functional organization at new scales or instruments?

A repeated visual pattern is hypothesis-generating only.

Failure to transport is a valid result.

## 26. Failure and outlier discipline

Preserve and report:

- immediate recoveries;
- repeated failures;
- adaptation/strengthening;
- sign-reversed cases;
- baseline migration without recovery-law change;
- recovery-law change without slower-scale migration;
- transient amplification;
- scalar refusal;
- modal refusal;
- numerical/conditioning failure;
- sparse repeated-event strata;
- event/news-associated episodes;
- extreme outliers;
- majority distribution.

Outliers are investigated for root cause but do not replace the majority behavior.

## 27. Explicit nonclaims

Q040 v0.2 does not establish:

- a universal \(\chi\);
- that EMA or VWAP is \(\chi\);
- that MACD/L2 is automatically \(Χ\);
- that discretionary trading interpretation is \(Χ_{\mathrm{arc}}\);
- reduced basin size from slower recovery alone;
- lower transition threshold from slower recovery alone;
- causal Stability Inheritance;
- universal market fatigue;
- universal scale invariance;
- fractality;
- cross-asset universality;
- event prediction;
- profitable trading;
- news predictability.

## 28. External APQ questions

Reviewers must attack:

1. Is the native-start \(Z_S\) approach sufficient to isolate Q040 from Q039?
2. Is the scalar \(\chi\) admission rule appropriately strict?
3. Does \(Χ_S\) require a stronger independent representation gate before recovery analysis?
4. Is deferring \(Χ_{\mathrm{arc}}\) until after Q040-W the correct anti-circular choice?
5. Which baseline operator, K1 or K2, is least arbitrary and most identifiable?
6. Is train-whitened Mahalanobis displacement a defensible perturbation coordinate?
7. How should entry/return/sustain thresholds be frozen without outcome tuning?
8. Is survival/hazard analysis the correct primary estimator?
9. Can independence time be estimated without circularity in observational market data?
10. Does the native comparator adequately absorb order-flow clustering and state dependence?
11. How should \(\xi(t)\) be handled in the first real development test?
12. Is the cross-scale mechanical-overlap firewall sufficient?
13. Are NC-R1 through NC-R15 adequate known truths?
14. What additional null can distinguish a moving landscape from a changing local recovery law?
15. Which claim level \(R_0\)-\(R_3\) is realistically reachable from observational market data?
16. Could a strong native market-state/history model make \(\chi\), \(Χ\), and \(Χ_{\mathrm{arc}}\) scientifically unnecessary?

## 29. Plan status

Q040 v0.2 is an APQ candidate, not a preregistration.

No real Q040 outcome may be opened.

The next gate is isolated external APQ review bound to the exact v0.2 commit. BLOCKER and MATERIAL objections must be adjudicated by evidence/discriminating tests, not vote.

After APQ:
1. issue Plan Delta if required;
2. freeze synthetic known-truth definitions/seeds;
3. implement synthetic qualification through the guarded conveyor;
4. only after a pass/refusal-consistent qualification, construct the P0-D preregistration;
5. freeze data identity, thresholds, estimators, implementation hashes, and outcome labels;
6. only then expose real MNQ development outcomes.
