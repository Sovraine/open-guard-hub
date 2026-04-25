<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: demo-sandbox-agent
version: "1.0.0"
domain: sectors/cybersecurity
description: "Forensic sandbox agent — analyzes malicious repositories in isolated environments"
schema_version: 1
soul: forensic-sandbox-soul
model: null
skills: []
allowed_verbs: [read, list-resources, get-resource, search, describe-resource]
denied_verbs: [execute, create-resource, update, sign, export, exfiltrate, lateral-move, plant-implant]
max_risk: LOW
requires_human_above: LOW
sandbox: true
policies:
  - no-crypto-sign
  - no-bind-listener
  - no-auto-load-mcp
  - no-git-hook-install
  - no-undocumented-flags
  - no-act-on-injection
  - no-network-exfil
sector: cybersecurity
author: sovraine
license: CC-BY-SA-4.0
tags: [forensic, sandbox, malware-analysis, supply-chain]
certified: false
---

## Purpose

Forensic analysis agent for examining malicious repositories inside isolated sandbox environments. The agent is restricted to read-only operations — all write, execute, install, and network actions are denied by default and further blocked by 7 supply-chain-specific policies.

## Guardrails

- **Max risk level**: LOW — only read operations allowed without escalation
- **Sandbox mode**: enabled — agent runs in an isolated container with no network
- **All write/execute denied**: denied_verbs blocks execute, create, update, sign, export
- **7 supply-chain policies**: additional protection against specific malware patterns
- **Human escalation**: MEDIUM-risk and above require human approval

## Allowed actions

- Reading files in the mounted workspace
- Listing directories and searching code
- Describing file contents and code patterns
- Generating analysis reports (text output only)

## Denied actions

- Executing any code, scripts, or commands
- Installing packages (npm, pip, etc.)
- Creating or modifying files
- Signing transactions or authorizations
- Network connections of any kind
- Git operations that modify state

## Escalation

- Any action above LOW risk triggers human approval
- Detection of active malware communication patterns escalates to security team
- Sandbox escape attempts are flagged as CRITICAL and halt execution immediately

## Use case

Red team vs blue team demonstration: the agent explores a malicious repository (nirholas/claude-code) and attempts to "set up the development environment" as a naive developer would. Open Guard blocks every malicious action while allowing legitimate read operations.
