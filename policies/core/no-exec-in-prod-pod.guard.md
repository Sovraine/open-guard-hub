---
name: no-exec-in-prod-pod
version: "1.0.0"
domain: core/kubernetes
description: Escalate to human before exec-in-pod in production
schema_version: 1
match:
  actions: ["exec-in-pod"]
  contexts:
    environment: "production"
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 100
author: sovraine
license: CC-BY-SA-4.0
tags: [kubernetes, production, safety]
signature: null
certified: false
---

## What it does

Requires explicit human approval before any `exec-in-pod` action targeting a production environment.

## Why it exists

Executing commands inside a production pod can compromise running workloads, exfiltrate data, or cause outages. Unlike staging or development, production pods serve real users and contain live data. Human review ensures that the command is justified, scoped, and that alternatives (logs, metrics, read-only debug endpoints) have been considered first.

## What gets blocked

- `exec-in-pod` on any pod where `environment` is `production`
- Applies regardless of the command being executed (read-only or not)

## What is still allowed

- `exec-in-pod` in `staging`, `development`, or `test` environments (no escalation)
- Reading pod logs via `get-logs` (separate action, not matched)
- Port-forwarding for local debugging

## How to override

A human operator must approve the escalation. The approval is recorded in the audit log with the approver identity, timestamp, and justification.
