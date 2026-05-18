# Levanta API + PostgreSQL (producción local / despliegue con Docker)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".env")) {
    Write-Host "No existe .env. Ejecuta: copy .env.example .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "Iniciando Panaderia Zapatoca (API + PostgreSQL)..." -ForegroundColor Cyan
Write-Host "  Rebuild limpio: .\scripts\rebuild.ps1  o  make rebuild" -ForegroundColor DarkGray
docker compose up --build @args
