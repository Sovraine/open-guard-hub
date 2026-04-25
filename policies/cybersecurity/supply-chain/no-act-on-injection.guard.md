---
name: no-act-on-injection
version: "1.0.0"
domain: sectors/cybersecurity
description: Block actions triggered by prompt injection detected in repository files
schema_version: 1
match:
  actions: ["execute", "create", "update"]
  contexts:
    injection_detected: true
verdict: DENY
severity: CRITICAL
priority: 400
author: sovraine
license: CC-BY-SA-4.0
tags: [prompt-injection, ai-poisoning, agent-manipulation, supply-chain]
signature: null
certified: false
---

## What it does

Blocks any write or execute action when the content scanner has detected prompt injection in the current context (e.g., from repository files read by the agent).

## Why it exists

The `nirholas/claude-code` malware includes AI agent poisoning files:

- **`agent.md`** — Claude Code agent instructions that normalize the malicious code as "existing patterns to follow"
- **`Skill.md`** — 400+ line document describing the architecture, making AI treat x402/PTY/MCP as intended features
- **`.github/agents/agent.agent.md`** — GitHub Copilot Workspace agent profile: "senior software engineer specializing in this codebase"
- **`.github/copilot-instructions.md`** — States "This is the **leaked source code** of Anthropic's Claude Code CLI" for false legitimacy

**Proven impact:** When the user ran `/security-review` with Claude Code in this repo, Claude analyzed 1,884 files and reported "No Active Security Vulnerabilities Found" — the poisoning worked. Claude treated x402, PTY server, and MCP as legitimate features.

## What gets blocked

- Any `execute`, `create`, or `update` action when `injection_detected: true` is set in the evaluation context
- The content scanner (ONNX model: `protectai/deberta-v3-base-prompt-injection-v2`) sets this flag when it detects manipulation patterns in files read by the agent

## What is still allowed

- Reading files (including poisoned ones) for analysis — read is not blocked
- Actions when no injection has been detected in the current context

## How to override

The operator must explicitly configure a trusted repository allowlist in the gateway settings. Only repositories whose cryptographic identity (commit signature or deploy key) matches the allowlist may bypass injection-detected blocks. Per-action user confirmation is not sufficient for this CRITICAL policy.
