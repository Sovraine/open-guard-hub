---
name: hub-contribution-check
description: Local pre-flight before pushing a hub contribution. Checks frontmatter, taxonomy verbs, body sections, cross-refs, fast-path traps, and runs sovctl guard scan. Trigger keywords — check contribution, pre-flight, validate, ready to push, hub check.
---

# Hub Contribution Check

Complete pre-flight before pushing a hub contribution.

## Step 1: Identify modified files

```bash
git diff --name-only main...HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard
```

### Classify hub files

- `.guard.md` → policy
- `.agent.md` → agent
- `.soul.md` → soul
- `.skill.md` → skill
- `.mapping.yaml` → mapping
- `_verbs.yaml` → verb file
- `_sector.yaml` → sector file

## Step 2: Frontmatter validation

Community PRs must have: `certified: false`, `signature: null`, `author: community`, `license: CC-BY-SA-4.0`, `schema_version: 1`.

Type-specific required fields:
- **Policy**: name, version, domain, description, match.actions (non-empty), verdict, severity, priority (0-99)
- **Agent**: soul (existing), allowed_verbs, denied_verbs, max_risk, policies
- **Soul**: tone, language, safety_rules, forbidden_topics, max_risk, escalation_trigger
- **Skill**: verbs, risk
- **Mapping**: server, description, version, license, tools (with action, risk, description, target_from)

## Step 3: Verb taxonomy check

Extract all referenced verbs. For each (except globs):
```bash
grep -r "^  $VERB:" core/ sectors/ --include="_verbs.yaml"
```
Missing verb → ERROR.

## Step 4: Body sections

- **Policy**: `## What it does`, `## Why it exists`, `## What gets blocked`, `## What is still allowed`, `## How to override`
- **Agent**: `## Purpose`, `## Guardrails`, `## Allowed actions`, `## Denied actions`, `## Escalation`
- **Soul**: `## Identity`, `## Boundaries`, `## Tone guidelines`, `## Safety instructions`
- **Skill**: `## What it does`, `## Inputs`, `## Governance constraints`, `## Side effects`, `## Error handling`

## Step 5: Cross-refs and fast-path traps

- Check that referenced souls/policies/skills exist on `main` or in the same PR
- DENY on READ-ONLY verbs → WARNING (fast-path trap: engine ALLOWs before policy evaluation)

## Step 6: Run sovctl guard scan

```bash
sovctl guard scan . --format text
```
**Always scan `.` (the repo root) as a whole** (subdirectory scan produces false GUARD-070). Target: Grade A.

---

## Output

```markdown
## Contribution Pre-flight Report

**Type:** Policy / Agent / Soul / Skill / Mapping / Verb
**Files:** N modified

| Check | Status | Details |
|-------|--------|---------|
| ... | PASS/FAIL | ... |

**Ready to push: YES / NO**
```
