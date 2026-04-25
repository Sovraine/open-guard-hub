---
name: guard-policy-create
description: Create a .guard.md policy with the full format (YAML frontmatter + Markdown body). Use to write new policies, validate format, generate the 5 onboarding policies. Knows the 6 verdicts, the priority system, and the glob match syntax.
---

# Guard Policy Create

## Complete GuardFile Schema

### YAML Frontmatter

```yaml
---
name: descriptive-kebab-case-name
version: "1.0.0"
domain: sector/sub-sector          # e.g. financial-services/banking
description: "One-line description"
schema_version: 1

match:
  actions:
    - "transfer-funds"             # Canonical verb from taxonomy
    - "transfer-funds-*"           # Glob wildcard
  targets:
    - "account-*"                  # Glob on target
  contexts:
    agent: "ops-*"                 # Glob on agent name
    environment: "production"
    # Any arbitrary key=value

verdict: DENY                      # ALLOW | DENY | WARN | FILTER | ESCALATE_DEBATE | ESCALATE_HUMAN
severity: CRITICAL                 # LOW | MEDIUM | HIGH | CRITICAL
priority: 100                      # int, higher = evaluated first, DENY wins on tie

author: "community"
license: "CC-BY-SA-4.0"
tags: ["finance", "psd2", "4-eyes"]
requires: []                       # Prerequisite policies
conflicts_with: []                 # Incompatible policies

# Signature (null if unsigned, filled by guard sign)
signature: null                    # "sovraine:ed25519:<base64>"
certified: false
certified_for: []                  # ["SOC2-CC6.1", "DORA-Art.9"]
certified_date: null
certified_expires: null
---
```

### Markdown Body — REQUIRED Headers

```markdown
## What it does
<1-2 sentences. What exactly.>

## Why it exists
<Regulatory context, past incident, best practice.>

## What gets blocked
<Concrete list of blocked actions with examples.>

## What is still allowed
<Cases that are NOT blocked by this policy.>

## How to override
<How to legitimately bypass: policy exception, approval, context.>
```

### OPTIONAL Headers

```markdown
## Compliance
<Regulatory mapping: DORA Art.X, HIPAA §Y, etc.>

## Related policies
<Links to complementary policies.>

## Changelog
<Modification history.>
```

## 6 Verdicts

| Verdict | Behavior | When to use |
|---------|----------|-------------|
| `ALLOW` | Action executed | Explicit authorization |
| `DENY` | Action blocked | Firm prohibition |
| `WARN` | Action executed + warning logged | Monitoring, no blocking |
| `FILTER` | Action executed with modified params | Mask sensitive data, token saving |
| `ESCALATE_DEBATE` | Send to multi-agent debate | Ambiguous case, reasoning needed |
| `ESCALATE_HUMAN` | Wait for human approval | Irreversible actions, 4-eyes |

## Verdict Decision Tree

```
Is the action ALWAYS forbidden, without exception?
  → YES: DENY (e.g. reverse shell, SQL injection, plaintext secrets)
  → NO:
    Does the action require explicit human approval?
      → YES: ESCALATE_HUMAN (e.g. delete tenant data, 4-eyes transfer, KYC override)
      → NO:
        Is the case ambiguous and requires multi-agent reasoning?
          → YES: ESCALATE_DEBATE (e.g. kill-switch, deploy model to prod)
          → NO:
            Should the action be traced but not blocked?
              → YES: WARN (e.g. decrypt sensitive, break-glass access)
              → NO: ALLOW
```

**GUARD-076**: `ALLOW` + severity `HIGH` or `CRITICAL` = scanner error. An ALLOW cannot have a high severity.

## Priority

- `priority`: integer, **higher = evaluated first**
- On priority tie: **DENY wins** (fail-closed)
- **Actual ranges** (based on current hub, not onboarding defaults):

| Verdict | Severity | Typical Range | Examples |
|---------|----------|---------------|----------|
| DENY | CRITICAL | 200-400 | cybersecurity agent-diversion (350-400), supply-chain (300-350), core (100-200) |
| DENY | HIGH | 80-300 | secrets/TLS (250), injection (85-95), hidden-file (300) |
| ESCALATE_HUMAN | CRITICAL | 95-120 | 4-eyes (100), compliance override (110-120) |
| ESCALATE_HUMAN | HIGH | 80-90 | financial (90), bulk ops (80), browser exec (80) |
| ESCALATE_DEBATE | CRITICAL | 85-90 | kill-switch (90), isolate-host (90) |
| ESCALATE_DEBATE | HIGH | 80 | deploy-model (80) |
| WARN | HIGH | 50-200 | decrypt (50), context-flood (200), break-glass (90) |
| ALLOW | LOW | 5-10 | read-only-by-default (5) |

**General rule**: cybersecurity DENY policies are highest (300-400), followed by core infrastructure DENY (100-250), then ESCALATE (80-120), then WARN (50-200).

- Onboarding policies (`sg guard init`): 5-20 (low, easily overridden)

## Match Syntax — Glob v1

| Pattern | Matches | Does NOT match |
|---------|---------|----------------|
| `transfer-funds` | exactly `transfer-funds` | `transfer-funds-international` |
| `transfer-*` | `transfer-funds`, `transfer-crypto` | `approve-transfer` |
| `*-override` | `kyc-override`, `sanction-override` | `override-alarm` |
| `*` | everything | — |
| `_unknown` | any action not in taxonomy | known actions |
| `_any` | any action (known or not) | — |

## Naming Convention

```
<sector>/<descriptive-name>.guard.md

Examples:
  core/no-destructive-without-confirmation.guard.md
  financial-services/no-international-transfer-without-4-eyes.guard.md
  healthcare/break-glass-requires-justification.guard.md
```

## Scanner

- `sg guard scan` only takes **directories**, never individual files
- Always scan `.` (the repo root) as a whole: `sg guard scan .`
- Scanning a subdirectory (`policies/core/`) will produce false GUARD-070 because verbs from other sectors are not in scope

## Validation Checklist

- [ ] Each verb in `match.actions` exists in the taxonomy (or is a glob)
- [ ] `severity` consistent with the risk level of matched verbs
- [ ] `priority` in the correct range for the policy type
- [ ] All 5 required body headers are present
- [ ] `domain` matches the file path
- [ ] No conflict with `conflicts_with`
- [ ] `requires` satisfied
- [ ] `schema_version: 1` present
