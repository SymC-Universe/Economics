param(
    [Parameter(Mandatory=$true)][string]$Root,
    [string]$OutDir = ""
)

$ErrorActionPreference = "Stop"
$rootPath = (Resolve-Path -LiteralPath $Root).Path
if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = Join-Path $rootPath "_symc_market_inventory" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$extensions = @(".csv", ".txt", ".tsv", ".parquet", ".feather", ".arrow", ".json", ".jsonl", ".h5", ".hdf5")
$files = Get-ChildItem -LiteralPath $rootPath -Recurse -File | Where-Object { $extensions -contains $_.Extension.ToLowerInvariant() }

$inventory = foreach ($f in $files) {
    $header = $null; $firstRow = $null
    if ($f.Extension.ToLowerInvariant() -in @(".csv", ".txt", ".tsv")) {
        try {
            $preview = Get-Content -LiteralPath $f.FullName -TotalCount 2
            if ($preview.Count -ge 1) { $header = $preview[0] }
            if ($preview.Count -ge 2) { $firstRow = $preview[1] }
        } catch { $header = "<READ_ERROR>" }
    }
    [pscustomobject]@{
        FullName = $f.FullName
        RelativePath = $f.FullName.Substring($rootPath.Length).TrimStart('\')
        Extension = $f.Extension.ToLowerInvariant()
        Bytes = $f.Length
        MB = [math]::Round($f.Length / 1MB, 3)
        LastWriteTimeUtc = $f.LastWriteTimeUtc.ToString("o")
        Header = $header
        FirstRow = $firstRow
    }
}

$inventory | Export-Csv (Join-Path $OutDir "market_file_inventory.csv") -NoTypeInformation -Encoding UTF8
$summary = [pscustomobject]@{
    Root = $rootPath
    GeneratedUtc = (Get-Date).ToUniversalTime().ToString("o")
    FileCount = $inventory.Count
    TotalBytes = ($inventory | Measure-Object -Property Bytes -Sum).Sum
    Extensions = ($inventory | Group-Object Extension | Sort-Object Name | ForEach-Object { [pscustomobject]@{ Extension=$_.Name; Count=$_.Count } })
}
$summary | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $OutDir "market_inventory_summary.json") -Encoding UTF8
Write-Host "Inventory complete."
Write-Host "  CSV:  $(Join-Path $OutDir 'market_file_inventory.csv')"
Write-Host "  JSON: $(Join-Path $OutDir 'market_inventory_summary.json')"
