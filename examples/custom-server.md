# Custom MCP Server Example

MCP Bridge works with any local MCP server that communicates over stdio.

## Configuration

Copy `config.example.json` to `config.json` and configure your server:

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

## Start

```bash
python scripts/mcp-bridge.py
```

MCP Bridge will expose the local stdio server as a remote HTTPS MCP endpoint.

The same setup works for any MCP-compatible server, including developer tools,
automation tools, and local AI integrations.
