$ErrorActionPreference = "Stop"

$configPath = Join-Path $PSScriptRoot "..\config.json"

if (!(Test-Path $configPath)) {
    Write-Host "Missing config.json. Copy config.example.json first." -ForegroundColor Red
    exit 1
}

$config = Get-Content $configPath | ConvertFrom-Json

function Require($command) {
    if (!(Get-Command $command -ErrorAction SilentlyContinue)) {
        Write-Host "Missing dependency: $command" -ForegroundColor Red
        exit 1
    }
}

Require "node"
Require "supergateway"

Write-Host "Starting MCP Bridge: $($config.serverName)"

Start-Process powershell -ArgumentList "-NoExit", "supergateway --stdio `"$($config.mcpCommand)`" --outputTransport streamableHttp --port $($config.port)"

if ($config.enableCloudflareTunnel) {
    Require "cloudflared"
    Start-Process powershell -ArgumentList "-NoExit", "cloudflared tunnel --url http://localhost:$($config.port)"
}

Write-Host "MCP Bridge started on port $($config.port)"
