---
name: no-recall-wire-without-4-eyes
version: "1.0.0"
domain: sectors/financial-services
description: Require multi-party approval for wire transfer recalls
schema_version: 1
match:
  actions: ["recall-wire"]
  contexts:
    approval_count: "<2"
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 100
author: sovraine
license: CC-BY-SA-4.0
tags: [banking, wire, compliance, PSD2]
signature: null
certified: false
---

## What it does

Escalates wire transfer recall requests to a human approver when fewer than two independent approvals have been recorded (four-eyes principle).

## Why it exists

PSD2 Article 88 and internal banking controls require multi-party approval for wire recalls. A single compromised or negligent actor should not be able to recall funds unilaterally. The four-eyes principle ensures that at least two authorized individuals review and approve the recall before execution.

## What gets blocked

- `recall-wire` when `approval_count` is less than 2
- The action is paused and escalated to a human approver

## What is still allowed

- `recall-wire` with 2 or more recorded approvals proceeds normally
- Initiating a wire recall request (creating the request, not executing it)
- Viewing wire transfer details and status

## How to override

A second authorized approver must provide explicit approval. Both approvals are recorded in the audit log with approver identities, timestamps, and the wire reference number. Emergency overrides require compliance officer sign-off.
