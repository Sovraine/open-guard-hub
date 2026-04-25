---
name: guard-skill-create
description: Create a skill .skill.md with the full format (YAML frontmatter + Markdown body). Defines the mapped verbs, risk, pre/post-conditions, side effects and governance constraints. Knows the taxonomy and hub conventions.
---

# Guard Skill Create

## Schema SkillDef

### YAML Frontmatter

```yaml
---
name: descriptive-kebab-case-name
version: "1.0.0"
domain: sectors/financial-services  # sectors/<sector> or core/<domain>
description: "One-line description"
schema_version: 1

# Action mapping
verbs:                              # taxonomy verbs this skill invokes
  - kyc-verify
  - read
  - search
target: customer                    # what this skill operates on
risk: MEDIUM                        # READ-ONLY | LOW | MEDIUM | HIGH | CRITICAL

# Constraints
requires_context:                   # required context fields
  - customer_id
  - verification_type
preconditions:                      # pre-execution conditions
  - "customer_id is not null"
  - "session is authenticated"
postconditions:                     # post-execution conditions
  - "audit log entry created"
  - "verification status updated"
side_effects:                       # state changes
  - "Updates customer verification status"
  - "Creates compliance record"
idempotent: true                    # safe to re-execute
reversible: false                   # can it be undone

# Metadata
sector: financial-services
author: "community"
license: "CC-BY-SA-4.0"
tags: [kyc, compliance, identity]
signature: null
certified: false
---
```

### Body Markdown — REQUIRED Headers

```markdown
## What it does
<Functional description. What exactly.>

## Inputs
<Expected parameters, required context, types.>

## Governance constraints
<Why certain restrictions exist. Link to policies.>

## Side effects
<What state changes occur.>

## Error handling
<What happens on failure. Rollback? Retry?>
```

## Risk Levels

The `risk` of the skill must match the highest risk level of the invoked verbs:

| Verb | Typical Risk | Examples |
|------|-------------|----------|
| `read`, `list`, `search` | READ-ONLY | Lookup, search |
| `create`, `notify`, `comment` | LOW | Non-destructive creation |
| `update`, `configure`, `schedule` | MEDIUM | Reversible modification |
| `delete`, `grant`, `transfer-funds` | HIGH | Impactful action |
| `drop`, `truncate`, `exploit` | CRITICAL | Irreversible |

## Properties

| Field | Meaning | Governance impact |
|-------|---------|-------------------|
| `idempotent: true` | Re-execution safe | Automatic retry possible |
| `idempotent: false` | Re-execution dangerous | Watch for duplicates |
| `reversible: true` | Can be undone | Less risk |
| `reversible: false` | Irreversible | ESCALATE recommended |

## Naming Convention

```
skills/<sector>/<descriptive-name>.skill.md

Examples:
  skills/core/file-read.skill.md
  skills/core/data-search.skill.md
  skills/healthcare/patient-lookup.skill.md
  skills/financial-services/kyc-verify.skill.md
  skills/cybersecurity/threat-hunt.skill.md
```

## Validation Checklist

- [ ] `name` is in kebab-case
- [ ] Each verb in `verbs` exists in the taxonomy
- [ ] `risk` is coherent with the risk level of the verbs
- [ ] `target` is defined (what the skill operates on)
- [ ] All 5 required body headers are present
- [ ] `side_effects` documented if `idempotent: false`
- [ ] `requires_context` documented (what inputs are mandatory)
- [ ] `schema_version: 1` present

## Scan command

```bash
sg guard scan skills/                    # Scan all skills
sg guard scan skills/healthcare/         # Scan a sector
```
