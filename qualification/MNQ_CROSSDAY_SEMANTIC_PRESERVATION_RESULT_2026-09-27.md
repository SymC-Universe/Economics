# MNQ Cross-Day Semantic Preservation Result

Date: 2026-09-27
Stage: P0-D development replication
Qualification gate: Q037
Source artifact SHA-256: `5558f21077f442b684055045e51616ba8d9c3d673e1c6f2dec1a138225899ab0`
Source code commit: `31b949d75efe5ba3010737193864f52a8245a47c`
Holdout: `SEALED_NOT_ACCESSED`
Time basis: ordinary UTC wall-clock

## Frozen analysis executed

The received artifact contains all 252 prespecified development windows:

- May 27: 21 hourly + 42 half-hour windows;
- May 29: 21 hourly + 42 half-hour windows;
- June 1: 21 hourly + 42 half-hour windows;
- June 2: 21 hourly + 42 half-hour windows.

All 252 windows are COMPLETE. Fixed leading subspaces were evaluated at k = 2, 3, 4, 6, and 10. The frozen isotropic control used 256 fixed random unit directions in d = 20 with seed 20260927. No adaptive k was used.

## Primary disposition

**PASS P0-D: RECURRENT SEMANTIC BACKBONE; RANK MIGRATION IS RECURRENT BUT NOT UNIVERSAL.**

The central Q037 question is resolved positively at the development level: the symmetric-depth / bid-ask-imbalance semantic backbone is substantially more stable across mature-session MNQ than individual principal-component rank identity.

The stronger statement that rank migration itself occurs every day is rejected.

## Full-day references

Across all four previously unseen development days, the full mature-session references recover symmetric depth and bid-ask imbalance strongly.

At k = 2:
- May 27: symmetric depth 0.9719; imbalance 0.9596.
- May 29: symmetric depth 0.9729; imbalance 0.9042.
- June 1: symmetric depth 0.9708; imbalance 0.9592.
- June 2: symmetric depth 0.9820; imbalance 0.9397.

For both canonical directions, the empirical percentile against the frozen 256-direction isotropic control is 1.0 on every full-day reference and at every frozen k = 2, 3, 4, 6, 10.

The isotropic control behaves as expected from dimension: its mean capture remains near k/20.

## Window-level replication

Define the descriptive core capture as the weaker of symmetric-depth and bid-ask-imbalance capture. This is not a new threshold or admission rule.

Across all four days:

### 60-minute windows, n = 84

- median core capture:
  - k=2: 0.8980
  - k=6: 0.9510
  - k=10: 0.9749
- 5th percentile core capture:
  - k=2: 0.0078
  - k=6: 0.8384
  - k=10: 0.9128
- minimum core capture:
  - k=2: 0.0001
  - k=6: 0.4973
  - k=10: 0.7316
- both canonical directions exceed the frozen isotropic q95 in:
  - 83/84 windows at k=6
  - 82/84 windows at k=10

### 30-minute windows, n = 168

- median core capture:
  - k=2: 0.8794
  - k=6: 0.9371
  - k=10: 0.9656
- 5th percentile core capture:
  - k=2: 0.0122
  - k=6: 0.6847
  - k=10: 0.8753
- minimum core capture:
  - k=2: 0.0002
  - k=6: 0.0213
  - k=10: 0.6781
- both canonical directions exceed the frozen isotropic q95 in:
  - 162/168 windows at k=6
  - 164/168 windows at k=10

The widening-subspace recovery is therefore not an artifact of random orientation alone.

## Rank migration is state-dependent, not universal

The strongest-mode rank of either symmetric depth or imbalance leaves the leading two PCs with the following frequencies:

### 60-minute
- May 27: 4/21 windows.
- May 29: 6/21.
- June 1: 0/21.
- June 2: 0/21.

### 30-minute
- May 27: 11/42.
- May 29: 12/42.
- June 1: 0/42.
- June 2: 3/42.

Thus rank migration replicates independently on May 27 and May 29, is sparse on June 2, and is absent on June 1. It is a recurrent state-dependent phenomenon, not a universal property of every mature session.

## Preserved failures and localized disturbances

The replication also falsifies any claim that the core semantic backbone is perfectly preserved at every fixed k.

### May 27

At 09:30-10:00 UTC:
- top-two core capture collapses to 0.0003;
- k=6 recovers the pair to a weaker-member capture of 0.5625;
- k=10 recovers it to 0.8495.

At 10:30-11:00 UTC:
- symmetric-depth capture remains only 0.3402 at k=6;
- it recovers to 0.8850 at k=10;
- imbalance is already 0.9049 at k=6.

### May 29

This day contains the strongest cross-day localized disturbance.

At 08:30-09:00 UTC:
- symmetric-depth capture is 0.0851 at k=6 and 0.6781 at k=10;
- imbalance is 0.8327 at k=6 and 0.8782 at k=10.

At 10:00-10:30 UTC:
- symmetric-depth capture is only 0.0213 at k=6 and 0.7434 at k=10;
- imbalance is 0.7682 at k=6 and 0.8010 at k=10.

This is a genuine partial semantic disturbance, not merely a PC2/PC3 label swap.

### June 1

June 1 is the clean counterexample to universal rank migration.

Its weakest 30-minute core capture remains:
- 0.7171 at k=2;
- 0.8284 at k=6;
- 0.9271 at k=10.

No canonical strongest mode leaves the leading two PCs at either 60-minute or 30-minute resolution.

### June 2

June 2 is intermediate.

At 10:30-11:00 UTC:
- top-two core capture falls to 0.0296;
- k=6 recovers to 0.6959;
- k=10 recovers to 0.9104.

Rank migration is otherwise sparse.

## Relation to May 28

May 28 is not unique.

Its Q036 minima were:
- 60-minute: core 0.7062 at k=6 and 0.8676 at k=10;
- 30-minute: core 0.2866 at k=6 and 0.7541 at k=10.

May 29 contains a sharper local disturbance than May 28, while June 1 is substantially more stable. The cross-day result therefore supports a layered state-dependent architecture rather than a single anomalous-day story.

## Exploratory wall-clock pattern

A post-hoc timing map, not part of the frozen Q037 pass/fail question, shows that the strongest top-rank disturbances on May 27, May 29 and June 2 cluster approximately in the 08:30-11:00 UTC interval. June 1 does not show the same collapse.

This is a candidate session-phase phenomenon, not yet a licensed mechanism. It must not be promoted from Q037 without a separately frozen test.

## Current interpretation

The development-level statement now licensed is:

> **Across five MNQ development sessions, the L10 symmetric-depth / imbalance semantic backbone is substantially more stable than individual PCA rank identity. Rank migration and partial semantic disturbance occur in a state-dependent manner, while wider fixed subspaces usually recover the canonical architecture well above isotropic-orientation controls.**

This supports a modal/vector description of local market organization. It does not establish market-wide Χ universality and it does not license scalar χ.

## Scalar χ

Scalar χ remains refused under the existing production rules. Q037 does not change that result.

## Next gate

Q038 may now be frozen as the first holdout-facing semantic-preservation diagnostic.

The holdout question must be specified completely before June 9-11 is opened, including:
- primary estimand;
- fixed k;
- isotropic comparator;
- wall-clock windows;
- exclusions;
- serial-dependence treatment;
- uncertainty method;
- explicit failure criteria;
- no tuning after holdout inspection.

The exploratory 08:30-11:00 UTC pattern may be carried as a separately labeled secondary diagnostic only if frozen before holdout access.
