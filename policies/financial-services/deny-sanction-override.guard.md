---
name: deny-sanction-override
version: "1.0.0"
domain: sectors/financial-services
description: Unconditionally deny any attempt to override sanctions screening
schema_version: 1
match:
  actions: ["sanction-override"]
verdict: DENY
severity: CRITICAL
priority: 200
author: sovraine
license: CC-BY-SA-4.0
tags: [banking, sanctions, compliance, AML]
signature: null
certified: false
---

## What it does

Unconditionally blocks any attempt to override, bypass, or suppress sanctions screening results.

## Why it exists

Sanction overrides are NEVER automated — they carry direct legal and criminal liability. Sanctions are imposed by governments and international bodies (OFAC, EU, UN) to prevent financing of terrorism, weapons proliferation, and other threats. Violating sanctions can result in criminal prosecution, billions in fines, and loss of banking licenses. No agent, automated system, or individual employee should have the ability to override sanctions screening without formal legal review.

## What gets blocked

- All `sanction-override` actions, unconditionally
- No context, justification, or approval level can override this policy

## What is still allowed

- Running sanctions screening checks
- Reviewing sanctions screening results
- Flagging false positives for manual review by the compliance team
- Submitting license applications to OFAC/EU for specific exemptions

## How to override

This policy cannot be overridden through the guard system. Sanctions exemptions must go through the institution's legal counsel and be filed with the relevant regulatory authority. Any approved exemption is implemented as a separate, audited process outside the automated pipeline.
