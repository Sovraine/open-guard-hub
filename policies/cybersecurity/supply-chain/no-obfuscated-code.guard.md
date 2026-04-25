---
name: no-obfuscated-code
version: "1.0.0"
domain: sectors/cybersecurity
description: Block execution of obfuscated or dynamically constructed code
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "eval\\(atob|eval\\(Buffer\\.from|eval\\(decode|new Function\\(|Function\\(.*fromCharCode|\\\\x[0-9a-f]{2}\\\\x[0-9a-f]{2}|\\\\u00[0-9a-f]{2}\\\\u00|String\\.fromCharCode\\(.*\\)|unescape\\(%|exec\\(.*base64|eval\\(unescape"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [obfuscation, eval, code-injection, supply-chain, deobfuscation]
signature: null
certified: false
---

## What it does

Blocks execution of code that uses obfuscation techniques to hide its true intent.

## Why it exists

Obfuscated code is a hallmark of malicious payloads:

- **eval + base64**: `eval(atob("bWFsd2FyZQ=="))` — hides the actual code
- **Function constructor**: `new Function(String.fromCharCode(97,108,101,114,116))` — constructs code at runtime
- **Hex escape sequences**: `\x63\x6f\x6e\x73\x6f\x6c\x65` — obscures strings
- **Unicode escapes**: `\u0063\u006f\u006e\u0073\u006f\u006c\u0065` — same as above
- **Nested encoding**: `eval(unescape('%63%6F%6E%73%6F%6C%65'))` — multiple layers
- **Buffer.from chains**: `eval(Buffer.from('...','base64').toString())` — Node.js specific

Legitimate code rarely uses these patterns. When they appear in postinstall scripts or dynamically loaded modules, they almost always indicate malicious intent.

## What gets blocked

- `execute` — code containing `eval()` with encoded/decoded content
- `execute` — `new Function()` with character code construction
- `execute` — strings with high density of hex or unicode escape sequences
- `execute` — chained encoding/decoding followed by execution

## What is still allowed

- Reading and analyzing obfuscated code (no execution)
- Legitimate uses of base64 (data URIs, image encoding, API payloads)
- `JSON.parse()` with base64 input (parsing, not execution)
- Source maps and minified code (compression, not obfuscation)

## How to override

The operator must add specific file paths or package names to an obfuscation exception list in the gateway configuration, with documented justification (e.g., known minified vendor bundles). Exceptions require the file hash to be pinned. Users cannot bypass this policy at runtime without operator pre-approval.
