# Q040 Confirmatory Feature-Bridge Gap Audit

**Date:** 2026-10-02
**Authority:** Q040 Synthetic Estimator Implementation Closure v0.1
**Stage:** pre-C-bank feature construction
**Real Q040 outcomes opened:** NO
**C-bank realizations opened:** NO
**Disposition:** IMPLEMENTABLE CORE / C-BANK EXECUTION STILL GATED

The final closure fixes the M0 feature blocks and M2 history extension, but two execution-level feature conventions are not uniquely specified in the authoritative October 2 record.

First, M0 includes one scalar called the "causal trailing 20-sample realized native-difference RMS," but no formula defines whether RMS is taken over coordinate-wise first differences, vector norms, only valid-update differences, or carried-forward one-sample differences.

Second, M0 includes `log1p previous estimated inter-event interval` but the final closure does not state the first-estimated-event value. An older superseded implementation delta used elapsed=0 plus a separate `HAS_PRIOR_EVENT` indicator, but the final closure no longer includes that indicator in M0.

The final closure also does not restate the older per-world 0-2047 calibration / 2048-4095 eligible-episode split. That split may not be silently assumed for the C bank without lineage confirmation because the closure explicitly redefines the disjoint C-bank cross-validation structure.

## Mechanically implementable feature core

A feature constructor may be implemented now if it:
- follows the frozen 42-column M0 block order exactly;
- constructs baseline-relative residual, baseline location, perturbation unit direction, event amplitude, baseline-velocity terms, session phase, native proxies, coordinate-4 directional sign, and prior-incomplete indicator directly from supplied frozen objects;
- requires the unresolved trailing-RMS and previous-interval scalars as explicit caller inputs rather than inventing them;
- adds only `L_obs` and `U_obs` for the 44-column M2 vector;
- exposes NC-R17b withheld covariate only through a separate synthetic-oracle constructor.

No C-bank realization may be generated or scored until the unresolved bridge conventions and H-stage prerequisite are prospectively closed.
