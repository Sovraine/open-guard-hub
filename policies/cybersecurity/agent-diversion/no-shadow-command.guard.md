---
name: no-shadow-command
version: "1.0.0"
domain: sectors/cybersecurity
description: Block creation of scripts that shadow legitimate system commands
schema_version: 1
match:
  actions: ["create", "execute"]
  contexts:
    content_pattern: "alias.*=|PATH=.*:\\$PATH|ln -s.*\\/usr\\/local\\/bin|cp.*\\/usr\\/local\\/bin|chmod.*\\+x.*\\/usr\\/local\\/bin"
    target_pattern: "\\/usr\\/local\\/bin\\/|~/\\.local\\/bin\\/|~/bin\\/"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [command-shadowing, path-hijack, persistence, trojan, ai-safety]
signature: null
certified: false
---

## What it does

Blocks creation of scripts or aliases that shadow legitimate system commands, enabling persistent code execution.

## Why it exists

Command shadowing places a malicious script earlier in `$PATH` than the legitimate command:

**Techniques:**
- Create `~/bin/git` that wraps the real git but exfiltrates credentials
- `alias claude='malicious-claude-wrapper'` in `.bashrc`
- `ln -s /tmp/evil.sh /usr/local/bin/npm` — shadow npm globally
- Modify `$PATH` to prepend an attacker-controlled directory

**Why it's effective:**
- The user types the same command they always do — no behavioral change
- The shadow script calls the real command after its payload → invisible
- Persists across sessions (if in `$PATH` or shell config)
- Even security-aware users may not check `which <command>` regularly

In the nirholas attack:
- The Docker entrypoint creates `/usr/local/bin/claude` as a wrapper script
- `gitpretty-apply.sh` clones scripts to `~/.gitpretty/` and makes them executable
- The `$PATH` modification in `.zshrc` (`export PATH="/Users/hoko/bin/:$PATH"`) means any script in `~/bin/` shadows system commands

## What gets blocked

- `create` — executable scripts in PATH directories from repository context
- `execute` — commands that create aliases or PATH modifications
- `create` — symlinks to attacker-controlled scripts in system directories

## What is still allowed

- Operator-initiated PATH modifications
- Package manager installations (npm, brew) that create legitimate binaries
- Development scripts in the project directory (not in PATH)

## How to override

The operator must explicitly approve PATH-visible script installations in the gateway configuration by specifying the target path, script hash, and purpose. Legitimate development tool installations (via brew, npm global, pip) should use their standard installation paths. No repository-originated action can place executables in PATH directories without operator pre-approval.
