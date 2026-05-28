---
name: deny-delete-customer-account
version: "1.0.0"
domain: sectors/retail-ecommerce
description: Deny autonomous deletion of customer accounts
schema_version: 1
match:
  actions: ["delete-customer-account", "ban-member"]
verdict: DENY
severity: CRITICAL
priority: 95
author: community
license: CC-BY-SA-4.0
tags: [retail, customer-data, privacy, irreversible]
signature: null
certified: false
---

## What it does

Blocks AI agents from deleting customer accounts or banning loyalty program members. These are irreversible, high-impact operations that require human authorization and often have legal implications (GDPR right-to-erasure workflows, data retention requirements).

## Why it exists

Customer account deletion destroys order history, loyalty points, saved payment methods, and preferences. An agent acting on a misunderstood request — or a prompt injection attack — could permanently erase customer data. In jurisdictions with data retention laws, premature deletion may also create compliance violations.

## What gets blocked

- `delete-customer-account` — permanent account removal
- `ban-member` — loyalty program permanent bans

## What is still allowed

- Deactivating accounts (reversible)
- Anonymizing customer data (for GDPR compliance, with proper workflow)
- Suspending loyalty membership (reversible)
- Viewing customer account details

## How to override

```yaml
override:
  policy: deny-delete-customer-account
  reason: "GDPR erasure request — ticket GDPR-2026-1234"
  approved_by: human
  audit_reference: "GDPR-2026-1234"
```
