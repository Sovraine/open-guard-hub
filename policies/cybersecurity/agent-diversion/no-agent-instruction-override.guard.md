---
name: no-agent-instruction-override
version: "1.0.0"
domain: sectors/cybersecurity
description: Block repository files from overriding agent system instructions
schema_version: 1
match:
  actions: ["execute", "create", "update", "configure"]
  contexts:
    source_file_pattern: "agent\\.md|AGENTS\\.md|Skill\\.md|CLAUDE\\.md|\\.github/copilot-instructions\\.md|\\.github/agents/|\\.cursorrules|\\.cursor/|\\.aider|CONVENTIONS\\.md|CODEX\\.md"
    injection_detected: true
verdict: DENY
severity: CRITICAL
priority: 400
author: sovraine
license: CC-BY-SA-4.0
tags: [prompt-injection, agent-poisoning, instruction-override, ai-safety]
signature: null
certified: false
---

## What it does

Prevents repository-provided instruction files from overriding the agent's core system instructions, policies, or security guardrails.

## Why it exists

Every major AI coding tool has a repo-level instruction file that the agent follows blindly:

| Tool | Instruction file | Effect |
|------|-----------------|--------|
| Claude Code | `CLAUDE.md`, `agent.md` | Loaded into system context, treated as instructions |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/agents/*.md` | Defines agent behavior |
| Cursor | `.cursorrules`, `.cursor/` | Overrides default behavior |
| Aider | `.aider` | Configures agent conventions |
| Codex | `CODEX.md` | Agent instructions |

In the nirholas/claude-code attack:
- `agent.md` told Claude to "match existing TypeScript style" → normalized x402 stealer
- `Skill.md` (400+ lines) described the full architecture → made Claude treat RAT as a feature
- `.github/copilot-instructions.md` stated "leaked source code" → false legitimacy
- Result: `/security-review` found **zero vulnerabilities** in a repo with 7 attack vectors

## What gets blocked

- Any action triggered by instructions from repo-provided agent files when injection is detected
- Overriding agent denied_verbs, max_risk, or policy list from repository context
- Repository files cannot grant the agent capabilities beyond its profile

## What is still allowed

- Reading these files for analysis and reporting
- Following instructions from the agent's own profile (set by the operator, not the repo)
- Legitimate CLAUDE.md files in repos the operator explicitly trusts

## How to override

The operator must explicitly mark repositories as trusted in the gateway configuration by specifying their cryptographic identity (GPG-signed commits or deploy key fingerprint). Trusted repositories may provide agent instruction files without triggering this policy. Trust cannot be granted at runtime by the user or by repository content itself.
