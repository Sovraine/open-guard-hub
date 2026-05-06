# CLAUDE.md — open-guard-hub

## Project Overview

OpenGuard Hub is the community registry of governance artifacts for AI agent actions. It contains the action taxonomy (18 sectors, ~66 sub-sectors), policies (.guard.md), agent definitions (.agent.md), souls (.soul.md), skills (.skill.md), and MCP server mappings (.mapping.yaml).

Licensed under **CC-BY-SA-4.0**. Contributions require DCO sign-off.

## Commands

```bash
# Validate the full hub
sg guard scan .

# Validate taxonomy only
sg guard scan --taxonomy .

# Download sg binary
# https://github.com/Sovraine/open-guard-cli/releases
```

## Structure

Root IS the hub — no `hub/` prefix.

```
core/       — Cross-sector verb definitions (9 domains)
sectors/    — Industry-specific verbs (18 sectors)
policies/   — Governance policies (.guard.md)
mappings/   — MCP server action mappings (.mapping.yaml)
agents/     — Agent definitions (.agent.md)
souls/      — Agent personas (.soul.md)
skills/     — Atomic capabilities (.skill.md)
gates/      — Kubernetes admission policies
templates/  — Scaffolding templates
spec/       — OGS format specification (CC-BY-4.0)
```

## Key Rules

- `sg guard scan` takes **directories**, never individual files
- Always scan `.` (root), not subdirectories — subdirectory scan produces false GUARD-070
- **Grade A required** for merge
- Community contributions: `certified: false`, `signature: null`, `author: community`

## Agents & Skills

See [AGENTS.md](AGENTS.md) for Claude Code agents and skills available for AI-assisted contribution.
