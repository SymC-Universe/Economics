# MNQ May 28 Mature Reorganization Plan

Date frozen: 2026-09-27
Stage: P0-D follow-up
Source: development data only
Holdout: June 9-11 remains sealed

## Trigger

The fixed-session development sweep identified May 28 00:00-21:00 UTC as the only mature development day with negative total-depth forward-risk association at all five tested horizons. The same window also had the weakest within-window top-2 half-subspace cosine (0.6480), while its full-window PC1/PC2 semantics and cross-day subspace remained strongly aligned.

This combination is retained as a potential within-session reorganization rather than treated as an exclusion or tuning target.

## Time rule

All segmentation is ordinary UTC wall-clock time. No market-dependent rescaling of seconds is used.

## Frozen windows

Primary:
- seven non-overlapping 3-hour windows covering 00:00-21:00 UTC.

Sensitivity:
- three non-overlapping 7-hour windows covering 00:00-21:00 UTC.

A window is analyzed only if coverage is at least 0.80 and its requested start is observed.

## Outputs

For each window:
- PC1/PC2 variance and semantic alignments;
- best depth-gradient and side-gradient alignment among the first six PCs;
- top-2 within-window half-subspace cosine;
- production chi admissions/refusals under the unchanged 1-60 s screen;
- forward-risk Spearman association for native total depth, spread, L10 imbalance and PC1;
- PC1/native-total-depth semantic association.

Cross-window:
- top-2 principal cosines to the full May 28 mature reference;
- adjacent-window top-2 principal cosines;
- sign and magnitude trajectory of total-depth forward-risk association;
- location of the largest adjacent modal change and any risk-sign transition.

## Interpretation limits

No principal-cosine threshold, risk threshold, or transition boundary is introduced after viewing the subwindows. Continuous values are reported first.

A time-local change is a development reorganization candidate only. It does not establish causality, a universal session regime, a trading rule, or scalar chi.

If the May 28 anomaly is stable across all subwindows, the outlier remains a whole-session state. If it localizes to a subset of windows, the next question becomes what native flow/liquidity change accompanies that transition.

June 9-11 remains sealed regardless of outcome.
