<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Agent Specification (`.agent.md`)

An Agent defines the identity, capabilities, and governance constraints of an AI agent. It references other hub artifacts (souls, skills, policies) by name.

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
| `domain` | string | Sector path (e.g. `sectors/healthcare`) |
| `description` | string | One-line description |
| `schema_version` | integer | Must be `1` |
| `allowed_verbs` | list[string] | Whitelist of taxonomy verbs |
| `denied_verbs` | list[string] | Blacklist of taxonomy verbs (overrides allowed) |
| `max_risk` | enum | Maximum risk level: `READ-ONLY`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `requires_human_above` | enum | Auto-escalate if risk >= this level |
| `policies` | list[string] | Policy names to apply |
| `author` | string | `"community"` for community contributions |
| `license` | string | `"CC-BY-SA-4.0"` for hub content |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `soul` | string\|null | `null` | Referenced `.soul.md` by name |
| `model` | string\|null | `null` | Recommended model (advisory) |
| `skills` | list[string] | `[]` | Referenced `.skill.md` names |
| `sandbox` | boolean | `false` | Must run in sandbox |
| `sector` | string | — | Sector name |
| `tags` | list[string] | `[]` | Classification tags |
| `signature` | string\|null | `null` | Ed25519 signature |
| `certified` | boolean | `false` | Whether audited |

## Cross-References

| Field | Resolves to |
|-------|-------------|
| `soul` | `souls/{sector}/{name}.soul.md` |
| `skills[]` | `skills/{sector}/{name}.skill.md` |
| `policies[]` | `policies/{sector}/{name}.guard.md` |
| `allowed_verbs[]` | `core/**/_verbs.yaml` or `sectors/**/_verbs.yaml` |
| `denied_verbs[]` | same |

Referenced artifacts must exist on `main` (not in other open PRs).

## Required Body Sections

```markdown
## Purpose
## Guardrails
## Allowed actions
## Denied actions
## Escalation
```

## Validation Rules

| Check ID | Severity | Description |
|----------|----------|-------------|
| GUARD-026 | MEDIUM | Verb in both `allowed_verbs` and `denied_verbs` |
| GUARD-027 | MEDIUM | Unknown verb in `allowed_verbs` or `denied_verbs` |
| GUARD-028 | MEDIUM | Referenced soul does not exist |
| GUARD-030 | MEDIUM | Referenced policy does not exist |

## Example

```yaml
---
name: clinical-assistant
version: "1.0.0"
domain: sectors/healthcare
description: "Clinical decision support agent"
schema_version: 1
soul: clinical-empathetic
skills:
  - patient-lookup
  - drug-interaction-check
allowed_verbs: [read, search, list]
denied_verbs: [delete, drop, truncate]
max_risk: MEDIUM
requires_human_above: HIGH
sandbox: true
policies:
  - no-override-drug-interaction
  - escalate-break-glass
sector: healthcare
author: community
license: CC-BY-SA-4.0
tags: [healthcare, clinical]
signature: null
certified: false
---
```

```markdown
## Purpose
Clinical decision support for healthcare professionals. Helps with patient lookup,
drug interaction checks, and lab result summaries.

## Guardrails
Limited to read-only operations. Cannot modify patient records or prescriptions.

## Allowed actions
- Read patient records
- Search drug interaction databases
- List lab results

## Denied actions
- Delete any patient data
- Modify treatment plans
- Override drug interaction warnings

## Escalation
Any action above MEDIUM risk is automatically escalated to a human clinician.
```
