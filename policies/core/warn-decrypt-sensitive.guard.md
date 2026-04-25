---
name: warn-decrypt-sensitive
version: "1.0.0"
domain: core/security
description: Warn and log when decryption of sensitive data occurs
schema_version: 1
match:
  actions: ["decrypt"]
verdict: WARN
severity: HIGH
priority: 50
author: sovraine
license: CC-BY-SA-4.0
tags: [security, encryption, audit]
signature: null
certified: false
---

## What it does

Emits a warning and creates an audit log entry whenever a `decrypt` action is requested, regardless of environment or target.

## Why it exists

Decryption of data is a security-sensitive operation that should always be visible in audit trails. Even when decryption is legitimate (e.g., reading encrypted secrets for deployment), the event must be recorded for compliance, incident investigation, and anomaly detection. This policy does not block the action but ensures visibility.

## What gets blocked

Nothing is blocked. The action proceeds after the warning is emitted.

## What is still allowed

- All `decrypt` operations proceed normally
- The warning is logged with the action context (who, what, when, why)

## How to override

No override is needed — this is a WARN-level policy. To suppress the warning entirely, remove or disable this policy in your GuardFile. This is not recommended for production environments.
