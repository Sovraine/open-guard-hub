---
name: no-git-hook-install
version: "1.0.0"
domain: sectors/cybersecurity
description: Block installation of git hooks from untrusted sources
schema_version: 1
match:
  actions: ["create", "update", "execute"]
  contexts:
    target_pattern: "\\.git/hooks/|pre-commit|post-checkout|post-merge|pre-push"
    content_pattern: "git.*clone.*exec|chmod.*\\+x|gitpretty|hooks.*install"
verdict: DENY
severity: CRITICAL
priority: 300
author: sovraine
license: CC-BY-SA-4.0
tags: [git, hooks, trojan, persistence, supply-chain]
signature: null
certified: false
---

## What it does

Blocks creation, modification, or installation of git hooks from untrusted sources, and blocks execution of scripts that install git hooks.

## Why it exists

The `nirholas/claude-code` malware includes `gitpretty-apply.sh` which:

1. Clones `https://github.com/nirholas/gitpretty.git` into `~/.gitpretty/`
2. `chmod +x` on ALL `.sh` files
3. Optionally installs git hooks via `emoji-hooks.sh install`
4. Executes `emoji-file-commits.sh` — arbitrary code controlled by the attacker
5. The attacker can change `nirholas/gitpretty` contents at any time

Persistence: git hooks execute on every `git commit` and `git push`, running whatever code the attacker pushes to the remote repo.

## What gets blocked

- `create` / `update` — writing to `.git/hooks/*` paths
- `execute` — shell scripts that install git hooks (`hooks install`, `chmod +x`)
- `execute` — cloning repos that chain to immediate code execution

## What is still allowed

- Reading git hook files for analysis
- Git operations (commit, push, pull) with existing hooks
- Installing hooks from verified, audited sources via package managers

## How to override

The operator must configure an approved hook sources list in the gateway settings, specifying repository URLs and commit hashes for allowed hook installers. Hook scripts must pass a content audit before installation. Only hooks from signed, verified sources (e.g., husky via npm with lockfile integrity) can be pre-approved.
