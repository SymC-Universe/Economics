# Q040 External APQ Adjudication of v0.2 Searches

Date: 2026-09-29
Governance: SymC GOM v1.0
Plan reviewed: \`33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`
Real Q040 outcome exposure: NONE

## Review identity

Two independent Undermind searches were launched against the v0.2 APQ package:

1. \`/Q040 v0.2 adversarial APQ review\`
2. \`/Q040 v0.2 statistical identifiability attack\`

Workspace:
\`c9911501-f69c-401b-9658-4851eaf10682\`

Neither return is accepted as a conformant external qualification.

### Review 1 conformance

The review produced substantive literature-grounded criticism but did not return the required exact APQ footer/status binding.

Disposition:
\`NONCONFORMANT_AS_CLEARANCE / VALID_AS_ADVERSARIAL_INPUT\`.

### Review 2 conformance

The review explicitly stated that it could not audit the plan clause by clause because the deep-search process did not receive the plan text, despite the workspace file being present.

Disposition:
\`NONCONFORMANT_AS_CLEARANCE / TOOL_ACCESS_FAILURE / VALID_GENERAL_METHOD_INPUT\`.

The review access failure is mechanical, not scientific.

## Accepted MATERIAL objections

### M1. Baseline location and state scaling are not sufficiently separated

Threat:
changing covariance/heteroskedasticity can alter Mahalanobis distance and event thresholds even when the recovery law is unchanged.

Accepted fix:
- estimate baseline location and scaling/covariance as separate objects;
- freeze scaling within each evaluation fold before target events;
- require conditioning/robustness diagnostics;
- add a heteroskedastic/state-dependent-noise known truth;
- refuse full-covariance geometry when unstable.

### M2. Native event-history comparator must be state dependent

Threat:
ordinary Hawkes-like history may leave apparent "erosion" that is actually state-dependent order-flow clustering, session background intensity, or queue-reactive dynamics.

Accepted fix:
- require a state-dependent event-history comparator or an explicit qualification failure;
- include flexible session/background intensity;
- require calibration/diagnostics before using the comparator as adequate.

### M3. Recurrent-event risk sets and censoring are under-specified

Threat:
new perturbations, session end, timeout, and repeated episodes create informative censoring/dependence.

Accepted fix:
- define explicit risk-set entry/exit;
- treat a new qualifying perturbation before recovery as a competing/interruption event rather than ordinary independent censoring;
- use recurrent-event/day clustering in uncertainty;
- add an informative-censoring known truth.

### M4. \(T_{\mathrm{ind}}\) is too strong as an observational estimand

Threat:
independence time is model/return-set dependent and can be circularly inferred from the same trajectories used to test history.

Accepted fix:
- demote \(T_{\mathrm{ind}}\) to a descriptive/model-qualified comparator;
- primary native controls use observed time since prior perturbation and incomplete-recovery state directly;
- no "independence-time shift" claim without a separately qualified model.

### M5. Cross-scale propagation needs a latent-common-regime null in addition to nested-overlap controls

Threat:
both fast history and slower migration may be driven by a common unobserved regime even when mechanical aggregation overlap is removed.

Accepted fix:
- add a latent-regime/common-cause known truth;
- require slower native regime/persistence controls;
- restrict interpretation to incremental predictive ordering.

## Accepted MINOR / strengthening points

- report scale-specific effects; do not pool scales as replication;
- separate threshold sensitivity from primary inference;
- preserve perturbation direction/magnitude dependence;
- retain conditional-noise diagnostics;
- do not use recovery duration alone as critical-transition evidence.

## Rejected / already resolved objections

No objection supports abandoning the native-state-first design.

No review evidence supports forcing \(\chi\), \(Χ\), or \(Χ_{\mathrm{arc}}\).

The v0.2 plan already:
- separates local recovery from resistance/basin claims;
- includes non-normal transient amplification;
- includes baseline migration;
- includes nested-aggregation controls;
- permits native-model sufficiency/refusal.

Those parts remain.

## Adjudication

\`APQ_V0_2_CLEARANCE=NOT_GRANTED\`

A v0.3 Plan Delta is required before a conformant external re-review.

The re-review will embed the actual plan text directly in the review request to avoid the workspace-file access failure.
