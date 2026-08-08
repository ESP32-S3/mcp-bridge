# MCP Bridge Quickstart

## What is MCP Bridge?

MCP Bridge lets remote AI clients use local MCP servers by converting a local stdio MCP server into an HTTPS MCP endpoint.

## Setup

1. Install Node.js.
2. Install Supergateway:

```
npm install -g supergateway
```

3. Install Cloudflare Tunnel if you want internet access.

4. Copy configuration:

```
config.example.json -> config.json
```

5. Set your MCP command.

Example:

```json
{
  "port": 8000,
  "serverName": "My Server",
  "mcpCommand": "python server.py"
}
```

6. Start:

```powershell
./scripts/mcp-bridge.ps1
```

7. Copy the generated `/mcp` URL into your AI client.

## Safety

Treat the URL like an API key. Anyone with access may be able to call your MCP tools.

Use authentication and private networking for production deployments.
