---
name: no-warrant-without-judge
version: "1.0.0"
domain: sectors/public-sector
description: Require judicial authorization for warrants and surveillance
schema_version: 1
match:
  actions: ["issue-warrant", "authorize-surveillance"]
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 120
author: sovraine
license: CC-BY-SA-4.0
tags: [law-enforcement, legal, constitutional]
signature: null
certified: false
---

## What it does

Escalates warrant issuance and surveillance authorization requests to a human with judicial authority for review and approval.

## Why it exists

Warrants and surveillance orders require judicial authorization under constitutional law (Fourth Amendment in the US, Article 8 ECHR in Europe, and equivalent protections in most democratic legal systems). No automated system should issue warrants or authorize surveillance without a judge or magistrate reviewing the probable cause, scope, and proportionality. Unauthorized surveillance is a fundamental rights violation and carries severe legal consequences.

## What gets blocked

- `issue-warrant` — generating or issuing any form of warrant
- `authorize-surveillance` — enabling surveillance of individuals or communications
- The action is paused and escalated to a human with judicial authority

## What is still allowed

- Preparing warrant applications for judicial review
- Analyzing publicly available information (OSINT)
- Processing warrants that have already been judicially authorized
- Generating reports for judicial review

## How to override

A judge or magistrate must review and sign the warrant or surveillance order. The signed authorization must be recorded in the system with the judicial officer's identity, the scope of the authorization, and the expiration date. No emergency override exists for this policy — exigent circumstances procedures must still go through a judge (telephonic warrants are acceptable).
