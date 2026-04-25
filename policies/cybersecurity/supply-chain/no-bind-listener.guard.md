---
name: no-bind-listener
version: "1.0.0"
domain: sectors/cybersecurity
description: Block binding network listeners on all interfaces
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "0\\.0\\.0\\.0|listen\\(|createServer|WebSocketServer|node-pty|pty\\.spawn|net\\.Server"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [rat, network, pty, remote-access, supply-chain]
signature: null
certified: false
---

## What it does

Blocks any action that attempts to bind a network listener, especially on all interfaces (0.0.0.0), or spawn remote terminal sessions.

## Why it exists

The `nirholas/claude-code` malware includes a full Remote Access Trojan (RAT) in `src/server/web/pty-server.ts`:
- Express + WebSocket server on `0.0.0.0:3000`
- Spawns PTY terminals via `node-pty` giving full shell access
- Admin dashboard at `/admin` to list, monitor, kill sessions
- Multi-user support with API key, OAuth, and token authentication
- Docker deployment with `ANTHROPIC_API_KEY` forwarded to child processes
- Session persistence, scrollback buffer, grace periods

This is a complete Command & Control (C2) infrastructure.

## What gets blocked

- `execute` — any code that binds network listeners (`listen()`, `createServer`, `WebSocketServer`)
- `execute` — PTY/terminal spawning (`node-pty`, `pty.spawn`)
- `execute` — server binding on all interfaces (`0.0.0.0`)

## What is still allowed

- Connecting to existing servers as a client
- Reading server code for analysis
- localhost-only listeners for legitimate development tools

## How to override

The operator must define an authorized network services manifest in the gateway configuration, listing allowed listen addresses, ports, and protocols. Binding on all interfaces (0.0.0.0) requires an explicit operator approval with documented justification. Localhost-only listeners for known development tools can be pre-approved in the manifest.
