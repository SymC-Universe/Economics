# Q040 Plan Delta v0.3 -> v0.4

Date: 2026-09-29
Governance: SymC GOM v1.0
Real Q040 outcome exposure: NONE
Source plan commit: \`d29366b67bba5d51722f89af88d88644ef9977fc\`

## Reason

The exact-plan v0.3 adversarial review did not establish conformant external clearance, but its literature-grounded synthesis identified one wording risk worth resolving prospectively: observed return before a new perturbation is not the same estimand as counterfactual shock-free recovery.

A mechanical audit also found stale v0.2/v0.3 self-references and an NC-R15 wording remnant after the suite had expanded to NC-R19.

## Changes

1. Primary recurrent-event estimand is now explicitly the conditional sustained-return hazard/cumulative incidence under the **observed competing-event process**.
2. New perturbation/interruption hazard is reported separately.
3. No counterfactual "would have recovered if no later shock occurred" claim is licensed.
4. If history changes both return and re-perturbation hazards, use \`HISTORY_ASSOCIATED_WITH_RECOVERY_AND_REPERTURBATION\` unless stronger gates isolate a recovery-specific component.
5. M3 no longer includes an observational \(T_{\mathrm{ind}}\)-derived indicator by default. It uses prior sustained-return state, residual displacement, elapsed time, and frozen incomplete-recovery burden.
6. Mechanical version labels are normalized to v0.4.
7. External APQ question now references NC-R1 through NC-R19.

No threshold, representation, real-data endpoint, or positive claim was selected from outcomes.
