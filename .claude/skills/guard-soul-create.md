---
name: guard-soul-create
description: Create a soul/persona .soul.md with the full format (YAML frontmatter + Markdown body). The body IS the system prompt template with integrated safety rules. Defines the tone, safety rules, forbidden topics and escalation thresholds.
---

# Guard Soul Create

## Schema SoulDef

### YAML Frontmatter

```yaml
---
name: descriptive-kebab-case-name
version: "1.0.0"
domain: sectors/cybersecurity       # sectors/<sector> or core/<domain>
description: "One-line description"
schema_version: 1

# Persona
tone: professional                  # professional | friendly | formal | technical | empathetic
language: en                        # ISO 639-1

# Safety boundaries
safety_rules:                       # hard rules integrated into the persona
  - "Never execute exploits without explicit authorization"
  - "Always verify target scope before scanning"
  - "Escalate any finding above CVSS 9.0 immediately"
forbidden_topics:                   # topics the persona must refuse
  - "Creating malware"
  - "Social engineering against real targets"
  - "Bypassing security controls without authorization"

# Governance integration
max_risk: HIGH                      # the persona refuses above this risk
escalation_trigger: CRITICAL        # auto-escalate at this risk level

# Metadata
sector: cybersecurity
author: "community"
license: "CC-BY-SA-4.0"
tags: [cybersecurity, soc, persona]
signature: null
certified: false
---
```

### Body Markdown — REQUIRED Headers

The body of a soul is **the system prompt template**. It is executable (used as prompt), not just documentary.

```markdown
## Identity
<Who the agent is. How it presents itself. Its role.>

## Boundaries
<What it must refuse. Explicit limits.>

## Tone guidelines
<How it communicates. Style, register, language.>

## Safety instructions
<Safety rules in natural language. Integrated into the prompt.>
```

### OPTIONAL Headers

```markdown
## Expertise
<Domains of competence. Specific knowledge.>

## Escalation behavior
<How the agent reacts when an action exceeds its scope.>

## Interaction patterns
<Example dialogues. Expected responses.>
```

## Tone Values

| Tone | Description | Use case |
|------|-------------|----------|
| `professional` | Neutral, factual, formal | Default, general use |
| `friendly` | Approachable, warm | Customer support, education |
| `formal` | Very formal, regulatory | Legal, compliance, public-sector |
| `technical` | Precise, technical jargon | DevOps, cybersecurity, engineering |
| `empathetic` | Attentive, patient, caring | Healthcare, HR, support |

## Safety Rules — Patterns to detect

The scanner verifies that the soul does NOT contain these dangerous patterns:

| Pattern | Risk | Check ID |
|---------|------|----------|
| "ignore policies" | Governance bypass | `soul-governance-bypass` |
| "you have full access" | Privilege escalation | `soul-privilege-escalation` |
| "act as admin/root" | Privilege escalation | `soul-privilege-escalation` |
| "do whatever is needed" | Uncontrolled delegation | `soul-uncontrolled-delegation` |
| "DAN", "developer mode" | Jailbreak | `soul-jailbreak-pattern` |
| "use any tool" | No scope limits | `soul-no-scope-limits` |

## Governance Integration

| Field | Effect |
|-------|--------|
| `max_risk: HIGH` | The persona refuses actions above HIGH |
| `escalation_trigger: CRITICAL` | Auto-escalate to a human if risk = CRITICAL |
| `safety_rules` | Integrated into the system prompt |
| `forbidden_topics` | The scanner verifies the body does not contradict them |

## Naming Convention

```
souls/<sector>/<descriptive-name>.soul.md

Examples:
  souls/core/helpful-professional.soul.md
  souls/healthcare/clinical-empathetic.soul.md
  souls/cybersecurity/soc-analyst.soul.md
  souls/financial-services/compliance-strict.soul.md
```

## Validation Checklist

- [ ] `name` is in kebab-case
- [ ] `safety_rules` is not empty (a soul without safety rules = danger)
- [ ] `forbidden_topics` is not empty
- [ ] Body is not empty (a soul without a prompt = useless)
- [ ] All 4 required body headers are present
- [ ] Body does not contain jailbreak patterns
- [ ] Body does not contradict `forbidden_topics`
- [ ] `max_risk` and `escalation_trigger` are valid risk levels
- [ ] `schema_version: 1` present

## Scan command

```bash
sg guard scan .                          # Always scan from repo root (subdirectory scan produces false GUARD-070)
```
