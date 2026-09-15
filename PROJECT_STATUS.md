# Market Χ Project Status

Date: 2026-09-14
Branch: `market-chi-architecture`
Stage: P0-D / P0-Q

## Scientific direction

The project no longer begins by assuming a damped oscillator. Uppercase Χ is the broader reconstructed market stability architecture. Lowercase χ is emitted only when a licensed local or modal second-order factor supports it.

## Current executable paths

Local scalar qualification scaffold:

`native series -> AR0/AR1/AR2 qualification scaffold -> pole inspection -> χ if licensed -> otherwise refusal`

Preferred real-market path:

`Databento MBP-10 -> validated native fields -> contract segmentation -> quality/snapshot handling -> 10-level book vectors + trade/order-flow features -> modal/vector Χ analysis -> χ only if later licensed`

The native microstructure path is now operational. Extractor v2 streams `.csv.zst` directly and preserves signed microprice offsets.

## Real data locked

The user corpus is CME Globex `GLBX.MDP3` for Databento continuous calendar-front `MNQ.c.0`:

- trades: `[2026-04-03, 2026-06-03)` with 52 returned daily files;
- development MBP-10: `[2026-05-27, 2026-06-03)` with returned files on May 27, 28, 29, 31 and June 1, 2;
- sealed MBP-10 holdout: `[2026-06-09, 2026-06-12)` with returned files June 9, 10 and 11.

The June 9-11 block remains sealed at observation level in `qualification/HOLDOUT_FREEZE_2026-09-14.md`.

Databento continuous-contract prices are unadjusted. All real-data code segments by actual `instrument_id` and mapped `symbol` before dynamics are analyzed so a rollover cannot masquerade as a Χ transition or χ event.

## First real empirical result

The May 31 first pass read 725,631 MBP-10 rows and produced 7,225 one-second event bins with no event-time disorder, one actual instrument ID, no bad-book flags, and no contract-roll contamination.

A discovery interval from 22:00-24:00 UTC was densified to 7,200 one-second states (98.96% event-second coverage). PCA/SVD of the log-standardized 20-dimensional L10 size vector found:

- PC1: 39.16% variance, nearly symmetric total-depth/liquidity mode;
- PC2: 9.55% variance, nearly bid-versus-ask depth-imbalance mode;
- PC1+PC2: 48.71% variance;
- top-2 subspace principal cosines across the two one-hour halves: 0.9917 and 0.9797.

This is the first empirical modal/vector Χ structure in the rebuild.

## First Χ versus χ result

The production scalar gate was applied downstream to log total depth, spread, depth imbalance, and leading depth PCs at 1-60 second sampling intervals.

**No lowercase χ was admitted.**

Several one-second series strongly prefer an AR(2) representation to AR(0)/AR(1), but the fitted discrete factors contain a negative real pole. The χ mapper correctly refuses the canonical continuous second-order interpretation because of alias ambiguity.

This is a useful result, not a failure: modal/vector Χ structure exists in the real book while scalar χ is not licensed.

## First predictive-direction signal ceiling

Exploratory associations on May 31 suggest the strongest channel is near-term movement capacity/risk rather than direction:

- greater total depth / depth PC1 -> smaller subsequent price-path movement;
- wider spread -> larger subsequent price-path movement;
- direction associations are substantially weaker and decay quickly with horizon.

These are P0-D findings only. Overlapping windows have not been promoted to independent evidence and no predictive claim is made.

## Mechanical defect closed for future extraction

The v1 extractor incorrectly used a positive-price scaler for signed microprice offsets, causing negative and zero offsets to become `NaN`. This does not affect the first depth-modal result. Extractor v2 now has separate positive-price and signed-value scalers, streams compressed `.zst` directly, and passes a regression test covering positive, zero, and negative microprice offsets.

## Legacy status

The July MarketFWv2 package remains preserved as lineage. Its oscillator-first estimator is not authoritative because the audit found an observation-kernel inconsistency and inadequate refusal against native alternatives.

## Immediate development sequence

1. Run extractor v2 on a normal weekday development file, May 27 first.
2. Replicate or falsify the May 31 two-axis depth geometry across weekdays.
3. Compare PC1 directly against total depth under the GOM `ADDS / EQUIVALENT / SUBTRACTS / INDETERMINATE` framework.
4. Characterize the negative-pole microstructure component rather than relabeling it as damping.
5. Integrate the April 3-June 2 trades as the longer execution-flow baseline.
6. Expand candidate dynamics beyond AR0/AR1/AR2 to heteroskedastic, stochastic-volatility, state-space, jump, and regime-switching alternatives.
7. Freeze the first diagnostic/predictive question, comparator, endpoint, exclusions, uncertainty method, and failure criteria before opening the June 9-11 holdout.
8. Open the holdout only through the explicit qualification gate.
