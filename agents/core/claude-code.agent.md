<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: claude-code
version: "1.0.0"
domain: core/common
description: "Claude Code AI assistant — development and operations agent"
schema_version: 1
soul: claude-code-soul
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
sector: saas-tech
author: sovraine
license: CC-BY-SA-4.0
tags: [claude-code, development, operations]
certified: false
---

## Purpose

Agent profile for Claude Code operating through the open-guard-gateway. Permits read and standard CRUD operations on Kubernetes and other MCP servers, with escalation on high-risk destructive actions.

## Guardrails

- **Max risk level**: MEDIUM — most read/write operations allowed
- **Destructive denied**: delete-resource, drop, truncate, exec-in-pod explicitly denied
- **Human escalation**: HIGH-risk operations require human approval

## Allowed actions

- Reading resources (namespaces, pods, services, configmaps)
- Listing and searching resources
- Creating and updating resources (deployments, configmaps)
- Applying manifests
- Executing standard operations

## Denied actions

- Deleting resources directly (must escalate)
- Executing commands inside pods (exec-in-pod)
- Database destructive operations (drop, truncate)

## Escalation

HIGH-risk operations (e.g., modifying RBAC, editing secrets) escalate to human review.
