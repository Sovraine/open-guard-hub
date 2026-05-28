---
name: guard-agent-create
description: Create an agent .agent.md with the full format (YAML frontmatter + Markdown body). Defines the identity, allowed skills, permitted/denied verbs, max risk, applicable policies and referenced soul. Knows the 18 sectors and taxonomy conventions.
---

# Guard Agent Create

## Schema AgentDef

### YAML Frontmatter

```yaml
---
name: descriptive-kebab-case-name
version: "1.0.0"
domain: sectors/healthcare          # sectors/<sector> or core/<domain>
description: "One-line description"
schema_version: 1

# Identity
soul: clinical-empathetic           # reference to a .soul.md by name (optional)
model: null                         # recommended model (advisory, not enforced)

# Capabilities
skills:                             # list of .skill.md by name
  - patient-lookup
  - drug-interaction-check
  - lab-results-summary

allowed_verbs:                      # explicit whitelist of taxonomy verbs
  - read
  - search
  - list

denied_verbs:                       # explicit blacklist (overrides allowed)
  - delete
  - drop
  - truncate

# Governance
max_risk: MEDIUM                    # READ-ONLY | LOW | MEDIUM | HIGH | CRITICAL
requires_human_above: HIGH          # auto-escalate if risk >= this level
sandbox: true                       # must run in sandbox
policies:                           # policy references to apply
  - no-override-drug-interaction
  - escalate-break-glass

# Metadata
sector: healthcare
author: "community"
license: "CC-BY-SA-4.0"
tags: [healthcare, clinical, decision-support]
signature: null
certified: false
---
```

### Body Markdown — REQUIRED Headers

```markdown
## Purpose
<1-2 sentences. What this agent does, use cases.>

## Guardrails
<What governance constraints are applied and why.>

## Allowed actions
<List of allowed actions with context.>

## Denied actions
<List of denied actions. Why they are blocked.>

## Escalation
<When and how actions escalate to a human.>
```

## Risk Levels

| Level | Description | Default behavior |
|-------|-------------|------------------|
| `READ-ONLY` | Read only | ALLOW immediate (FastPath) |
| `LOW` | Low risk | ALLOW if no policy |
| `MEDIUM` | Moderate risk | ALLOW if no policy |
| `HIGH` | High risk | DENY if no policy (fail-closed) |
| `CRITICAL` | Irreversible | DENY if no policy (fail-closed) |

## Cross-References

The agent references other hub artifacts by **name**:

| Field | Reference | File |
|-------|-----------|------|
| `soul` | soul name | `souls/{sector}/{name}.soul.md` |
| `skills[]` | skill name | `skills/{sector}/{name}.skill.md` |
| `policies[]` | policy name | `policies/{sector}/{name}.guard.md` |
| `allowed_verbs[]` | taxonomy verb | `core/**/_verbs.yaml` or `sectors/**/_verbs.yaml` |
| `denied_verbs[]` | taxonomy verb | same |

## Naming Convention

```
agents/<sector>/<descriptive-name>.agent.md

Examples:
  agents/core/safe-assistant.agent.md
  agents/healthcare/clinical-assistant.agent.md
  agents/financial-services/compliance-officer.agent.md
  agents/cybersecurity/soc-analyst.agent.md
```

## Validation Checklist

- [ ] `name` is in kebab-case
- [ ] Each verb in `allowed_verbs` and `denied_verbs` exists in the taxonomy
- [ ] No overlap between `allowed_verbs` and `denied_verbs`
- [ ] `max_risk` <= `requires_human_above` (logical)
- [ ] `soul` references an existing .soul.md
- [ ] Each `skills[]` references an existing .skill.md
- [ ] Each `policies[]` references an existing .guard.md
- [ ] All 5 required body headers are present
- [ ] `schema_version: 1` present

## Scan command

```bash
sovctl guard scan .                          # Always scan from repo root (subdirectory scan produces false GUARD-070)
```
