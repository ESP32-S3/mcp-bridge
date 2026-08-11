# MCP Bridge

> **Expose any local stdio MCP server as a remote HTTPS MCP endpoint.**

MCP Bridge is a cross-platform infrastructure tool for the **Model Context Protocol (MCP)**. It wraps an existing local stdio MCP server with HTTP transport and, when enabled, exposes it through a Cloudflare Tunnel so an MCP-compatible AI client can reach it through an HTTPS URL.

RELEASES PAGE: https://github.com/ESP32-S3/CMD-Chat/releases?utm_source=chatgpt.com

**Local MCP server → Supergateway → HTTP → Cloudflare Tunnel → HTTPS MCP endpoint**

No changes to the MCP server itself are required.

## Why MCP Bridge?

A lot of MCP servers are designed to run on the same machine as the AI client. That becomes a problem when your AI client is remote, browser-based, or otherwise unable to launch a local process.

MCP Bridge separates those pieces:

- Your MCP server stays local.
- MCP Bridge provides the transport bridge.
- Supergateway converts stdio to HTTP.
- A reverse proxy/tunnel makes the HTTP service reachable remotely.
- Your AI client connects using the resulting MCP URL.

## Architecture

```text
┌─────────────────────┐
│   Remote AI Client  │
│  ChatGPT / Claude / │
│    other MCP client │
└──────────┬──────────┘
           │
           │ HTTPS MCP
           ▼
┌─────────────────────┐
│ Cloudflare Tunnel   │
│ or reverse proxy    │
└──────────┬──────────┘
           │
           │ HTTP / Streamable HTTP
           ▼
┌─────────────────────┐
│    Supergateway     │
└──────────┬──────────┘
           │
           │ stdio
           ▼
┌─────────────────────┐
│  Local MCP Server   │
│ Roblox / Blender /  │
│ Filesystem / custom │
└─────────────────────┘
```

## What Can You Use It With?

MCP Bridge is **not a Roblox-specific project**. Roblox Studio is simply one example of a local MCP server that benefits from this architecture.

Examples include:

- **Roblox Studio MCP**
- **Blender MCP**
- **Filesystem MCP servers**
- Python-based MCP servers
- Node.js MCP servers
- Your own custom stdio MCP implementation

If the server can communicate over stdio, MCP Bridge is designed to sit in front of it.

## Features

- Convert an existing **stdio MCP server into an HTTP MCP endpoint**
- Optional **Cloudflare Tunnel** support
- Automatic detection and display of the generated Quick Tunnel URL
- Configuration-driven setup
- Cross-platform Python launcher
- Windows, macOS, and Linux support
- Works with existing MCP servers without modifying them
- Supports Streamable HTTP through Supergateway
- Portable MCP server command and argument configuration
- Beginner-friendly dependency and setup scripts

## Quick Start

### Requirements

You need:

- Python 3.10+
- Node.js
- Supergateway
- An MCP server that uses stdio transport
- Cloudflared if you want a public HTTPS endpoint through Cloudflare

### 1. Clone the repository

```bash
git clone https://github.com/ESP32-S3/mcp-bridge.git
cd mcp-bridge
```

### 2. Install dependencies

Use the dependency installer for your operating system, or install Python, Node.js, Supergateway, and Cloudflared manually.

See [`QUICKSTART.md`](QUICKSTART.md) for the complete Windows, macOS, and Linux setup.

### 3. Configure your MCP server

Copy the example configuration:

```text
config.example.json → config.json
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

Change the command and arguments to match your MCP server.

### 4. Start MCP Bridge

Windows, macOS, and Linux:

```bash
python scripts/mcp-bridge.py
```

MCP Bridge starts the local transport bridge and, when Cloudflare is enabled, detects the generated endpoint automatically:

```text
Cloudflare tunnel started.

Your MCP endpoint:

https://example.trycloudflare.com/mcp

Copy this URL into your AI client.
```

Paste that URL into your MCP-compatible AI client.

## Demo

The intended user experience is deliberately simple:

```text
Local MCP server
       │
       ▼
python scripts/mcp-bridge.py
       │
       ├── Supergateway ✓
       │
       └── Cloudflare Tunnel ✓
                │
                ▼
https://example.trycloudflare.com/mcp
                │
                ▼
           AI client
```

A short demo GIF/video showing **launch → endpoint generation → AI client connection → tool call** is the recommended way to demonstrate MCP Bridge in the repository and project announcements.

## Platform Support

The main launcher is Python-based and is intended to work across:

| Platform | Launcher |
| --- | --- |
| Windows | `python scripts/mcp-bridge.py` |
| macOS | `python3 scripts/mcp-bridge.py` |
| Linux | `python3 scripts/mcp-bridge.py` |

The repository also contains platform-specific helper scripts where appropriate. **Do not run a PowerShell `.ps1` helper on macOS or Linux.**

## Configuration

MCP Bridge reads its server settings from `config.json` rather than requiring users to edit the launcher.

A minimal configuration looks like:

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

This makes it possible to use the same bridge with completely different MCP servers without modifying the Python source code.

## Cloudflare Quick Tunnel Warning

Cloudflare Quick Tunnels are excellent for development and quick testing, but they are **temporary**.

If your computer:

- goes to sleep
- shuts down
- loses its network connection
- closes MCP Bridge
- restarts MCP Bridge

the Quick Tunnel can disappear and a new URL may be generated when you start it again.

For example:

```text
Old:
https://old-name.trycloudflare.com/mcp

New:
https://new-name.trycloudflare.com/mcp
```

When this happens:

1. Relaunch MCP Bridge.
2. Copy the newly generated `/mcp` endpoint.
3. Replace the old endpoint in your AI client's MCP configuration.

For a stable deployment, use a configured Cloudflare Tunnel with a persistent hostname or another production reverse-proxy setup.

See [`docs/cloudflare-quick-tunnel.md`](docs/cloudflare-quick-tunnel.md) for more details.

## Security

**A public MCP endpoint can expose every tool made available by your local MCP server.** Treat the endpoint as sensitive.

For development:

- Do not expose sensitive or destructive tools unnecessarily.
- Do not publish your temporary endpoint publicly.
- Only share the endpoint with trusted users.
- Review exactly which MCP tools your server exposes.

For production:

- Add authentication before exposing MCP over the public internet.
- Prefer a persistent, controlled tunnel or reverse proxy.
- Use private networking where practical.
- Consider Cloudflare Access or another identity-aware gateway.
- Audit and restrict the MCP tools available through the bridge.

Cloudflare Quick Tunnels are **not an authentication system**.

## Examples

See the example guides for common MCP server types:

- [`examples/roblox-studio.md`](examples/roblox-studio.md)
- [`examples/blender.md`](examples/blender.md)
- [`examples/filesystem.md`](examples/filesystem.md)

## Documentation

- [`QUICKSTART.md`](QUICKSTART.md) — beginner-friendly setup
- [`docs/architecture.md`](docs/architecture.md) — how MCP Bridge works
- [`docs/cloudflare-quick-tunnel.md`](docs/cloudflare-quick-tunnel.md) — Quick Tunnel behavior and limitations
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — common problems and fixes
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contributing to the project
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## Troubleshooting

### MCP server does not start

Run the MCP server command manually first. Confirm the executable, working directory, arguments, and environment are correct.

### Supergateway does not start

Check that Node.js and Supergateway are installed and available on your `PATH`.

### Cloudflare endpoint does not appear

Check that `cloudflared` is installed and available on your `PATH`, then verify that Cloudflare is enabled in `config.json`.

### Endpoint works but tools fail

Confirm that the underlying MCP server stays alive and communicates correctly over stdio. Check its own logs before debugging the tunnel layer.

### Endpoint stopped working after sleep or restart

If you are using a Cloudflare Quick Tunnel, this is expected behavior. Restart MCP Bridge and replace the old endpoint in your AI client's configuration.

## Project Status

MCP Bridge is an open-source developer tool under active development. The core stdio → HTTP → HTTPS workflow is the primary focus.

Planned improvements include:

- Authentication support
- Docker deployment
- Multiple MCP server management
- Web UI configuration
- More deployment options

## Contributing

Issues, bug reports, documentation improvements, examples, and pull requests are welcome.

Before submitting a change, please read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MCP Bridge is released under the MIT License. See [`LICENSE`](LICENSE).
