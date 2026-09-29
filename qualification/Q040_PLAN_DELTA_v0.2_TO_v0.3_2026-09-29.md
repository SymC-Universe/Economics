# Q040 Plan Delta v0.2 -> v0.3

Date: 2026-09-29
Governance: SymC GOM v1.0
Real Q040 outcome exposure: NONE
Source plan commit: \`33c3c033b62e3f9343cdcbe768239a12f94bdbfa\`
External-adversarial adjudication: \`qualification/Q040_EXTERNAL_APQ_ADJUDICATION_v0.2_2026-09-29.md\`

## Accepted prospective changes

1. Baseline location and state scaling/covariance are now separate estimands.
2. Test-fold covariance/scaling is frozen before target events; unstable full-covariance geometry is refused.
3. A diagonal training-scale norm is the preregistered fallback if full covariance fails qualification.
4. State-dependent noise/heteroskedasticity becomes an explicit null and native covariate problem.
5. Return-time analysis now requires explicit recurrent-event risk sets and a competing interruption event when a new perturbation arrives before recovery.
6. \(T_{\mathrm{ind}}\) is demoted from primary observational estimand to model-qualified descriptive comparator.
7. Native event-history controls must be state dependent and allow flexible background/session intensity.
8. Cross-scale inference gains slower-regime/common-state proxies and pair-specific reporting.
9. Known-truth suite expands to NC-R16 through NC-R19.
10. Observational claim ceiling is explicit: no global basin/resilience or causal Stability-Inheritance claim from Q040 alone.

## Tool-conformance correction

The v0.2 external searches are adversarial inputs but not clearance because:
- one omitted the required exact APQ footer;
- one explicitly lacked clause-level access to the plan.

The v0.3 re-review request must embed the actual plan text directly.

No real outcome was used to make any change.
