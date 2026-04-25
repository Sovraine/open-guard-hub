---
name: deny-plaintext-secret-in-message
version: "1.0.0"
domain: core
description: Deny actions that transmit plaintext secrets via messages, notifications, or shared content
schema_version: 1
match:
  actions: ["notify", "share", "create", "execute"]
verdict: DENY
severity: HIGH
priority: 80
author: community
license: CC-BY-SA-4.0
tags: [secrets, messaging, exfiltration, security]
signature: null
certified: false
---

# deny-plaintext-secret-in-message

## What it does

Blocks any agent action that would send plaintext secrets (API keys, passwords, tokens, private keys) through messaging channels, notifications, shared documents, or any outbound communication.

## Why it exists

Secret exfiltration via messages is a common attack vector for compromised or misconfigured agents. An agent with access to environment variables or secret stores could inadvertently (or maliciously) leak credentials through Slack messages, email notifications, PR comments, or shared documents. This policy stops secrets at the gate before they leave the system boundary.

## What gets blocked

- Sending messages containing patterns like `AKIA...`, `sk-...`, `ghp_...`, `xoxb-...`
- Sharing documents or notifications with plaintext `password`, `secret`, `token`, or `api_key` values
- Creating comments or issues that embed private keys or connection strings
- Executing outbound API calls with secret material in the request body

## What is still allowed

- Messages referencing secret names without values (`"rotated the DB_PASSWORD credential"`)
- Notifications about secret-related events (`"secret xyz expired"`)
- Sharing masked or redacted values (`sk-...xxxx`, `****`)
- Internal agent-to-agent communication through the guard runtime

## How to override

If an agent legitimately needs to transmit a secret (e.g. credential rotation flow):

```yaml
override:
  policy: deny-plaintext-secret-in-message
  reason: "Automated credential rotation via secure channel"
  approved_by: human
```
