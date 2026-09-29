# Q040 v0.2 Adversarial Review Adjudication

Date: 2026-09-29
Governance: SymC GOM v1.0
Plan reviewed: \`33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`
Real Q040 outcome exposure: NONE

## Review identities

Two isolated Undermind literature-grounded attacks were launched:

1. \`/Q040 v0.2 adversarial APQ review\`
2. \`/Q040 v0.2 statistical identifiability attack\`

Both completed without inspecting Q040 or Q039 real outcomes.

## Conformance finding

Neither return qualifies as final external APQ clearance.

- Review 1 produced substantive plan-relevant objections but its stored summary did not end with the required exact APQ status/footer.
- Review 2 explicitly reported that it did not ingest the plan text and therefore could not audit K1/K2 or NC-R1--NC-R15 clause by clause. Its disposition was HOLD/not auditable, not one of the allowed exact APQ statuses.
- The separate Q039 v0.4 re-binding search demonstrated the same tooling limitation: naming workspace files in a deep-search goal does not reliably make their contents available to the review agent.

Therefore the reviews are retained as **adversarial evidence**, not as qualification, blocking, or approval.

A later external review must receive the exact plan text directly in its prompt/input or use a tool path proven to expose the full document.

## Valid objections accepted from Review 1

### A1. Strong native state-and-history baseline is mandatory

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

The recovery-history signal cannot be interpreted as stability-specific if a state-dependent native order-book model with event history explains it.

v0.3 must explicitly include:
- state-dependent event history;
- flexible background/session intensity;
- queue/book state;
- diagnostic checks for Hawkes/background misspecification.

### A2. Hawkes/self-excitation can be falsely inflated by nonstationarity

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

Seasonality, regime shifts, outliers, and flexible exogenous intensity can bias branching/self-excitation estimates. A single Hawkes fit is not a sufficient control.

v0.3 must require:
- a non-self-exciting time-varying/background comparator;
- state-dependent intensity;
- goodness-of-fit/residual diagnostics;
- a known-truth world in which background intensity changes but true self-excitation/recovery law does not.

### A3. Recurrent recovery episodes require risk-set/dependence treatment

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

Perturbations cannot be treated as independent first events. v0.3 must explicitly define:
- recurrent-event identity;
- right/interval censoring;
- competing new perturbations before recovery;
- session-end/data-gap censoring;
- within-day/within-episode dependence;
- cluster/frailty or equivalent dependence handling.

### A4. Perturbation direction, magnitude, and profile are part of the estimand

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

Repeated perturbation cannot be interpreted without matching/conditioning on current perturbation geometry. v0.3 must preserve vector direction and raw/normalized magnitude rather than using one radial score as the whole event description.

## Valid objections accepted from Review 2

### S1. Mahalanobis event coordinate can drift mechanically

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

A changing covariance matrix can change the distance score and event threshold even if the restoring law is unchanged.

v0.3 must demote train-whitened Mahalanobis distance from preferred primary status and instead prospectively qualify a metric family using synthetic/input-geometry criteria only.

A new known-truth world must vary covariance/heteroskedasticity with unchanged recovery law.

### S2. Baseline motion and conditional noise must be estimated separately

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

A moving mean, changing variance, and colored noise can each mimic slower recovery.

v0.3 must require:
- explicit local baseline state;
- explicit conditional scale/covariance state;
- raw and normalized perturbation magnitudes;
- known truths for colored/heteroskedastic noise and baseline migration;
- refusal when mean/scale separation is not identifiable.

### S3. Survival analysis needs competing-risk/recurrent-event rules

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

v0.3 must define recovery as a recurrent-event problem with sustained return as the recovery event and new perturbation/session end/data loss handled explicitly.

No naive independent-event Kaplan-Meier interpretation is permitted.

### S4. "Independence time" is model-dependent and can be overinterpreted

**Severity:** MATERIAL  
**Disposition:** ACCEPTED.

The first-cycle observational quantity will be renamed a candidate **recovery-separation horizon**:

\[
T_{\mathrm{sep},S}^{*}.
\]

It may operationalize incomplete recovery but must not be called evidence of stochastic or dynamical independence.

### S5. Nested time bins can create false cross-scale propagation

**Severity:** MATERIAL  
**Disposition:** ACCEPTED / ALREADY PARTLY PRESENT.

v0.2 already required a mechanical-overlap firewall. v0.3 strengthens it by making a **non-overlapping future slower-scale target** the primary Q040-H target. Leave-child-out and nested-aggregation synthetic nulls remain sensitivities.

## Minor clarifications accepted

- Recovery-duration claims are conditional on the declared event/return geometry.
- Scale-specific estimates are reported separately before any pooled statement.
- No \(\chi\), \(Χ\), or \(Χ_{\mathrm{arc}}\) value is inferred from a Hawkes branching ratio or recovery duration by analogy.
- Observational first-cycle data cannot by themselves establish a physical basin or causal resilience mechanism.

## Rejected / non-adjudicable elements

The "HOLD/not auditable" status from Review 2 is not a scientific objection to the plan; it is a transport failure because the reviewer did not ingest the plan.

The Q039 literature-only non-review is likewise a transport failure and does not alter Q039 v0.4 scientific status.

## Required v0.3 changes

1. native event-history comparator with flexible background/state dependence;
2. metric-family qualification rather than presumptive Mahalanobis primary;
3. separate baseline and conditional-noise state;
4. recurrent-event/competing-risk recovery definition;
5. rename observational independence-time analogue to \(T_{\mathrm{sep},S}^{*}\);
6. non-overlapping slower-scale future target primary;
7. new known truths:
   - covariance/heteroskedasticity drift without recovery-law change;
   - changing background event intensity without self-excitation change;
   - competing perturbation/censoring artifact;
   - latent regime/common-cause world;
8. external review transport fix: full plan text embedded directly in the next review input.

## Disposition

\`Q040_V02_REVISE_TO_V03\`

No real Q040 outcome is authorized.
