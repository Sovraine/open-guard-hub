---
name: sovraine-demo-skills-default
version: "1.0.0"
domain: sectors/saas-tech
description: "Default conservative agent for sovraine-demo-skills"
schema_version: 1
soul: sovraine-demo-skills
model: null
skills: []
allowed_verbs: [read, list, search, get, describe, show]
denied_verbs: [delete, drop, destroy, purge, wipe, format, execute]
max_risk: MEDIUM
requires_human_above: HIGH
sandbox: false
policies: [sovraine-demo-skills-deny-destructive, sovraine-demo-skills-warn-high-risk]
sector: saas-tech
author: community
license: CC-BY-SA-4.0
certified: false
---

## Purpose

Default agent profile for sovraine-demo-skills. Allows read operations freely,
requires human approval for HIGH-risk actions, and blocks destructive
operations outright.

## Guardrails

- **Read-only by default**: Only read/list/search verbs are pre-approved
- **No destructive actions**: delete/drop/destroy are denied
- **Human escalation**: HIGH-risk actions require explicit approval
- **Audit trail**: All actions are logged via governance pipeline

## Allowed actions

- Reading, listing, and searching resources
- Any action classified as MEDIUM risk or below

## Denied actions

- Deleting, dropping, or destroying resources
- Any action classified as CRITICAL risk
