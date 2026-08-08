param([int]$Port = 8000)

while ($true) {
    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue

    if ($connection) {
        Write-Host "MCP Bridge healthy: port $Port active"
    } else {
        Write-Host "MCP Bridge unavailable: port $Port not listening"
    }

    Start-Sleep -Seconds 10
}
