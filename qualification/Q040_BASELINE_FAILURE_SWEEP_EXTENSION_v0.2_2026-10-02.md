# Q040 Baseline Failure Sweep Extension v0.2
**Date:** 2026-10-02
**Parent failure audit:** `qualification/Q040_BASELINE_SELECTION_FAILURE_IDENTIFIABILITY_AUDIT_2026-10-02.md`
**Promotion eligible:** NO
**Real Q040 outcomes:** SEALED

The first exploratory sweep through 240 samples did not recover the frozen 90% coverage requirement in every NC-R20 20%-density clustered-update cell at 15 s or 30 s. Coverage was still monotonically improving at the outer edge, while NC-R5 moving-baseline median error was also still decreasing.

Therefore the failure boundary is not yet mapped.

A second exploratory-only extension is frozen:

[
Win{320,480,640}.
]

It uses the same controls:
- all four NC-R20 density=0.20, CLUSTERED curvature×noise cells;
- NC-R5 moving-baseline truth;

and a new seed namespace using `950+r` rather than the prior exploratory `900+r`.

This extension cannot promote K1/K2 or alter the failed v0.1 baseline result.

If no window reaches full per-world 90% coverage across the sparse clustered cells, retain `BASELINE_OPERATOR_REFUSED` for that measurement regime.

If an identifiable window region appears, it may motivate a new prospective estimator Plan Delta, which must use a fresh qualification bank not used in either exploratory sweep.

`NEXT=MAP_OUTER_IDENTIFIABILITY_BOUNDARY`
