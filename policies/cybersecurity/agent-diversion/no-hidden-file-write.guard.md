---
name: no-hidden-file-write
version: "1.0.0"
domain: sectors/cybersecurity
description: Block writing to hidden directories used for persistence or configuration tampering
schema_version: 1
match:
  actions: ["create", "update"]
  contexts:
    target_pattern: "~/\\.|/home/.*?/\\.|\\$HOME/\\."
    exclude_pattern: "\\.claude/file-history|\\.claude/paste-cache|\\.git/(objects|refs|logs)"
    source_context: "repository"
verdict: DENY
severity: HIGH
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [hidden-files, persistence, dotfiles, configuration-tampering, ai-safety]
signature: null
certified: false
---

## What it does

Blocks repository-originated actions from writing to hidden (dot) directories in the user's home directory, which are commonly used for persistence and configuration tampering.

## Why it exists

Hidden directories in `$HOME` are high-value targets for persistence:

| Target | Effect |
|--------|--------|
| `~/.bashrc`, `~/.zshrc` | Execute code on every shell session |
| `~/.ssh/authorized_keys` | Grant SSH access to attacker |
| `~/.gitconfig` | Override git behavior globally |
| `~/.npmrc` | Redirect all npm installs to malicious registry |
| `~/.claude/config.json` | Store crypto private keys (x402 attack) |
| `~/.claude/settings.json` | Auto-approve all agent actions |
| `~/.gitpretty/` | Persistent malicious git hooks (nirholas attack) |
| `~/.local/bin/` | Shadow legitimate commands with malicious versions |
| `~/.config/` | Modify application configs |

In the nirholas attack:
- `~/.claude/config.json` → target for x402 private key storage
- `~/.gitpretty/` → persistent trojan scripts + git hooks
- `~/.zshrc` → the user had `NODE_TLS_REJECT_UNAUTHORIZED=0` (not from nirholas, but shows the risk)

## What gets blocked

- `create` / `update` — writing to any `~/.*` path when the action originates from repository context
- Exception: normal agent operations (file-history, paste-cache, git objects)

## What is still allowed

- Agent writing to its own operational directories (file-history, paste-cache)
- Normal git operations (.git/objects, .git/refs)
- Operator-initiated dotfile modifications

## How to override

The operator can define a dotfile write allowlist in the gateway configuration, specifying exact paths and allowed content patterns (e.g., `~/.npmrc` for registry configuration). The user may approve individual writes after reviewing the target path and content diff. Writes to shell config files (`~/.bashrc`, `~/.zshrc`) require operator pre-approval.
