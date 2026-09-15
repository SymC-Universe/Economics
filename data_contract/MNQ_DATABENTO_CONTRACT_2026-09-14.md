# MNQ Databento Data Contract — 2026-09-14

## Acquisition

All supplied batches request Databento `GLBX.MDP3` for the continuous symbol `MNQ.c.0`, using `stype_in=continuous` and `stype_out=instrument_id`, `map_symbols=true`, raw fixed-precision prices (`pretty_px=false`) and raw nanosecond timestamps (`pretty_ts=false`).

### Trades development/history batch

- job: `GLBX-20260707-R8DPEBBKYS`
- schema: `trades`
- interval: `[2026-04-03T00:00:00Z, 2026-06-03T00:00:00Z)`
- manifest contains 52 returned trade-day files plus metadata/condition files.

### MBP-10 development batch

- job: `GLBX-20260707-AC64RNMSPL`
- schema: `mbp-10`
- interval: `[2026-05-27T00:00:00Z, 2026-06-03T00:00:00Z)`
- returned observation files: May 27, 28, 29, 31 and June 1, 2.
- May 31 is already present locally as an uncompressed CSV and is the first loader-qualification target.

### MBP-10 sealed holdout batch

- job: `GLBX-20260707-MJC5YBJBLU`
- schema: `mbp-10`
- interval: `[2026-06-09T00:00:00Z, 2026-06-12T00:00:00Z)`
- returned observation files: June 9, 10, 11.
- frozen separately in `qualification/HOLDOUT_FREEZE_2026-09-14.md`.

## Field conventions that the loader must preserve

- `ts_event`: matching-engine received time, nanoseconds since Unix epoch.
- `ts_recv`: Databento capture-server received time, nanoseconds since Unix epoch.
- prices: signed fixed-precision integers with scale `1e-9`; `UNDEF_PRICE=9223372036854775807` is not a physical price.
- MBP-10 actions: Add `A`, Modify `M`, Cancel `C`, Clear `R`, Trade `T`, None `N`.
- side `B` is bid/buy side and, for a trade, buy aggressor; side `A` is ask/sell side and, for a trade, sell aggressor; `N` means unspecified/indeterminate.
- `F_SNAPSHOT=32`: replay/snapshot-sourced record. It may initialize book state but must not be counted as endogenous market flow.
- `F_BAD_TS_RECV=8`: receive timestamp is unreliable.
- `F_MAYBE_BAD_BOOK=4`: unrecoverable channel gap; affected rows are excluded from derived book-state means in the first-pass extractor.

## Continuous-symbol safeguard

`MNQ.c.0` is Databento calendar-roll continuous symbology. It maps to an actual tradable contract and preserves original, unadjusted contract prices. Therefore:

- never calculate cross-roll returns as though the series were one adjusted instrument;
- segment derived state by `instrument_id` and mapped `symbol` before local dynamics are fit;
- a roll transition is a contract-mapping event, not evidence of a Χ transition or a χ boundary crossing.

## Architecture role

This contract establishes native observables only. MBP-10 extraction produces price/book state, ten-level depth vectors, order-count vectors, event-flow counts, aggressor trade flow, quality flags, and timestamps. It does not compute lowercase χ. Modal/vector, conglomerate/system, and χ analyses occur only after this data layer is qualified.
