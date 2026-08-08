#!/usr/bin/env bash

set -e

CONFIG="${1:-config.json}"

if [ ! -f "$CONFIG" ]; then
  echo "Missing $CONFIG"
  echo "Copy config.example.json to config.json and configure your MCP server."
  exit 1
fi

command -v node >/dev/null || { echo "Node.js is required"; exit 1; }
command -v supergateway >/dev/null || { echo "Supergateway is required: npm install -g supergateway"; exit 1; }

PORT=$(python3 -c "import json; print(json.load(open('$CONFIG'))['port'])")
COMMAND=$(python3 -c "import json; print(json.load(open('$CONFIG'))['mcpCommand'])")

 echo "Starting MCP Bridge"
 echo "Port: $PORT"
 echo "Server command: $COMMAND"

supergateway --stdio "$COMMAND" --outputTransport streamableHttp --port "$PORT" &
BRIDGE_PID=$!

trap "kill $BRIDGE_PID" EXIT

if command -v cloudflared >/dev/null; then
  echo "Starting Cloudflare Tunnel"
  cloudflared tunnel --url "http://localhost:$PORT"
else
  echo "cloudflared not installed. Local endpoint: http://localhost:$PORT/mcp"
  wait $BRIDGE_PID
fi
