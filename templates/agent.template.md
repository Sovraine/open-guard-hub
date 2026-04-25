---
name: CHANGE-ME
version: "1.0.0"
domain: core                              # or sectors/<sector>
description: "One-line description"
schema_version: 1
soul: CHANGE-ME                           # Must match a soul in souls/
model: null
skills: []
allowed_verbs: [read, list, search]       # Must be valid taxonomy verbs
denied_verbs: [delete, execute]           # Must be valid taxonomy verbs
max_risk: MEDIUM                          # Maximum risk level this agent can handle
requires_human_above: MEDIUM              # Escalate to human above this risk
sandbox: false
policies:
  - CHANGE-ME                             # Must match policies in policies/
sector: core
author: community
license: CC-BY-SA-4.0
tags: []
certified: false                          # Must be false (community)
---

<!-- Cross-ref rules:
  - soul: must match souls/<sector>/<name>*.soul.md
  - skills: must match skills/<sector>/<name>.skill.md
  - policies: must match policies/<sector>/<name>.guard.md
  - All referenced artifacts must exist on main (not in other open PRs)
  - A verb cannot be in both allowed_verbs and denied_verbs (GUARD-026)
-->

## Purpose

What this agent does and in what context.

## Guardrails

What constraints govern this agent's behavior.

## Allowed actions

- List of actions this agent can perform.

## Denied actions

- List of actions this agent is explicitly forbidden from performing.

## Escalation

When and how this agent escalates to a human or debate.
