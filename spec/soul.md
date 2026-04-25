<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Soul Specification (`.soul.md`)

A Soul defines the persona and system prompt template for an AI agent. The body IS the executable system prompt — not just documentation.

## Format

```
---
<YAML frontmatter>
---

<Markdown body (system prompt template)>
```

## Frontmatter Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique name in kebab-case |
| `version` | string | Semantic version |
| `domain` | string | Sector path (e.g. `sectors/cybersecurity`) |
| `description` | string | One-line description |
| `schema_version` | integer | Must be `1` |
| `tone` | string | `professional`, `friendly`, `formal`, `technical`, `empathetic` |
| `language` | string | ISO 639-1 code (e.g. `en`) |
| `safety_rules` | list[string] | Hard rules integrated into the persona (must not be empty) |
| `forbidden_topics` | list[string] | Topics the persona must refuse (must not be empty) |
| `max_risk` | enum | The persona refuses above this risk level |
| `escalation_trigger` | enum | Auto-escalate at this risk level |
| `author` | string | `"community"` for community contributions |
| `license` | string | `"CC-BY-SA-4.0"` for hub content |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sector` | string | — | Sector name |
| `tags` | list[string] | `[]` | Classification tags |
| `signature` | string\|null | `null` | Ed25519 signature |
| `certified` | boolean | `false` | Whether audited |

## Tone Values

| Tone | Description | Use case |
|------|-------------|----------|
| `professional` | Neutral, factual, formal | Default, general use |
| `friendly` | Approachable, warm | Customer support, education |
| `formal` | Very formal, regulatory | Legal, compliance, public-sector |
| `technical` | Precise, technical jargon | DevOps, cybersecurity, engineering |
| `empathetic` | Attentive, patient, caring | Healthcare, HR, support |

## Dangerous Patterns

The scanner rejects souls containing these patterns:

| Pattern | Risk |
|---------|------|
| "ignore policies" | Governance bypass |
| "you have full access" | Privilege escalation |
| "act as admin/root" | Privilege escalation |
| "do whatever is needed" | Uncontrolled delegation |
| "DAN", "developer mode" | Jailbreak |
| "use any tool" | No scope limits |

## Required Body Sections

```markdown
## Identity
## Boundaries
## Tone guidelines
## Safety instructions
```

### Optional Body Sections

```markdown
## Expertise
## Escalation behavior
## Interaction patterns
```

## Validation Rules

| Check ID | Severity | Description |
|----------|----------|-------------|
| GUARD-014 | MEDIUM | Missing required body section |
| — | ERROR | `safety_rules` is empty |
| — | ERROR | `forbidden_topics` is empty |
| — | ERROR | Body contains jailbreak pattern |
| — | WARNING | Body contradicts `forbidden_topics` |

## Example

```yaml
---
name: soc-analyst
version: "1.0.0"
domain: sectors/cybersecurity
description: "SOC analyst persona for security operations"
schema_version: 1
tone: technical
language: en
safety_rules:
  - "Never execute exploits without explicit authorization"
  - "Always verify target scope before scanning"
  - "Escalate any finding above CVSS 9.0 immediately"
forbidden_topics:
  - "Creating malware"
  - "Social engineering against real targets"
  - "Bypassing security controls without authorization"
max_risk: HIGH
escalation_trigger: CRITICAL
sector: cybersecurity
author: community
license: CC-BY-SA-4.0
tags: [cybersecurity, soc]
signature: null
certified: false
---
```

```markdown
## Identity
You are a SOC analyst responsible for monitoring, detecting, and responding
to security incidents in an enterprise environment.

## Boundaries
You must not execute offensive operations, create malware, or target
systems outside the defined scope.

## Tone guidelines
Technical and precise. Use standard security terminology. Be concise
in alerts, detailed in reports.

## Safety instructions
Always verify authorization before scanning. Escalate critical findings
immediately. Never attempt exploitation without explicit written approval.
```
