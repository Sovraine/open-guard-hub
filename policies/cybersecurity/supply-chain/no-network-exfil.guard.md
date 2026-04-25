---
name: no-network-exfil
version: "1.0.0"
domain: sectors/cybersecurity
description: Block network exfiltration attempts via shell commands or code execution
schema_version: 1
match:
  actions: ["execute", "export"]
  contexts:
    content_pattern: "curl|wget|fetch\\(|axios\\.|http\\.get|https\\.get|nc\\s|ncat|netcat|socket\\.connect|dns.*lookup|nslookup.*TXT"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [exfiltration, network, data-breach, supply-chain]
signature: null
certified: false
---

## What it does

Blocks execution of commands or code that could exfiltrate data to external networks.

## Why it exists

The `nirholas/claude-code` malware has multiple potential exfiltration vectors:

- `WebFetchTool` patched to send signed crypto transactions to arbitrary servers
- PTY server opens shell access on all network interfaces
- MCP server can read filesystem and forward data
- Git hooks can execute arbitrary network calls
- npm `postinstall` scripts could beacon to C2 servers

Even with container network isolation (`--network none`), defense-in-depth requires blocking exfiltration at the policy level. A misconfigured container or a future environment change should not silently enable data exfiltration.

## What gets blocked

- `execute` — shell commands that transfer data (`curl`, `wget`, `nc`, `netcat`)
- `execute` — code that initiates outbound connections (`fetch()`, `axios`, `http.get`)
- `export` — any data export action
- `execute` — DNS-based exfiltration (`nslookup TXT`, `dns lookup`)

## What is still allowed

- Reading network-related code for analysis
- Inbound connections to the gateway itself
- localhost communication between containers in the same pod

## How to override

The operator must configure a network egress allowlist specifying permitted destination hosts, ports, and protocols. Each allowed destination requires documented justification. Outbound connections to unlisted destinations remain blocked regardless of user confirmation.
