---
name: escalate-crm-bulk
version: "1.0.0"
domain: core/common
description: Escalate bulk and delete operations on CRM and project management MCP servers
schema_version: 1
match:
  servers: ["hubspot", "linear", "notion"]
  actions: ["update", "delete"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 80
author: sovraine
license: CC-BY-SA-4.0
tags: [crm, project-management, bulk, data-loss, safety]
signature: null
certified: false
---

## What it does

Requires human approval before deleting or archiving objects on CRM and project management platforms.

## Why it exists

CRM and project management platforms store business-critical data: customer records, deal pipelines, project issues, and content blocks. Deleting or archiving objects can break cross-references, lose customer history, and disrupt team workflows. Bulk operations amplify the risk — a single batch archive on HubSpot can affect hundreds of records.

## What gets blocked

- `update` and `delete` actions on HubSpot, Linear, and Notion servers
- Batch archive operations on CRM objects
- Any action matching these servers with risk >= HIGH

## Servers covered

- **HubSpot** — `crm_archive_object`, `crm_batch_archive_objects`
- **Linear** — `linear_delete_issue`, `linear_bulk_update_issues`
- **Notion** — `API-delete-a-block`

## What is still allowed

- All `read`, `list`, and `search` actions
- `create` and `update` on individual records
- Creating and updating properties, associations, comments

## How to override

A human operator must confirm the deletion with: the object type, number of affected records, and acknowledgment that archived/deleted objects may not be recoverable. The confirmation is recorded in the audit log.
