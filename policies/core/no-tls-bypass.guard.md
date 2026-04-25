---
name: no-tls-bypass
version: "1.0.0"
domain: core/common
description: Block disabling TLS certificate verification
schema_version: 1
match:
  actions: ["execute", "configure"]
  contexts:
    content_pattern: "NODE_TLS_REJECT_UNAUTHORIZED.*0|SSL_CERT_FILE.*\\/dev\\/null|REQUESTS_CA_BUNDLE.*\\/dev\\/null|verify.*=.*False|rejectUnauthorized.*false|InsecureSkipVerify.*true|--insecure|--no-check-certificate|-k\\s"
verdict: DENY
severity: HIGH
priority: 250
author: sovraine
license: CC-BY-SA-4.0
tags: [tls, ssl, certificates, mitm, network-security]
signature: null
certified: false
---

## What it does

Blocks any action that disables TLS/SSL certificate verification, which would expose all HTTPS traffic to man-in-the-middle attacks.

## Why it exists

Disabling TLS verification is a common "quick fix" that creates catastrophic security exposure:

- `NODE_TLS_REJECT_UNAUTHORIZED=0` → all Node.js HTTPS requests accept any certificate
- `requests.get(url, verify=False)` → Python accepts forged certificates
- `curl -k` / `wget --no-check-certificate` → ignores invalid certificates
- Go `InsecureSkipVerify: true` → same for Go HTTP clients

Real incident from this investigation:
- The user's `~/.zshrc` contained `export NODE_TLS_REJECT_UNAUTHORIZED=0` (originally for OpenShift CRC self-signed certs). This meant **all Node.js processes on the machine** (including Claude Code, npm, and any MCP servers) were vulnerable to MITM attacks. Fixed by commenting it out.

The correct approach for self-signed certs is to add them to the trust store (`NODE_EXTRA_CA_CERTS`) or set them per-request, never globally disable verification.

## What gets blocked

- `execute` — commands that set `NODE_TLS_REJECT_UNAUTHORIZED=0`
- `configure` — setting TLS bypass in environment or configuration
- `execute` — `curl -k`, `wget --no-check-certificate`
- `execute` — Python/Go/Node code with certificate verification disabled

## What is still allowed

- `NODE_EXTRA_CA_CERTS=/path/to/ca.pem` (adding custom CA, not disabling verification)
- Connecting to services with valid certificates
- Using `--cacert` with specific certificate files

## How to override

The operator can configure TLS exceptions for specific internal hosts that use self-signed certificates, specifying the host, port, and expected certificate fingerprint. The correct approach is to add the CA to the trust store (`NODE_EXTRA_CA_CERTS`), not disable verification. Global TLS bypass (e.g., `NODE_TLS_REJECT_UNAUTHORIZED=0`) cannot be overridden without operator approval and is logged as a security event.
