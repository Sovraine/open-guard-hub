---
name: contributor-onboard
description: Interactive guide for a new contributor. Checks prerequisites, identifies the contribution type, launches the appropriate scaffolding skill. Trigger keywords — onboard contributor, new contributor, how to contribute, getting started, first contribution.
---

# Contributor Onboard

Guide a new contributor through setup and the first commit.

## Important — Scanner rules

- `sg guard scan` only takes **directories**, never individual files
- Always scan `.` (the repo root) as a whole: `sg guard scan .`
- Scanning a subdirectory (`policies/core/`) will produce false GUARD-070 because verbs from other subdirectories are not in scope
- Grade A required for merge

## Verdict decision tree

When a contributor hesitates on the verdict:

```
Is the action ALWAYS forbidden, without exception?
  → YES: DENY (e.g. reverse shell, SQL injection, plaintext secrets)
  → NO:
    Does the action require explicit human approval?
      → YES: ESCALATE_HUMAN (e.g. delete tenant data, 4-eyes transfer)
      → NO:
        Is the case ambiguous and requires multi-agent reasoning?
          → YES: ESCALATE_DEBATE (e.g. kill-switch, deploy model to prod)
          → NO:
            Should the action be traced but not blocked?
              → YES: WARN (e.g. decrypt sensitive, break-glass access)
              → NO: ALLOW
```

## Repo state the contributor MUST know about

`main` is protected. A PR that satisfies all CI checks can still be BLOCKED if any of these are violated:

| Rule | Effect | How to satisfy |
|---|---|---|
| `required_signatures: true` | Every commit must carry a valid GPG or SSH signature | Follow the signing setup runbook **before** the first commit |
| `required_linear_history: true` | No merge commits on the PR branch | Use `git rebase origin/main`, never `git merge` |
| `required_conversation_resolution: true` | All review threads must be marked resolved | Click "Resolve conversation" on every comment before asking for merge |
| DCO sign-off | All commits must have `Signed-off-by` trailer | Use `git commit -s` |

On a fresh machine, Step 1 below will detect missing config and walk the contributor through setup inline — never assume they'll read docs off-screen.

## Step 1: Check & set up the environment

Run the checks:

```bash
# Git 2.34+ required for SSH signing
git --version

# gh CLI
gh auth status

# sg CLI (Sovraine Guard binary)
sg --version 2>/dev/null || echo "sg not installed — download from GitHub Releases: https://github.com/Sovraine/open-guard-hub/releases"

# SSH signing configured? (required for main)
git config --get gpg.format           # expect: ssh (or openpgp if GPG)
git config --get user.signingkey      # expect: a path or key ID
git config --get commit.gpgsign       # expect: true
```

### If any check fails — walk the contributor through setup, do not just link a doc

When a check fails, you (the assistant) are responsible for running the setup **inline, step by step**.

| Failing check | What to do |
|---|---|
| `git --version < 2.34` | Stop. Ask the contributor to upgrade git (Homebrew, apt, etc.) and resume. |
| `gh auth status` not logged in | Run `gh auth login` with the contributor, pick HTTPS + browser flow. |
| `sg --version` not found | Direct to GitHub Releases page for their platform. |
| Signing config missing | Generate ed25519 key, upload to GitHub as Signing Key, configure git, verify with a test commit. |

Do not let the contributor proceed to Step 2 with any of these unresolved.

## Step 2: Identify the contribution type

Ask the user:

**"What type of contribution do you want to make?"**

| Type | Description | Skill to launch |
|------|-------------|-----------------|
| **Policy** | New governance policy (.guard.md) | `/guard-policy-create` |
| **Agent** | New agent with soul (.agent.md + .soul.md) | `/guard-agent-create` |
| **Mapping** | MCP server mapping (.mapping.yaml) | `/guard-mapping-create` |
| **Skill** | New skill (.skill.md) | `/guard-skill-create` |
| **Soul** | New soul/persona (.soul.md) | `/guard-soul-create` |
| **Verb/Sector** | New verb or sector | `/guard-scan-taxonomy` to check |

## Step 3: Local setup

```bash
# Fork the repo (if not a collaborator)
gh repo fork Sovraine/open-guard-hub --clone

cd open-guard-hub

# Verify that scanning works
sg guard scan .
```

## Step 4: Create a branch

```bash
git checkout -b contrib/<type>/<description>
# Examples:
# contrib/policy/deny-plaintext-secrets
# contrib/mapping/grafana-mcp
# contrib/agent/soc-analyst
```

## Step 5: Launch the appropriate skill

Based on the type identified in Step 2, launch the corresponding skill.

Remind:
- `certified: false`, `signature: null` mandatory
- Verbs must exist in the taxonomy (`sg guard scan --taxonomy .`)
- Exact body sections (see CONTRIBUTING.md)
- Cross-refs must point to artifacts on `main`
- `sg guard scan .` must return grade A

## Step 6: Consistency with existing content

Before the pre-flight, check consistency with existing policies in the same sector:

```bash
# List policies in the same sector
ls policies/<sector>/

# Compare verdict/severity/priority
grep -r "^verdict:\|^severity:\|^priority:" policies/<sector>/ --include="*.guard.md"
```

Questions to ask:
- Is the priority in the correct range for this verdict+severity? (see decision tree)
- Are there existing policies that cover a similar case?
- Are the matched verbs consistent with the risk level?

## Step 7: Pre-flight

Before pushing, run `/hub-contribution-check`.

**Reminder**: always `sg guard scan .` (entire repo root), never a subdirectory.

## Step 8: Create the PR

```bash
git push -u origin contrib/<type>/<description>
gh pr create --template hub_proposal.md
```

## Step 9: Wait for CI

CI runs automatically. The checks:

| # | Check | What it does |
|---|---|---|
| 1 | `yaml-lint` | YAML structure validation, reject bombs |
| 2 | `self-cert` | Reject `certified: true` or non-null `signature` |
| 3 | `grade-a-scan` | `sg guard scan .` must return Grade A |
| 4 | `dco-check` | Verify `Signed-off-by` on all commits |

A PR can show all green and **still be BLOCKED** if:
- Commits are unsigned (`required_signatures`)
- Branch has merge commits (`required_linear_history`) — solve with `git rebase origin/main`
- Review threads are not resolved (`required_conversation_resolution`)
