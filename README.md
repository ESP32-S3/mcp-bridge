# MCP Bridge

> Turn any local stdio MCP server into a remote HTTPS MCP endpoint.

MCP Bridge is an infrastructure utility for the Model Context Protocol ecosystem. It creates a bridge between local MCP servers and remote AI clients by wrapping stdio servers with HTTP transport.

## The Problem

Many MCP servers run locally using `stdio` transport. This works well for desktop AI clients, but remote clients often cannot launch local processes or access your machine.

MCP Bridge solves this by exposing those local tools through a URL.

## Architecture

```
Remote AI Client
      |
      | HTTPS MCP
      |
Cloudflare Tunnel / Reverse Proxy
      |
      | HTTP Streamable Transport
      |
Supergateway
      |
      | stdio
      |
Local MCP Server
```

## Supported MCP Servers

MCP Bridge is not tied to one application. Examples:

- Roblox Studio MCP
- Blender MCP
- Filesystem MCP servers
- Python MCP servers
- Custom stdio MCP implementations

## Features

- Convert stdio MCP servers into HTTP MCP endpoints
- Works with existing MCP servers without modification
- Supports Streamable HTTP transport
- Configuration-based setup
- Cross-platform Python launcher
- Works on Windows, macOS, and Linux
- Supports Cloudflare Tunnel and other reverse proxies

## Quick Start

### 1. Install dependencies

Requirements:

- Python 3.10+
- Node.js
- Supergateway
- An MCP server using stdio transport

Optional:

- Cloudflare Tunnel

### 2. Configure your server

Copy:

```
config.example.json -> config.json
```

Example:

```json
{
  "port": 8000,
  "serverName": "My MCP Server",
  "server": {
    "command": "python",
    "args": ["server.py"]
  },
  "cloudflare": {
    "enabled": true
  }
}
```

### 3. Run

Windows, macOS, and Linux:

```bash
python scripts/mcp-bridge.py
```

You will receive an endpoint like:

```
https://example.trycloudflare.com/mcp
```

Paste this URL into your MCP-compatible AI client.

## Security

A public MCP endpoint exposes the tools provided by your MCP server.

For development:

- Cloudflare Quick Tunnels are convenient
- Do not expose sensitive tools publicly
- Only share URLs with trusted users

For production:

- Add authentication
- Use private networking
- Restrict access with Cloudflare Access or another gateway
- Audit available MCP tools

## Examples

See:

- `examples/roblox-studio.md`
- `examples/blender.md`
- `examples/filesystem.md`

## Troubleshooting

Common issues:

**MCP server does not start**

Verify your command and arguments work manually first.

**Endpoint loads but tools fail**

Check that your MCP server supports the expected transport and that the stdio process stays alive.

**Tunnel URL unavailable**

Confirm Cloudflare Tunnel is installed and running.

## Roadmap

- Authentication support
- Docker deployment
- Multiple MCP server management
- Web UI configuration

## License

MIT
