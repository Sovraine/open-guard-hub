---
name: deny-bulk-price-change
version: "1.0.0"
domain: sectors/retail-ecommerce
description: Deny bulk price updates without human approval
schema_version: 1
match:
  actions: ["bulk-update-prices"]
verdict: DENY
severity: CRITICAL
priority: 90
author: community
license: CC-BY-SA-4.0
tags: [retail, pricing, bulk-operations, safety]
signature: null
certified: false
---

## What it does

Blocks all bulk price update operations across the product catalog unless a human explicitly approves them.

## Why it exists

A single bulk price update can instantly change thousands of product prices. An AI agent acting on a misinterpreted instruction — or a hallucinated tool call — could set all products to $0, apply a 99% discount, or introduce pricing errors that result in fulfilled orders at catastrophic losses. The damage is immediate and often irreversible once orders are placed.

## What gets blocked

- All `bulk-update-prices` actions, unconditionally
- Applies across all sub-sectors: catalog, pricing, marketplace

## What is still allowed

- Setting individual product prices (`set-price`)
- Applying discounts to single products or orders (`apply-discount`)
- Price matching on individual items (`price-match`)
- Reviewing current pricing data

## How to override

```yaml
override:
  policy: deny-bulk-price-change
  reason: "Approved seasonal sale — 15% off winter collection"
  approved_by: human
  scope: "category:winter-2026"
```
