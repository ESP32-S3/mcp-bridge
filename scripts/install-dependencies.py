#!/usr/bin/env python3
"""
MCP Bridge dependency installer.

Checks and installs the tools required to run MCP Bridge:
- Python
- Node.js / npm
- Supergateway
- Cloudflared (optional)

Usage:
    python scripts/install-dependencies.py
"""

import platform
import shutil
import subprocess
import sys


def command_exists(command):
    return shutil.which(command) is not None


def run(command):
    print(f"\n> {' '.join(command)}")
    return subprocess.run(command, check=False)


def install_supergateway():
    if command_exists("supergateway"):
        print("✓ Supergateway detected")
        return

    if not command_exists("npm"):
        print("✗ npm not found. Install Node.js first.")
        return

    print("Installing Supergateway...")
    result = run(["npm", "install", "-g", "supergateway"])

    if result.returncode == 0:
        print("✓ Supergateway installed")
    else:
        print("✗ Failed installing Supergateway")


def check_node():
    if command_exists("node"):
        print("✓ Node.js detected")
    else:
        print("✗ Node.js missing. Install it from https://nodejs.org/")


def check_cloudflared():
    if command_exists("cloudflared"):
        print("✓ Cloudflared detected")
    else:
        print("! Cloudflared not found (optional)")
        print("  Install it for public HTTPS endpoints.")


def main():
    print("MCP Bridge Dependency Installer")
    print("=" * 32)
    print(f"Platform: {platform.system()}")

    if sys.version_info < (3, 10):
        print("✗ Python 3.10+ required")
        return

    print("✓ Python version supported")

    check_node()
    install_supergateway()
    check_cloudflared()

    print("\nDependency check complete.")
    print("Run:")
    print("  python scripts/mcp-bridge.py")


if __name__ == "__main__":
    main()
