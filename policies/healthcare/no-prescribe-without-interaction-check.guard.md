---
name: no-prescribe-without-interaction-check
version: "1.0.0"
domain: sectors/healthcare
description: "Require human approval before prescribing medication without a prior drug interaction check"
schema_version: 1
match:
  actions: ["prescribe-medication"]
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 110
author: community
license: CC-BY-SA-4.0
tags: [clinical, patient-safety, drug-interaction]
signature: null
certified: false
---

## What it does

Escalates to a human reviewer whenever an AI agent attempts to prescribe medication (`prescribe-medication`) without evidence that a drug interaction check (`check-drug-interaction`) was performed in the same session.

## Why it exists

Drug-drug interactions are one of the leading causes of preventable adverse drug events (ADEs). The WHO estimates that medication errors cause at least one death every day and injure approximately 1.3 million people annually in the US alone. Automated prescription without interaction verification bypasses a fundamental patient safety gate that every pharmacist and physician performs manually.

Relevant regulations:
- **Joint Commission NPSG.03.06.01** — Maintain and communicate accurate medication information
- **EU Directive 2010/84/EU** — Pharmacovigilance requirements
- **HIPAA Security Rule** — Safeguards for electronic health information integrity

## What gets blocked

- An agent calling `prescribe-medication` when no `check-drug-interaction` call exists in the current session's audit trail
- Bulk prescription workflows that skip interaction verification
- Automated refill systems that bypass safety checks for new combinations

## What is still allowed

- Prescriptions preceded by a `check-drug-interaction` call in the same session (the human approval may still be waived by a break-glass policy)
- Reading prescription history (`access-patient-record`)
- Running drug interaction checks independently (`check-drug-interaction`)
- Emergency break-glass access (governed by `escalate-break-glass` policy, which logs separately)

## How to override

1. **Standard path**: Perform `check-drug-interaction` before `prescribe-medication` in the same session — the escalation is then handled by the interaction result
2. **Emergency path**: Use break-glass access (`break-glass-access` verb) with mandatory justification — logged and audited
3. **Policy exception**: A hospital compliance officer can approve a temporary exception via `ESCALATE_HUMAN` approval with documented clinical rationale
