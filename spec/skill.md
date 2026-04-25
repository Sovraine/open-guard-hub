<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Skill Specification (`.skill.md`)

A Skill defines an atomic capability with mapped taxonomy verbs, risk level, pre/post-conditions, and side effects.

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
| `version` | string | Semantic version |
| `domain` | string | Sector path (e.g. `sectors/financial-services`) |
| `description` | string | One-line description |
| `schema_version` | integer | Must be `1` |
| `verbs` | list[string] | Taxonomy verbs this skill invokes |
| `risk` | enum | `READ-ONLY`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `target` | string | What the skill operates on |
| `author` | string | `"community"` for community contributions |
| `license` | string | `"CC-BY-SA-4.0"` for hub content |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `requires_context` | list[string] | `[]` | Required context fields |
| `preconditions` | list[string] | `[]` | Pre-execution conditions |
| `postconditions` | list[string] | `[]` | Post-execution conditions |
| `side_effects` | list[string] | `[]` | State changes |
| `idempotent` | boolean | `true` | Safe to re-execute |
| `reversible` | boolean | `true` | Can be undone |
| `sector` | string | — | Sector name |
| `tags` | list[string] | `[]` | Classification tags |
| `signature` | string\|null | `null` | Ed25519 signature |
| `certified` | boolean | `false` | Whether audited |

## Risk Level Rule

The `risk` of the skill must match the **highest** risk level of the invoked verbs:

| Verb examples | Typical Risk |
|---------------|-------------|
| `read`, `list`, `search` | READ-ONLY |
| `create`, `notify`, `comment` | LOW |
| `update`, `configure`, `schedule` | MEDIUM |
| `delete`, `grant`, `transfer-funds` | HIGH |
| `drop`, `truncate`, `exploit` | CRITICAL |

## Properties

| Field | Meaning | Governance impact |
|-------|---------|-------------------|
| `idempotent: true` | Re-execution safe | Automatic retry possible |
| `idempotent: false` | Re-execution dangerous | Watch for duplicates |
| `reversible: true` | Can be undone | Less risk |
| `reversible: false` | Irreversible | ESCALATE recommended |

## Required Body Sections

```markdown
## What it does
## Inputs
## Governance constraints
## Side effects
## Error handling
```

## Validation Rules

| Check ID | Severity | Description |
|----------|----------|-------------|
| GUARD-044 | MEDIUM | Missing required body section |
| — | WARNING | `risk` inconsistent with verb risk levels |
| — | WARNING | `idempotent: false` without documented `side_effects` |

## Example

```yaml
---
name: kyc-verify
version: "1.0.0"
domain: sectors/financial-services
description: "Verify customer identity for KYC compliance"
schema_version: 1
verbs: [kyc-verify, read, search]
risk: MEDIUM
target: customer
requires_context: [customer_id, verification_type]
preconditions:
  - "customer_id is not null"
  - "session is authenticated"
postconditions:
  - "audit log entry created"
  - "verification status updated"
side_effects:
  - "Updates customer verification status"
  - "Creates compliance record"
idempotent: true
reversible: false
sector: financial-services
author: community
license: CC-BY-SA-4.0
tags: [kyc, compliance]
signature: null
certified: false
---
```

```markdown
## What it does
Verifies customer identity against identity databases for KYC compliance.

## Inputs
- `customer_id`: unique customer identifier
- `verification_type`: "basic" or "enhanced"

## Governance constraints
Must create an audit trail entry. Enhanced verification requires human review
for flagged results.

## Side effects
Updates the customer's verification status in the compliance system.
Creates a timestamped compliance record.

## Error handling
On failure, the verification status remains unchanged. The attempt is logged.
Retry is safe (idempotent).
```
