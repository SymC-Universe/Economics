# Local Market Data Handoff

The raw market corpus may remain on the user's computer. The current branch includes a metadata-first intake path so Engine development can begin without placing the entire corpus in GitHub.

## Windows / PowerShell

From a checkout of `market-chi-architecture`:

```powershell
git fetch origin
git checkout market-chi-architecture
git pull

powershell -ExecutionPolicy Bypass -File .\tools\collect_market_metadata.ps1 -Root "D:\PATH\TO\MARKET\DATA"
```

The script creates `_symc_market_inventory` under the data root unless `-OutDir` is supplied.

Share only that generated handoff folder first. It contains:

- `market_file_inventory.csv`: file identities, sizes, extensions, and text-file header previews;
- `market_inventory_summary.json`: corpus-level counts and storage summary;
- `market_schema_groups.csv`: files grouped by apparent schema;
- `profiles/*.json`: metadata profiles of representative CSV/TSV schemas;
- `HANDOFF.json`: handoff manifest.

Raw market observations are not copied into the handoff folder by these scripts. The metadata profiles include first/last timestamps where parseable but do not reproduce price series.

## Why this is the first data step

The GOM requires input/schema/provenance qualification before scale. The metadata pass lets us determine asset/instrument organization, file families and formats, date ranges and sampling intervals, available price/return/volume/spread/depth/order-flow fields, whether multivariate alignment is possible, whether microstructure analysis is possible, which files are appropriate for P0-D discovery/P0-Q qualification/later untouched testing, and what production loader is actually needed.

No thresholds, model selection, or future outcome rules will be tuned from file names or Atlas labels during this inventory pass.
