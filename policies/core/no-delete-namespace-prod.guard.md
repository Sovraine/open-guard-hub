---
name: no-delete-namespace-prod
version: "1.0.0"
domain: core/kubernetes
description: Deny deletion of production namespaces
schema_version: 1
match:
  actions: ["delete-namespace"]
  contexts:
    environment: "production"
verdict: DENY
severity: CRITICAL
priority: 120
author: sovraine
license: CC-BY-SA-4.0
tags: [kubernetes, production, destructive]
signature: null
certified: false
---

## What it does

Unconditionally blocks any attempt to delete a Kubernetes namespace in the production environment.

## Why it exists

Deleting a production namespace destroys all resources within it — deployments, services, secrets, persistent volume claims, and config maps — irreversibly. This is the single most destructive operation in a Kubernetes cluster. No automated agent should ever perform this action, regardless of context or justification.

## What gets blocked

- `delete-namespace` where `environment` is `production`
- Applies to all namespaces in the production cluster, regardless of name or content

## What is still allowed

- Deleting namespaces in `staging`, `development`, or `test` environments
- Deleting individual resources within a production namespace (governed by other policies)
- Creating or updating namespaces in production

## How to override

This policy has no override mechanism. Namespace deletion in production must be performed manually by a cluster administrator using `kubectl` or `oc` directly, with full audit trail and change management approval.
