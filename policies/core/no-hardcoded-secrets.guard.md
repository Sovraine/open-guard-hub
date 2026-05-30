---
name: no-hardcoded-secrets
version: "1.0.0"
domain: core
description: Deny actions that embed plaintext secrets, API keys, or tokens in source code or configuration
schema_version: 1
match:
  actions: ["create", "update", "configure", "execute"]
  contexts:
    privacy_classification: "RESTRICTED"
verdict: DENY
severity: HIGH
priority: 85
author: community
license: CC-BY-SA-4.0
tags: [secrets, credentials, security, devsecops]
signature: null
certified: false
---

# no-hardcoded-secrets

## What it does

Blocks any agent action that would write plaintext secrets (API keys, passwords, tokens, private keys) directly into source files, configuration, or version-controlled resources.

## Why it exists

Hardcoded secrets are the #1 cause of credential leaks in public and private repositories. Once committed, secrets end up in git history and are extremely difficult to fully revoke. This policy enforces secret hygiene at the agent level before code ever reaches a repository.

## What gets blocked

- Writing files containing patterns like `AKIA...`, `sk-...`, `ghp_...`, `-----BEGIN.*PRIVATE KEY-----`
- Creating config resources with plaintext `password`, `secret`, or `token` fields
- Committing changes that introduce new secret-like strings

## What is still allowed

- References to environment variables (`$SECRET`, `os.environ["KEY"]`)
- References to secret managers (Vault, AWS Secrets Manager, 1Password CLI)
- Placeholder values (`<your-api-key-here>`, `changeme`, `xxx`)
- Hash values (SHA-256, bcrypt, etc.)

## How to override

If an agent legitimately needs to write a secret (e.g. seeding a local `.env.example`):

```yaml
override:
  policy: no-hardcoded-secrets
  reason: "Seeding example env file with placeholder values"
  approved_by: human
```
