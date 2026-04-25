---
name: no-credential-in-prompt
version: "1.0.0"
domain: sectors/cybersecurity
description: Detect and redact credentials, tokens, and secrets in LLM prompts and responses
schema_version: 1
match:
  actions: ["execute", "create", "export"]
  contexts:
    content_pattern: "sk-ant-|ANTHROPIC_API_KEY=sk-|Bearer sk-|eyJ[A-Za-z0-9_-]{20,}\\.eyJ|-----BEGIN.*PRIVATE KEY|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|glpat-[A-Za-z0-9-]{20}|xox[bpas]-[A-Za-z0-9-]{10,}"
verdict: DENY
severity: CRITICAL
priority: 400
author: sovraine
license: CC-BY-SA-4.0
tags: [credentials, secrets, tokens, api-keys, data-leak, ai-safety]
signature: null
certified: false
---

## What it does

Detects credentials, API keys, tokens, and private keys appearing in tool call arguments, LLM prompts, or agent responses, and blocks actions that would expose or transmit them.

## Why it exists

AI agents routinely read configuration files, environment variables, and logs that contain credentials. Without protection, these credentials can:

1. **Leak into LLM context**: Agent reads `.env` → credential appears in prompt → sent to LLM API
2. **Leak into tool calls**: Agent passes a credential as an argument to a tool
3. **Leak into output**: Agent includes credentials in generated code, commit messages, or reports
4. **Be stolen by malicious repos**: The nirholas/claude-code attack stored private keys in `~/.claude/config.json` and OAuth tokens were found in Claude session logs at `.guard/.credentials.json`

Credential patterns detected:
- **Anthropic**: `sk-ant-*` API keys, OAuth access/refresh tokens (JWT `eyJ...`)
- **AWS**: `AKIA*` access key IDs
- **GitHub**: `ghp_*` personal access tokens
- **GitLab**: `glpat-*` personal access tokens
- **Slack**: `xoxb-*`, `xoxp-*` bot and user tokens
- **SSH/TLS**: `-----BEGIN * PRIVATE KEY-----`

## What gets blocked

- `execute` — commands that include credentials in arguments
- `create` — file creation with embedded credentials
- `export` — any data export containing credential patterns

## What is still allowed

- Reading files that happen to contain credentials (read-only, but the credentials are redacted before reaching the LLM)
- Using credentials via secure channels (environment variables, keychain, file descriptors)
- Referencing credential patterns in documentation or security analysis

## How to override

The operator must configure a credential handling policy specifying which credential types may pass through the gateway (e.g., for rotation workflows). All credentials must be redacted by default; exceptions require the operator to enable passthrough for specific patterns with mandatory audit logging. Users cannot disable credential detection at runtime.
