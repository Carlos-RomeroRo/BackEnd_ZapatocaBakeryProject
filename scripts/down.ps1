$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Deteniendo contenedores..." -ForegroundColor Cyan
docker compose down @args
