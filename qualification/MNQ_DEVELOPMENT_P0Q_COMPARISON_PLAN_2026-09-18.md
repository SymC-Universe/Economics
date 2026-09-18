# MNQ Development Sweep P0-Q Comparison Plan

Date frozen: 2026-09-18
Branch: market-chi-architecture
Scope: development data only
Holdout: June 9-11 remains sealed

## Purpose

Freeze the analysis sequence for the remaining development days before their outcomes are inspected. This is a P0-D/P0-Q development plan, not P1 confirmation.

## Primary structural question

Does the native L10 order-book geometry found on May 31 and replicated on May 27 persist across additional development days when comparisons are made within the same fixed session phase?

Two wall-clock phases remain separate:
- mature: 00:00-21:00 UTC
- session_open: 22:00-24:00 UTC

Elapsed time is not rescaled across markets or phases.

## Fixed structural outputs

For every complete day/phase record report:
- PC1 and PC2 variance fractions and cumulative variance;
- semantic basis alignment for the first six PCs;
- PC1 versus total-depth Spearman association;
- PC2 versus depth-imbalance Spearman association;
- within-day top-2 half-period principal cosine;
- production chi admissions/refusals across the existing 1, 2, 5, 10, 15, 30, 60 s screen.

For every same-phase pair of days compare the top-2 loading subspaces using principal cosines. This comparison is sign- and within-subspace-rotation invariant. No PC sign will be interpreted physically.

No hard principal-cosine promotion threshold is introduced during this development sweep. The continuous values and their distribution across day pairs are reported first. Any later threshold must be justified and versioned before confirmatory use.

## Session-phase question

The May 27 and May 31 forward-risk signs differed while sampling different session phases. Therefore:
- mature periods are compared only with mature periods;
- session-open periods are compared only with session-open periods;
- no global depth -> risk sign is claimed by pooling phases.

For total depth, PC1, spread, and L10 imbalance, preserve the existing forward-risk Spearman associations at 1, 5, 10, 30, and 60 s. Report sign consistency, magnitude range, and day-to-day variation within phase.

No IID p-value is used for these overlapping time-series horizons.

## PC1 versus native total-depth comparator

PC1 is not awarded novelty merely because it is a PCA mode. During this development stage:
- report PC1-total-depth association for each day/phase;
- compare the forward-risk association pattern of PC1 with native total depth;
- if they are effectively carrying the same information, retain an EQUIVALENT interpretation;
- an ADDS claim is deferred until an explicitly frozen out-of-sample incremental metric exists.

## chi rule

The existing production chi gate is unchanged. A refusal remains a valid result. No BIC margin, sampling interval, pole rule, or mapping convention is retuned in response to these development days.

If a new chi admission appears, preserve it as a development result and inspect the admitted model/poles before changing any interpretation. Do not promote it merely because it is favorable to SymC.

## Gradient-mode question

PC3/PC4 depth-gradient and side-gradient alignments are reported because May 27 suggested them. They remain post-result exploratory structure until they recur on additional days. Their presence or absence does not alter the frozen PC1/PC2 comparison.

## Failed-recovery and temporal-inheritance scaffolds

The new recovery and temporal-inheritance modules are not tuned against the remaining sweep outcomes.

The development sweep first establishes the session/geometry map. Only afterward will reference construction, break definition, recovery excursion, sustain rule, and temporal target definitions be frozen for market-data application.

The historical 3-5 reclaim attempts remain descriptive of the user's trading process, not a scientific event threshold.

## Decision after sweep

After the phase index is produced:
1. run the frozen same-phase modal comparison;
2. record whether PC1/PC2 geometry is recurrent, state-dependent, or non-replicating;
3. characterize session-phase dependence of forward-risk associations without forcing a universal sign;
4. leave chi admitted or refused exactly as the production engine returns it;
5. decide whether there is enough development stability to freeze the first recovery/inheritance market-data experiment;
6. only then prepare the confirmatory record that would permit opening June 9-11.

A negative or mixed sweep does not trigger retuning. It narrows the claim or redirects the Function/Limit Map.
