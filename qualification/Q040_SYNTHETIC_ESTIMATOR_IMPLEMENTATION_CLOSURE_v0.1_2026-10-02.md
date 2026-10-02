# Q040 Synthetic Estimator Implementation Closure v0.1
**Date:** 2026-10-02  
**Authority:** Q040 Recoverability Plan Packet v0.6; Q040 Synthetic Estimator-Qualification Specification Freeze v0.1; Q040 Repaired Synthetic Lineage v0.2  
**Stage:** synthetic-only estimator qualification  
**Real Q040 outcomes:** SEALED  
**Purpose:** close implementation degrees of freedom left intentionally open by the higher-level estimator specification before any estimator-selection outcome is generated.

## 1. Seed banks and anti-overfitting firewall

Three disjoint deterministic banks are frozen.

### Selection bank S
Used only for K1/K2, D1/D2, event-definition, and horizon selection.

- 14 replicas per control × scale;
- replica \(r=0,\ldots,13\);
- seed for a single-condition control:
\[
\mathrm{SeedSequence}([20261002,\mathrm{ordinal},S,100+r,0]).
\]
- for a frozen multi-cell control such as NC-R20, append the zero-based frozen cell ordinal in the final position:
\[
\mathrm{SeedSequence}([20261002,\mathrm{ordinal},S,100+r,c]).
\]

This cell-ordinal extension was documented before any baseline candidate score value was opened; only shard completion/status had been observed.

### Confirmatory history bank C
Used only after baseline, metric, event, return, and horizon definitions are frozen.

- 30 replicas per control × scale;
- replica \(r=0,\ldots,29\);
- seed:
\[
\mathrm{SeedSequence}([20261002,\mathrm{ordinal},S,200+r]).
\]

### Event-history calibration bank H
Used only for the native self-excitation comparator.

- 200 replicas per frozen calibration cell;
- seed namespace beginning with 300.

No realization may cross banks.

## 2. Baseline candidates K1/K2

Candidate windows remain \(W\in\{10,20,40\}\) samples.

Carried-forward duplicates do not count as independent effective observations. Baseline fitting uses only samples whose frozen update mask is true.

### K1
At time \(t\), use valid updates in \([t-W,t)\).

Coordinate location is the median.

K1 refuses at \(t\) if fewer than 5 distinct valid updates are available.

### K2
At time \(t\), use valid updates in \([t-W,t)\) and fit each coordinate to:

\[
z_k(\tau)=a_k+b_k(\tau-t).
\]

The baseline estimate is \(a_k\) and baseline velocity is \(b_k\).

K2 refuses at \(t\) if:
- fewer than 10 distinct valid updates are available;
- the intercept/slope design is rank deficient.

### Baseline error

For synthetic scoring only:

\[
e_B(t)=
\frac{1}{\sqrt 8}
\left\|
D_{\sigma_0}^{-1}
\left(
\hat B(t)-B_{\mathrm{true}}(t)
\right)
\right\|_2.
\]

A baseline candidate must produce valid estimates for at least 90% of eligible test samples in every required baseline/noise qualification cell.

Within K1 and K2 separately, after all required false-disposition controls are passed, select the window with the lowest median \(e_B\) across the complete selection bank. Exact ties choose the shorter window.

Between surviving classes choose the lower median error; exact ties choose K1.

No baseline candidate is finally admitted until the full downstream false-history controls also pass.

## 3. Conditional scale and D1

For each fold, compute training residuals:

\[
r_t=Z_{\mathrm{observed}}(t)-\hat B(t)
\]

on baseline-valid training samples.

Coordinate scale is:

\[
s_k=1.4826\,\mathrm{MAD}(r_{t,k}),
\]

with frozen floor \(10^{-8}\).

D1 is:

\[
d_1(t)=
\sqrt{\sum_k(r_{t,k}/s_k)^2}.
\]

Training-only scale is frozen through each test fold.

## 4. D2 linear shrinkage covariance

D2 uses training residuals centered by their training mean.

Let empirical covariance be:

\[
S=\frac1n X^\top X.
\]

Let:

\[
\mu=\frac{\mathrm{tr}(S)}{p},
\qquad
F=\mu I.
\]

Define:

\[
\delta=
\frac{1}{p}\|S-F\|_F^2,
\]

and:

\[
\beta_{\mathrm{raw}}
=
\frac{1}{pn^2}
\sum_{i=1}^{n}
\left\|
x_i x_i^\top-S
\right\|_F^2.
\]

Then:

\[
\beta=\min(\beta_{\mathrm{raw}},\delta),
\qquad
\lambda=
\begin{cases}
0,&\delta=0\\
\beta/\delta,&\delta>0,
\end{cases}
\]

and:

\[
\Sigma_{\mathrm{LW}}
=
(1-\lambda)S+\lambda F.
\]

The pre-shrink empirical effective rank is the participation ratio:

\[
r_{\mathrm{eff}}
=
\frac{\mathrm{tr}(S)^2}
{\mathrm{tr}(S^2)}.
\]

D2 refuses if:
- \(r_{\mathrm{eff}}<0.5p\);
- any covariance entry is non-finite;
- post-shrink condition number exceeds \(10^6\);
- inversion fails.

D2 distance is:

\[
d_2(t)=
\sqrt{r_t^\top\Sigma_{\mathrm{LW}}^{-1}r_t}.
\]

This is a prospectively frozen linear-shrinkage implementation in the Ledoit–Wolf family; no real outcome selects shrinkage.

## 5. Candidate event definitions

Entry quantiles remain:

\[
q_E\in\{0.95,0.975,0.99\}.
\]

Return quantiles remain:

\[
q_R\in\{0.50,0.60,0.70\}.
\]

Sustain durations remain:

\[
K\in\{2,3,5\}
\]

samples.

Minimum entry separations remain:

\[
M\in\{2,5,10\}
\]

samples.

Thresholds are computed from training-fold candidate distance only.

An estimated entry requires:
- current distance at or above the entry threshold;
- immediately previous **valid** distance below entry threshold;
- minimum separation from the previous estimated entry.

A high first sample after an invalid gap is not called an entry because an upcrossing cannot be established.

While an episode is active, a new qualifying entry after the minimum separation is an interruption, not a merge.

Sustained return is the first \(K\)-sample valid run at or below the return threshold.

### 5.1 Selection-control families and fold boundaries

Baseline ranking uses only the controls whose scientific purpose directly challenges baseline/noise/measurement separation:
- NC-R5;
- NC-R15;
- NC-R16;
- NC-R20.

For NC-R20, every one of the 24 frozen measurement cells is included in every declared selection replica at every scale.

Metric/event ranking uses:
- NC-R1 through NC-R7 except NC-R8;
- NC-R9 through NC-R13;
- NC-R15 through NC-R20.

NC-R8 is scalar/modal qualification, NC-R14 is cross-scale mechanical-overlap qualification, and NC-R21 is sparse-support refusal; they do not rank event thresholds but remain mandatory downstream controls.

For each frozen test fold, the metric and thresholds are trained only on samples before the fold start.

The event detector is reset at the fold boundary. It may inspect the immediately preceding valid distance sample only to establish whether the first in-fold sample is an upcrossing. No active episode is carried from training into test.

Entry localization scores true events whose injected entry lies inside the test fold.

Sustained-return timing scores only true entries with enough remaining in-fold support to evaluate the selected horizon; boundary-truncated episodes are right-censored for scoring rather than treated as misses.

## 6. Synthetic truth matching and event adequacy

For scoring only, partition time by successive true injected events.

For true event \(j\), the earliest estimated entry in:

\[
[t_j,t_{j+1})
\]

is its match.

If none exists, the event is missed.

Normalized entry timing error is:

\[
e_{E,j}
=
\begin{cases}
(\hat t_j-t_j)/(t_{j+1}-t_j),&\text{matched}\\
1,&\text{missed}.
\end{cases}
\]

For the final true event, denominator is the remaining world length, capped below by 1.

Extra estimated entries in the same true-event interval after the matched entry are false entries.

A candidate event definition must satisfy on the selection bank:
- median true-event recall at least 0.80;
- no required control × scale cell with median recall below 0.60;
- median false-entry/true-entry ratio at most 0.25;
- no required cell with ratio above 0.75.

Failure refuses that event tuple; thresholds are not relaxed.

## 7. Sustained-return timing adequacy

For true episodes that achieve sustained return, compare estimated and true sustained-return times only when the true entry was matched.

Normalize absolute timing error by the smaller of:
- the true inter-event interval;
- 80 samples,

with floor 1.

A missed sustained return receives error 1.

For true interrupted episodes, an estimated sustained return after the true interruption counts as terminal-state misclassification.

A candidate tuple must achieve median terminal-state concordance at least 0.75 across the selection bank.

Among candidates surviving all refusal/false-positive gates, select lexicographically by:
1. median normalized entry-timing error;
2. median normalized sustained-return timing error;
3. false-entry ratio.

Existing tie-breaks from the estimator specification then apply:
- less extreme entry threshold;
- shorter sustain duration;
- longer minimum separation.

Metric exact ties prefer D1 over D2.

## 8. Horizon selection

Candidate horizons remain:

\[
H\in\{20,40,80\}
\]

samples.

Use the already-frozen saturation rule:
select the shortest horizon for which cumulative sustained-return incidence changes by <0.02 when extended to the next candidate horizon in every required stable-recovery known-truth family while retaining at least 90% of recoveries observed by 80 samples.

If none qualifies, use 80 and append:

\`HORIZON_SATURATION_NOT_ESTABLISHED\`.

## 9. Sparse-support rule

Primary history-support strata are the training-bank tertiles of the observed cumulative-amplitude history variable \(L_j\).

A scale returns:

\`INSUFFICIENT_REPEATED_EVENTS\`

if any required stratum contains fewer than 10 qualifying estimated episodes in the declared synthetic evaluation unit.

NC-R21 must trigger this refusal.

## 10. Synthetic M0 feature vector

All M0 features are available at estimated episode entry.

Fixed feature blocks:

1. baseline-relative native residual vector: 8;
2. estimated baseline location vector: 8;
3. estimated perturbation unit-direction vector: 8;
4. candidate event amplitude: 1;
5. baseline-velocity norm: 1;
6. baseline-velocity projection on perturbation direction: 1;
7. log1p previous estimated inter-event interval: 1;
8. session phase: 4;
9. current update indicator: 1;
10. log1p current staleness: 1;
11. observed exogenous forcing: 1;
12. observed regime proxy: 1;
13. observed apparent-history proxy: 1;
14. current noise-scale proxy: 1;
15. causal past-event-intensity proxy: 1;
16. causal trailing 20-sample realized native-difference RMS: 1;
17. observed directional sign, defined prospectively as the sign of baseline-relative coordinate 4: 1;
18. prior incomplete-episode indicator: 1.

Training-zero-variance columns are removed deterministically and logged. No outcome-dependent feature selection is allowed.

NC-R17b's withheld native covariate is never supplied to M0.

## 11. M2 history extension

M2 is M0 plus observed, not truth-derived:

\[
L_j^{\mathrm{obs}}
\]

cumulative prior estimated event amplitude and:

\[
U_j^{\mathrm{obs}}
\]

cumulative prior estimated time outside the frozen return set.

Truth burdens exist only for synthetic scoring.

## 12. Discrete-time competing-risk model

The primary estimator is an unpenalized multinomial logistic discrete-time hazard model.

Per at-risk episode-time row, categories are:
- 0: no terminal event this sample;
- 1: sustained return;
- 2: interruption by new perturbation.

Category 0 is reference.

Baseline hazard uses eight equal-width piecewise-constant time bins over \(1,\ldots,H\). Seven dummy columns are included with the first bin reference.

Covariates are fixed at episode entry except the frozen time-bin basis.

All continuous columns are standardized from training data only.

Fit by Newton–Raphson maximum likelihood with:
- maximum 100 iterations;
- gradient max-norm convergence tolerance \(10^{-8}\);
- step halving until log likelihood is non-decreasing;
- no penalty.

Refuse a fold if:
- design rank is deficient after deterministic zero-variance removal;
- Hessian condition number exceeds \(10^{10}\);
- a finite improving Newton step cannot be found;
- convergence is not reached.

## 13. Grouped confirmatory cross-validation

History qualification uses the 30-replica confirmation bank only.

Five grouped folds are frozen by:

\[
\mathrm{fold}=r\bmod5.
\]

Each fold trains on 24 whole replicas and tests on 6 whole replicas.

No episode from one replica can enter both training and test data in the same fold.

## 14. Sustained-return cumulative incidence

For each test episode, the multinomial hazards produce:

\[
h_R(k),\quad h_I(k).
\]

Survival is:

\[
S(k)
=
\prod_{m=1}^{k}
[1-h_R(m)-h_I(m)].
\]

Sustained-return CIF is:

\[
F_R(k)
=
\sum_{m=1}^{k}
S(m-1)h_R(m).
\]

If numerical prediction yields invalid probabilities, the fold is refused.

## 15. Training-only censoring weights and integrated Brier score

Right censoring is distinct from interruption.

Estimate censoring survival \(\hat G(k)\) on training episodes only using Kaplan–Meier, with sustained return and interruption treated as observed non-censoring terminal events.

If \(\hat G(k)<0.05\) anywhere on the scoring grid, return:

\`CENSORING_WEIGHT_NOT_QUALIFIED\`

rather than clipping.

Score the sustained-return CIF at every integer \(k=1,\ldots,H\) using IPCW.

Competing interruption is an observed \(Y_R(k)=0\) outcome, not censoring.

The primary integrated Brier score is the equal-weight mean over the \(H\) time points.

This follows the standard IPCW Brier-score construction; the censoring model never uses test outcomes.

## 16. M2 promotion statistic

For each confirmatory replica compute:

\[
\Delta \mathrm{IBS}
=
\mathrm{IBS}_{M0}
-
\mathrm{IBS}_{M2}.
\]

Positive favors M2.

At each scale use a 10,000-replicate paired bootstrap across the 30 independent replicas.

A positive history-adds result requires:
- point \(\Delta\mathrm{IBS}>0\);
- ordinary two-sided 95% paired-bootstrap interval excludes zero positively;
- at least 20/30 replica-level differences are positive;
- the scale-level Holm-adjusted p-value is <0.05 across the four frozen scales.

A secondary metric cannot rescue failed primary IBS.

## 17. Direction classification

Erosion/adaptation direction is not assigned from coefficient sign alone.

For held-out predictions, split episodes by the training-defined median of observed cumulative burden.

Compare calibrated sustained-return CIF at the selected horizon:
- lower high-burden CIF with supported M2 -> erosion direction;
- higher high-burden CIF with supported M2 -> adaptation direction;
- sign inconsistency across perturbation direction -> mixed/direction-dependent.

For NC-R6 only, a predeclared secondary interaction diagnostic adds:
- \(L_j^{\mathrm{obs}}\times s_j\);
- \(U_j^{\mathrm{obs}}\times s_j\).

It must preserve opposite directional history effects. It cannot serve as an alternate primary success route if M2 fails.

## 18. Omitted-covariate diagnostic for NC-R17b

NC-R17b includes a synthetic-only oracle diagnostic.

After ordinary M0/M2 scoring, fit:

\[
M0_{\mathrm{oracle}}
=
M0
+
z_{\mathrm{withheld}}
\]

using the same folds.

If the oracle improves IBS over M0 with a positive paired 95% interval, mark:

\`M0_MISSPECIFICATION_EXPOSED\`.

Any apparent M2 improvement in NC-R17b is then prohibited from receiving an unconditional \`HISTORY_ADDS_*\` disposition.

The oracle variable never enters ordinary M0 or real Q040.

## 19. Native event-history comparator

Q040 uses an equivalent discrete-time self-exciting event-history model rather than requiring a continuous-time Hawkes implementation.

Three calibration cells are frozen:

### H0 background-only
Session-modulated Bernoulli/Poisson event intensity with no self-excitation.

### H1 exponential self-excitation
Same background plus one causal exponential event-history kernel.

### H2 queue-reactive self-excitation
H1 plus one observed native queue/regime proxy affecting background intensity.

Three fitted configurations mirror H0/H1/H2.

History kernel decay is frozen to the generator value within each correctly specified calibration cell; this calibration stage tests the comparator structure, not decay-parameter search.

Use 200 deterministic replicas per cell.

Fit on the first half of each replica and evaluate the second half.

Required diagnostics:
- absolute relative event-rate error <=0.20;
- held-out time-rescaling KS statistic <= \(1.36/\sqrt{n_{\mathrm{test\ events}}}\);
- self-excitation coefficient relative error <=0.25 where nonzero and identifiable;
- background-intensity normalized RMSE <=0.20;
- no false M2/history-adds disposition in the corresponding null family.

A configuration is admitted only if at least 95% of its 200 correctly specified replicas pass every applicable diagnostic.

Among admitted configurations, choose lowest median standardized aggregate diagnostic error; exact ties choose lower dimensionality.

If none qualifies:

\`HAWKES_DIAGNOSTIC_REFUSED\`

and no claim may depend on Hawkes adjustment.

## 20. Predeclared candidate ordering and fallback

Before any selection-bank result is opened, every full candidate pipeline is assigned a deterministic rank.

Primary ordering key:

1. baseline candidate median normalized baseline error;
2. event-entry normalized timing error;
3. sustained-return normalized timing error;
4. false-entry ratio.

Exact ties resolve in this order:
- K1 before K2;
- shorter baseline window;
- D1 before D2;
- less extreme entry threshold;
- shorter sustain duration;
- longer minimum separation.

The selection bank produces this ordered candidate list only.

The confirmatory known-truth stage evaluates candidates **in that frozen order**. The first candidate that passes all required known-truth/refusal gates is admitted. A later candidate is not inspected for promotion unless every earlier candidate has a documented refusal.

No candidate may be chosen because it produces a larger history effect.

## 21. Qualification ordering

Execution order is frozen:

1. baseline/metric/event/horizon selection on bank S;
2. freeze selected measurement/recovery pipeline;
3. event-history comparator qualification on bank H;
4. M0/M2 confirmatory qualification on bank C;
5. known-truth disposition audit across NC-R1 through NC-R21;
6. only after complete pass/refusal-acceptable closeout may Stage Q040-3 preregistration construction begin.

No real Q040 outcome is opened at any stage above.

## 22. References for implementation family

- Ledoit O, Wolf M. *A well-conditioned estimator for large-dimensional covariance matrices.* Journal of Multivariate Analysis 88 (2004) 365–411. DOI: 10.1016/S0047-259X(03)00096-4.
- Discrete-time competing-risk hazards are implemented as a multinomial logistic hazard with the no-event state as reference.
- IPCW integrated Brier scoring uses training-only censoring survival.

## 23. Current status

\`Q040_ESTIMATOR_IMPLEMENTATION_CLOSURE=v0.1_FROZEN\`

\`Q040_REAL_OUTCOMES=SEALED\`

\`NEXT=IMPLEMENT_SELECTION_BANK_PIPELINE\`
