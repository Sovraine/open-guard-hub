<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: data-search
version: "1.0.0"
domain: core/common
description: "Search structured data with filters and pagination"
schema_version: 1
verbs: [search, list]
target: database
risk: READ-ONLY
requires_context: [dataset, query]
preconditions: ["dataset exists", "caller has read permission on dataset"]
postconditions: ["matching records returned", "original data unchanged"]
side_effects: []
idempotent: true
reversible: false
sector: core
author: sovraine
license: CC-BY-SA-4.0
tags: [data-access, read-only, query]
certified: false
---

## What it does

Searches a structured dataset (SQL database, NoSQL store, data warehouse) using filters, full-text queries, or parameterized search. Returns matching records without modifying the data.

## Inputs

- **dataset** (required): Name or identifier of the data source
- **query** (required): Filter expression, full-text query, or parameterized conditions
- **page** (optional): Pagination token or offset (default: 1)
- **limit** (optional): Maximum results per page (default: 100, max: 10000)
- **sort** (optional): Sort order and field

## Governance constraints

- READ-ONLY risk: No records are created, modified, or deleted
- Query validation: All filters are parsed and validated before execution
- SQL injection prevention: Parameterized queries used exclusively
- No wildcard full scans: Queries must include meaningful filters
- Rate limiting: Search calls are rate-limited per caller to prevent resource exhaustion
- Pagination enforced: Results cannot exceed max_limit to prevent memory exhaustion

## Side effects

- **Audit logging**: All searches are logged with timestamp, caller, dataset, and query
- **Query metrics**: Search count recorded for performance monitoring
- **Cached results**: Repeated searches may return cached results if within TTL
- **No data modification**: Dataset remains unchanged

## Error handling

- Invalid dataset → returns 404 error
- Permission denied → returns 403 error, logged for audit
- Malformed query → returns 400 error with validation details
- Query timeout → returns 504 error after max duration
- Result set too large → returns 413 error, caller must add more filters
