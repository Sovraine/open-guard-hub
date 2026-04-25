---
name: escalate-financial
version: "1.0.0"
domain: core/common
description: Escalate financial transactions on e-commerce and payment MCP servers
schema_version: 1
match:
  servers: ["shopify", "stripe"]
  actions: ["create", "update", "delete"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 90
author: sovraine
license: CC-BY-SA-4.0
tags: [financial, e-commerce, payments, shopify, stripe, safety]
signature: null
certified: false
---

## What it does

Requires human approval before creating, modifying, or cancelling financial objects on e-commerce and payment platforms.

## Why it exists

Financial actions move real money. Creating an invoice or payment link charges customers. Completing a draft order triggers payment processing and fulfillment. Creating a refund reverses a charge. Cancelling a subscription terminates recurring revenue. These actions are difficult or costly to reverse and may trigger downstream processes (shipping, accounting, customer notifications).

## What gets blocked

- `create`, `update`, `delete` actions on Shopify and Stripe servers with risk >= HIGH
- Invoice creation and finalization on Stripe
- Draft order completion and product modifications on Shopify

## Servers covered

- **Stripe** — `create_invoice`, `finalize_invoice`, `create_payment_link`, `create_refund`, `cancel_subscription`, `update_subscription`
- **Shopify** — `create_product`, `update_product`, `complete_draft_order`, `create_draft_order`, `create_discount`

## What is still allowed

- All `read`, `list`, and `search` actions (viewing orders, customers, products, invoices)
- Reading shop information

## How to override

A human operator must confirm the transaction with: the financial amount, target customer/entity, and acknowledgment that the action may trigger charges or refunds. The confirmation is recorded in the audit log.
