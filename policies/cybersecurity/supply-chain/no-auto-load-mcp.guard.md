---
name: no-auto-load-mcp
version: "1.0.0"
domain: sectors/cybersecurity
description: Block automatic loading and installation of untrusted MCP servers
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "npx.*mcp|npm.*install.*mcp|claude.*mcp.*add|mcp-server|claude-code-explorer"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [mcp, supply-chain, npm, package-install]
signature: null
certified: false
---

## What it does

Blocks automatic installation or execution of MCP (Model Context Protocol) servers from untrusted sources.

## Why it exists

The `nirholas/claude-code` malware uses multiple vectors to inject a malicious MCP server:

1. `.mcp.json` in repo root — auto-loads `node mcp-server/dist/index.js` when Claude Code opens the directory
2. `.vscode/mcp.json` — auto-loads via VS Code with `npx tsx mcp-server/src/index.ts`
3. npm package `claude-code-explorer-mcp` published by `claudecodes` (email: `ninabrekkerese@outlook.com`)
4. Registered in MCP Registry as `io.github.nirholas/claude-code-explorer-mcp`
5. GitHub Actions workflow auto-publishes to npm + MCP Registry on git tags

The MCP server exposes filesystem read tools (`read_file`, `search_files`, `list_directory`, `directory_tree`) giving the attacker read access to the victim's machine.

## What gets blocked

- `execute` — running MCP server binaries from untrusted repos
- `execute` — `npm install` or `npx` of MCP packages not in an allowlist
- `execute` — `claude mcp add` from unverified sources

## What is still allowed

- Reading `.mcp.json` files for analysis
- Using pre-approved MCP servers from verified publishers
- MCP server development in controlled environments

## How to override

The operator must maintain an explicit MCP server allowlist in the gateway configuration, specifying publisher identity and package hash. Adding a server to the allowlist requires a signed approval from the security team. No runtime user confirmation can bypass this policy.
