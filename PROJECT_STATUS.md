# Market Χ Project Status

Date: 2026-09-14
Branch: `market-chi-architecture`
Stage: P0-D / P0-Q

## Scientific direction

The project no longer begins by assuming a damped oscillator. Uppercase Χ is the broader reconstructed market stability architecture. Lowercase χ is emitted only when a licensed local or modal second-order factor supports it.

## Current executable paths

Local scalar qualification scaffold:

`native series -> AR0/AR1/AR2 qualification scaffold -> pole inspection -> χ if licensed -> otherwise refusal`

Native MNQ microstructure path:

`Databento MBP-10 -> validated native fields -> contract segmentation -> quality/snapshot handling -> 10-level book vectors + trade/order-flow features -> modal/vector analysis -> χ only if later licensed`

The second path is now the preferred real-market development route. It preserves the native structure instead of reducing the market to a price oscillator first.

## Real data now locked

The user corpus has been identified as CME Globex `GLBX.MDP3` data for the Databento continuous calendar-front symbol `MNQ.c.0`:

- trades: `[2026-04-03, 2026-06-03)` with 52 returned daily files;
- development MBP-10: `[2026-05-27, 2026-06-03)` with returned files on May 27, 28, 29, 31 and June 1, 2;
- sealed MBP-10 holdout: `[2026-06-09, 2026-06-12)` with returned files June 9, 10 and 11.

The later MBP-10 block is frozen untouched at observation level in `qualification/HOLDOUT_FREEZE_2026-09-14.md`.

Databento continuous-contract prices are unadjusted. All real-data code must therefore segment by actual `instrument_id` and mapped `symbol` so a contract rollover cannot masquerade as a Χ transition or χ event.

## Legacy status

The July MarketFWv2 package is preserved as lineage. Its synthetic results remain P0-Q historical evidence, but the oscillator-first estimator is not inherited as authoritative because the audit found an observation-kernel inconsistency and insufficient refusal against simple alternatives.

## Immediate development sequence

1. Qualify the new MBP-10 loader on the already-uncompressed May 31 file.
2. Verify mapped contract identity, timestamps, flags, event ordering, spread/depth sanity, action/side semantics, and output hashes from the real data.
3. Build the first native depth-vector modal map from the May 31 derived stream.
4. Expand to the remaining May 27-June 2 development files after the compressed-file path is qualified.
5. Integrate the April 3-June 2 trade history as the longer execution-flow baseline.
6. Expand local model competition beyond AR0/AR1/AR2, with stochastic-volatility and heteroskedastic alternatives explicitly included.
7. Freeze the first diagnostic question, comparator, endpoint, exclusions, uncertainty, and failure criteria before opening the June 9-11 holdout.
8. Open the holdout only through the explicit qualification gate.
