# Stock Analysis Runner - Windows PowerShell
# This script runs the stock analysis directly using local Python

$ErrorActionPreference = "Stop"

# IMPORTANT: Get original working directory FIRST before any location changes
$OriginalDir = Get-Location

# Get paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AnalyzeScript = Join-Path $ScriptDir "analyze_stock.py"

# Check if stock code is provided
if ($args.Count -eq 0) {
    Write-Host "Usage: .\run.ps1 <stock_code>" -ForegroundColor Yellow
    Write-Host "Example: .\run.ps1 000001" -ForegroundColor Yellow
    exit 1
}

$StockCode = $args[0]

# Run the analysis (pass original directory as argument for output)
python $AnalyzeScript $StockCode --output-dir $OriginalDir.Path
