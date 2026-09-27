# MNQ Development Sweep v3 Same-Phase Result

Date: 2026-09-27
Stage: P0-D / P0-Q development evidence
Source commit: `22dbccf2cb7f1921598c72715f4d7c232932c456`
Holdout: `SEALED_NOT_ACCESSED`

## Data integrity

The v3 manifest records May 27, May 28, May 29, June 1 and June 2 development data. The truncated external May 27 cache was detected, left untouched, rebuilt from the raw development .zst, and verified by gzip EOF/CRC and SHA-256. June 9-11 was not referenced or opened.

Nine fixed phase windows were analyzable. May 29 22:00-24:00 UTC had zero coverage and was skipped under the frozen coverage rule.

## Native modal geometry

Across the nine complete phase windows:
- PC1 symmetric-depth alignment: 0.9550-0.9924.
- PC2 bid/ask-imbalance alignment: 0.9246-0.9791.
- absolute Spearman association of PC1 with native total depth: 0.9366-0.9906.
- same-phase cross-day top-2 minimum principal cosine: 0.9686-0.9937, median 0.9899.

The recurrent liquidity/depth plus side-imbalance subspace therefore survives same-phase cross-day comparison. The depth-gradient family also recurs in every complete phase, although its order swaps between PC3 and PC4. The side-gradient family recurs with weaker and more variable order/strength.

## Scalar chi

Production chi admission remained fully refused:
- 0 admissions in 378 screens.
- 288 screens supported AR2 but were refused because a negative real discrete pole leaves continuous-embedding alias ambiguity.
- 90 screens preferred AR0/AR1 under the existing BIC-margin rule.

The development result therefore strengthens the distinction between reproducible modal/vector Chi structure and canonical scalar chi licensing.

## Session-phase control

For native total depth across all five forward horizons (1, 5, 10, 30, 60 s):
- mature: 4 of 5 days were positive at every horizon; May 28 was negative at every horizon.
- session open: all 4 available days were negative at every horizon.

Spread mostly moved oppositely:
- mature: 4 of 5 days were negative at every horizon; May 28 was mixed/positive at longer horizons.
- session open: 3 of 4 days were positive at every horizon; June 2 was negative.

Session phase therefore materially conditions the forward-risk map, but it is not a complete two-regime law. May 28 mature is retained as an exception/outlier rather than removed or retuned away.

## PC1 versus native total-depth comparator

After orienting PC1 to the sign of native total depth:
- mean absolute difference between PC1 and total-depth forward-risk Spearman values = 0.0136.
- maximum absolute difference = 0.0376.
- |rho|(PC1, total depth) = 0.9366-0.9906 across complete phases.

Comparator outcome: **EQUIVALENT at P0-D**. PC1 remains useful as a structural mode, but current development evidence does not show incremental forward-risk information beyond native total depth.

## Outlier retained

May 28 mature is the main development outlier:
- only mature day with negative total-depth risk across all horizons;
- weakest within-window top-2 half-subspace cosine, 0.6480;
- yet full-window PC1/PC2 semantics and same-phase cross-day subspace remain strongly aligned.

This pattern motivates a targeted time-local reorganization test on May 28 rather than discarding the day.

## Development decision

Q023 session-phase control is complete at P0-D.

Next development action:
1. inspect May 28 mature using frozen wall-clock subwindows to test whether the anomalous sign accompanies an internal structural transition;
2. freeze market-data definitions for failed-recovery trajectories and temporal substrate inheritance;
3. keep June 9-11 sealed until the first diagnostic/predictive question and failure criteria are frozen.

No P1 promotion is made from this development sweep.
