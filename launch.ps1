Write-Host "Starting Python Learning App..." -ForegroundColor Cyan

Write-Host "Syncing dependencies..." -ForegroundColor Yellow
try {
    uv sync --group dev
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Host "Error syncing dependencies. Make sure 'uv' is installed." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host "Press Enter to quit..."
    return
}

Write-Host "Launching app..." -ForegroundColor Green
uv run python-learning session
if ($LASTEXITCODE -ne 0) {
    Read-Host "Press Enter to quit..."
}
