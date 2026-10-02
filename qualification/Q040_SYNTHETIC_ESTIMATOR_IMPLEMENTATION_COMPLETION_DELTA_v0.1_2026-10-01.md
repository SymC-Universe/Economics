# Q040 Synthetic Estimator Implementation Completion Delta v0.1
**Date:** 2026-10-01  
**Authority:** Q040 Recoverability Plan Packet v0.6 + Q040 Synthetic Estimator-Qualification Specification Freeze v0.1 + qualified Synthetic Observation/Episode Contract v0.1  
**Real Q040 outcomes:** SEALED  
**Purpose:** close implementation-level degrees left open by the estimator specification before candidate evaluation.

## 1. No-retuning rule

Everything below is frozen before running estimator-selection outcomes.

If the resulting pipeline fails a mandatory known truth, preserve the failure. Do not alter grids, thresholds, penalties, link functions, effect sizes, or generator truths to rescue the candidate.

## 2. Candidate baseline operators

Treat each class × horizon as a separate candidate:

- K1-10, K1-20, K1-40;
- K2-10, K2-20, K2-40.

Horizon is measured in samples, equivalent to \(\{10S,20S,40S\}\).

At time \(t\), baseline estimation uses only samples \(\tau<t\).

### K1
Coordinate-wise median of the prior horizon.

Require at least 5 finite past observations; otherwise the baseline is unavailable at that sample.

### K2
Per-coordinate ordinary least-squares local linear fit over the prior horizon, evaluated one step forward at \(t\).

Require at least 10 finite past observations and full rank of the two-column intercept/time design; otherwise unavailable.

### Baseline ranking
For each candidate compute generator-truth normalized baseline-location error:

\[
E_B
=
\operatorname{median}
\sqrt{
(\hat B_t-B_t)^\top
\Sigma_0^{-1}
(\hat B_t-B_t)
}
\]

over all available samples in the required baseline-challenge controls:
NC-R5, NC-R15, NC-R16, and all NC-R20 cells, at all four scales.

Rank candidates by median \(E_B\) across cells. Exact ties choose:
1. K1 over K2;
2. shorter horizon within the same class.

This is a **pre-ranking only**. Final admission still requires the complete chosen recovery pipeline not to manufacture a recovery-law/history disposition on the required null/control family. If the top-ranked baseline later fails a mandatory full-pipeline known truth, remove it and advance to the next pre-ranked baseline without changing any rule.

## 3. D1 implementation

Given the selected candidate baseline and one frozen out-of-sample fold:

- compute training residuals \(R_t=Z_t-\hat B_t\);
- coordinate center is the training residual median;
- coordinate scale is \(1.4826\times\mathrm{MAD}\);
- scale floor is \(10^{-8}\);
- test-fold scale is frozen from training.

Distance is robust standardized Euclidean distance.

## 4. D2 implementation

Training residuals are centered by their training mean.

Let biased sample covariance be:

\[
S=\frac1n X^\top X.
\]

Let:

\[
\mu=\frac{\mathrm{tr}(S)}{p},
\qquad
T=\mu I.
\]

Freeze the linear shrinkage estimate:

\[
\hat\beta
=
\frac{1}{n^2}
\sum_{i=1}^n
\left\|
x_i x_i^\top-S
\right\|_F^2,
\]

\[
\hat\delta
=
\|S-T\|_F^2,
\]

\[
\lambda
=
\begin{cases}
1,&\hat\delta\le10^{-18},\\
\min(1,\max(0,\hat\beta/\hat\delta)),&\text{otherwise}.
\end{cases}
\]

Then:

\[
\Sigma_{\mathrm{shrink}}
=
(1-\lambda)S+\lambda T.
\]

Freeze effective rank as participation ratio:

\[
r_{\mathrm{eff}}
=
\frac{\mathrm{tr}(\Sigma)^2}
{\mathrm{tr}(\Sigma^2)}.
\]

D2 is refused for a fold if:
- covariance is nonfinite;
- \(r_{\mathrm{eff}}<0.5p\);
- condition number \(>10^6\);
- inversion fails.

No pseudoinverse rescue is allowed.

## 5. Recurrent perturbation detector

The same candidate metric supplies two training-only coordinates:

1. baseline-relative state displacement:
   \[
   d_t=\mathcal D(Z_t,\hat B_t);
   \]
2. baseline-relative one-step innovation:
   \[
   j_t=
   \mathcal D\left(
   (Z_t-\hat B_t)-(Z_{t-1}-\hat B_{t-1}),
   0
   \right).
   \]

For candidate entry quantile \(q_e\in\{0.95,0.975,0.99\}\):
- state-entry threshold is the \(q_e\) training quantile of \(d_t\);
- interruption/innovation threshold is the same \(q_e\) training quantile of \(j_t\).

When no episode is active, observed perturbation entry requires:
- \(d_t\) at or above the state-entry threshold;
- previous valid \(d_{t-1}\) below that threshold;
- minimum separation satisfied.

While an episode is active, a new perturbation/interruption requires:
- \(j_t\) at or above the innovation threshold;
- minimum separation satisfied.

This closes the repeated-shock case without using true injected shock times in the detector.

## 6. Return-set detector

For candidate return quantile \(q_r\in\{0.50,0.60,0.70\}\), freeze the return threshold as the training-only \(q_r\) quantile of \(d_t\).

Sustained return requires \(d_t\) at or below the return threshold for candidate consecutive duration \(k\in\{2,3,5\}\) samples.

Candidate minimum separation is \(m\in\{2,5,10\}\) samples.

A detected new perturbation before sustained return terminates the prior episode as \`INTERRUPTED_BY_NEW_PERTURBATION\`.

No overlap is merged into a successful recovery.

## 7. Event/return candidate scoring

For every candidate tuple \((q_e,q_r,k,m)\), match detected entries to true injected entries greedily in time with maximum matching tolerance 5 samples.

Entry localization score:

\[
E_{\mathrm{entry}}
=
\frac{
\sum_{\mathrm{matched}}|\Delta t|
+
10\,N_{\mathrm{missed}}
}{
N_{\mathrm{true}}
}.
\]

Return timing score uses matched episodes and generator sustained-return truth. A missing observed sustained return for a true sustained-return episode receives penalty equal to the candidate horizon used for that scoring pass.

False-event rate is:

\[
F_{\mathrm{event}}
=
\frac{N_{\mathrm{unmatched\ detected}}}
{\max(1,N_{\mathrm{detected}})}.
\]

No truth event is removed from scoring because it is inconvenient.

## 8. Metric ranking

For each D1/D2 candidate:
1. fit only on training data;
2. apply the complete frozen event tuple grid;
3. retain the best event tuple for that metric using §9;
4. compute median event-localization error across frozen perturbation worlds.

A metric remains eligible only if required known-truth controls do not produce a false history/recovery-law disposition at the full-pipeline gate.

Among eligible metrics, choose lower median event-localization error. Exact tie chooses D1.

D3 remains \`NOT_APPLICABLE\` for first-cycle Q040.

## 9. Event-tuple ranking

Within each baseline/metric candidate, select the tuple lexicographically by:

1. absolute event-entry timing error;
2. sustained-return timing error;
3. false-event rate;
4. less extreme entry quantile: 0.95, then 0.975, then 0.99;
5. shorter sustain duration: 2, then 3, then 5;
6. longer minimum separation: 10, then 5, then 2;
7. stricter return quantile: 0.50, then 0.60, then 0.70.

This ordering is fixed before candidate outcomes.

## 10. Horizon qualification

Candidate horizons remain \(\{20,40,80\}\) samples.

Use generator truth, not detected outcomes, to evaluate horizon saturation in stable-recovery controls:

NC-R1, NC-R3, NC-R4, NC-R6, NC-R7, NC-R10, NC-R15, NC-R17, and NC-R20.

Choose the shortest horizon \(H\) for which:
- extending to the next candidate changes true sustained-return cumulative incidence by <0.02 absolute in every required stable cell;
- \(H\) captures at least 90% of all true sustained returns occurring by 80 samples.

If neither 20 nor 40 qualifies, use 80 and append:
\`HORIZON_SATURATION_NOT_ESTABLISHED\`.

## 11. Exact discrete-time competing-risk model

Freeze one estimator, not a model search.

For each at-risk episode-time row \(h=1,\ldots,H\), outcome is:
- 0: remains at risk;
- 1: sustained return occurs at \(h\);
- 2: interruption occurs at \(h\).

Use multinomial-logit hazards with class 0 as reference:

\[
\eta_{1}=X\beta_1,
\qquad
\eta_{2}=X\beta_2,
\]

\[
p_0=\frac1{1+e^{\eta_1}+e^{\eta_2}},
\quad
p_1=\frac{e^{\eta_1}}{1+e^{\eta_1}+e^{\eta_2}},
\quad
p_2=\frac{e^{\eta_2}}{1+e^{\eta_1}+e^{\eta_2}}.
\]

Time basis is frozen as:
- \(h/H\);
- \((h/H)^2\);
- \(\log(1+h)/\log(1+H)\).

Continuous episode-entry covariates are standardized on training episodes only.

Optimization uses deterministic damped Newton iterations implemented in NumPy.

Freeze ridge penalty:
\[
\lambda_{\mathrm{ridge}}=10^{-4}
\]
on all non-intercept coefficients. The intercept is unpenalized.

No penalty search is allowed.

Refuse a fit if:
- objective is nonfinite;
- Newton system cannot be solved after deterministic damping;
- maximum absolute coefficient exceeds 30;
- predicted class probability is nonfinite.

## 12. M0 and M2

M0 uses the frozen native comparator available at entry:
- observed state;
- candidate baseline position and velocity;
- detected perturbation amplitude;
- perturbation direction;
- market-direction label;
- elapsed time since prior detected event;
- session phase;
- update/staleness state;
- noise/activity proxy;
- observed exogenous forcing;
- observed regime proxy;
- causal recent-event intensity.

M2 adds only observed-history:
- cumulative prior detected perturbation amplitude \(L_j\);
- cumulative prior observed time outside return set \(U_j\).

Truth burdens are never estimator features.

## 13. Primary synthetic score

From predicted cause-specific hazards, construct sustained-return cumulative incidence:

\[
\widehat F_R(h)
=
\sum_{u\le h}
\widehat S(u-1)\widehat p_R(u).
\]

Primary score is integrated Brier score over \(h=1,\ldots,H\).

For synthetic qualification, right-censored rows after censoring are omitted from that episode/time contribution. Because censoring is generator-known in synthetic qualification, no truth label after censoring is exposed to fitting.

The real-data preregistration must separately freeze training-only IPCW before real execution. Synthetic qualification does not license omission of IPCW in real data.

## 14. Synthetic M2 admission rule

For each synthetic replicate and scale:
- compute held-out integrated Brier for M0 and M2;
- M2 \`ADDS\` only if held-out Brier(M2) < Brier(M0);
- coefficient sign alone is never used.

History direction is determined from a model-based burden perturbation:
- increase both standardized M2 burden coordinates by +1 training SD while holding M0 covariates fixed;
- recompute sustained-return CIF at \(H\);
- average the CIF change across held-out episodes.

Negative average change = erosion direction.
Positive average change = adaptation direction.

Required synthetic operating characteristics per scale over 200 deterministic replicates:
- true erosion NC-R2: at least 80% \`ADDS\` and at least 80% of adding replicates have erosion direction;
- adaptation NC-R4: at least 80% \`ADDS\` and at least 80% of adding replicates have adaptation direction;
- memoryless/null controls NC-R1 and NC-R3: at most 5% \`ADDS\`;
- moving baseline NC-R5, changing noise NC-R15, heteroskedastic coordinate NC-R16, latent-regime NC-R17, matched-timing NC-R20: at most 5% unconditional \`ADDS\`;
- NC-R17b may show apparent M2 gain but must retain comparator-insufficiency/ambiguity and may never count as unconditional history mechanism;
- NC-R13 and NC-R18 are adjudicated by the already-declared incomplete-recovery/competing-risk dispositions, not by forcing an unconditional M2 null.

Failure of these operating characteristics refuses the estimator pipeline. No effect-size retuning is permitted.

## 15. Cross-validation

Use the observation-contract expanding folds:
- train 0–2047, test 2048–2559;
- expand through folds 2–4.

All baseline/global metric training objects for a test fold use only prior observations.

Episode-entry covariates in a test fold are computed causally.

A fold with insufficient train/test episodes is reported and excluded only under a prospectively declared refusal, never silently.

## 16. Hawkes-equivalent native event-history diagnostic

To avoid an unfrozen package dependency, first-cycle qualification uses a discrete-time exponential self-excitation comparator, which is an allowed equivalent event-history model under Q040 v0.6.

Frozen decay candidates:

\[
\rho\in\{0.90,0.96,0.99\}.
\]

For each \(\rho\), causal excitation state is:

\[
C_t=\rho C_{t-1}+I_{t-1},
\]

where \(I_{t-1}\) is prior detected event entry.

Background terms:
- intercept;
- the four frozen session-phase terms;
- observed activity/noise proxy.

Fit a Bernoulli-logit event-arrival model with fixed ridge \(10^{-4}\), no tuning.

Synthetic calibration uses 200 deterministic replicates per required clustering generator cell.

Diagnostics:
- absolute event-rate error;
- inter-event-time KS distance;
- excitation-coefficient recovery where identifiable;
- calibration error by predicted-probability decile.

A candidate decay is admitted only if at least 95% of replicates lie within the 2.5–97.5% self-generated correct-model envelope for all four diagnostics and it does not create a false M2/history-adds disposition in required null worlds.

Choose the admitted decay with lowest median standardized aggregate diagnostic error. Exact tie chooses smaller \(\rho\).

If none qualifies:
\`HAWKES_DIAGNOSTIC_REFUSED\`.

Q040 may continue with native non-Hawkes controls, but no claim may depend on Hawkes adjustment.

## 17. Candidate advancement

The synthetic qualification proceeds in this order:

1. rank baseline candidates;
2. for the top baseline candidate, rank D1/D2 and event tuples;
3. freeze horizon from generator truth;
4. run full M0/M2 known-truth operating-characteristic gate;
5. run native event-history diagnostic qualification;
6. if the full-pipeline null/control gate fails because of baseline/metric/event choice, eliminate the implicated candidate and advance to the next prospectively ranked candidate without changing any frozen rule;
7. if no candidate survives, return the corresponding refusal.

## 18. Current status

\`Q040_ESTIMATOR_IMPLEMENTATION_COMPLETION_DELTA=v0.1_FROZEN\`

\`Q040_REAL_OUTCOMES=SEALED\`

\`NEXT=IMPLEMENT_BASELINE_METRIC_EVENT_HORIZON_QUALIFICATION\`
