<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: file-read
version: "1.0.0"
domain: core/common
description: "Read file contents from local or remote filesystems"
schema_version: 1
verbs: [read]
target: file
risk: READ-ONLY
requires_context: [path]
preconditions: ["file exists", "caller has read permission"]
postconditions: ["file contents returned unchanged"]
side_effects: []
idempotent: true
reversible: false
sector: core
author: sovraine
license: CC-BY-SA-4.0
tags: [io, read-only, safe]
certified: false
---

## What it does

Reads and returns the contents of a file from a local filesystem or remote storage backend. Supports text and binary files. No modifications are made to the file.

## Inputs

- **path** (required): Absolute or relative file path
- **offset** (optional): Start reading from byte offset
- **limit** (optional): Maximum bytes to read (prevents memory exhaustion)

## Governance constraints

- READ-ONLY risk: File contents are never modified
- No wildcards allowed: Must specify exact file path
- Permissions enforced: Caller must have read access to the file
- No symlink traversal: Path canonicalization prevents escape from designated directories
- Idempotent: Reading the same file multiple times returns identical results

## Side effects

- **Audit logging**: File read is logged with timestamp, caller identity, and path
- **Access metrics**: Read count incremented for audit and billing
- **No state changes**: File system remains unmodified

## Error handling

- File not found → returns 404 error, no escalation
- Permission denied → returns 403 error, logged for audit
- Path traversal detected → returns 400 error, triggers security alert
- File too large → returns 413 error, caller must request with offset/limit
