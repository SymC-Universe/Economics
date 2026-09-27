# MNQ May 28 Mature Reorganization Result

Date: 2026-09-27
Stage: P0-D development follow-up
Holdout: SEALED_NOT_ACCESSED
Source code commit: `527c9a05cbb7a4a0a005173b31d684ac700f661e`
Time basis: ordinary UTC wall-clock

## Question

The multiday development sweep identified May 28 mature as the only mature day with negative total-depth forward-risk association at all five horizons and the weakest full-window half-subspace stability. The frozen follow-up asked whether that anomaly was a whole-session state or a time-local reorganization.

## Result

It is not a whole-session state.

### 00:00-06:00 UTC: canonical stable architecture

The first two 3-hour windows preserve the expected native structure:
- PC1 symmetric-depth alignment 0.9306 then 0.9950;
- PC2 imbalance alignment 0.8921 then 0.9542;
- within-window top-2 minimum principal cosine 0.9560 then 0.9865;
- top-2 similarity to the full May 28 mature reference 0.9749 then 0.9738;
- total-depth forward-risk association negative at all five horizons;
- chi admissions 0/42 in each window.

### 06:00-12:00 UTC: leading-subspace reorganization

The 06:00-09:00 window undergoes the sharpest early disruption:
- PC1 symmetric-depth alignment falls to 0.4136;
- PC2 imbalance alignment falls to 0.1548;
- PC1-total-depth Spearman falls to -0.4019;
- within-window top-2 minimum principal cosine falls to 0.1692;
- top-2 similarity to the full-day reference falls to 0.2390;
- canonical depth-gradient and side-gradient alignments also weaken;
- total-depth forward-risk remains negative at all horizons;
- chi remains refused.

The 09:00-12:00 window partially reconstructs the canonical modes but remains unstable:
- PC1 symmetric-depth alignment 0.8165;
- PC2 imbalance alignment 0.7542;
- within-window top-2 minimum principal cosine 0.3545;
- top-2 similarity to full-day reference 0.8631;
- total-depth forward-risk remains negative.

Adjacent top-2 minimum principal cosine drops from 0.9981 for 00:00-03:00 vs 03:00-06:00 to 0.2068 for 03:00-06:00 vs 06:00-09:00, then 0.3407 for 06:00-09:00 vs 09:00-12:00.

### 12:00-15:00 UTC: canonical reconstruction with risk-sign reversal

The 12:00-15:00 window sharply reconstructs:
- PC1 variance rises to 0.3496;
- PC1 symmetric-depth alignment 0.9861;
- PC2 imbalance alignment 0.9826;
- PC1-total-depth Spearman 0.9842;
- within-window top-2 minimum principal cosine 0.9790;
- top-2 similarity to full-day reference 0.9629.

At the same time, total-depth forward-risk association flips positive at all five horizons and spread flips negative. This is the first 3-hour window in the day with the mature-session sign pattern seen on four of the five development days.

### 15:00-18:00 UTC: canonical semantics but internal instability

The 15:00-18:00 window retains strong semantic axes:
- PC1 symmetric-depth alignment 0.9861;
- PC2 imbalance alignment 0.9568;
- PC1-total-depth |Spearman| 0.9711.

Yet its within-window top-2 minimum principal cosine is only 0.1480. The total-depth risk sign returns negative at all horizons. Thus semantic identity can be retained while the leading subspace reorganizes internally.

### 18:00-21:00 UTC: rank reorganization

The final 3-hour window is structurally different again:
- PC1 becomes extremely dominant, 47.10% variance;
- PC1 remains symmetric-depth aligned at 0.9886 and total-depth correlated at 0.9920;
- the imbalance mode is no longer PC2; the strongest imbalance alignment is PC3 at 0.9254;
- PC2 instead carries a depth-gradient alignment of 0.7673;
- within-window top-2 minimum principal cosine is 0.8229;
- top-2 similarity to the full-day reference is only 0.1762 because the canonical imbalance direction has moved out of the top-two subspace;
- total-depth risk returns positive at all horizons.

This is a modal-rank reorganization, not disappearance of the underlying imbalance direction.

## Seven-hour sensitivity

The coarser windows support the same interpretation:
- 00:00-07:00 is strongly canonical and internally stable, top-2 minimum cosine 0.9915.
- 07:00-14:00 preserves full-window top-2 similarity (~0.9734) but is internally unstable, top-2 minimum cosine 0.1842.
- 14:00-21:00 is internally stable, top-2 minimum cosine 0.9893, but its top-2 similarity to the full-day reference is only 0.1096 because the modal ordering has reorganized.

The adjacent 7-hour top-2 minimum cosine is 0.9634 between the first and middle blocks, then 0.0593 between the middle and final blocks.

## Scalar chi

All ten analyzed windows report zero chi admissions. The reorganization is therefore visible in native modal/vector structure without requiring a licensed scalar chi.

## Interpretation

May 28 is best described at P0-D as a **sequence of native modal reorganizations**:
1. stable canonical architecture;
2. loss/reordering of the leading canonical subspace around 06:00-12:00;
3. reconstruction around 12:00-15:00 with forward-risk sign reversal;
4. another internal reorganization during 15:00-18:00;
5. late-session rank reorganization in which liquidity remains PC1 while imbalance shifts to PC3.

This is stronger than the earlier whole-session outlier description and explains why the 21-hour aggregate had poor half-session stability.

The next question is native: what changes in book depth, spread, imbalance, event activity and trade flow accompany these structural transitions? That question will be localized without using the forward-risk sign to choose boundaries.

No confirmatory or trading claim is made.
