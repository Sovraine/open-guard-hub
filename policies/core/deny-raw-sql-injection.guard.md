---
name: deny-raw-sql-injection
version: "1.0.0"
domain: core/common
description: Deny database queries containing SQL injection patterns
schema_version: 1
match:
  actions: ["execute", "insert", "update", "delete"]
  servers: ["sqlite", "mysql", "postgres", "postgresql", "mssql", "database", "db"]
verdict: DENY
severity: CRITICAL
priority: 95
author: community
license: CC-BY-SA-4.0
tags: [database, sql-injection, owasp, security]
signature: null
certified: false
---

# deny-raw-sql-injection

## What it does

Blocks database queries that contain common SQL injection patterns such as unparameterized string concatenation, tautology conditions (`1=1`, `OR TRUE`), stacked queries with semicolons, and UNION-based injection attempts.

## Why it exists

SQL injection remains OWASP Top 10 #1. When AI agents construct database queries dynamically, they may inadvertently introduce injection vectors — especially when incorporating user-supplied input or tool outputs into raw SQL strings.

## What gets blocked

- Queries with tautology patterns (`' OR '1'='1`, `OR TRUE`)
- Stacked queries using semicolons to chain destructive operations
- UNION SELECT injection attempts
- String concatenation in WHERE clauses without parameterization
- Comment-based truncation (`--`, `#`, `/* */`)

## What is still allowed

- Parameterized queries using placeholders (`$1`, `%s`, `?`)
- ORM-generated queries (SQLAlchemy, Django ORM, Prisma)
- Stored procedure calls
- Legitimate uses of UNION in application queries

## How to override

If an agent needs to execute raw SQL for a legitimate migration or administrative task:

```yaml
override:
  policy: deny-raw-sql-injection
  reason: "Running approved schema migration script"
  approved_by: human
```
