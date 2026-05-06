---
name: sovraine-demo-skills-warn-high-risk
version: "1.0.0"
domain: sectors/saas-tech
description: "Warn on HIGH risk actions targeting sovraine-demo-skills"
schema_version: 1
match:
  actions:
    - "*"
  min_risk: HIGH
verdict: WARN
severity: HIGH
priority: 50
author: community
license: CC-BY-SA-4.0
certified: false
signature: null
---

## What it does

Emits a warning for any action classified as HIGH risk or above when
targeting sovraine-demo-skills resources.

## Why it exists

High-risk actions should be logged and monitored even when allowed,
creating an audit trail for compliance review.

## What gets blocked

Nothing is blocked. Actions proceed with a warning logged.

## What is still allowed

All actions proceed normally. The warning creates an audit trail.

## How to override

No override needed — this is a monitoring policy.
