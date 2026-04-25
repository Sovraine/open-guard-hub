---
name: no-world-readable-secrets
version: "1.0.0"
domain: core/common
description: Block setting world-readable permissions on files containing secrets
schema_version: 1
match:
  actions: ["execute", "update"]
  contexts:
    content_pattern: "chmod.*(644|666|755|777).*\\.(pem|key|p12|pfx|env|credentials|keystore|id_rsa|id_ed25519)|chmod.*[og]\\+r.*\\.(pem|key)"
verdict: DENY
severity: HIGH
priority: 250
author: sovraine
license: CC-BY-SA-4.0
tags: [permissions, secrets, file-security, hardening]
signature: null
certified: false
---

## What it does

Blocks setting world-readable or group-readable permissions on files that contain or are likely to contain secrets.

## Why it exists

Secret files must be readable only by their owner (mode 600 or 400). Common mistakes:

- `chmod 644 server.pem` → any user on the system can read the private key
- Downloading a file via browser → macOS defaults to 644
- `git checkout` → respects umask, may create world-readable files
- Docker COPY → may reset permissions to 644

Real incident from this investigation:
- `/Users/hoko/Downloads/sovraine.2026-03-31.private-key.pem` was mode 644 (world-readable). Fixed to 600.

Many tools refuse to use world-readable keys:
- `ssh` refuses keys with mode > 600 ("Permissions too open")
- Some TLS libraries warn about readable private keys
- But GitHub App private keys have no such protection — they work regardless of permissions

## What gets blocked

- `execute` — `chmod 644/666/755/777` on secret file patterns
- `update` — permission changes that make secrets group or world readable

## What is still allowed

- `chmod 600` or `chmod 400` on secret files (correct permissions)
- `chmod 644` on non-secret files (code, docs, configs)
- Reading file permissions for auditing

## How to override

The operator can configure permission exceptions for specific file paths where group-readable access is required (e.g., shared service accounts in a controlled environment). The user may approve a permission change after reviewing the file path and target mode. World-readable (644/666/777) permissions on private key files cannot be overridden without operator pre-approval.
