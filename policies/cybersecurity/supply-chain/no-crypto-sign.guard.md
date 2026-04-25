---
name: no-crypto-sign
version: "1.0.0"
domain: sectors/cybersecurity
description: Block unauthorized cryptocurrency signing and payment authorization
schema_version: 1
match:
  actions: ["sign", "execute"]
  contexts:
    content_pattern: "transferWithAuthorization|signTypedData|EIP-712|EIP-3009|USDC|payment.*sign|crypto.*wallet|privateKey.*sign|402.*payment"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [crypto, supply-chain, x402, financial]
signature: null
certified: false
---

## What it does

Blocks any action that attempts to sign cryptocurrency transactions or authorize token transfers without explicit user consent per transaction.

## Why it exists

The `nirholas/claude-code` malware injects an x402 payment system that automatically signs EIP-3009 `transferWithAuthorization` transactions (USDC on Base/Ethereum) when any HTTP server responds with status 402. The private key is stored in `~/.claude/config.json` and transactions are signed silently without per-transaction user confirmation.

Attack flow:
1. `/x402 setup` generates or imports a secp256k1 private key
2. Key stored in plaintext in `~/.claude/config.json`
3. `WebFetchTool` intercepts HTTP 402 responses
4. Parses `x-payment-required` header for payment requirements
5. Signs EIP-3009 `transferWithAuthorization` with user's private key
6. Retries request with signed payment header — funds transferred silently

## What gets blocked

- `sign` — any cryptographic signing of financial transactions
- `execute` — code execution involving payment signing patterns (EIP-712, EIP-3009, USDC transfer authorization)

## What is still allowed

- Reading cryptocurrency-related code (analysis, audit)
- Standard HTTPS requests (non-402)
- Cryptographic operations for non-financial purposes (JWT signing, TLS)

## How to override

Each financial transaction must receive explicit per-transaction user confirmation with amount, recipient, and chain displayed. The operator must configure a signing policy that includes maximum transaction limits, approved contract addresses, and a hardware wallet requirement. No batch or silent signing is permitted.
