# Q040 Confirmatory Numerical Implementation Delta v0.1

**Date:** 2026-10-02
**Authority:** Q040 Synthetic Estimator Implementation Closure v0.1
**Stage:** pre-C-bank implementation
**Real Q040 outcomes opened:** NO
**Confirmatory C-bank outcomes opened:** NO

This delta closes numerical conventions required to implement the already-frozen confirmatory estimator. It does not alter M0/M2 features, model family, folds, thresholds, controls, promotion gates, horizon, or any known-truth target.

## 1. Discrete censoring convention

Training-only censoring survival uses discrete Kaplan-Meier with right-censoring as the censoring event and sustained return/interruption treated as observed non-censoring terminals.

Let `G_after(k)` be censoring survival after censorings at integer time k and `G_left(k)` the left limit immediately before k. For an observed sustained-return or interruption terminal at time k, IPCW uses `1/G_left(k)`. An episode still observed and event-free through scoring time k uses `1/G_after(k)`. A right-censored episode contributes no Brier term at its censoring time or later.

If any `G_after(k) < 0.05` on the scoring grid, the fold returns `CENSORING_WEIGHT_NOT_QUALIFIED`.

## 2. Bootstrap interval and p-value

The scale-level paired bootstrap resamples the 30 replica-level `Delta IBS` values with replacement, 30 values per bootstrap replicate, for exactly 10,000 replicates.

The ordinary two-sided 95% interval is the percentile interval at 2.5% and 97.5%, using linear interpolation between adjacent ordered bootstrap means.

The two-sided raw bootstrap p-value is:
`2 * min(P*(Delta_boot <= 0), P*(Delta_boot >= 0))`,
with finite-sample correction `(count + 1)/(10000 + 1)` applied to each tail before doubling and cap at 1.

## 3. Deterministic bootstrap seeds

Primary scale-level M0/M2 bootstrap:
`SeedSequence([20261002, 400, scale_seconds])`.

NC-R17b oracle diagnostic bootstrap:
`SeedSequence([20261002, 401, scale_seconds])`.

No bootstrap seed is selected from outcomes.

## 4. Holm adjustment

Across the four frozen scale-level primary p-values, apply ordinary Holm step-down adjustment in ascending raw-p order. Ties are ordered by ascending scale seconds. Adjusted p-values are monotone non-decreasing in ordered position and capped at 1.

These conventions are frozen before any C-bank realization is generated or scored.
