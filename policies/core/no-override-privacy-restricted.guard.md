---
name: no-override-privacy-restricted
version: "1.0.0"
domain: core/data-privacy
description: Block forced cloud routing of RESTRICTED data
schema_version: 1
match:
  actions: ["override-privacy-route"]
  contexts:
    classification: "restricted"
verdict: DENY
severity: CRITICAL
priority: 200
author: sovraine
license: CC-BY-SA-4.0
tags: [privacy, compliance, gdpr, hipaa, pci-dss]
signature: null
certified: false
---

## What it does

Blocks any attempt to force cloud LLM routing when the Privacy Router has classified the data as RESTRICTED. This is a hard DENY — no debate, no escalation, no override.

## Why it exists

RESTRICTED data includes secrets (API keys, tokens), patient health records (PHI), credit card numbers (PCI), and government identifiers (SSN, passports). Sending this data to a cloud LLM violates GDPR Art. 44-49 (cross-border transfer), HIPAA Security Rule (PHI disclosure), and PCI DSS Req. 3 (cardholder data protection). The Privacy Router in Sovraine One's MCP Gateway (Couche 1) classifies data and routes RESTRICTED data to local LLMs. This policy ensures that no agent or workflow can bypass that classification.

## What gets blocked

- `override-privacy-route` when `classification=restricted`
- This applies regardless of the agent, debate outcome, or business justification

## What is still allowed

- `override-privacy-route` when `classification=sensitive` (requires audit trail, separate policy)
- `route-to-cloud` for PUBLIC/INTERNAL classified data (normal flow)
- `route-to-local` for any classification level (always safe)
- `redact-pii` for SENSITIVE data before cloud routing (controlled flow)

## How to override

This policy cannot be overridden through normal escalation. Changing RESTRICTED routing requires:
1. A compliance officer to modify the policy in the Guard hub
2. A new signed policy version via the Sovraine Trust Chain
3. A documented regulatory exception with legal review
