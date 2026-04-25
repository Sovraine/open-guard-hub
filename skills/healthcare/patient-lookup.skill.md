<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: patient-lookup
version: "1.0.0"
domain: sectors/healthcare
description: "Access patient medical records with HIPAA audit logging"
schema_version: 1
verbs: [access-patient-record, read]
target: patient-record
risk: HIGH
requires_context: [patient_id, reason_for_access]
preconditions: ["patient exists", "caller is member of care team", "patient_id is valid UUID"]
postconditions: ["patient data returned", "access logged for audit"]
side_effects: ["hipaa-access-log entry created"]
idempotent: true
reversible: false
sector: healthcare
author: sovraine
license: CC-BY-SA-4.0
tags: [hipaa, patient-safety, clinical]
certified: false
---

## What it does

Retrieves patient medical records including demographics, medication history, allergies, clinical notes, and lab results. All access is logged for HIPAA compliance and can be audited by compliance team.

## Inputs

- **patient_id** (required): Valid patient identifier (UUID or MRN)
- **reason_for_access** (required): Clinical justification (diagnosis, treatment, emergency)
- **data_elements** (optional): Specific fields to retrieve (default: demographics + current medications)

## Governance constraints

- **HIGH risk**: Patient data is protected health information (PHI)
- **Care team only**: Caller must be member of patient's authorized care team
- **HIPAA audit required**: Every access logged with timestamp, caller identity, and justification
- **Minimal disclosure**: Only requested data elements are returned
- **Reason validation**: "Break glass" access requires special justification
- **Consent required**: Non-clinical access (research, administrative) requires documented patient consent

## Side effects

- **HIPAA access log**: Entry created with timestamp, access level, caller, and reason
- **Audit trail**: Compliance team can review access history per patient
- **Break-glass escalation**: Emergency access flagged for retrospective review
- **No data modification**: Patient record is read-only from this skill

## Error handling

- Patient not found → returns 404 error
- Unauthorized access → returns 403 error, logged as potential HIPAA violation
- Insufficient justification → returns 400 error, action denied
- Invalid patient_id format → returns 400 error
- Break-glass without approval → returns 403 error, escalates to supervisor
