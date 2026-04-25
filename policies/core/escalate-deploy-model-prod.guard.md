---
name: escalate-deploy-model-prod
version: "1.0.0"
domain: core/ai-ml
description: Escalate ML model deployments to production for debate
schema_version: 1
match:
  actions: ["deploy-model", "promote-to-production"]
  contexts:
    environment: "production"
verdict: ESCALATE_DEBATE
severity: HIGH
priority: 80
author: sovraine
license: CC-BY-SA-4.0
tags: [ai-ml, production, safety]
signature: null
certified: false
---

## What it does

Triggers a multi-agent debate before any ML model deployment or promotion to the production environment.

## Why it exists

Deploying ML models to production can cause downstream failures across dependent services — incorrect predictions, biased outputs, latency regressions, or data pipeline breakdowns. A debate between specialized agents (ops, security, business) evaluates the risk, validates that testing was completed, and assesses rollback readiness before the deployment proceeds.

## What gets blocked

- `deploy-model` where `environment` is `production`
- `promote-to-production` where `environment` is `production`
- The action is paused until the debate reaches a verdict

## What is still allowed

- Deploying models to `staging`, `development`, or `test` environments
- Retraining or evaluating models without deploying
- Rolling back a production model to a previous version (separate action)

## How to override

The debate must reach consensus. If the debate verdict is APPROVE, the deployment proceeds automatically. If DENY, the action is blocked. A human can override a DENY verdict with explicit justification recorded in the audit log.
