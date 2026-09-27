# MNQ Cross-Day Semantic Preservation Plan

Date frozen: 2026-09-27
Stage: P0-D
Qualification gate: Q037
Holdout: June 9-11 remains sealed
Time basis: ordinary UTC wall-clock

## Question

Does the May 28 pattern, persistent native semantic backbone with unstable individual PC rank identity and localized partial disturbance, recur across the other mature development days?

The identifiability outputs for May 27, May 29, June 1 and June 2 have not been inspected under this fixed-k framework at plan freeze.

## Development days

Apply the same mature-session analysis to:

- 2026-05-27;
- 2026-05-29;
- 2026-06-01;
- 2026-06-02.

May 28 is not used to tune the cross-day outcome. Its Q036 result is the discovery comparison.

## Frozen windows

For each day:

Primary:
- 21 non-overlapping 60-minute windows from 00:00 through 21:00 UTC.

Sensitivity:
- 42 non-overlapping 30-minute windows over the same interval.

Coverage floor remains 0.80. Each requested start state must be observed.

## Frozen modal representation

Use the same 20-dimensional standardized log-depth PCA and the same fixed leading subspaces:

`k = {2, 3, 4, 6, 10}`

No adaptive k, post-result k selection, or tuned capture threshold is permitted.

## Canonical semantic directions

Use the previously defined L10 bases:

- symmetric depth;
- bid/ask imbalance;
- depth gradient;
- side gradient.

For each direction b and fixed k:

`C_k(b) = ||Q_k^T b||^2`

where `Q_k` spans the leading k loading subspace.

## Frozen isotropic-direction control

To prevent wider subspaces from appearing informative merely because dimension increases:

- feature dimension d = 20;
- random direction count = 256;
- NumPy generator seed = 20260927;
- generate 256 standard-normal vectors once, normalize each to unit length;
- reuse the exact same 256 directions for every day, window and k.

For each k and window record the random-direction capture distribution:
- mean;
- median;
- q05;
- q95;
- theoretical isotropic mean k/20.

For each canonical semantic direction also record its empirical percentile within the frozen random-direction capture set.

These percentiles are descriptive controls, not p-values. No multiplicity-adjusted significance or promotion threshold is introduced at this stage.

## Full-subspace preservation

For every fixed k:

1. compare each window with that day's 00:00-21:00 UTC full-day reference using principal cosines;
2. compare adjacent windows using principal cosines.

This remains sign- and within-subspace-rotation invariant.

## Cross-day interpretation

The output will be summarized without a tuned pass/fail threshold.

Evidence for a recurrent semantic backbone requires the canonical directions to remain systematically stronger than isotropic orientation controls across days while individual PC ranks and higher-order subspaces may vary.

Evidence against recurrence includes one or more days where canonical capture is not distinguishable descriptively from the fixed isotropic controls or where wider fixed subspaces fail to recover the semantic axes.

Localized disturbances are retained and mapped by wall-clock interval rather than excluded.

## Exclusions

Q037 does not:
- inspect June 9-11;
- alter scalar χ licensing;
- use forward-risk outcomes to select windows;
- tune k;
- introduce an adaptive semantic basis;
- establish market-wide universality;
- test a trading strategy.

## Promotion consequence

If the fixed semantic-preservation pattern replicates across the four unseen mature development days, the result licenses a development-level statement that the MNQ L10 semantic backbone is more stable than individual PC rank identity.

Only after that result is frozen may a holdout-facing diagnostic be specified. The June 9-11 block remains sealed until the full holdout question, comparator, endpoint, exclusions, uncertainty method and failure criteria are frozen.
