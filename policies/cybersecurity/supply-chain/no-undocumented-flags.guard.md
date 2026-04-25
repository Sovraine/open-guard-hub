---
name: no-undocumented-flags
version: "1.0.0"
domain: sectors/cybersecurity
description: Block activation of undocumented or hidden feature flags
schema_version: 1
match:
  actions: ["configure", "enable", "execute"]
  contexts:
    content_pattern: "KAIROS|WORKFLOW_SCRIPTS|TORCH|ULTRAPLAN|feature_flag.*enable|enableExperimental|CLAUDE_CODE_KAIROS|CLAUDE_CODE_WORKFLOW_SCRIPTS"
verdict: DENY
severity: HIGH
priority: 200
author: sovraine
license: CC-BY-SA-4.0
tags: [feature-flags, hidden-capability, supply-chain]
signature: null
certified: false
---

## What it does

Blocks activation of undocumented feature flags that could enable hidden or malicious code paths.

## Why it exists

The `nirholas/claude-code` malware injects hidden feature flags in `src/shims/bun-bundle.ts`:

| Flag | Env Variable | Purpose |
|------|-------------|---------|
| `KAIROS` | `CLAUDE_CODE_KAIROS` | Unknown — not in original Claude Code |
| `KAIROS_BRIEF` | `CLAUDE_CODE_KAIROS_BRIEF` | Unknown |
| `KAIROS_GITHUB_WEBHOOKS` | `CLAUDE_CODE_KAIROS_GITHUB_WEBHOOKS` | Unknown |
| `WORKFLOW_SCRIPTS` | `CLAUDE_CODE_WORKFLOW_SCRIPTS` | Unknown |
| `TORCH` | `CLAUDE_CODE_TORCH` | Unknown |
| `ULTRAPLAN` | `CLAUDE_CODE_ULTRAPLAN` | Unknown |

These flags enable dead-code paths via Bun's compile-time feature system. When set, they activate code that was not present in the legitimate Claude Code source, potentially containing additional payloads.

## What gets blocked

- `configure` / `enable` — setting environment variables for undocumented flags
- `execute` — running build commands with these flags activated

## What is still allowed

- Reading code that references feature flags (analysis)
- Using documented, legitimate feature flags from the original software

## How to override

The operator can register known feature flags in the gateway configuration with their expected behavior and source documentation. Flags must be verified against the upstream project's official release notes. Unrecognized flags can be allowed per-session with explicit user confirmation and an audit log entry.
