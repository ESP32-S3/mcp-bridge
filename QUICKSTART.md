# MCP Bridge Quickstart

## What is MCP Bridge?

MCP Bridge lets remote AI clients use local MCP servers by converting a local stdio MCP server into an HTTPS MCP endpoint.

## Setup

### 1. Install dependencies

Install:

- Python 3.10+
- Node.js
- Supergateway

Optional:

- Cloudflare Tunnel (for public HTTPS access)

Install Supergateway:

```bash
npm install -g supergateway
```

### 2. Configure your MCP server

Copy:

```
config.example.json -> config.json
```

Edit the server section:

```json
{
  "port": 8000,
  "serverName": "My Server",
  "server": {
    "command": "python",
    "args": ["server.py"]
  },
  "cloudflare": {
    "enabled": true
  }
}
```

The command and arguments are portable across Windows, macOS, and Linux.

### 3. Start MCP Bridge

Run:

```bash
python scripts/mcp-bridge.py
```

The launcher will:

1. Start your local MCP server
2. Start Supergateway
3. Start Cloudflare Tunnel if enabled
4. Provide your HTTPS MCP endpoint

Example:

```
https://example.trycloudflare.com/mcp
```

Copy that URL into your MCP-compatible AI client.

## Safety

Treat the URL like an API key. Anyone with access may be able to call your MCP tools.

Use authentication and private networking for production deployments.
