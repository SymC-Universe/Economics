# MNQ May 28 Native Driver Localization Plan

Date frozen: 2026-09-27
Stage: P0-D development follow-up
Holdout: June 9-11 remains sealed
Source day: May 28, 2026 mature session only
Time rule: ordinary UTC wall-clock

## Trigger

The frozen 3-hour/7-hour follow-up localized multiple modal reorganizations within May 28. The next question is whether those changes co-occur with measurable changes in native order-book and flow variables.

## Independence rule

Structural localization is based on the L10 modal geometry and ordinary wall-clock windows only.

Forward-risk signs are not used to choose windows, detect transitions, set thresholds, or rank candidate change points. They may be overlaid only after the native structural and flow trajectories are produced.

## Frozen windows

Primary:
- 21 non-overlapping 60-minute windows from 00:00 through 21:00 UTC.

Sensitivity:
- 42 non-overlapping 30-minute windows over the same interval.

A window is analyzed only when coverage is at least 0.80 and the requested start state is observed.

## Native structural outputs

For each window:
- PC1 through PC6 variance fractions;
- top-two loading subspace;
- PC rank and alignment of symmetric-depth, bid/ask-imbalance, depth-gradient and side-gradient bases;
- PC1 association with native total depth;
- strongest-PC association with native depth imbalance;
- adjacent-window top-two principal cosines;
- top-two principal cosine to the full May 28 mature reference.

No post-result structural threshold is introduced.

## Native driver outputs

For each window:
- total-depth median, mean, standard deviation and IQR;
- spread median, mean and 90th percentile;
- L10 imbalance median and IQR;
- event rows per second: mean, median and 90th percentile;
- trade-volume total and active-trade-second fraction;
- signed-trade-volume total;
- absolute signed-trade-volume total;
- mean absolute signed-trade-volume per second.

These are descriptive native observables, not causal labels.

## Transition summaries

For every adjacent pair:
- top-two principal cosine;
- change in PC1 variance;
- changes in the native-driver summaries above.

The result will identify which native variables move with the largest observed subspace changes, without claiming that those variables cause the reorganization.

## Outcome interpretation

Possible development interpretations include:
- flow-linked reorganization candidate;
- liquidity/depth-linked reorganization candidate;
- spread-state-linked candidate;
- mixed native-state transition;
- structural reorganization without a clear native scalar driver.

If no single driver tracks the modal transition, that is retained rather than forcing a scalar explanation.

Scalar chi is not part of this experiment and remains governed by the unchanged production licensing rules.
