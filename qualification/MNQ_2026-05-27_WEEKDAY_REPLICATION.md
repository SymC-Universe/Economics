# MNQ MBP-10 Weekday Replication: 2026-05-27

Status: P0-D replication / P0-Q screening
Instrument request: `MNQ.c.0`
Resolved instrument_id: `42004936`
Extractor: `mnq-mbp10-first-pass-v2`
Source SHA-256: `4937650f9dba2bae44bb82b75afbaddeae7fabac1c1e41bd8be1c566feb5023b`
Derived feature SHA-256: `7642e03f2473f093bdc0f292edc1709ff4eb3207472807da19d27e9d47ae81a9`
Analysis interval selected by the frozen high-coverage rule: 2026-05-27 00:00:00 UTC through 21:00:00 UTC (end-exclusive)
Holdout status: June 9-11 MBP-10 remains sealed and was not inspected.

## Loader qualification

The v2 streaming extractor read 37,491,279 raw MBP-10 rows and emitted 82,713 one-second feature bins for the calendar-day file.

- event-time rows out of order: 0
- actual instrument IDs: one (`42004936`)
- mapped symbols: one (`MNQ.c.0`)
- bad-book flag rows: 0
- bad-receive-time flag rows: 1
- synthetic snapshot rows: 1

The automatically selected analysis block contains 75,600 dense seconds, 75,523 event-bearing seconds, and 77 carry-forward seconds, for 99.8981% event-second coverage.

## Weekday modal replication

The same 20-dimensional L10 size vector used on May 31 was transformed by `log1p`, standardized, and decomposed by SVD/PCA.

Explained variance:

| Mode | May 27 | May 31 discovery |
|---|---:|---:|
| PC1 | 29.6425% | 39.1572% |
| PC2 | 7.8434% | 9.5518% |
| PC1+PC2 | 37.4859% | 48.7090% |

Despite lower variance concentration, the leading modes retain the same native semantics.

### PC1: symmetric depth / liquidity mode

- May 27 symmetric-depth basis alignment: 0.9843
- May 27 Spearman relationship with total L10 depth: -0.9835

The sign of a PCA eigenvector is arbitrary. Therefore the negative correlation does not indicate a reversed semantic mode; orienting PC1 toward positive total depth gives the same liquidity/depth interpretation as May 31.

### PC2: bid-versus-ask imbalance mode

- May 27 bid-minus-ask basis alignment: 0.9782
- May 27 Spearman relationship with L10 depth imbalance: +0.9580

### PC3 and PC4

May 27 provides additional interpretable geometry beyond the first two modes:

- PC3 alignment with depth-gradient basis: 0.7845
- PC4 alignment with side-gradient basis: 0.7082

These are discovery observations only and are not yet promoted as stable Χ components.

## Within-day subspace stability

The 21-hour selected block was split into two halves and decomposed independently.

- top-2 principal cosine 1: 0.9934
- top-2 principal cosine 2: 0.9209
- minimum top-2 principal cosine: 0.9209

The leading two-dimensional depth subspace therefore remains strongly aligned across the weekday block, although less tightly than the shorter May 31 Sunday-open interval (minimum cosine 0.9797).

Interpretation: the two-axis liquidity/imbalance geometry replicates, while the amount of variance concentrated into that subspace is state- and/or session-phase dependent.

## Χ versus χ replication

The production χ screen was again applied to:

- log total depth;
- depth imbalance;
- spread;
- depth PC1;
- depth PC2;
- depth PC3;

at 1, 2, 5, 10, 15, 30, and 60 second sampling intervals.

**χ admissions: 0 of 42 screens.**

Thirty-five screens admitted an AR(2) discrete factor but refused canonical χ because one discrete pole was negative, creating continuous-time logarithm / alias ambiguity. Seven coarser screens preferred AR(0) or AR(1).

Examples at 1 second:

| Series | AR2 BIC gain | Discrete poles | χ result |
|---|---:|---|---|
| log total depth | 7091.91 | +0.9538, -0.3140 | REFUSED |
| spread | 3745.72 | +0.6047, -0.3642 | REFUSED |
| depth PC1 | 8613.18 | +0.9648, -0.3404 | REFUSED |
| depth imbalance | 3458.08 | +0.8108, -0.2612 | REFUSED |
| depth PC2 | 3559.93 | +0.7777, -0.2763 | REFUSED |

This independently reproduces the May 31 result that strong native second-order *discrete* structure does not automatically license the canonical damped-oscillator χ interpretation.

## Forward-risk finding: replication of channel, not sign

The May 31 discovery suggested deeper books preceded smaller near-term price-path movement and wider spreads preceded larger movement. May 27 does **not** reproduce those signs in its automatically selected block.

Spearman association with forward realized path movement:

| Predictor | 1 s | 5 s | 10 s | 30 s | 60 s |
|---|---:|---:|---:|---:|---:|
| total L10 depth | +0.182 | +0.294 | +0.330 | +0.373 | +0.390 |
| depth PC1 (raw sign) | -0.197 | -0.319 | -0.357 | -0.403 | -0.421 |
| spread | -0.112 | -0.180 | -0.200 | -0.228 | -0.238 |
| L10 depth imbalance | -0.058 | -0.097 | -0.106 | -0.121 | -0.120 |

Because May 27 PC1 is oriented negatively with total depth, its raw-sign risk association is consistent with the total-depth result after sign orientation. The substantive result is therefore that greater depth is associated with *more* subsequent path movement in this selected May 27 interval, opposite the May 31 discovery interval.

This falsifies any immediate general claim that `greater depth -> quieter future path` or `wider spread -> larger future path` across all MNQ states.

## Session-phase confound identified

The two analyses do not cover equivalent parts of the Globex session:

- May 31 discovery: 22:00-24:00 UTC, the opening two hours of the Sunday session;
- May 27 automatic weekday block: 00:00-21:00 UTC, the later portion of a regular daily session.

For late-May Central Daylight Time, CME equity-index futures trade approximately 22:00 UTC through 21:00 UTC with a 21:00-22:00 UTC maintenance interval. Therefore the forward-risk sign reversal may reflect session phase, liquidity regime, event environment, or another state variable rather than failure of the modal geometry itself.

The next experiment must compare like-for-like fixed session phases before any predictive direction is frozen.

## Replication conclusion

What replicated:

1. A dominant symmetric depth/liquidity mode.
2. A second bid-versus-ask imbalance mode.
3. A strongly aligned leading two-dimensional book subspace.
4. Canonical scalar χ refusal across all 42 screened series/resolutions.
5. Weak directional-price associations relative to capacity/risk associations.

What did not replicate:

1. The sign of the depth-to-forward-risk association.
2. The sign of the spread-to-forward-risk association.
3. The exact amount of variance concentrated in PC1+PC2.

The correct P0-D interpretation is therefore:

`native modal Χ geometry replicated; scalar χ remained unlicensed; forward-risk mapping is state/session dependent and not yet a portable rule.`

## Next gate

1. Compare fixed 22:00-24:00 UTC opening blocks across weekday development files.
2. Compare fixed 00:00-21:00 UTC mature-session blocks separately.
3. Keep the June 9-11 holdout sealed.
4. Freeze prediction/comparator logic only after the session-phase map is established.
5. Continue treating total depth as the native comparator for PC1 under ADDS/EQUIVALENT/SUBTRACTS/INDETERMINATE.
