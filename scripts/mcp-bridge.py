#!/usr/bin/env python3
"""
MCP Bridge - Cross platform launcher

Starts a local MCP stdio server through Supergateway and optionally exposes it
through a Cloudflare HTTPS tunnel.
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

CONFIG_FILE = Path(sys.argv[1] if len(sys.argv) > 1 else "config.json")
processes = []

DEFAULT_CONFIG = {
    "port": 8000,
    "serverName": "My MCP Server",
    "server": {
        "command": "python",
        "args": ["server.py"]
    },
    "cloudflare": {
        "enabled": True
    }
}


def fail(message):
    print(f"\n[ERROR] {message}")
    sys.exit(1)


def check_command(name):
    if shutil.which(name) is None:
        fail(f"Missing dependency: {name}. Run scripts/install-dependencies.py first.")


def expand_path(value):
    if not isinstance(value, str):
        return value
    return os.path.expandvars(os.path.expanduser(value))


def extract_cloudflare_url(line):
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    return match.group(0) if match else None


def create_default_config():
    if CONFIG_FILE.exists():
        return

    print(f"No {CONFIG_FILE} found.")
    print("Creating a starter configuration...")

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(DEFAULT_CONFIG, file, indent=2)

    print(f"Created {CONFIG_FILE}.")
    print("Edit the server.command and server.args values, then run MCP Bridge again.")
    sys.exit(0)


def load_config():
    create_default_config()

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def start_process(command, name, capture_output=False):
    print(f"[+] Starting {name}...")
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.STDOUT if capture_output else None,
            text=True if capture_output else False
        )
        processes.append(process)
        return process
    except Exception as error:
        fail(f"Could not start {name}: {error}")


def shutdown(*_):
    print("\nStopping MCP Bridge...")
    for process in processes:
        try:
            process.terminate()
        except Exception:
            pass
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    config = load_config()

    check_command("node")
    check_command("supergateway")

    tunnel_enabled = config.get("cloudflare", {}).get("enabled", True)
    if tunnel_enabled:
        check_command("cloudflared")

    port = str(config.get("port", 8000))
    server_name = config.get("serverName", "MCP Server")

    server = config.get("server")
    if not server:
        legacy_command = config.get("mcpCommand")
        if legacy_command:
            server = {"command": legacy_command, "args": []}
        else:
            fail("server configuration is missing from config.json")

    command = expand_path(server.get("command"))
    args = [expand_path(arg) for arg in server.get("args", [])]

    if not command:
        fail("server.command is missing from config.json")

    print("\nMCP Bridge")
    print("==========")
    print(f"Server: {server_name}")
    print(f"Port: {port}")

    start_process([
        "supergateway",
        "--stdio",
        command,
        *args,
        "--outputTransport",
        "streamableHttp",
        "--port",
        port,
    ], "Supergateway")

    time.sleep(2)

    if tunnel_enabled:
        cloudflare_process = start_process([
            "cloudflared",
            "tunnel",
            "--url",
            f"http://localhost:{port}"
        ], "Cloudflare Tunnel", capture_output=True)

        endpoint_found = False
        if cloudflare_process.stdout:
            start_time = time.time()
            while time.time() - start_time < 15:
                line = cloudflare_process.stdout.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                url = extract_cloudflare_url(line)
                if url:
                    print("\nCloudflare tunnel started.")
                    print("\nYour MCP endpoint:")
                    print(f"{url}/mcp")
                    print("\nCopy this URL into your AI client.")
                    print("\nQuick Tunnel warning: This endpoint is temporary and changes after restart, shutdown, or sleep.")
                    endpoint_found = True
                    break

        if not endpoint_found:
            print("\nCloudflare tunnel started.")
            print("Check the cloudflared output above for your HTTPS MCP endpoint.")
    else:
        print(f"\nLocal MCP endpoint: http://localhost:{port}")

    print("\nMCP Bridge is running. Press Ctrl+C to stop.")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
