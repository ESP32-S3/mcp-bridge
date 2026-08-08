# Cloudflare Quick Tunnel limitations

MCP Bridge can use Cloudflare Quick Tunnels to expose a local MCP server over HTTPS.

Quick Tunnels are designed for development and testing.

## Important limitations

The endpoint is temporary. It can change when:

- your computer goes to sleep
- the machine restarts
- MCP Bridge is closed
- your network connection drops

When this happens:

1. Start MCP Bridge again:

```bash
python scripts/mcp-bridge.py
```

2. Copy the new HTTPS MCP endpoint.

3. Update the URL in your AI client.

For production deployments, use a configured Cloudflare Tunnel with a persistent hostname and authentication.
