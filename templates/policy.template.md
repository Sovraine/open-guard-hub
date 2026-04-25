---
name: CHANGE-ME
version: "1.0.0"
domain: core                              # or sectors/<sector>
description: "One-line description"
schema_version: 1
match:
  actions: ["VERB"]                       # Must be valid taxonomy verbs
verdict: DENY                             # ALLOW, DENY, WARN, ESCALATE_DEBATE, ESCALATE_HUMAN
severity: HIGH                            # READ-ONLY, LOW, MEDIUM, HIGH, CRITICAL
priority: 85                              # See ranges below
author: community
license: CC-BY-SA-4.0
tags: [security]
signature: null                           # Must be null (community)
certified: false                          # Must be false (community)
---

<!-- Priority ranges (based on real hub data):
  DENY CRITICAL:          200-400
  DENY HIGH:              80-300
  ESCALATE_HUMAN CRITICAL: 95-120
  ESCALATE_HUMAN HIGH:    80-90
  ESCALATE_DEBATE CRITICAL: 85-90
  ESCALATE_DEBATE HIGH:   80
  WARN HIGH:              50-200

  GUARD-076: ALLOW + HIGH/CRITICAL = scanner error
  Fast-path: READ-ONLY verbs in DENY/ESCALATE are silently skipped
-->

## What it does

Describe what this policy enforces.

## Why it exists

Explain the risk or compliance requirement.

## What gets blocked

- Specific examples of actions that will be blocked/escalated.

## What is still allowed

- Specific examples of actions that remain permitted.

## How to override

Describe the override mechanism (e.g., break-glass, human approval).
