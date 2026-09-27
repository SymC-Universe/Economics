# MNQ May 28 Modal Identifiability / Rank-Migration Plan

Date frozen: 2026-09-27
Stage: P0-D
Holdout: June 9-11 remains sealed
Source day: May 28, 2026 mature interval only
Time basis: ordinary UTC wall-clock

## Trigger

The May 28 native-driver localization found that no single native scalar jump consistently explains adjacent top-two subspace changes. The strongest observed relationship is instead between top-two stability and PC2-PC3 spectral separation. In several low-top-two-similarity windows, the symmetric-depth and imbalance directions remain strongly identifiable at lower PC ranks.

This creates two competing interpretations:

1. **broader architecture loss / genuine higher-dimensional reorganization**;
2. **rank redistribution or reduced modal identifiability under near-degenerate eigenvalues**.

The present experiment distinguishes those possibilities without changing the native representation.

## Frozen windows

Primary:
- 21 non-overlapping 60-minute windows from 00:00 through 21:00 UTC.

Sensitivity:
- 42 non-overlapping 30-minute windows over the same interval.

Coverage floor remains 0.80. The requested start state must be observed.

## Frozen modal subspaces

For every window use the full 20-dimensional standardized log-depth PCA.

Evaluate only these fixed leading subspaces:

`k = {2, 3, 4, 6, 10}`

No adaptive k, post-result k selection, or threshold tuning is permitted in this test.

## Semantic bases

Use the already defined native L10 bases:

- symmetric depth;
- bid/ask imbalance;
- depth gradient;
- side gradient.

For each semantic unit vector b and fixed k, calculate sign/rotation-invariant subspace capture:

`C_k(b) = ||Q_k^T b||^2`

where `Q_k` is an orthonormal basis for the leading k loading subspace.

Interpretation:
- capture near 1 means the semantic direction lies largely inside that fixed subspace;
- capture near 0 means it lies largely outside;
- no universal threshold is introduced here.

## Spectral diagnostics

For every window record:

- all 20 variance fractions;
- cumulative variance at k = 2, 3, 4, 6, 10;
- adjacent eigengaps through at least PC6;
- relative eigengaps;
- spectral entropy;
- normalized spectral entropy;
- effective rank.

These are identifiability diagnostics, not scalar χ.

## Subspace comparisons

For every fixed k:

1. compare each window with the full May 28 mature reference using principal cosines;
2. compare each adjacent pair of windows using principal cosines.

All comparisons are sign- and within-subspace-rotation invariant.

## Primary interpretation rule

The outcome remains descriptive at P0-D.

Evidence favors **rank migration / identifiability loss** when top-two similarity degrades while:
- one or more wider fixed-k subspaces remain substantially more preserved; and/or
- semantic-basis capture rises materially as k widens.

Evidence favors **broader reorganization** when:
- wider fixed-k subspaces also lose preservation; and
- the semantic bases are not recovered by the wider fixed subspaces.

Mixed outcomes are retained as mixed.

No threshold is tuned after inspection to force either interpretation.

## Exclusions

This experiment does not:
- use forward-risk signs to identify transitions;
- alter χ admission;
- infer a causal native scalar driver;
- open the June 9-11 holdout;
- test a trading rule;
- establish market-wide universality.

## Promotion consequence

After this May 28 identifiability question is resolved, the same fixed metrics may be applied without modification to May 27, May 29, June 1, and June 2 mature development data.

Only after that cross-day development replication may this modal-identifiability pattern be considered for a holdout-facing question.
