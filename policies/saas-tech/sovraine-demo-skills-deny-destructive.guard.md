---
name: sovraine-demo-skills-deny-destructive
version: "1.0.0"
domain: sectors/saas-tech
description: "Deny destructive actions on sovraine-demo-skills without human approval"
schema_version: 1
match:
  actions:
    - "delete:*"
    - "drop:*"
    - "purge:*"
    - "destroy:*"
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 100
author: community
license: CC-BY-SA-4.0
certified: false
signature: null
---

## What it does

Blocks destructive operations (delete, drop, purge, destroy) targeting
sovraine-demo-skills resources and routes them to a human reviewer.

## Why it exists

Destructive operations are irreversible. Requiring human approval prevents
accidental data loss when agents interact with sovraine-demo-skills.

## What gets blocked

Any action matching delete, drop, purge, or destroy verbs targeting
sovraine-demo-skills resources.

## What is still allowed

Read, create, update, list, and search operations proceed normally.

## How to override

Approved by a human reviewer via the escalation flow.
