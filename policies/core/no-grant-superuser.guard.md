---
name: no-grant-superuser
version: "1.0.0"
domain: core/database
description: Deny granting superuser or all privileges via SQL GRANT
schema_version: 1
match:
  actions: ["grant"]
  contexts:
    privileges: "*"
verdict: DENY
severity: CRITICAL
priority: 100
author: sovraine
license: CC-BY-SA-4.0
tags: [database, privileges, security]
signature: null
certified: false
---

## What it does

Blocks any SQL `GRANT` statement that assigns superuser, `ALL PRIVILEGES`, or wildcard (`*`) privileges to any role or user.

## Why it exists

Granting superuser or all privileges bypasses all role-based access control (RBAC). A single compromised account with superuser rights can read, modify, or destroy every object in the database. This policy enforces the principle of least privilege at the guard level, preventing privilege escalation whether intentional or accidental.

## What gets blocked

- `GRANT ALL PRIVILEGES ON *.* TO 'user'`
- `GRANT SUPERUSER TO role_name`
- `GRANT ALL ON SCHEMA public TO user`
- Any GRANT where the resolved privileges match `*` or `ALL`

## What is still allowed

- `GRANT SELECT ON table_name TO readonly_role`
- `GRANT INSERT, UPDATE ON schema.table TO app_role`
- Any GRANT with explicitly scoped, non-superuser privileges

## How to override

This policy cannot be overridden by agents. A database administrator must connect directly and execute the GRANT manually, outside of the MCP tool chain. All such actions should be logged in the audit trail.
