---
name: no-kyc-override-without-compliance
version: "1.0.0"
domain: sectors/financial-services
description: Require compliance officer approval for KYC overrides
schema_version: 1
match:
  actions: ["kyc-override"]
verdict: ESCALATE_HUMAN
severity: CRITICAL
priority: 110
author: sovraine
license: CC-BY-SA-4.0
tags: [banking, kyc, compliance, AML]
signature: null
certified: false
---

## What it does

Escalates all KYC (Know Your Customer) override requests to a human compliance officer for review and approval.

## Why it exists

KYC overrides bypass anti-money laundering (AML) safeguards designed to verify customer identity and assess risk. Automated KYC overrides could allow sanctioned entities, shell companies, or fraudulent actors to onboard or transact without proper due diligence. Regulatory frameworks (AML4/5 Directives, BSA/USA PATRIOT Act) impose severe penalties — including criminal liability — for inadequate KYC controls.

## What gets blocked

- All `kyc-override` actions regardless of context or justification
- The action is paused and escalated to a compliance officer

## What is still allowed

- Standard KYC verification workflows (no override)
- Requesting additional documentation from customers
- Viewing KYC status and verification history

## How to override

A designated compliance officer must approve the override with documented justification. The approval must reference the specific regulatory exception being applied, the risk assessment performed, and the compensating controls in place. All overrides are reported to the AML officer in the next compliance review.
