<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: kyc-verify
version: "1.0.0"
domain: sectors/financial-services
description: "Know-Your-Customer verification against government and sanctions databases"
schema_version: 1
verbs: [kyc-verify, search]
target: customer
risk: MEDIUM
requires_context: [customer_name, date_of_birth, jurisdiction]
preconditions: ["customer data is valid", "regulatory database access is available"]
postconditions: ["kyc_status updated", "verification result logged"]
side_effects: ["kyc_record created", "audit_trail entry recorded"]
idempotent: false
reversible: false
sector: financial-services
author: sovraine
license: CC-BY-SA-4.0
tags: [compliance, KYC, regulatory]
certified: false
---

## What it does

Performs Know-Your-Customer verification by cross-referencing customer identity, date of birth, and jurisdiction against government ID databases, sanctions lists (OFAC, EU, UN), and PEP (Politically Exposed Person) registries. Returns verification status and flags any matches for manual review.

## Inputs

- **customer_name** (required): Full legal name
- **date_of_birth** (required): Birth date (YYYY-MM-DD)
- **jurisdiction** (required): Country of citizenship or residence
- **id_type** (optional): ID document type (passport, drivers_license, national_id)
- **id_number** (optional): ID document number for direct validation

## Governance constraints

- **MEDIUM risk**: Verification is deterministic but not reversible
- **Sanctions compliance**: Results are final; cannot be overridden by automated systems
- **No false clearances**: Ambiguous matches escalate to human analyst
- **Audit trail required**: Every verification logged with timestamp and operator
- **Regulatory reporting**: Suspicious matches reported to FinCEN or equivalent
- **GDPR compliance**: Personal data processed only for KYC purpose, retained per regulation

## Side effects

- **KYC record created**: Customer verification status stored in KYC database
- **Sanctions match escalation**: Any OFAC or EU match triggers alert to compliance team
- **PEP flag**: Politically exposed persons flagged for enhanced due diligence
- **Audit log**: Verification attempt, result, and operator identity recorded
- **No data deletion**: Records retained per regulatory retention requirements

## Error handling

- Customer not found in ID database → returns UNVERIFIED status, requires manual review
- Sanctions match → returns BLOCKED status, mandatory human review
- PEP match → returns FLAGGED status, enhanced due diligence required
- Database unavailable → returns SERVICE_UNAVAILABLE, queued for retry
- Data quality issues → returns INCOMPLETE, requires updated customer data
