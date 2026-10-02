# Q040 Estimator-Qualification Implementation Gap Audit
**Date:** 2026-10-01
**Authority:** Q040 Recoverability Plan Packet v0.6 + Q040 Synthetic Estimator-Qualification Specification Freeze v0.1
**Real Q040 outcomes:** SEALED
**Disposition:** SCIENTIFIC_GATE — SYNTHETIC OBSERVATION/EPISODE CONTRACT MISSING

## 1. What is already frozen

The current Q040 authority freezes:
- candidate baseline classes K1/K2 and their grids;
- perturbation metric classes D1/D2, with D3 conditional on an independently admitted (Χ_S);
- entry/return quantiles, sustain durations, event separations, overlap treatment;
- timeout/censoring family;
- discrete-time competing-risk recovery framework;
- M2 cumulative burden as primary history extension;
- integrated Brier score as the primary probabilistic score;
- Hawkes/queue-reactive calibration logic;
- multiplicity/refusal rules.

The 22-control synthetic generator contract also passes its generator-level invariants.

## 2. Exact implementation gap

The existing generator contract does **not** define one common observed-state and episode object that can be passed through the frozen estimator pipeline.

Examples from `market_chi/q040_synthetic_generators_v0_1.py`:

- NC-R1/R2/R3/R4/R5/R6/R7/R9/R10/R11/R13/R15/R18/R21 return combinations of truth variables such as `shock`, `burden`, `rate`, `baseline`, `noise_scale`, `slow`, and `resistance`, but do not return an observed native trajectory (Z_S(t)).
- NC-R12 returns a 2D non-normal state `x`, but not a common perturbation-entry/return/interruption truth object.
- NC-R16 returns heteroskedastic `x` and `cov_scale`, but no frozen event truth.
- NC-R17/17b/19 return latent/common-cause variables and proxies, but no common observed recovery state.
- NC-R20 returns a scalar `latent`/`observed` carry-forward process and update mask, but not the common multidimensional (Z_S(t)) + episode truth required by the full Q040 estimator.

The generator runner explicitly records:
`estimator_qualified=false`
and states that generator-contract PASS does not qualify the estimator, thresholds, K1/K2, representations, or real-data execution.

## 3. Why this cannot be filled mechanically

The frozen estimator requires all of the following on a common observation contract:

1. observed (Z_S(t));
2. true baseline (B^{Z}_{S,mathrm{true}}(t)) for baseline-location error;
3. true perturbation entry times or event-support truth for event-localization error;
4. true sustained-return times;
5. true interruption/re-perturbation events;
6. censoring truth;
7. history/burden variables and current-state/native covariates available causally;
8. measurement/update timing where relevant;
9. the known expected disposition for each control.

Constructing these from the present truth-variable arrays requires choosing a dynamical observation law, state dimension, shock injection law, noise injection law, baseline coupling, event truth convention, and specialized mappings for controls whose current outputs are structurally different.

Those choices are outcome-consequential: they can change K1/K2 selection, D1/D2 selection, event-threshold qualification, horizon selection, and M2-vs-M0 scoring.

Therefore they are scientific specification, not neutral coding.

## 4. Required missing contract

Before full estimator qualification, freeze a versioned:
`Q040_SYNTHETIC_OBSERVATION_EPISODE_CONTRACT`

For every control and scale it must deterministically provide at least:

- `Z_observed[n,p]`;
- `baseline_true[n,p]`;
- `update_mask[n]` / staleness where applicable;
- `event_entry_true[n]` or an equivalent exact event list;
- `sustained_return_true[n]`;
- `interruption_true[n]`;
- `censoring_true[n]`;
- `burden_true[n]`;
- causal native comparator covariates;
- `exogenous_forcing[n]` where applicable;
- expected control disposition;
- deterministic seed lineage.

The contract must state which controls use a shared state-transition law and which require specialized constructions.

## 5. D3 disposition

Q039 v0.5 did not independently admit a scale-uniform (Χ_S) representation for Q040.

Therefore under the already-frozen estimator specification:

`Q040_D3=NOT_APPLICABLE_FIRST_CYCLE`

No D3 implementation is required for first-cycle estimator qualification.

## 6. Allowed paths from this gate

### Path A — full contract freeze
Freeze the missing common observation/episode contract, then implement and run the complete K1/K2 -> D1/D2 -> event/return -> horizon -> M0/M2 -> Hawkes qualification pipeline.

### Path B — partial module qualification only
Qualify only modules on controls that already expose sufficient state/truth objects, but retain:
`Q040_FULL_ESTIMATOR_NOT_QUALIFIED`.

Path B cannot authorize real Q040 execution and cannot substitute for Path A.

## 7. Current disposition

`Q040_GENERATOR_CONTRACT=PASS`

`Q040_ESTIMATOR_SPECIFICATION=FROZEN`

`Q040_ESTIMATOR_IMPLEMENTATION=BLOCKED_SCIENTIFIC_CONTRACT`

`Q040_SCIENTIFIC_GATE=SYNTHETIC_OBSERVATION_EPISODE_CONTRACT_FREEZE`

`Q040_REAL_OUTCOMES=SEALED`

No estimator candidate has been selected and no real recovery outcome has been opened.
