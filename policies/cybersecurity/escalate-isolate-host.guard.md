---
name: escalate-isolate-host
version: "1.0.0"
domain: sectors/cybersecurity
description: Escalate host isolation for multi-agent debate on blast radius
schema_version: 1
match:
  actions: ["isolate-host", "contain-breach"]
verdict: ESCALATE_DEBATE
severity: CRITICAL
priority: 90
author: sovraine
license: CC-BY-SA-4.0
tags: [incident-response, containment, availability]
signature: null
certified: false
---

## What it does

Triggers a multi-agent debate before isolating a host or containing a breach, evaluating the trade-off between security containment and service availability.

## Why it exists

Host isolation is a double-edged sword in incident response. While it prevents lateral movement and limits breach scope, it also takes the host offline — potentially disrupting critical services, breaking dependencies, and causing cascading failures. A debate between agents (security, ops, business) evaluates the blast radius: Is this host serving production traffic? What depends on it? Is the threat confirmed or suspected? Are there less disruptive containment options?

## What gets blocked

- `isolate-host` — network isolation of a specific host
- `contain-breach` — broader containment actions affecting host availability
- The action is paused until the debate reaches a verdict

## What is still allowed

- Monitoring the host (read-only observation)
- Collecting forensic data from the host
- Blocking specific network connections (micro-segmentation)
- Alerting the incident response team

## How to override

The debate must reach a verdict. If security risk outweighs availability impact, the debate approves isolation. In active breach scenarios where debate latency is unacceptable, the incident commander can invoke emergency override with mandatory post-incident review within 24 hours.
