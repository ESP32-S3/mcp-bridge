# ==========================================================
# MCP URL Bridge Launcher
# 
# Starts a local stdio MCP server and exposes it as a URL
# endpoint for AI clients that support remote MCP.
#
# ==========================================================

$ErrorActionPreference = "Continue"

$AppName = "MCP URL Bridge"

$BaseFolder = Split-Path -Parent $MyInvocation.MyCommand.Path

$GatewayPort = 8000

$EndpointFile = "$BaseFolder\mcp_endpoint.txt"


function Set-Title($title)
{
    $Host.UI.RawUI.WindowTitle = $title
}


function Notify($title,$message)
{
    try
    {
        Add-Type -AssemblyName System.Windows.Forms

        $notify = New-Object System.Windows.Forms.NotifyIcon
        $notify.Icon = [System.Drawing.SystemIcons]::Information
        $notify.BalloonTipTitle = $title
        $notify.BalloonTipText = $message
        $notify.Visible = $true
        $notify.ShowBalloonTip(8000)

        Start-Sleep 10

        $notify.Dispose()
    }
    catch
    {
        Write-Host $message
    }
}


function Start-Gateway
{
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        @"

`$Host.UI.RawUI.WindowTitle='MCP URL Bridge - Gateway'

Write-Host 'Starting MCP gateway...' -ForegroundColor Cyan

supergateway `
--stdio "cmd.exe /c `%LOCALAPPDATA%\Roblox\mcp.bat" `
--outputTransport streamableHttp `
--port $GatewayPort

"@
    )
}



function Start-Tunnel
{
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        @"

`$Host.UI.RawUI.WindowTitle='MCP URL Bridge - Cloudflare'

cloudflared tunnel --url http://localhost:$GatewayPort

"@
    )
}



function Wait-For-Tunnel
{
    Write-Host "Waiting for Cloudflare URL..."

    while($true)
    {

        $cloud = Get-Process cloudflared -ErrorAction SilentlyContinue

        if($cloud)
        {
            $logs = Get-Content "$env:TEMP\cloudflared.log" -ErrorAction SilentlyContinue

            foreach($line in $logs)
            {
                if($line -match "https://.*trycloudflare.com")
                {
                    return $matches[0]
                }
            }
        }


        Start-Sleep 2
    }
}



function Start-Monitor
{
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        @"

`$Host.UI.RawUI.WindowTitle='MCP URL Bridge - Monitor'


while(`$true)
{

Write-Host ''
Write-Host '========== MCP HEALTH ==========' -ForegroundColor Cyan
Write-Host (Get-Date)


if(Get-NetTCPConnection -LocalPort $GatewayPort -ErrorAction SilentlyContinue)
{
Write-Host '[OK] MCP HTTP endpoint running' -ForegroundColor Green
}
else
{
Write-Host '[FAIL] MCP gateway missing' -ForegroundColor Red
}



if(Get-Process cloudflared -ErrorAction SilentlyContinue)
{
Write-Host '[OK] Cloudflare tunnel running' -ForegroundColor Green
}
else
{
Write-Host '[FAIL] Tunnel missing' -ForegroundColor Red
}



if(Get-Process StudioMCP -ErrorAction SilentlyContinue)
{
Write-Host '[OK] MCP server process detected' -ForegroundColor Green
}
else
{
Write-Host '[WARN] MCP server not detected' -ForegroundColor Yellow
}



Write-Host '==============================='


Start-Sleep 30

}

"@
    )
}




# ==========================================================
# MAIN
# ==========================================================


Set-Title $AppName


Write-Host ""
Write-Host "Starting $AppName" -ForegroundColor Cyan
Write-Host ""


# Capture cloudflared output

Start-Process powershell `
-ArgumentList "-Command cloudflared tunnel --url http://localhost:$GatewayPort *> $env:TEMP\cloudflared.log" `
-WindowStyle Hidden


Start-Sleep 3


Start-Gateway


Start-Sleep 5


Start-Tunnel


Start-Sleep 8


# Find URL

Write-Host "Searching for tunnel URL..."


$url = $null


for($i=0;$i -lt 60;$i++)
{

$data = Get-Content "$env:TEMP\cloudflared.log" -ErrorAction SilentlyContinue


foreach($line in $data)
{
    if($line -match "https://[a-zA-Z0-9-]+\.trycloudflare\.com")
    {
        $url=$matches[0]
    }
}


if($url)
{
break
}


Start-Sleep 2

}



if($url)
{

$endpoint="$url/mcp"


Set-Clipboard $endpoint


$endpoint | Out-File $EndpointFile


Write-Host ""
Write-Host "===================================="
Write-Host " MCP ENDPOINT READY "
Write-Host "===================================="
Write-Host $endpoint
Write-Host ""
Write-Host "Copied to clipboard!"
Write-Host "Paste this into your AI MCP connector."
Write-Host ""


Notify `
"MCP Endpoint Ready" `
"Copied MCP URL to clipboard:`n$endpoint"


}
else
{

Notify `
"MCP Setup Failed" `
"Could not find Cloudflare tunnel URL."

}


Start-Monitor
