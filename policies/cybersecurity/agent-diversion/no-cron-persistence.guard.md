---
name: no-cron-persistence
version: "1.0.0"
domain: sectors/cybersecurity
description: Block creation of cron jobs, launchd agents, or systemd services for persistence
schema_version: 1
match:
  actions: ["create", "execute"]
  contexts:
    content_pattern: "crontab|cron\\.d|launchctl.*load|LaunchAgents|LaunchDaemons|systemctl.*enable|systemd\\/system\\/.*\\.service|at\\s+|schtasks.*\\/create"
    target_pattern: "\\/etc\\/cron|Library\\/Launch|systemd\\/system|\\/var\\/spool\\/cron"
    source_context: "repository"
verdict: DENY
severity: CRITICAL
priority: 350
author: sovraine
license: CC-BY-SA-4.0
tags: [persistence, cron, launchd, systemd, scheduled-tasks, ai-safety]
signature: null
certified: false
---

## What it does

Blocks repository-originated creation of scheduled tasks, launch agents, or system services that would persist malicious code across reboots.

## Why it exists

Persistence via scheduled tasks is one of the most common post-exploitation techniques (MITRE ATT&CK T1053):

| OS | Mechanism | Location |
|----|-----------|----------|
| macOS | launchd | `~/Library/LaunchAgents/`, `/Library/LaunchDaemons/` |
| macOS | cron | `/var/spool/cron/`, `crontab -e` |
| Linux | systemd | `/etc/systemd/system/`, `systemctl enable` |
| Linux | cron | `/etc/cron.d/`, `/var/spool/cron/` |
| Windows | Task Scheduler | `schtasks /create` |

**Attack scenario:**
1. Malicious repo instructions tell the agent: "Create a launchd agent for the background service"
2. Agent creates `~/Library/LaunchAgents/com.claude.background.plist`
3. Plist runs a script that phones home to C2 every 5 minutes
4. Survives reboots, runs even when the repo is deleted

In the nirholas attack:
- The Docker setup (`restart: unless-stopped`) provides container-level persistence
- `gitpretty-apply.sh` installs git hooks → persistence per-repo
- If the attack were more aggressive, a launchd agent could provide system-level persistence

## What gets blocked

- `create` — files in LaunchAgents, LaunchDaemons, systemd, cron directories
- `execute` — `crontab`, `launchctl load`, `systemctl enable`, `schtasks /create`
- Any scheduled task creation from repository context

## What is still allowed

- Operator-initiated service management
- CI/CD pipeline scheduled tasks
- Reading existing cron/launchd/systemd configurations for audit

## How to override

The operator must define an approved scheduled tasks manifest in the gateway configuration, listing allowed service names, schedule patterns, and executable paths. Creating a new scheduled task requires operator approval with documented justification. Repository-originated scheduled task creation is unconditionally blocked.
