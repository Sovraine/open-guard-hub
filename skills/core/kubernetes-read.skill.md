<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: kubernetes-read
version: "1.0.0"
domain: core/kubernetes
description: "Read-only Kubernetes operations: list, get, describe resources"
schema_version: 1
verbs: [list-resources, get-resource, describe-resource]
target: kubernetes-resource
risk: READ-ONLY
requires_context: []
preconditions: ["caller has RBAC read access"]
postconditions: ["cluster state unchanged"]
side_effects: []
idempotent: true
reversible: false
sector: core
author: sovraine
license: CC-BY-SA-4.0
tags: [kubernetes, read-only, safe]
certified: false
---

## What it does

Provides read-only access to Kubernetes resources: listing pods, namespaces, nodes, events, deployments, and getting individual resource details. No cluster state is modified.

## Verbs covered

- **list-resources**: List pods, namespaces, nodes, events, deployments, services
- **get-resource**: Get a specific pod, node, deployment, or any K8s resource
- **describe-resource**: Get detailed description of a resource

## Governance constraints

- READ-ONLY risk: Cluster state is never modified
- No mutations: Cannot create, update, delete, or scale resources
- No exec: Cannot execute commands inside pods
- RBAC enforced: Kubernetes RBAC limits what the caller can see
- Idempotent: Reading the same resource multiple times returns identical results

## Inputs

- **resource_type** (required): Kubernetes resource type (pod, deployment, service, node, namespace, event)
- **name** (optional): Specific resource name for get/describe operations
- **namespace** (optional): Kubernetes namespace (default: current namespace)
- **label_selector** (optional): Label filter for list operations

## Side effects

- None — all operations are strictly read-only
- No cluster state is modified
- No resources are created, updated, or deleted

## Error handling

- Resource not found → returns 404 error with resource type and name
- Namespace not found → returns 404 error
- RBAC denied → returns 403 error, logged for audit
- API server unavailable → returns 503 error
- Timeout → returns 504 error after configurable deadline
