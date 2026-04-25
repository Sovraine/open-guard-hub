---
name: no-override-drug-interaction
version: "1.0.0"
domain: sectors/healthcare
description: Require pharmacist or physician approval to override drug interaction alerts
schema_version: 1
match:
  actions: ["override-drug-interaction", "override-interaction-alert"]
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 110
author: sovraine
license: CC-BY-SA-4.0
tags: [pharmacy, safety, clinical]
signature: null
certified: false
---

## What it does

Escalates all drug interaction override requests to a qualified human (pharmacist or physician) for clinical review and approval.

## Why it exists

Drug interaction alerts exist to prevent adverse drug events that can cause patient harm, including organ damage, toxicity, or death. Automated overrides of these alerts bypass a critical safety net. Clinical judgment by a licensed professional is required to evaluate whether the benefit of co-prescribing outweighs the interaction risk, and to implement monitoring or dosage adjustments as needed.

## What gets blocked

- `override-drug-interaction` — overriding a flagged drug-drug interaction
- `override-interaction-alert` — suppressing an interaction alert in the prescribing system
- The action is paused and escalated to a pharmacist or physician

## What is still allowed

- Viewing drug interaction alerts and severity levels
- Adding clinical notes to justify a known interaction
- Adjusting dosages to mitigate interaction risk (separate action)
- Prescribing non-interacting alternatives

## How to override

A licensed pharmacist or physician must approve the override with documented clinical justification. The approval must include: the specific interaction being overridden, the clinical rationale, any compensating measures (dose adjustment, monitoring schedule), and the approver's credentials. The override is logged for pharmacy review.
