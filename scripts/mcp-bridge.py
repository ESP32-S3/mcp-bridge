#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys

config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"

try:
    with open(config_file, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Missing {config_file}. Copy config.example.json to config.json")
    sys.exit(1)

for dependency in ["node", "supergateway"]:
    if shutil.which(dependency) is None:
        print(f"Missing dependency: {dependency}")
        sys.exit(1)

port = str(config.get("port", 8000))
command = config["mcpCommand"]

print("Starting MCP Bridge")
print(f"Port: {port}")
print(f"MCP Server: {config.get('serverName', 'Unknown')}")

process = subprocess.Popen([
    "supergateway",
    "--stdio",
    command,
    "--outputTransport",
    "streamableHttp",
    "--port",
    port
])

try:
    process.wait()
except KeyboardInterrupt:
    process.terminate()
