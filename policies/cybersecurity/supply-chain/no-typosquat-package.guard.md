---
name: no-typosquat-package
version: "1.0.0"
domain: sectors/cybersecurity
description: Detect and block installation of typosquatted package names
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "cIaude|cl4ude|claudee|claudes|cloude|anth[r]?opic[s]?-|anthroplc|axois|axio[sz]$|reqeusts|requets|colars|colurs|fak[e]?rs|cryptoo|web3[jJ]|ethereumj[s]?"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [typosquatting, npm, pip, supply-chain, package-naming]
signature: null
certified: false
---

## What it does

Detects and blocks installation of packages with names that are common typos or visual lookalikes of popular packages.

## Why it exists

Typosquatting is a persistent supply chain attack:

- **Visual confusion**: `cIaude-code` (capital I) vs `claude-code` (lowercase L)
- **Keyboard typos**: `axois` vs `axios`, `reqeusts` vs `requests`
- **Plural/suffix tricks**: `claudees`, `anthropics-sdk`, `fakers`
- **Homoglyphs**: Cyrillic characters that look like Latin (`а` vs `a`, `о` vs `o`)

Real-world examples:
- `event-stream` → `event-strean` (2018, crypto theft)
- `colors` → `colars`, `colurs` (attempted)
- `@anthropic-ai/sdk` → `anthropic-sdk`, `anthroplc-ai` (attempted)
- `claude-code` → `claude-code-explorer-mcp` (nirholas attack, 2026)

## What gets blocked

- `execute` — packages matching known typosquat patterns for popular packages
- Focus on: Claude/Anthropic ecosystem, popular npm/pip packages (axios, requests, etc.)

## What is still allowed

- Installing the correct, verified package names
- Packages from verified publishers (@anthropic-ai, @modelcontextprotocol, etc.)

## Limitations

Pattern-based detection has inherent false positive risk. This policy should be combined with:
- Package signature verification
- Publisher identity verification
- Lockfile integrity checks

## How to override

The operator must add confirmed-legitimate package names to a verified packages list in the gateway configuration, along with their publisher identity and registry URL. False positives can be resolved by the user confirming the package name after reviewing the publisher, download count, and repository link. Each override is logged with the verification evidence.
