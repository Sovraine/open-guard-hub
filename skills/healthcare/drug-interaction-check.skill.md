<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: drug-interaction-check
version: "1.0.0"
domain: sectors/healthcare
description: "Check drug-drug and drug-allergy interactions against clinical databases"
schema_version: 1
verbs: [check-drug-interaction, read]
target: medication
risk: MEDIUM
requires_context: [drug_list, patient_id]
preconditions: ["drug codes are valid RxNorm identifiers", "patient_id exists"]
postconditions: ["interaction severity returned", "interaction alerts generated if present"]
side_effects: ["interaction alert created in EHR if HIGH or CRITICAL severity"]
idempotent: true
reversible: false
sector: healthcare
author: sovraine
license: CC-BY-SA-4.0
tags: [pharmacy, patient-safety, clinical]
certified: false
---

## What it does

Screens a list of medications against clinical interaction databases (RxNorm, FDA, DrugBank) to identify drug-drug interactions, drug-allergy conflicts, and contraindications. Returns severity level and clinical recommendations. If HIGH or CRITICAL interactions are detected, an alert is automatically created in the Electronic Health Record.

## Inputs

- **drug_list** (required): Array of RxNorm drug codes or medication names
- **patient_id** (required): Patient identifier for allergy context
- **severity_threshold** (optional): Minimum severity to report (default: MODERATE)

## Governance constraints

- **MEDIUM risk**: Clinical decision support, not a final prescription decision
- **Evidence-based**: All interaction data sourced from FDA and peer-reviewed databases
- **Cannot override**: If interaction is detected, only a pharmacist or physician can override
- **Allergy integration**: Patient allergies are checked against all drugs in the list
- **Elderly/renal considerations**: May flag interactions that are higher-risk in specific populations

## Side effects

- **EHR alert**: HIGH or CRITICAL interactions automatically alert prescribing physician
- **Audit log**: Drug interaction check is logged with patient, drugs, and result
- **Clinical documentation**: Interaction severity is recorded in patient chart
- **No prescription block**: This skill only alerts; it does not prevent prescribing (physician decides)

## Error handling

- Invalid drug code → returns 400 error with drug name suggestions
- Patient not found → returns 404 error
- Database timeout → returns 504 error, recommends manual pharmacy review
- No interactions found → returns 200 OK with empty alerts array
- Conflicting data → returns pharmacist alert with conflicting sources
