---
name: no-context-window-flooding
version: "1.0.0"
domain: sectors/cybersecurity
description: Detect and block context window flooding designed to push security instructions out of context
schema_version: 1
match:
  actions: ["read"]
  contexts:
    file_size_exceeds: 50000
    source_file_pattern: "Skill\\.md|CONVENTIONS\\.md|ARCHITECTURE\\.md|CONTRIBUTING\\.md|docs/.*\\.md"
    content_pattern: "## (Architecture|Patterns|Conventions|Directory|Style|Naming|Import)"
verdict: WARN
severity: HIGH
priority: 200
author: sovraine
license: CC-BY-SA-4.0
tags: [context-flooding, prompt-injection, attention-dilution, ai-safety]
signature: null
certified: false
---

## What it does

Detects when repository files attempt to flood the agent's context window with large volumes of benign-looking content, pushing security-relevant instructions out of the model's attention window.

## Why it exists

Context window flooding is a subtle prompt injection technique:

1. Attacker creates a massive instruction file (Skill.md in nirholas was 400+ lines)
2. File contains legitimate-looking architecture docs, coding conventions, naming guides
3. The sheer volume of "trusted" content pushes the agent's security instructions toward the end of the context window
4. LLMs pay less attention to middle/end content (lost in the middle effect)
5. Security guardrails become less effective as they lose attention weight

In the nirholas attack, `Skill.md` contained:
- Detailed directory maps, file lists, naming conventions
- Complete tool/command/component pattern documentation
- Import practices, service descriptions, configuration details
- All of this was real Claude Code documentation — mixed with x402/PTY as normal features

The flooding served two purposes:
1. Made Claude treat the repo as thoroughly documented/legitimate
2. Diluted Claude's attention to its own security review instructions

## What gets blocked

- Loading extremely large files (>50KB) into agent context when they match known documentation flooding patterns (e.g., Skill.md, CONVENTIONS.md, ARCHITECTURE.md)
- Injecting massive base64-encoded blobs or serialized data designed to consume context window capacity
- Flooding with repetitive or near-duplicate content sections intended to push security instructions out of the model's active attention window
- Concatenating multiple large documentation files in a single prompt to dilute instruction priority
- Embedding oversized inline data (encoded images, serialized configs, full dependency trees) that serve no functional purpose but exhaust context budget

## What gets triggered

- `WARN` — large instruction files (>50KB) in a repository that match documentation patterns
- The warning alerts the operator that the agent's context may be polluted

## What is still allowed

- Reading large files (the action is WARN, not DENY)
- Legitimate large documentation files (but the operator is alerted)
- The gateway can optionally truncate or summarize large instruction files before they enter the LLM context

## How to override

The operator can raise the file size threshold or whitelist specific documentation files in the gateway configuration. The user may acknowledge the warning and proceed on a per-file basis. Increasing the threshold should be accompanied by enabling the gateway's context summarization feature to mitigate attention dilution.
