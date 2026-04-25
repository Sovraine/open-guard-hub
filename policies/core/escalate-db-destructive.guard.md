---
name: escalate-db-destructive
version: "1.0.0"
domain: core/common
description: Escalate destructive operations and unreviewed queries on database MCP servers
schema_version: 1
match:
  servers: ["mongodb", "bigquery", "motherduck", "chroma"]
  actions: ["create", "update", "delete", "_detect"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 95
author: sovraine
license: CC-BY-SA-4.0
tags: [database, sql, destructive, data-loss, safety]
signature: null
certified: false
---

## What it does

Requires human approval before executing destructive operations, unreviewed SQL queries, or high-privilege changes on database platforms.

## Why it exists

Database operations can cause irreversible data loss at scale. Dropping a collection or database deletes all data with no undo. `DELETE FROM` without a `WHERE` clause wipes a table. `UPDATE` on the wrong scope corrupts data. Creating database users or access lists grants persistent access that may outlive the session. SQL queries via `_detect` actions may contain arbitrary DDL/DML that bypasses the action classification.

## What gets blocked

- `create`, `update`, `delete` actions on MongoDB, BigQuery, MotherDuck, and Chroma servers with risk >= HIGH
- `_detect` actions (SQL queries) that may contain destructive DDL/DML
- Database user and access list creation on Atlas

## Servers covered

- **MongoDB** — `drop-database` (CRITICAL), `drop-collection` (CRITICAL), `drop-index`, `delete-many`, `update-many`, `rename-collection`, `atlas-create-db-user`, `atlas-create-access-list`, `atlas-streams-build`, `atlas-streams-manage`, `atlas-streams-teardown`
- **BigQuery** — `query` (CRITICAL, `_detect` + `sql_mapping`)
- **MotherDuck** — `execute_query` (CRITICAL, `_detect` + `sql_mapping`)

## What is still allowed

- `read` and `list` actions (listing datasets, tables, collections, indexes)
- `dry_run` on BigQuery (validates without executing)
- Schema inspection (get_table_info, collection metadata)
- `search` actions

## How to override

A human operator must confirm the operation with: the target database/collection/table, the scope of affected records, and acknowledgment that the action may be irreversible. For SQL queries, the full query text must be reviewed. The confirmation is recorded in the audit log.
