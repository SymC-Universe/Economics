param(
    [string]$Root = "C:\Users\CCGTi\OneDrive\Desktop\SymC_Economics\SymC_TF\Data"
)

$ErrorActionPreference = "Stop"
$out = Join-Path $Root "_symc_databento_contract"
New-Item -ItemType Directory -Force -Path $out | Out-Null

# Copy JSON request metadata with parent-folder prefixes to avoid name collisions.
Get-ChildItem -LiteralPath $Root -Recurse -File -Filter "*.json" |
    Where-Object { $_.FullName -notlike "$out*" } |
    ForEach-Object {
        $parent = Split-Path $_.DirectoryName -Leaf
        $safeParent = $parent -replace '[^A-Za-z0-9._-]', '_'
        $dest = Join-Path $out ($safeParent + "__" + $_.Name)
        Copy-Item -LiteralPath $_.FullName -Destination $dest -Force
    }

# Capture schema headers only, never observation rows.
$trade = Get-ChildItem -LiteralPath (Join-Path $Root "Databento_Data") -Recurse -File |
    Where-Object { $_.Name -like "*.trades.csv" } |
    Select-Object -First 1
if ($trade) {
    Get-Content -LiteralPath $trade.FullName -TotalCount 1 |
        Set-Content -LiteralPath (Join-Path $out "trades_header.txt") -Encoding UTF8
}

$mbp = Get-ChildItem -LiteralPath (Join-Path $Root "MBR10_Data") -Recurse -File |
    Where-Object { $_.Name -like "*.mbp-10.csv" -and $_.Extension -eq ".csv" } |
    Select-Object -First 1
if ($mbp) {
    Get-Content -LiteralPath $mbp.FullName -TotalCount 1 |
        Set-Content -LiteralPath (Join-Path $out "mbp10_header.txt") -Encoding UTF8
}

# List ZIP central directories without extracting raw market data.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipRows = @()
Get-ChildItem -LiteralPath $Root -File -Filter "*.zip" | ForEach-Object {
    $zipPath = $_.FullName
    $archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
    try {
        foreach ($entry in $archive.Entries) {
            $zipRows += [pscustomobject]@{
                Zip = $_.Name
                Entry = $entry.FullName
                UncompressedBytes = $entry.Length
                CompressedBytes = $entry.CompressedLength
            }
        }
    }
    finally {
        $archive.Dispose()
    }
}
$zipRows | Export-Csv -LiteralPath (Join-Path $out "zip_contents.csv") -NoTypeInformation

Write-Host ""
Write-Host "DONE"
Write-Host "Contract bundle saved to:"
Write-Host $out
Write-Host ""
Get-ChildItem -LiteralPath $out | Select-Object Name, Length
