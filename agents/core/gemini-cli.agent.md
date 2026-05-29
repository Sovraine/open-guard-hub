<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
<!-- Copyright (c) 2026 SOVRAINE PTE.LTD -->

---
name: gemini-cli
version: "1.0.0"
domain: core/common
description: "Gemini CLI AI assistant — development and operations agent"
schema_version: 1
soul: cautious
model: null
skills: []
allowed_verbs: [read, list, search, create, update, write, get, fetch, describe, execute]
denied_verbs: [delete, drop, truncate, destroy, purge]
max_risk: MEDIUM
requires_human_above: HIGH
sandbox: false
policies: []
sector: generic
author: sovraine
license: CC-BY-SA-4.0
tags: [gemini-cli, development]
certified: false
---

## Purpose

Agent profile for Gemini CLI operating through the open-guard-gateway. Permits standard read/write operations with escalation on destructive actions.
