---
name: microsoft-skills-default
version: "1.0.0"
domain: sectors/saas-tech
description: "Default conservative agent for microsoft-skills"
schema_version: 1
soul: microsoft-skills
model: null
skills: []
allowed_verbs: [read, list, search, get, describe, show]
denied_verbs: [delete, drop, destroy, purge, wipe, format, execute]
max_risk: MEDIUM
requires_human_above: HIGH
sandbox: false
policies: [microsoft-skills-deny-destructive, microsoft-skills-warn-high-risk]
sector: saas-tech
author: community
license: CC-BY-SA-4.0
certified: false
---

## Purpose

Default agent profile for microsoft-skills. Allows read operations freely,
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
