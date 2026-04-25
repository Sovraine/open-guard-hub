---
name: escalate-browser-execute
version: "2.0.0"
domain: core/common
description: Escalate execute and delete actions from browser automation MCP servers
schema_version: 1
match:
  servers: ["playwright", "chrome-devtools", "skyvern", "firecrawl"]
  actions: ["execute", "delete"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 80
author: sovraine
license: CC-BY-SA-4.0
tags: [browser, automation, safety]
signature: null
certified: false
---

## What it does

Requires human approval before any `execute` or `delete` action from browser automation MCP servers.

## Why it exists

Browser automation tools expose powerful capabilities: evaluating arbitrary JavaScript, running code snippets, installing browsers, scraping web pages, and closing pages. These actions can exfiltrate data, execute arbitrary code in authenticated contexts, or consume significant resources. Human confirmation ensures the action is intentional and scoped to the right target.

## What gets blocked

- `execute` actions on Playwright, Chrome DevTools, Skyvern, and Firecrawl servers
- `delete` actions on browser automation servers
- Any action matching these servers with risk >= HIGH

## Servers covered

- **Playwright** — `browser_evaluate`, `browser_run_code`, `browser_install`
- **Chrome DevTools** — `evaluate_script`
- **Skyvern** — `skyvern_act`, `skyvern_run_task`, `skyvern_evaluate`, `skyvern_login`, `skyvern_workflow_run`, `skyvern_workflow_delete`, `skyvern_credential_delete`
- **Firecrawl** — `firecrawl_agent`, `firecrawl_browser_execute`

## What is still allowed

- `read` — screenshots, snapshots, console messages, network requests
- `search` — geocoding, POI lookup
- `list` — tab listing, page listing
- `create` — opening new pages
- `configure` — resizing, emulating devices

## How to override

A human operator must approve the escalation. The approval is recorded in the audit log with the approver identity, timestamp, and justification.
