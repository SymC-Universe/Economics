# Q040 Synthetic Estimator-Qualification Specification Freeze v0.1
**Date:** 2026-10-01
**Authority:** Q040 Recoverability Plan Packet v0.6
**Stage:** synthetic-only estimator qualification
**Real Q040 outcomes:** SEALED
**Purpose:** close the remaining estimator-qualification degrees of freedom without using real recovery outcomes.

## 1. General rule
All selection below is performed only on frozen synthetic known-truth worlds. No candidate may be selected because it performs well on real Q040 recovery outcomes. A candidate that cannot satisfy its required known-truth and numerical gates is refused rather than rescued.

## 2. Baseline operator K1/K2 grid
K1 is a causal trailing robust-location baseline. Candidate window lengths are frozen as {10S, 20S, 40S}, where S is the analysis scale. Coordinate location is the training-past median; coordinate scale is training-past MAD with the standard 1.4826 consistency factor and a frozen positive floor of 1e-8 after native-unit normalization.

K2 is a causal local linear moving-attractor model fit on the same three trailing horizons {10S, 20S, 40S}. It estimates level and local slope per coordinate from past observations only. K2 is refused for a fold if fewer than 5 effective observations per fitted coefficient are available or if the design is rank deficient.

Qualification order follows v0.6 §9.1: numerical/identification gate, required known-truth dispositions, then median normalized baseline-location error across the complete frozen synthetic grid. If exactly one class survives it wins. If both survive, lower median normalized error wins. Exact ties choose K1. If neither survives, return `BASELINE_OPERATOR_REFUSED`.

## 3. Perturbation metric family D1/D2/D3
D1: robust standardized Euclidean distance using the frozen K baseline, training-past median/MAD scale, and no test-period rescaling.

D2: shrinkage Mahalanobis distance using Ledoit-Wolf-style linear shrinkage estimated from training data only. D2 is refused for a fold if covariance is non-finite, effective rank < 0.5p, or post-shrinkage condition number > 1e6.

D3: modal/subspace distance is eligible only when an independent Χ_S representation has already passed its representation gate without information-loss refusal. Otherwise D3 is `NOT_APPLICABLE`.

A metric class must pass NC-R5, NC-R15, NC-R16, NC-R17/17b, NC-R20, and NC-R21 without a false history/recovery-law disposition. Among survivors, choose the metric with the lowest median normalized event-localization error on the frozen known-truth perturbation worlds. Exact ties prefer D1, then D2, then D3, to minimize structural assumptions. If none survives, return `PERTURBATION_METRIC_REFUSED`.

## 4. Event thresholds and return set
Candidate entry quantiles of the training-only distance distribution are frozen at {0.95, 0.975, 0.99}. Candidate return-set quantiles are frozen at {0.50, 0.60, 0.70}. Return threshold must be strictly below the selected entry threshold.

Candidate sustain durations are {2S, 3S, 5S}. Candidate minimum event separations are {2S, 5S, 10S}. Overlapping entries before sustained return are classified as `INTERRUPTED_BY_NEW_PERTURBATION`, not merged into a successful recovery episode.

Select the tuple using synthetic known truths only. A tuple must first satisfy the frozen false-positive/refusal controls and then minimize, lexicographically: (1) absolute event-entry timing error, (2) sustained-return timing error, (3) false event rate. Exact ties choose the less extreme entry threshold, shorter sustain duration, and longer minimum separation in that order. If no tuple qualifies, return `EVENT_DEFINITION_REFUSED`.

## 5. Horizon and censoring
Candidate timeout horizons are frozen at {20S, 40S, 80S}. Session/end-of-world termination is right censoring. A new qualifying perturbation before sustained return is a competing event, never ordinary right censoring.

Select the shortest horizon for which synthetic cumulative incidence of sustained return changes by <0.02 absolute when extending to the next candidate horizon in all required stable-recovery known-truth worlds while retaining at least 90% of recoveries that occur by 80S. If no horizon qualifies, freeze 80S and append `HORIZON_SATURATION_NOT_ESTABLISHED`; this qualifier blocks strong separation-horizon claims but does not by itself invalidate finite-time recovery analysis.

## 6. Within-scale estimator and history extension
The primary estimator remains the preregistered discrete-time competing-risk framework with separate sustained-return and interruption hazards. The primary history extension is M2 cumulative burden, already signed off before real-outcome exposure. The primary probabilistic score is competing-risk integrated Brier score for sustained-return cumulative incidence.

M2 is compared against the native/current-state comparator stack using frozen out-of-sample folds. Promotion requires improvement in the primary Brier score plus concordant direction in sustained-return hazard calibration; otherwise history-specific promotion is refused.

## 7. Hawkes / queue-reactive diagnostic envelope
The Hawkes/queue-reactive comparator remains a diagnostic native-history control, not a substitute target. Its calibration envelope is generated only from frozen synthetic worlds where the true event-clustering mechanism is known.

Use 200 deterministic calibration replicates per frozen generator cell. For each replicate record event-rate error, inter-event-time KS distance, branching/self-excitation parameter error where identifiable, and sustained-return/interruption calibration error after conditioning on the comparator.

A comparator configuration is admitted only when at least 95% of replicates fall within the prespecified generator-validity bounds and it does not create a false M2/history-adds disposition in any required null family. Among admitted configurations, select the one with the lowest median standardized aggregate calibration error; exact ties select the lower-dimensional specification. If none qualifies, return `HAWKES_DIAGNOSTIC_REFUSED`; Q040 may continue with native non-Hawkes controls, but no claim may depend on Hawkes adjustment.

## 8. Multiplicity and refusal
No candidate-family search may use real Q040 outcomes. All failed candidates and refusal reasons are retained. Synthetic selection is one-way: after this specification is frozen, candidates may be refused by known-truth performance but the grid, thresholds, tie-breaks, and horizons may not be changed unless a documented scientific defect forces a prospective Plan Delta.

## 9. Execution ceiling
This freeze authorizes implementation and synthetic known-truth qualification only. It does not authorize opening real Q040 recovery outcomes. After implementation conformance and synthetic qualification, freeze code/data identities and then re-evaluate the real-data gate under the active GOM.
