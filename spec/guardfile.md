<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# GuardFile Specification (`.guard.md`)

A GuardFile defines a governance policy for AI agent actions. It uses YAML frontmatter for machine-readable metadata and a Markdown body for human-readable documentation.

## Format

```
---
<YAML frontmatter>
---

<Markdown body>
```

## Frontmatter Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique name in kebab-case |
| `version` | string | Semantic version (e.g. `"1.0.0"`) |
| `domain` | string | Sector path (e.g. `core`, `financial-services/banking`) |
| `description` | string | One-line description |
| `schema_version` | integer | Must be `1` |
| `match` | object | Action matching criteria (see below) |
| `verdict` | enum | One of: `ALLOW`, `DENY`, `WARN`, `FILTER`, `ESCALATE_DEBATE`, `ESCALATE_HUMAN` |
| `severity` | enum | One of: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `priority` | integer | Evaluation order (higher = first). DENY wins on tie. |
| `author` | string | `"community"` for community contributions |
| `license` | string | `"CC-BY-SA-4.0"` for hub content |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `tags` | list[string] | `[]` | Classification tags |
| `requires` | list[string] | `[]` | Prerequisite policy names |
| `conflicts_with` | list[string] | `[]` | Incompatible policy names |
| `signature` | string\|null | `null` | Ed25519 signature (set by `guard sign`) |
| `certified` | boolean | `false` | Whether audited by Sovraine |
| `certified_for` | list[string] | `[]` | Compliance standards (e.g. `"SOC2-CC6.1"`) |
| `certified_date` | string\|null | `null` | ISO 8601 date |
| `certified_expires` | string\|null | `null` | ISO 8601 date |

### Match Object

```yaml
match:
  actions:
    - "transfer-funds"           # Exact canonical verb
    - "transfer-*"               # Glob wildcard
  targets:                        # Optional
    - "account-*"
  contexts:                       # Optional
    agent: "ops-*"
    environment: "production"
```

- `actions` (required): list of taxonomy verbs or glob patterns
- `targets` (optional): list of target patterns
- `contexts` (optional): key-value pairs with glob support
- Only glob patterns (`*`, `?`) are allowed — **no regex** (injection risk)

## Verdicts

| Verdict | Behavior |
|---------|----------|
| `ALLOW` | Action is executed |
| `DENY` | Action is blocked |
| `WARN` | Action is executed, warning logged |
| `FILTER` | Action is executed with modified parameters |
| `ESCALATE_DEBATE` | Action is sent to multi-agent debate |
| `ESCALATE_HUMAN` | Action waits for human approval |

### Constraint

`ALLOW` + severity `HIGH` or `CRITICAL` = scanner error (GUARD-076). An ALLOW verdict cannot have a high severity.

### Fast-Path

READ-ONLY verbs (`read`, `list`, `search`, `select`, `describe-resource`) are fast-pathed as ALLOW **before** policy evaluation. A DENY or ESCALATE policy on a READ-ONLY verb will be silently ignored.

## Priority

- Integer value, **higher = evaluated first**
- On tie: **DENY wins** (fail-closed design)
- Ranges:
  - 0-49: default/onboarding policies
  - 50-99: sector policies
  - 100-149: enterprise policies
  - 150+: exception/override policies

## Required Body Sections

The Markdown body **must** contain these exact headers:

```markdown
## What it does
## Why it exists
## What gets blocked
## What is still allowed
## How to override
```

### Optional Body Sections

```markdown
## Compliance
## Related policies
## Changelog
```

## Validation Rules

| Check ID | Severity | Description |
|----------|----------|-------------|
| GUARD-070 | MEDIUM | Policy references an action not in the taxonomy |
| GUARD-076 | ERROR | ALLOW verdict with HIGH/CRITICAL severity |
| Fast-path | WARNING | DENY/ESCALATE on a READ-ONLY verb |

## Example

```yaml
---
name: no-plaintext-secrets
version: "1.0.0"
domain: core
description: "Deny storing secrets in plaintext"
schema_version: 1
match:
  actions: ["store-secret-plaintext", "commit-secret"]
verdict: DENY
severity: CRITICAL
priority: 250
author: community
license: CC-BY-SA-4.0
tags: [security, secrets]
signature: null
certified: false
---
```

```markdown
## What it does
Blocks any attempt to store secrets (API keys, passwords, tokens) in plaintext.

## Why it exists
Plaintext secrets in code or config are the #1 cause of credential leaks.

## What gets blocked
- Committing files containing API keys or passwords
- Storing secrets in environment variables without encryption

## What is still allowed
- Storing secrets in a vault (HashiCorp Vault, AWS Secrets Manager)
- Using encrypted secret references

## How to override
Use a secrets manager and reference the secret by ID instead of value.
```
