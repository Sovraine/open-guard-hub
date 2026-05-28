---
name: review-hub-pr
description: Specialized review for hub PRs. Checks taxonomy, body sections, cross-refs, self-certification, fast-path traps, risk coherence, naming conventions. Trigger keywords — review hub PR, hub review, check hub PR, review policy PR, review mapping PR.
---

# Review Hub PR

Specialized review for pull requests on the OpenGuard Hub.

## Prerequisites

- `gh` CLI authenticated
- `sovctl` CLI installed (download from GitHub Releases)
- Be in the open-guard-hub repo

## Agent Comment Marker

All comments posted by this skill **must** start with:

```
> **📋 hub-review-agent**
```

## Step 1: Fetch PR

```bash
gh pr view <number> --json title,body,headRefName,baseRefName,files
gh pr diff <number>
```

Identify modified hub files:
```bash
gh pr diff <number> --name-only
```

Classify by type (policy, agent, soul, skill, mapping, verb, sector).

## Step 2: Check taxonomy verbs

For each modified file, extract referenced verbs and check that they exist in the taxonomy.

GUARD checks:
- **GUARD-070** — policy `match.actions` contains an unknown verb
- **GUARD-027** — agent `allowed_verbs` / `denied_verbs` contains an unknown verb

```bash
sovctl guard scan --taxonomy . 2>/dev/null | grep "^  "
# OR
grep -r "^  [a-z]" core/ sectors/ --include="_verbs.yaml" | awk -F: '{print $2}' | sed 's/:.*//' | sort -u
```

## Step 3: Check body sections

Verify that the exact Markdown headers are present:

| Type | Required headers (exact text) |
|------|------------------------------|
| Policy | `## What it does`, `## Why it exists`, `## What gets blocked`, `## What is still allowed`, `## How to override` |
| Agent | `## Purpose`, `## Guardrails`, `## Allowed actions`, `## Denied actions`, `## Escalation` |
| Soul | `## Identity`, `## Boundaries`, `## Tone guidelines`, `## Safety instructions` |
| Skill | `## What it does`, `## Inputs`, `## Governance constraints`, `## Side effects`, `## Error handling` |

GUARD checks:
- **GUARD-014** — soul missing section (e.g. `## Tone` instead of `## Tone guidelines`)
- **GUARD-044** — skill missing section

## Step 4: Check cross-references

For agents:
1. `soul: <name>` → exists on `main`? **GUARD-028**
2. `policies: [<name>]` → exist on `main`? **GUARD-030**
3. `skills: [<name>]` → exist on `main`?

**Cross-ref trap**: if a referenced artifact is in ANOTHER PR (not on `main`), that's a problem. The CI scanner checks out `main` for validation.

Also check:
- **GUARD-026** — verb in both `allowed_verbs` and `denied_verbs` (conflict)

## Step 5: Check self-certification

```bash
gh pr diff <number> | grep -E 'certified:\s*true|signature:\s*(?!null)'
```

If found → **BLOCKER** — community PRs cannot set certified/signature.

## Step 6: Check fast-path traps

For DENY or ESCALATE policies:
- Extract `match.actions`
- Check if any verb is READ-ONLY (`select`, `read`, `list`, `list-resources`, `describe-resource`, `search`)
- If yes → **WARNING**: the engine fast-paths READ-ONLY as ALLOW, the policy will be ignored

## Step 7: Check risk coherence

For policies:
- `severity` of the policy vs `risk` of matched verbs
- A DENY HIGH policy on LOW verbs is suspicious

For agents:
- `max_risk` vs risk level of `allowed_verbs`
- An agent with `max_risk: LOW` that allows HIGH verbs is inconsistent

## Step 8: Check naming conventions

- Names in kebab-case
- Correct extensions (`.guard.md`, `.agent.md`, `.soul.md`, `.skill.md`, `.mapping.yaml`)
- In the correct directory (`<type>/<sector>/`)

## Step 9: Run sovctl guard scan (if local)

If the repo is checked out locally:
```bash
sovctl guard scan . --format text
```

Verify grade A.

## Step 10: Post review

```bash
gh pr review <number> --comment --body "$(cat <<'EOF'
> **📋 hub-review-agent**

## Hub Content Review

### Taxonomy Verbs
{results}

### Body Sections
{results}

### Cross-References
{results}

### Self-Certification
{results}

### Fast-Path Traps
{results}

### Risk Coherence
{results}

### Guard Scan
{results}

### Verdict: APPROVE / REQUEST CHANGES
{summary with specific fixes needed}
EOF
)"
```

If everything passes → `gh pr review <number> --approve`
If fixes are needed → `gh pr review <number> --request-changes`
