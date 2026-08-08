#!/usr/bin/env python3
"""
MCP Bridge dependency installer.

Checks and installs the tools required to run MCP Bridge:
- Python
- Node.js / npm
- Supergateway
- Cloudflared

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
        print("✗ Node.js missing. Install Node.js from https://nodejs.org/")


def install_cloudflared():
    if command_exists("cloudflared"):
        print("✓ Cloudflared detected")
        return

    system = platform.system()
    print("\nCloudflared not detected. Attempting installation...")

    if system == "Windows":
        if command_exists("winget"):
            run(["winget", "install", "--id", "Cloudflare.cloudflared"])
        else:
            print("✗ winget unavailable. Install cloudflared manually.")

    elif system == "Darwin":
        if command_exists("brew"):
            run(["brew", "install", "cloudflared"])
        else:
            print("✗ Homebrew unavailable. Install cloudflared manually.")

    elif system == "Linux":
        if command_exists("apt"):
            run(["sudo", "apt", "install", "cloudflared"])
        else:
            print("✗ Automatic Linux install unavailable. Install cloudflared manually.")

    else:
        print(f"✗ Unsupported platform: {system}")

    if command_exists("cloudflared"):
        print("✓ Cloudflared installed")
    else:
        print("! Cloudflared still missing")


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
    install_cloudflared()

    print("\nDependency setup complete.")
    print("Run:")
    print("  python scripts/mcp-bridge.py")


if __name__ == "__main__":
    main()
