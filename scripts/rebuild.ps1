# Equivalente a: make rebuild
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".env")) {
    Write-Host "No existe .env. Ejecuta: copy .env.example .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "Deteniendo contenedores..." -ForegroundColor Cyan
docker compose down

Write-Host "Reconstruyendo API (sin cache)..." -ForegroundColor Cyan
docker compose build --no-cache api

Write-Host "Levantando API + PostgreSQL..." -ForegroundColor Cyan
docker compose up --build @args
