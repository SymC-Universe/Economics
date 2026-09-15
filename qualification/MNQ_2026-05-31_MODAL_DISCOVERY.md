# MNQ MBP-10 Modal Discovery: 2026-05-31

Status: P0-D discovery / P0-Q screening
Instrument request: `MNQ.c.0`
Resolved instrument_id in source: `42004936`
Feature source SHA-256: `2e584ce4073303ec7d9ef2203026ccb2cf8d5e488b0af27a6cc0af00e60347eb`
Analysis interval: 2026-05-31 22:00:00 UTC through 2026-06-01 00:00:00 UTC (end-exclusive)
Holdout status: June 9-11 MBP-10 remains sealed and was not inspected.

## Why this interval

The source contains sparse pre-active records before 22:00 UTC with extremely wide spreads. At 22:00 UTC event density changes abruptly into a nearly continuous active book. The modal analysis therefore treats the 22:00-24:00 UTC block as the first discovery interval rather than pooling structurally different recording/market states.

- Dense seconds in interval: 7,200
- Seconds containing one or more recorded events: 7,125
- Carry-forward seconds with no event: 75
- Event-second coverage: 98.9583%

Book state is carried forward through eventless seconds; event/flow quantities remain zero in those seconds.

## First native modal result

A 20-dimensional book-depth vector was formed from last observed bid/ask size at levels 0-9. Each component was transformed with `log1p`, standardized, and decomposed by SVD/PCA.

Explained variance:

| Mode | Variance share |
|---|---:|
| PC1 | 39.1572% |
| PC2 | 9.5518% |
| PC3 | 4.4120% |
| PC4 | 4.3435% |
| PC5 | 3.9438% |
| PC1+PC2 | 48.7090% |

PC1 is nearly a symmetric depth/liquidity mode:

- absolute loading alignment with equal-weight symmetric depth basis: 0.9924
- Spearman correlation with total L10 depth: +0.9805

PC2 is nearly a bid-versus-ask imbalance mode:

- absolute loading alignment with bid-minus-ask basis: 0.9364
- Spearman correlation with L10 depth imbalance: +0.9542

PC3 begins to carry depth-gradient / side-gradient geometry rather than another copy of total depth or side imbalance.

## Within-interval stability

The 22:00-23:00 and 23:00-24:00 UTC halves were decomposed independently. Mode ordering changes between halves, so single-PC labels are not treated as invariant. The *two-dimensional leading subspace* is stable:

- principal cosine 1: 0.9917
- principal cosine 2: 0.9797
- minimum top-2 principal cosine: 0.9797

This is evidence that a two-axis native book geometry is reproducible within this discovery interval, while the decline in the leading eigenvalue in the second hour shows that variance concentration itself is time-varying.

## Χ versus χ result

The native book structure exists before scalar χ is considered. The current production χ gate was applied to log total depth, depth imbalance, spread, and the first three depth PCs at 1, 2, 5, 10, 15, 30, and 60 second sampling intervals.

**χ admissions: 0.**

At one second, several series strongly prefer AR(2) to AR(0)/AR(1) by the current exploratory BIC gate, but the fitted discrete second-order factors contain one positive and one negative real propagation pole. The production χ mapper refuses these cases because a negative real discrete pole introduces alias ambiguity under the continuous logarithmic embedding.

Examples at 1 s:

| Series | AR2 BIC gain vs best simple | Discrete poles | χ result |
|---|---:|---|---|
| log total depth | 537.90 | +0.9714, -0.2782 | REFUSED |
| spread | 849.80 | +0.7924, -0.4187 | REFUSED |
| depth PC1 | 649.88 | +0.9747, -0.3034 | REFUSED |
| depth imbalance | 213.57 | +0.7986, -0.2189 | REFUSED |
| depth PC2 | 165.55 | +0.7944, -0.1956 | REFUSED |

The same refusal pattern persists for the dominant liquidity/spread modes over the screened 1-60 s resolutions. Some weaker modes revert to AR(1)/AR(0) as sampling is coarsened.

Interpretation ceiling: this is **not** evidence against Χ. It is direct evidence that native modal/vector Χ structure can be detectable while canonical scalar χ is not licensed. The alternating discrete component may reflect microstructure dynamics, sampling effects, or another native mechanism; it must not be relabeled as damped oscillation without resolving that ambiguity.

## Exploratory forward associations

These are P0-D associations only. No iid p-values are used, overlapping horizons are not treated as independent observations, and no predictive claim is made.

Spearman association with forward realized price-move magnitude (`sqrt(sum Δmid^2)`):

| Predictor | 1 s | 5 s | 10 s | 30 s | 60 s |
|---|---:|---:|---:|---:|---:|
| depth PC1 | -0.234 | -0.363 | -0.395 | -0.471 | -0.505 |
| total L10 depth | -0.231 | -0.359 | -0.393 | -0.463 | -0.491 |
| spread | +0.139 | +0.243 | +0.272 | +0.300 | +0.328 |
| L10 depth imbalance | -0.043 | -0.084 | -0.105 | -0.129 | -0.155 |

The strongest discovery signal is therefore not direction. It is **market capacity / near-term risk**: deeper books correspond to smaller subsequent price-path movement, while wider spreads correspond to larger subsequent movement. PC1 carries essentially the same information as total depth on this first day, which is important for the later ADDS/EQUIVALENT test.

Directional associations are much weaker. The largest is L1 imbalance versus the next one-second price change (Spearman about +0.127) and decays rapidly with horizon. This supports keeping direction separate from stability/capacity rather than assuming Χ or χ determines sign.

## Extractor defect found and contained

The first-pass extractor used the positive-price scaling helper for signed microprice offsets. That helper rejects values `<= 0`, so negative and zero microprice offsets were emitted as `NaN`.

This does not affect the depth PCA, total depth, imbalance, spread, trade-flow, or χ-screen results above. The exact last-state microprice offset is reconstructible as:

`microprice_offset_last = 0.5 * spread_last * l1_imbalance_last`.

The mean microprice offset cannot in general be reconstructed exactly from the product of aggregate means, so future raw extraction must use the corrected signed scaler. This defect is a release blocker for the microprice channel but not for the modal result reported here.

## Next scientific step

1. Correct and regression-test signed microprice extraction.
2. Run the same feature engine on a normal weekday development file (May 27 first) without opening the June 9-11 holdout.
3. Test whether the two-axis depth subspace replicates across weekdays and whether its orientation/variance concentration changes with market state.
4. Add native heteroskedastic/state-space alternatives before any lowercase χ promotion.
5. Treat total depth as the native comparator for PC1. A modal claim must show value beyond the simpler depth scalar to earn `ADDS`; otherwise the correct result is `EQUIVALENT`.
6. Build dependence-aware forward-risk validation only after the discovery geometry is frozen.

## Current interpretation

The first empirical result favors the revised architecture:

`native MBP-10 -> stable depth/liquidity + imbalance modal subspace -> Χ structure -> χ refused where not licensed`.

Damped oscillation did not need to be assumed to obtain an interpretable stability architecture, and the refusal gate prevented an AR(2) fit from being over-interpreted as canonical χ.
