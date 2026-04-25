---
name: no-env-file-commit
version: "1.0.0"
domain: core/common
description: Prevent committing secret files (.env, credentials, private keys) to version control
schema_version: 1
match:
  actions: ["create", "update", "execute"]
  contexts:
    target_pattern: "\\.env$|\\.env\\.|credentials\\.json|secrets\\.json|\\.pem$|\\.key$|\\.p12$|\\.pfx$|\\.keystore$|id_rsa|id_ed25519|\\.credentials$"
    content_pattern: "git add|git commit|git stage"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [git, secrets, credentials, environment, supply-chain]
signature: null
certified: false
---

## What it does

Prevents adding or committing secret files to git repositories.

## Why it exists

Accidentally committing secrets to git is one of the most common security mistakes:

- `.env` files with API keys and database credentials
- `credentials.json` with OAuth tokens (as found in the open-guard incident)
- `*.pem` and `*.key` private keys (GitHub App keys, TLS certificates)
- SSH keys (`id_rsa`, `id_ed25519`)
- Keystores and PKCS12 bundles

Once committed, secrets persist in git history even after deletion. They must be considered compromised and rotated immediately.

Real incidents from this investigation:
- `~/.app/credentials.json` contained plaintext OAuth tokens
- `~/Downloads/app.*.private-key.pem` was world-readable (644)

## What gets blocked

- `execute` — `git add` / `git commit` targeting secret file patterns
- `create` / `update` — writing secret files into `.git/` staging area

## What is still allowed

- Reading secret files for analysis
- `.env.example` and `.env.template` (templates without real values)
- `git add` of non-secret files
- Encrypted secret files (`.env.enc`, `.sops.yaml`)

## How to override

The operator must configure an exception list of secret file patterns that are permitted in version control (e.g., encrypted files, test fixtures with dummy values). The user may commit a flagged file after explicit confirmation that it contains no real credentials, and the action is logged for audit. Template files (`.env.example`) should be added to the exception list by default.
