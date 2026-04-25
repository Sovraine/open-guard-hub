---
name: no-postinstall-exec
version: "1.0.0"
domain: sectors/cybersecurity
description: Block execution of untrusted npm/pip/cargo postinstall and lifecycle scripts
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "postinstall|preinstall|prepare|prepublish|postpublish|pre-commit.*install|husky.*install|npm.*run.*postinstall|pip.*setup\\.py|cargo.*build\\.rs"
verdict: DENY
severity: HIGH
priority: 250
author: sovraine
license: CC-BY-SA-4.0
tags: [npm, pip, cargo, postinstall, supply-chain, lifecycle-scripts]
signature: null
certified: false
---

## What it does

Blocks execution of package manager lifecycle scripts (postinstall, preinstall, prepare, etc.) from untrusted or unaudited packages.

## Why it exists

Package lifecycle scripts are the #1 supply chain attack vector across all ecosystems:

- **npm**: `postinstall` runs arbitrary code after `npm install`. Used by `event-stream` (2018), `ua-parser-js` (2021), `colors`/`faker` (2022), and thousands of malicious packages yearly
- **pip**: `setup.py` executes during `pip install`. Used by typosquatting attacks on PyPI
- **cargo**: `build.rs` runs at compile time. Used by crate supply chain attacks
- **husky/lint-staged**: `prepare` script auto-installs git hooks

Attack pattern:
1. Attacker publishes package with innocuous name
2. `postinstall` script runs on `npm install` — downloads and executes second-stage payload
3. Payload runs with full user privileges — reads SSH keys, env vars, crypto wallets
4. Exfiltrates data before the developer notices anything

## What gets blocked

- `execute` — `npm install` / `pip install` when postinstall scripts are present and unaudited
- `execute` — direct execution of lifecycle scripts
- `execute` — `npm run postinstall`, `pip setup.py install`, `cargo build` with untrusted `build.rs`

## What is still allowed

- `npm install --ignore-scripts` (scripts disabled)
- Installing packages from an audited allowlist
- Reading package.json scripts section for analysis
- Package managers with lockfile integrity verification

## How to override

The operator can maintain a curated allowlist of packages whose lifecycle scripts have been audited and approved. Packages can be added to the allowlist after a security review with documented findings. For unlisted packages, the user may approve execution after reviewing the script content, and the decision is logged for audit.
