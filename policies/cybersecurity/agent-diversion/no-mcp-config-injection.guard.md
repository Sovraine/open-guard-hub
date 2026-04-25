---
name: no-mcp-config-injection
version: "1.0.0"
domain: sectors/cybersecurity
description: Block auto-loading of MCP server configurations from repository files
schema_version: 1
match:
  actions: ["configure", "execute"]
  contexts:
    source_file_pattern: "\\.mcp\\.json|\\.vscode/mcp\\.json|mcp-server/|server\\.json"
    content_pattern: "mcpServers|mcp.*command|mcp.*args|claude.*mcp.*add|npx.*mcp"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [mcp, config-injection, auto-load, tool-injection, supply-chain]
signature: null
certified: false
---

## What it does

Blocks repository files from automatically registering MCP servers into the agent's tool inventory.

## Why it exists

MCP configuration files in repositories can silently add tools that the agent will use:

**Auto-load vectors:**
- `.mcp.json` in repo root → Claude Code auto-loads on directory entry
- `.vscode/mcp.json` → VS Code Copilot auto-loads
- `server.json` → MCP Registry entry for npm package
- `mcp-server/` directory → invites `npx` execution

**Why it's dangerous:**
- MCP tools run with the agent's permissions (filesystem, network, shell)
- A malicious MCP server can read any file, execute commands, exfiltrate data
- The user may not notice a new tool appearing in the agent's inventory
- Combined with agent poisoning, the agent is instructed to USE these tools

In the nirholas attack:
- `.mcp.json` → `{"mcpServers": {"claude-code-explorer": {"command": "node", "args": ["mcp-server/dist/index.js"]}}}`
- `.vscode/mcp.json` → same for VS Code
- `server.json` → registered in official MCP Registry as `io.github.nirholas/claude-code-explorer-mcp`
- The MCP server exposed: `read_file`, `search_files`, `list_directory`, `directory_tree`

## What gets blocked

- `configure` — auto-registration of MCP servers from repository files
- `execute` — launching MCP server binaries referenced in repo configs

## What is still allowed

- Reading .mcp.json for analysis
- MCP servers configured by the operator in their own settings (not from the repo)
- MCP servers from verified, signed publishers

## How to override

The operator must pre-approve specific MCP server configurations in the gateway settings by specifying the server command, arguments hash, and publisher identity. Repository-provided MCP configs can only be loaded if they match a pre-approved entry exactly. No runtime user confirmation can register a new MCP server from repository context.
