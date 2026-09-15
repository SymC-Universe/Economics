# Market Data Inventory — 2026-09-14

Status: P0-D data intake
Source: user-local Databento / GLBX inventory generated from `C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data`
Raw observations remain local. This note records only file-level inventory and known schema implications.

## 1. Corpus summary

The current extracted/indexed corpus contains 68 files totaling approximately 9.19 GB before counting the two large ZIP archives outside these three working folders.

### Databento_Data

- 55 files total
- approximately 4.099 GB
- 52 `trades` CSV data files
- 3 JSON metadata/manifest/condition files
- date coverage represented by filenames: 2026-04-03 through 2026-06-02
- schema family: Databento `trades`

### MBR10_Data

- 10 files total
- approximately 5.088 GB
- 6 compressed `.csv.zst` MBP-10 files
- 1 uncompressed MBP-10 CSV file
- 3 JSON metadata/manifest/condition files
- dates represented: 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-31, 2026-06-01, 2026-06-02
- the 2026-05-31 date exists in both compressed and uncompressed form and should be treated as one observation day, not two independent datasets

### MBR_10_June 9-12

- 3 files total
- metadata/manifest/condition JSON only
- no market observation data file is currently present in the extracted folder
- the associated raw data may remain inside a ZIP or may not yet have been extracted/downloaded; this must be resolved before treating June 9-12 as available evidence

## 2. Extension totals

- `.csv`: 53 files, approximately 4.428 GB
- `.zst`: 6 files, approximately 4.759 GB
- `.json`: 9 files, negligible size

## 3. Largest files

The largest current files are MBP-10 depth files, including approximately:

- 2026-05-27: 1.13 GB compressed
- 2026-05-29: 1.01 GB compressed
- 2026-06-01: 0.95 GB compressed
- 2026-05-28: 0.91 GB compressed
- 2026-06-02: 0.85 GB compressed
- 2026-05-31: 337 MB uncompressed CSV, with a compressed copy also present

The largest trade-only daily files are roughly 100–150 MB.

## 4. Scientific implication

This is not merely bar-price data. The corpus includes two distinct native observation layers:

1. tick-by-tick executed trades;
2. MBP-10 L2 market depth for a smaller overlapping period.

The MBP-10 layer is potentially the highest-value current data for reconstructing the broader Χ architecture because it exposes multiple simultaneously interacting market-depth levels rather than a single price trajectory.

The project should therefore not begin by reducing these observations to returns and applying an oscillator estimator. Instead, the next data contract should preserve the native book and event structure long enough to test which scalar, modal/vector, and conglomerate/system representations are actually supported.

## 5. Immediate unresolved items

Before quantitative real-data modeling, obtain from the local metadata and headers:

- exact requested symbols / instrument families;
- schema and `stype_in` / `stype_out` mapping;
- exact start/end times and timezone conventions;
- actual CSV field order and whether symbol strings are already materialized;
- whether continuous/front-month, parent, or raw contract symbols were requested;
- number of unique instrument IDs per day;
- whether the trade and MBP-10 windows cover identical instruments;
- whether June 9-12 observation files exist inside an archive;
- any Databento condition/exclusion settings that alter event inclusion.

## 6. Evidence-control decision

Do not upload or commit the raw multi-gigabyte market observations at this stage.

Next intake should copy only:

- the nine JSON metadata/manifest/condition files;
- one header line from a representative `trades` CSV;
- one header line from the uncompressed MBP-10 CSV.

Those small artifacts are sufficient to write the first exact loader and data contract without exposing or duplicating the full corpus.
