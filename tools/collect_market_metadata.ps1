param(
    [Parameter(Mandatory=$true)][string]$Root,
    [string]$OutDir = "",
    [int]$MaxSchemas = 50
)

$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot
$rootPath = (Resolve-Path -LiteralPath $Root).Path
if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = Join-Path $rootPath "_symc_market_inventory" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

& (Join-Path $scriptDir "inventory_market_data.ps1") -Root $rootPath -OutDir $OutDir

$inventoryPath = Join-Path $OutDir "market_file_inventory.csv"
$inventory = Import-Csv $inventoryPath
$schemaRows = $inventory | Group-Object Extension, Header | ForEach-Object {
    $first = $_.Group | Select-Object -First 1
    [pscustomobject]@{
        Extension = $first.Extension
        Header = $first.Header
        FileCount = $_.Count
        TotalBytes = ($_.Group | Measure-Object -Property Bytes -Sum).Sum
        ExampleFile = $first.FullName
    }
} | Sort-Object FileCount -Descending

$schemaPath = Join-Path $OutDir "market_schema_groups.csv"
$schemaRows | Export-Csv $schemaPath -NoTypeInformation -Encoding UTF8

$profilesDir = Join-Path $OutDir "profiles"
New-Item -ItemType Directory -Force -Path $profilesDir | Out-Null
$profileScript = Join-Path $scriptDir "profile_market_csv.py"
$profiled = 0
foreach ($schema in ($schemaRows | Select-Object -First $MaxSchemas)) {
    if ($schema.Extension -notin @(".csv", ".tsv", ".txt")) { continue }
    $delim = if ($schema.Extension -eq ".tsv") { "`t" } else { "," }
    $safe = "schema_{0:D3}.json" -f $profiled
    $out = Join-Path $profilesDir $safe
    try {
        python $profileScript $schema.ExampleFile --out $out --delimiter $delim
        $profiled++
    } catch { Write-Warning "Could not profile $($schema.ExampleFile): $($_.Exception.Message)" }
}

$handoff = [pscustomobject]@{
    Root = $rootPath
    GeneratedUtc = (Get-Date).ToUniversalTime().ToString("o")
    Inventory = $inventoryPath
    SchemaGroups = $schemaPath
    ProfilesDirectory = $profilesDir
    ProfileCount = $profiled
    Note = "Share the inventory CSV, schema-groups CSV, inventory summary JSON, and profiles folder. Raw market files remain local."
}
$handoff | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $OutDir "HANDOFF.json") -Encoding UTF8

Write-Host ""
Write-Host "SymC market metadata handoff complete."
Write-Host "Raw market observations were not copied into the handoff folder."
Write-Host "Upload/share this folder: $OutDir"
