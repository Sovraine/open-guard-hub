<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: default
version: "1.0.0"
domain: core/common
description: "Default agent profile — permissive baseline for all AI clients"
schema_version: 1
soul: helpful-professional
model: null
skills: []
allowed_verbs: [read, list, search, create, update, execute, list-resources, get-resource, describe-resource, create-resource, apply-manifest]
denied_verbs: [delete, drop, truncate, delete-resource, exec-in-pod]
max_risk: MEDIUM
requires_human_above: MEDIUM
sandbox: false
policies:
  - no-tls-bypass
  - no-env-file-commit
  - no-world-readable-secrets
  - no-credential-in-prompt
  - no-tool-abuse-escalation
sector: generic
author: sovraine
license: CC-BY-SA-4.0
tags: [default, baseline, fallback]
certified: false
---

## Purpose

Fallback agent profile used when no specific agent definition exists for the AI client. Permits standard read/write operations with human escalation on high-risk actions.

## Guardrails

- **Max risk level**: MEDIUM — most read/write operations allowed
- **Destructive denied**: delete, drop, truncate, delete-resource, exec-in-pod
- **Human escalation**: MEDIUM-risk operations and above require human approval

## Allowed actions

- Reading files and resources
- Listing and searching resources
- Creating and updating resources
- Executing standard operations

## Denied actions

- Deleting resources directly (must escalate)
- Database destructive operations (drop, truncate)
- Executing commands inside pods (exec-in-pod)

## Escalation

MEDIUM-risk and above operations escalate to human review.
