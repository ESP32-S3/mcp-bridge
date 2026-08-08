# MCP URL Bridge - Quick Start Guide

## What This Does

MCP URL Bridge turns a local MCP server into a remote HTTPS MCP endpoint.

It is useful when:

- Your MCP server only supports local stdio connections
- Your AI client requires a URL-based MCP connection
- You want browser-based AI tools to access local tools

Architecture:

Local MCP Server
        |
        | stdio
        |
Supergateway
        |
        | HTTP
        |
Cloudflare Tunnel
        |
        | HTTPS MCP URL
        |
AI Client


---

# Before Setup

Make sure these are installed before running the bridge.


## Required Software


## 1. Node.js

Required for Supergateway.

Download:

https://nodejs.org/


Check installation:

node --version



---

## 2. Supergateway

Install:

npm install -g supergateway


Check:

supergateway --version



---

## 3. Cloudflared

Required to create the HTTPS tunnel.

Download:

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/


Check:

cloudflared --version



---

# Folder Layout

Recommended folder:

MCP-URL-Bridge

|
|-- MCP-URL-Bridge.ps1
|
|-- README.md
|
|-- QUICKSTART.md
|
|-- mcp_endpoint.txt


mcp_endpoint.txt is created automatically after setup.

It contains the final MCP URL to paste into your AI client.


---

# Before Running

You need an MCP server already working.

The bridge does NOT create an MCP server.

It only converts:

Local MCP server

into:

Remote HTTPS MCP endpoint


Examples:

- Roblox Studio MCP
- Blender MCP
- Filesystem MCP
- Custom MCP servers


---

# First Setup


## Step 1 - Edit The Script

Open:

MCP-URL-Bridge.ps1


Find:

$GatewayPort = 8000


Change this only if your MCP server uses a different port.


Find the Supergateway command:

supergateway --stdio "YOUR_COMMAND"


Replace it with your MCP server startup command.


Example Roblox Studio:

supergateway --stdio "cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat"



Example filesystem MCP:

supergateway --stdio "npx -y @modelcontextprotocol/server-filesystem C:\Users\User"



---

# Running The Bridge


Run:

.\MCP-URL-Bridge.ps1


or:

Right click the file

Select:

Run with PowerShell



---

# What Happens After Starting


The script opens three PowerShell windows.


## Window 1

Name:

MCP URL Bridge - Gateway


Runs Supergateway.


Expected:

Listening on port 8000



---

## Window 2

Name:

MCP URL Bridge - Cloudflare


Creates the HTTPS tunnel.


Expected output:

https://example-name.trycloudflare.com



---

## Window 3

Name:

MCP URL Bridge - Monitor


Checks the system every 30 seconds.


It checks:

- MCP gateway
- Cloudflare tunnel
- MCP processes


---

# Getting The MCP URL


When the tunnel starts, the script automatically:

1. Finds the Cloudflare URL
2. Adds /mcp
3. Copies it to clipboard
4. Saves it to:

mcp_endpoint.txt


Example:

https://example-name.trycloudflare.com/mcp



---

# Connecting Your AI Client


Paste the full endpoint:

https://YOUR-TUNNEL.trycloudflare.com/mcp


Important:

The /mcp part is required.


Do not use:

https://YOUR-TUNNEL.trycloudflare.com



---

# Troubleshooting


## Gateway Not Running


Check:

Get-NetTCPConnection -LocalPort 8000


Expected:

Listen



---

## Cloudflare URL Not Appearing


Quick tunnels are temporary.

Restart:

MCP-URL-Bridge.ps1


A new URL will be generated.


---

## AI Client Cannot Connect


Check:

1. MCP server is running

2. Supergateway is running

3. Port 8000 is listening

4. Cloudflare tunnel is active

5. The endpoint ends with /mcp



---

# Security Warning


Cloudflare Quick Tunnels are temporary testing tunnels.

The generated URL is public while active.

Anyone with the URL can attempt to connect.


For permanent usage:

- Use a Cloudflare named tunnel
- Add authentication
- Restrict access


---

# Supported MCP Servers


Any MCP server supporting stdio transport can work.

Examples:

- Roblox Studio MCP
- Blender MCP
- Filesystem MCP
- Custom MCP servers


---

# Quick Checklist


Before asking for help:

[ ] Node.js installed

[ ] Supergateway installed

[ ] Cloudflared installed

[ ] MCP server works locally

[ ] Supergateway starts

[ ] Port 8000 is listening

[ ] Cloudflare tunnel starts

[ ] Endpoint ends with /mcp

[ ] AI client uses the full endpoint


Done.
