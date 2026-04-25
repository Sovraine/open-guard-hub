---
name: no-delete-tenant-data-without-confirmation
version: "1.0.0"
domain: sectors/saas-tech
description: Require human confirmation before deleting tenant data
schema_version: 1
match:
  actions: ["delete-tenant-data"]
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 100
author: sovraine
license: CC-BY-SA-4.0
tags: [saas, tenant, data-loss, irreversible]
signature: null
certified: false
---

## What it does

Escalates tenant data deletion requests to a human operator for explicit confirmation before execution.

## Why it exists

Tenant data deletion is permanent and affects all users of that tenant. In a multi-tenant SaaS environment, deleting the wrong tenant's data — or deleting data prematurely — can violate SLAs, breach data retention agreements, and destroy business-critical information with no recovery path. Human confirmation ensures the correct tenant is targeted and that retention periods have been respected.

## What gets blocked

- `delete-tenant-data` for any tenant, regardless of environment
- The action is paused and escalated to a human operator

## What is still allowed

- Soft-deleting or archiving tenant data (reversible)
- Exporting tenant data before deletion
- Viewing tenant data and metadata
- Deleting individual records within a tenant (governed by other policies)

## How to override

A human operator must confirm the deletion with: the tenant identifier, confirmation that data export has been offered or completed, confirmation that the retention period has elapsed, and acknowledgment that the action is irreversible. The confirmation is recorded in the audit log.
