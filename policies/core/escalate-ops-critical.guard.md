---
name: escalate-ops-critical
version: "1.0.0"
domain: core/common
description: Escalate critical operations on incident management and monitoring MCP servers
schema_version: 1
match:
  servers: ["pagerduty", "sentry", "dynatrace", "apify"]
  actions: ["create", "execute", "delete"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 85
author: sovraine
license: CC-BY-SA-4.0
tags: [ops, incident, monitoring, alerting, safety]
signature: null
certified: false
---

## What it does

Requires human approval before creating incidents, executing workflows, or deleting resources on incident management and monitoring platforms.

## Why it exists

These actions have outsized real-world impact. Creating an incident pages on-call engineers and may wake people at night. Executing a workflow can trigger automated responses across infrastructure. Deleting services, schedules, or escalation policies silently breaks the incident response chain — the worst time to discover a gap is during an outage.

## What gets blocked

- `create`, `execute`, `delete` actions on PagerDuty, Sentry, Dynatrace, and Apify servers with risk >= HIGH
- Incident creation that pages on-call engineers
- Deletion of services, teams, schedules, and escalation policies

## Servers covered

- **PagerDuty** — `create_incident`, `run_incident_workflow`, `delete_service`, `delete_team`, `delete_schedule`, `delete_escalation_policy`, `delete_event_orchestration`
- **Sentry** — `delete_issue`
- **Dynatrace** — `run_workflow`

## What is still allowed

- All `read` and `list` actions (viewing incidents, services, teams, alerts)
- `update` actions (acknowledging, resolving, snoozing incidents)
- Adding notes and comments
- Searching and filtering

## How to override

A human operator must confirm the action with the target resource identifier and acknowledgment of the impact. The confirmation is recorded in the audit log.
