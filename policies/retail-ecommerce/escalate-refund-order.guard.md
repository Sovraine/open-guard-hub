---
name: escalate-refund-order
version: "1.0.0"
domain: sectors/retail-ecommerce
description: Escalate order refunds for human review before processing
schema_version: 1
match:
  actions: ["refund-order", "void-transaction"]
verdict: ESCALATE
severity: HIGH
priority: 80
author: community
license: CC-BY-SA-4.0
tags: [retail, refund, financial, fraud-prevention]
signature: null
certified: false
---

## What it does

Escalates all refund and void operations for human review before they execute. The agent may prepare the refund but cannot finalize it autonomously.

## Why it exists

Refund fraud is a top loss vector in e-commerce. An AI agent processing refunds without oversight can be manipulated through social engineering in customer conversations, or may misinterpret return policies. Each refund moves money out of the business — a pattern of unauthorized refunds can cause significant financial damage before detection.

## What gets blocked

- `refund-order` actions are escalated (not denied)
- `void-transaction` actions are escalated (not denied)
- Agent can still gather order details and prepare the refund request

## What is still allowed

- Viewing order details and refund history
- Calculating refund amounts
- Initiating return merchandise authorization (RMA)
- Providing refund status to customers

## How to override

```yaml
override:
  policy: escalate-refund-order
  reason: "Auto-refund for orders under $25 per CS policy"
  approved_by: human
  conditions:
    max_amount: 25.00
    currency: USD
```
