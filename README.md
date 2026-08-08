# MCP Bridge

Expose local MCP servers through a remote Streamable HTTP endpoint.

MCP Bridge allows MCP clients that cannot directly launch or access local MCP servers to connect through a URL instead.

## How It Works

Many MCP servers are designed to run locally through stdio.

MCP Bridge creates a connection layer between local MCP servers and remote MCP clients:

MCP Client
    |
    | Streamable HTTP
    |
Public URL / Local HTTP Endpoint
    |
    |
MCP Bridge
    |
    | stdio
    |
Local MCP Server


Example:

ChatGPT / Remote MCP Client
            |
            |
     https://example.com/mcp
            |
            |
     Streamable HTTP
            |
            |
       MCP Bridge
            |
            |
       stdio MCP Server


## Features

- Convert local stdio MCP servers into HTTP-accessible MCP endpoints
- Works with MCP servers using stdio transport
- Useful for remote MCP clients without native local server support
- Supports Cloudflare Tunnel, reverse proxies, or other HTTP exposure methods
- Simple command-line setup
- Works with many different MCP servers


## Requirements

Install:

- Node.js
- Supergateway
- An MCP server using stdio transport

Optional:

- Cloudflare Tunnel
- Reverse proxy software


## Installation

Install Supergateway:

npm install -g supergateway


Install Cloudflare Tunnel (optional):

winget install Cloudflare.cloudflared


## Usage

Start an MCP server through the bridge:

supergateway --stdio "your-mcp-command-here" --outputTransport streamableHttp --port 8000


Example:

supergateway --stdio "python server.py" --outputTransport streamableHttp --port 8000


The MCP endpoint will be available at:

http://localhost:8000/mcp


## Exposing To The Internet

You can expose the endpoint using any tunnel or reverse proxy.

Example using Cloudflare Tunnel:

cloudflared tunnel --url http://localhost:8000


Cloudflare will provide a URL:

https://example.trycloudflare.com


Your MCP endpoint becomes:

https://example.trycloudflare.com/mcp


## Example: Roblox Studio MCP

Roblox Studio includes a local MCP server.

MCP Bridge can expose it to remote MCP clients:

Remote MCP Client
        |
        |
Cloudflare Tunnel
        |
        |
MCP Bridge
        |
        |
Roblox mcp.bat
        |
        |
StudioMCP.exe
        |
        |
Roblox Studio


Command:

supergateway --stdio "cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat" --outputTransport streamableHttp --port 8000


## Health Checking

Example checks:

Get-Process StudioMCP

Get-NetTCPConnection -LocalPort 13469

Get-NetTCPConnection -LocalPort 8000


## Troubleshooting

### "Not connected to the WS host"

This usually means the MCP server started, but the application behind it is not connected.

Check that the MCP application is running and has an active connection.

For Roblox Studio:

Get-NetTCPConnection -LocalPort 13469


A healthy connection should show:

127.0.0.1:13469 LISTENING

127.0.0.1:13469 ESTABLISHED


### Multiple MCP Processes

Some MCP clients create multiple server processes.

Inspect running MCP processes:

Get-CimInstance Win32_Process |
Where-Object {
    $_.CommandLine -match "mcp"
} |
Select ProcessId,Name,CommandLine


## Why?

MCP was designed mainly around local tool execution.

However, some MCP clients cannot:

- Launch local MCP processes
- Access localhost services
- Manage stdio servers directly

MCP Bridge creates a transport layer that allows these local MCP tools to become accessible through a URL.


## Roadmap

- Native HTTP MCP server support
- WebSocket transport support
- Authentication
- Multiple MCP server management
- Configuration files
- Cross-platform launcher
- Docker support


## Security Warning

Exposing MCP servers publicly can provide access to powerful tools.

Only expose MCP endpoints to trusted clients.

For production use, add authentication and access controls.


## License

MIT License
