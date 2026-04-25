<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: threat-hunt
version: "1.0.0"
domain: sectors/cybersecurity
description: "Proactive threat hunting via SIEM queries and network behavior analysis"
schema_version: 1
verbs: [threat-hunt, query-siem, scan-vulnerability]
target: network
risk: MEDIUM
requires_context: [hunt_query, justification]
preconditions: ["caller is SOC analyst", "hunt_query is validated"]
postconditions: ["suspicious artifacts returned", "findings logged for incident review"]
side_effects: ["hunt_log created", "alerts generated if CRITICAL findings"]
idempotent: true
reversible: false
sector: cybersecurity
author: sovraine
license: CC-BY-SA-4.0
tags: [incident-response, threat-hunting, soc]
certified: false
---

## What it does

Performs proactive threat hunting by querying SIEM logs, network flows, and endpoint telemetry to detect anomalous behavior, command injection, lateral movement, and data exfiltration patterns. Supports both signature-based and behavioral-based hunt rules.

## Inputs

- **hunt_query** (required): SIEM query (KQL, SPL, or KQL format)
- **justification** (required): Business reason for hunt (e.g., "investigating reported breach")
- **time_range** (optional): Lookback window (default: last 30 days)
- **severity_threshold** (optional): Minimum alert severity to return (default: MEDIUM)

## Governance constraints

- **MEDIUM risk**: Hunt queries are read-only; no systems are modified
- **Query validation**: Queries are parsed and validated before execution to prevent false positives
- **Authorized analysts only**: Caller must have SOC analyst role
- **Evidence preservation**: All findings are logged with timestamp and query for forensics
- **No exploitation**: Threat hunt queries cannot include exploit payloads or code execution
- **Audit logging**: Every hunt is logged with analyst identity, query, and results

## Side effects

- **Hunt log created**: Query, timestamp, analyst, and results recorded
- **Evidence preservation**: Findings are immutable and stored with chain-of-custody
- **Automated alerting**: CRITICAL findings generate incident alerts
- **Incident correlation**: Findings linked to existing incident investigations
- **No data modification**: Network and logs remain unchanged

## Error handling

- Invalid hunt_query → returns 400 error with parsing details
- Unauthorized analyst → returns 403 error, logged for audit
- No results found → returns 200 OK with empty results (not an error)
- SIEM unavailable → returns 504 error, recommends manual investigation
- Query timeout → returns 504 error after max duration
- Suspicious pattern → returns CRITICAL alert, escalates to incident commander
