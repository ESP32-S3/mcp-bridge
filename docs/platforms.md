# Platform Support

MCP Bridge supports Windows, macOS, and Linux.

## Windows

Use:

```powershell
scripts/mcp-bridge.ps1
```

## macOS / Linux

Install dependencies:

```bash
npm install -g supergateway
```

Run:

```bash
chmod +x scripts/mcp-bridge.sh
./scripts/mcp-bridge.sh
```

You can also use the Python launcher:

```bash
python3 scripts/mcp-bridge.py
```

## Why not a single EXE?

A universal executable is possible, but MCP Bridge depends on platform tools like Node.js, Supergateway, and optional tunnel providers. A native binary wrapper would increase maintenance complexity.

The recommended design is a small platform launcher around a shared configuration format.

Future releases may provide packaged binaries using tools like PyInstaller or Rust.
