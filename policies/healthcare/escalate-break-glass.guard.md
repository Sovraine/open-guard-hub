---
name: escalate-break-glass
version: "1.0.0"
domain: sectors/healthcare
description: Warn and audit break-glass emergency access to patient data
schema_version: 1
match:
  actions: ["break-glass-access"]
verdict: WARN
severity: HIGH
priority: 90
author: sovraine
license: CC-BY-SA-4.0
tags: [healthcare, HIPAA, emergency, audit]
signature: null
certified: false
---

## What it does

Emits a critical warning and creates a detailed audit log entry whenever break-glass emergency access to patient data is invoked. The access is allowed to proceed — it is not blocked.

## Why it exists

Break-glass access is a recognized emergency mechanism in healthcare that allows clinicians to access patient records outside normal authorization workflows when there is an immediate threat to patient safety. HIPAA (45 CFR 164.312(a)(2)(ii)) requires that such access be logged and reviewed. This policy ensures that every break-glass event is visible for post-hoc compliance review, abuse detection, and regulatory audit.

## What gets blocked

Nothing is blocked. Break-glass access proceeds immediately to avoid delays in patient care.

## What is still allowed

- All break-glass access proceeds with full audit logging
- Normal access through standard authorization workflows
- Read-only access to de-identified data

## How to override

No override is needed — this is a WARN-level policy. The warning and audit record are mandatory. To suppress the warning, remove or disable this policy, but doing so would violate HIPAA audit requirements.
