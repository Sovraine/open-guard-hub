---
name: escalate-kill-switch
version: "1.0.0"
domain: sectors/saas-tech
description: Escalate kill switch activation for multi-agent debate
schema_version: 1
match:
  actions: ["kill-switch"]
verdict: ESCALATE_DEBATE
severity: CRITICAL
priority: 90
author: sovraine
license: CC-BY-SA-4.0
tags: [saas, feature-flags, emergency]
signature: null
certified: false
---

## What it does

Triggers a multi-agent debate before a kill switch can be activated, disabling a feature for all users.

## Why it exists

A kill switch disables features for all users globally. While it is a critical safety mechanism for emergencies (security vulnerabilities, data corruption, cascading failures), activating it also causes immediate user impact — broken workflows, lost work, and potential SLA violations. A debate between agents evaluates the severity of the incident, the blast radius of the kill switch, and whether less disruptive alternatives exist (feature flag rollback, canary disable, traffic shifting).

## What gets blocked

- `kill-switch` activation for any feature
- The action is paused until the debate reaches a verdict

## What is still allowed

- Toggling feature flags for individual users or cohorts
- Gradual rollback of feature flags (percentage-based)
- Viewing feature flag status and usage metrics

## How to override

The debate must reach a verdict. If the debate approves, the kill switch is activated immediately. If denied, the operator can override with explicit justification. In extreme emergencies where debate latency is unacceptable, the operator can invoke a break-glass override that bypasses the debate but triggers a post-incident review.
