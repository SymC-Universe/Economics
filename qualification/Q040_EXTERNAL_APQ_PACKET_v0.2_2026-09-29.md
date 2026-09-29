# Q040 External APQ Review Packet v0.2

Date: 2026-09-29
Governance: SymC GOM v1.0
APQ level: APQ-2 SUBSTANTIAL
Plan under review:
\`qualification/Q040_RECOVERABILITY_PLAN_PACKET_v0.2_2026-09-29.md\`

PLAN_COMMIT:
\`33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`

Supporting foundations:
- \`qualification/Q040_PRIOR_ART_NOVELTY_FOUNDATION_v0.1_2026-09-28.md\`
- \`qualification/Q040_RECOVERY_THEORY_FOUNDATION_v0.1_2026-09-28.md\`
- \`qualification/Q040_CHI_COLLISION_FOUNDATION_v0.1_2026-09-29.md\`
- \`qualification/Q040_PLAN_DELTA_v0.1_TO_v0.2_2026-09-29.md\`

No Q040 real-data outcome has been opened.

## Reviewer role

Perform an isolated adversarial review of the plan before any real Q040 outcome is exposed.

The review should determine whether the plan can distinguish:
- changed finite-time recovery dynamics;
- ordinary incomplete recovery;
- clustered/self-exciting shocks;
- moving baselines;
- changing forcing/noise;
- non-normal transient amplification;
- adaptation/strengthening;
- true versus mechanical cross-scale propagation;
- native market-state sufficiency;
- scalar/modal/architecture refusal.

Do not assume the Stability Architecture framing is necessary.

## Required severity classes

Every objection must be classified:

- BLOCKER
- MATERIAL
- MINOR

For every BLOCKER or MATERIAL objection provide:

1. threatened inference;
2. exact failure mechanism;
3. smallest discriminating fix or test;
4. whether the fix is outcome-independent;
5. whether it materially changes the plan;
6. claim restriction if unresolved.

A single valid MATERIAL objection requires adjudication.

## Mandatory attack domains

### A. Recovery theory

Attack whether the plan correctly separates:
- local/asymptotic return;
- finite-time recovery;
- reactivity/transient amplification;
- resistance;
- finite-shock recoverability;
- memory/history;
- baseline migration;
- adaptation;
- recurrent-disturbance effects.

Identify any remaining conceptual collapse.

### B. Native-state-first representation

Attack the decision to begin from \(Z_S(t)\) rather than assumed \(Χ_S(t)\).

Determine whether:
- this properly isolates Q040 from Q039;
- the proposed native state is sufficient;
- scale-dependent aggregation changes the meaning of \(Z_S\);
- a vector recovery problem requires a different geometry.

### C. Scalar \(\chi\) lane

Attack whether the canonical scalar admission rule is too permissive or too restrictive.

Specifically test:
- second-order factor identification;
- pole aliasing;
- model-order selection;
- nonstationarity;
- non-normality;
- moving baselines;
- whether any generalized scalar should use a different symbol.

A valid review may recommend permanent scalar refusal for the first Q040 cycle.

### D. \(Χ\) and \(Χ_{\mathrm{arc}}\)

Attack:
- modal/subspace admission;
- information loss;
- basis instability;
- whether \(Χ\) adds anything beyond the native state;
- whether deferring \(Χ_{\mathrm{arc}}\) is sufficient to avoid circularity;
- whether any architecture-level construction would simply repackage the native model.

### E. Baseline operators K1/K2

Attack:
- causal trailing location;
- moving-attractor estimation;
- bandwidth/window choice;
- baseline/recovery identifiability;
- operator dependence;
- trend leakage;
- nonstationary covariance.

Recommend the smallest pre-outcome qualification rule capable of refusing an inadequate operator.

### F. Perturbation coordinate

Attack the candidate train-whitened Mahalanobis distance:

\[
d_S(t)
=
\sqrt{
r_S(t)^\top
\Sigma^{-1}
r_S(t)
}.
\]

Consider:
- high-dimensional covariance instability;
- heavy tails;
- non-Euclidean/modal geometry;
- state-dependent covariance;
- regime-dependent scaling;
- whether whitening creates artificial radial recovery.

Propose a better metric only if it is prospectively identifiable.

### G. Event construction

Attack:
- entry threshold;
- return set;
- sustain rule;
- event timeout;
- merge/separation rule;
- nested events across scales;
- censoring;
- survivorship;
- event-rate adequacy.

No future recovery outcome may define event inclusion.

### H. Independence-time comparator

Attack whether an observational analogue of

\[
T_{\mathrm{ind},S}
\]

can actually be estimated without circularity or hidden conditioning.

Determine whether it should be:
- an explicit model quantity;
- a descriptive comparator;
- or omitted from decisive inference.

### I. Native history / self-excitation comparator

Attack whether a Hawkes-like or equivalent history model is strong enough.

Could apparent erosion still be:
- endogenous clustering;
- volatility clustering;
- depth depletion;
- order-sign persistence;
- regime duration;
- latent common cause?

Identify the strongest simpler market-native explanation.

### J. Exogenous forcing

Attack treatment of:

\[
\xi(t).
\]

Consider:
- scheduled macro releases;
- unscheduled news;
- cross-market shocks;
- data latency;
- event timestamp precision.

Recommend inclusion, exclusion, stratification, or refusal rules.

### K. Survival / hazard estimation

Attack whether survival/hazard modeling is appropriate for sustained recovery.

Consider:
- recurrent events;
- competing risks;
- informative censoring;
- time-varying covariates;
- within-day dependence;
- left truncation;
- repeated-event frailty/random effects.

### L. Resistance and finite-shock claims

Attack whether observational market data can support:
- resistance;
- finite-shock recoverability;
- basin/viability language.

If not, specify the exact claim ceiling.

### M. Cross-scale propagation

Attack whether the proposed non-overlap / leave-child-out / synthetic-overlap controls actually separate:
- true propagation;
- shared forcing;
- common latent regime;
- nested aggregation mechanics;
- slower-state persistence.

A valid outcome is that Q040-H is not identifiable from the available data.

### N. Known truths

Attack NC-R1 through NC-R15.

Require any missing synthetic worlds needed to discriminate:
- erosion;
- adaptation;
- moving baseline;
- memory/resistance tradeoff;
- non-normality;
- clustered shocks;
- nested-window artifacts;
- changing noise;
- representation refusal;
- true/no propagation.

### O. Shared-premise attack

At least once, test the hypothesis:

> A strong native market-state/history model explains everything and \(\chi\), \(Χ\), and \(Χ_{\mathrm{arc}}\) add no scientific value.

The plan must succeed scientifically if this is the result.

## Evidence firewall

Do not request or inspect:
- Q040 real outcomes;
- Q039 real outcomes;
- Q038 June 9-11 for Q040 tuning.

Review is plan-only.

## Required final section

### BLOCKER
[list or none]

### MATERIAL
[list or none]

### MINOR
[list or none]

### Minimum Plan Delta
[smallest outcome-independent revisions]

### Claim ceiling after fixes
[exact bounded inference]

### Final disposition

End exactly with one:

\`APQ_EXTERNAL_STATUS=QUALIFIED\`

or

\`APQ_EXTERNAL_STATUS=REVISE\`

or

\`APQ_EXTERNAL_STATUS=BLOCKED\`

Then exactly:

\`PLAN_COMMIT=33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`
