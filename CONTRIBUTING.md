# Contributing to OpenGuard Hub

Thank you for contributing to the OpenGuard Hub!

The Hub is licensed under **CC-BY-SA-4.0**. Contributions require a [DCO sign-off](DCO), not a CLA.

## What You Can Contribute

| Type | Directory | Format | Guide |
|---|---|---|---|
| Verbs | `sectors/<sector>/` | `_verbs.yaml` | [Adding a Verb](#adding-a-verb) |
| Policies | `policies/<sector>/` | `.guard.md` | [Adding a Policy](#adding-a-policy) |
| Agents | `agents/<sector>/` | `.agent.md` | [Adding an Agent](#adding-an-agent) |
| Skills | `skills/<sector>/` | `.skill.md` | [Adding a Skill](#adding-a-skill) |
| Souls | `souls/<sector>/` | `.soul.md` | [Adding a Soul](#adding-a-soul) |
| Mappings | `mappings/` | `.mapping.yaml` | [Adding a Mapping](#adding-a-mapping) |

---

## Quick Start with Claude Code

If you use [Claude Code](https://claude.com/claude-code), type `/contributor-onboard` to get an interactive guide. It will:

1. Check your prerequisites (`git`, `sg` CLI)
2. Ask what you want to contribute (policy, agent, mapping, skill, verb)
3. Scaffold the artifact with correct frontmatter and body sections
4. Validate against the taxonomy and run `sg guard scan`
5. Guide you through creating the PR

Other useful skills: `/guard-policy-create`, `/guard-agent-create`, `/guard-mapping-create`, `/hub-contribution-check` (pre-flight before push).

---

## Before You Start — The Taxonomy

Every verb referenced in policies, agents, or skills **must exist** in the taxonomy. The scanner rejects unknown verbs.

### Finding available verbs

```bash
# List all verbs in the taxonomy
sg guard scan --taxonomy .

# Browse verb files directly
ls core/common/_verbs.yaml      # Universal verbs (create, read, update, delete, list, search, ...)
ls core/kubernetes/_verbs.yaml   # Kubernetes verbs (scale, rollout-restart, exec-in-pod, ...)
ls core/cloud/_verbs.yaml        # Cloud verbs (provision-instance, terminate-instance, ...)
ls core/security/_verbs.yaml     # Security verbs (scan-vulnerability, rotate-secret, ...)
ls core/database/_verbs.yaml     # Database verbs (query, migrate, backup-database, ...)
```

**Common core verbs** (from `core/common/_verbs.yaml`):

`create`, `read`, `update`, `delete`, `list`, `search`, `export`, `import`, `archive`, `restore`, `approve`, `reject`, `escalate`, `assign`, `enable`, `disable`, `configure`, `execute`, `schedule`, `cancel`, `notify`, `comment`, `tag`, `share`, `clone`, `lock`, `unlock`

> **Common mistake:** Using verbs like `write-file`, `commit`, `restart`, `get-logs`, `terminate` which don't exist in the taxonomy. Use the canonical names: `create`, `execute`, `rollout-restart`, `read`, `terminate-instance`.

### Validating locally

Always run the scanner before pushing:

```bash
sg guard scan .
```

The scanner runs 105+ GUARD-XXX checks and assigns a grade. **Grade A is required** to pass CI.

---

## Adding a Verb

1. Find the correct `_verbs.yaml` file (sector/sub-sector)
2. Add your verb following the naming convention: `verb[-qualifier[-object]]`
3. Include: `risk` (required), `description` (required), and optionally `reversible`, `examples`
4. Submit a PR

```yaml
# In core/common/_verbs.yaml or sectors/<sector>/<sub>/_verbs.yaml
verbs:
  my-new-verb:
    risk: MEDIUM
    description: "What this verb does"
    reversible: true
    examples: ["Agent does X"]
```

**Risk levels:** `READ-ONLY`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (see [STYLE_GUIDE.md](STYLE_GUIDE.md) for criteria).

---

## Adding a Policy

Create a `.guard.md` file in `policies/<sector>/`.

### Required frontmatter

```yaml
---
name: my-policy-name
version: "1.0.0"
domain: core                          # or sectors/<sector>
description: One-line description
schema_version: 1
match:
  actions: ["create", "update"]       # Must be valid taxonomy verbs!
verdict: DENY                         # ALLOW, DENY, WARN, ESCALATE_DEBATE, ESCALATE_HUMAN
severity: HIGH                        # READ-ONLY, LOW, MEDIUM, HIGH, CRITICAL
priority: 85                          # 0-99
author: community
license: CC-BY-SA-4.0
tags: [security, example]
signature: null                       # Must be null (community cannot self-sign)
certified: false                      # Must be false (community cannot self-certify)
---
```

### Required body sections (exact headers)

The Markdown body **must** contain these 5 sections:

```markdown
## What it does
## Why it exists
## What gets blocked
## What is still allowed
## How to override
```

> **GUARD-070 — policy-unknown-action:** Every action in `match.actions` must exist in the taxonomy `_verbs.yaml` files. Glob patterns (`*`, `delete-*`) are allowed.

> **Fast-path trap:** Do not use READ-ONLY verbs (e.g. `select`, `read`, `list`, `search`) in a DENY or ESCALATE policy. The engine fast-paths READ-ONLY verbs as ALLOW **before** evaluating policies, so your rule would be silently ignored. Only match verbs with risk >= LOW in DENY/ESCALATE policies.

### Full example

See [`policies/saas-tech/escalate-kill-switch.guard.md`](policies/saas-tech/escalate-kill-switch.guard.md) for a complete working example.

---

## Adding an Agent

Create an `.agent.md` file in `agents/<sector>/`.

### Required frontmatter

```yaml
---
name: my-agent
version: "1.0.0"
domain: core
description: "One-line description"
schema_version: 1
soul: my-agent-soul                   # Must match a soul in souls/
model: null
skills: []
allowed_verbs: [read, list, search]   # Must be valid taxonomy verbs!
denied_verbs: [delete, execute]       # Must be valid taxonomy verbs!
max_risk: MEDIUM
requires_human_above: MEDIUM
sandbox: false
policies:
  - no-tls-bypass                     # Must match policies in policies/
sector: core
author: community
license: CC-BY-SA-4.0
tags: [example]
certified: false
---
```

### Required body sections (exact headers)

```markdown
## Purpose
## Guardrails
## Allowed actions
## Denied actions
## Escalation
```

> **GUARD-027 — agent-unknown-verb:** Every verb in `allowed_verbs` and `denied_verbs` must exist in the taxonomy. Use `sg guard scan --taxonomy .` to list all available verbs.

### Cross-references

Agents reference other hub artifacts by **name**:

- `soul: <name>` — must match `souls/<sector>/<name>*.soul.md`
- `skills: [<name>]` — must match `skills/<sector>/<name>.skill.md`
- `policies: [<name>]` — must match `policies/<sector>/<name>.guard.md`

> **Cross-ref trap:** Referenced artifacts must exist **on `main`**, not on other open PRs. The CI scanner checks out `main` for validation. If your agent depends on a new policy from another PR, either merge that PR first or reference an existing policy.

---

## Adding a Skill

Create a `.skill.md` file in `skills/<sector>/`.

### Required frontmatter

```yaml
---
name: my-skill
version: "1.0.0"
domain: core
description: "One-line description"
schema_version: 1
verbs: [read, update]                 # Must be valid taxonomy verbs!
risk: MEDIUM
target: "what this skill operates on"
author: community
license: CC-BY-SA-4.0
tags: [example]
certified: false
---
```

### Required body sections (exact headers)

```markdown
## What it does
## Inputs
## Governance constraints
## Side effects
## Error handling
```

---

## Adding a Soul

Create a `.soul.md` file in `souls/<sector>/`.

### Required frontmatter

```yaml
---
name: my-soul
version: "1.0.0"
domain: core
description: "One-line persona description"
schema_version: 1
tone: calm, precise, analytical
language: en
safety_rules:
  - "Rule 1"
  - "Rule 2"
forbidden_topics: ["topic1", "topic2"]
max_risk: MEDIUM
escalation_trigger: MEDIUM
sector: core
author: community
license: CC-BY-SA-4.0
tags: [example]
certified: false
---
```

### Required body sections (exact headers)

```markdown
## Identity
## Boundaries
## Tone guidelines
## Safety instructions
```

> **GUARD-014 — soul-missing-section:** The scanner checks for the **exact** header text. `## Tone` will fail — it must be `## Tone guidelines`. Same for `## Safety` — it must be `## Safety instructions`.

---

## Adding a Mapping

Create a `.mapping.yaml` file in `mappings/`.

### Required fields

```yaml
server: my-mcp-server                 # MCP server name
description: "What the server does"
version: "1.0.0"
license: CC-BY-SA-4.0
upstream:
  package: "@org/mcp-server"           # npm or PyPI package name
  registry: npm                        # npm or pypi
  transport: stdio                     # stdio or sse

tools:
  tool_name:
    action: read                       # Taxonomy verb
    risk: READ-ONLY                    # Risk level
    description: "What this tool does"
    target_from: resource_id           # Which parameter identifies the target
```

### Full example

See [`mappings/aws-rds.mapping.yaml`](mappings/aws-rds.mapping.yaml) for a complete working example.

---

## Review Process

Every hub PR goes through two reviews:

1. **Automated hub review** — The `review-hub-pr` agent checks taxonomy verbs, body sections, cross-references, self-certification, fast-path traps, risk coherence, naming conventions, and runs `sg guard scan`. Results are posted as a structured PR comment starting with `📋 hub-review-agent`.
2. **Human maintainer review** — Required for merge. The maintainer reviews the policy logic, not just the format.

If you use Claude Code, you can run the review locally before pushing:

```
/review-hub-pr <pr-number>
```

## Quality Gates

CI runs three jobs on every PR. All must pass to merge.

### Content security lint (13 checks)

These checks run without secrets and catch supply-chain attacks before the scanner even runs.

| # | Check | What it blocks | Fix |
|---|-------|----------------|-----|
| 1 | YAML bomb | Files > 1MB | Split large files or reduce content |
| 2 | Self-certification | `certified: true` or non-null `signature` | Set `certified: false` and `signature: null` |
| 3 | Symlinks | Any symbolic link | Use regular files only |
| 4 | Binary content | Null bytes in `.yaml`/`.yml`/`.md` | Remove binary data |
| 5 | Executable permissions | Files with +x bit | Run `chmod -x <file>` |
| 6 | Hidden files | Dotfiles outside `.github/`, `.claude/` | Remove hidden files |
| 7 | Non-ASCII filenames | Unicode in file/dir names | Use ASCII-only names (kebab-case) |
| 8 | Git config tampering | Changes to `.gitmodules`, `.mailmap` | Remove these changes |
| 9 | Workflow isolation | Workflow + content in same PR | Split into two PRs |
| 10 | Template injection | `${{ }}` in content files | Remove template expressions |
| 11 | Priority/author | `priority > 500` or `author != community` | Set `priority` <= 500 and `author: community` |
| 12 | YAML anchor abuse | > 20 anchors, > 50 aliases, > 40 indent | Simplify YAML structure |
| 13 | File type allowlist | Files not `.yaml`/`.yml`/`.md`/`.json`/`.html` | Use an allowed extension |

### Guard scan (Grade A)

The scanner runs 105+ GUARD checks and assigns a grade. **Grade A required** to merge. No PR is auto-merged — all require human review.

### Common GUARD checks and how to fix them

| Check | Severity | What it means | Fix |
|---|---|---|---|
| **GUARD-070** | MEDIUM | Policy references an action not in the taxonomy | Use a verb from `*/_verbs.yaml` or a glob pattern |
| **GUARD-027** | MEDIUM | Agent references an unknown verb | Use `sg guard scan --taxonomy .` to find valid verbs |
| **GUARD-014** | MEDIUM | Soul is missing a required body section | Add all 4 sections: `## Identity`, `## Boundaries`, `## Tone guidelines`, `## Safety instructions` |
| **GUARD-044** | MEDIUM | Skill is missing a required body section | Add all 5 sections (see [Adding a Skill](#adding-a-skill)) |
| **GUARD-028** | MEDIUM | Agent references a soul that doesn't exist | Check the `soul:` field matches a `.soul.md` name |
| **GUARD-030** | MEDIUM | Agent references a policy that doesn't exist | Policy must exist on `main` — merge it first or use an existing one |
| **GUARD-026** | MEDIUM | Agent has a verb in both allowed and denied | Remove the conflict |
| **Fast-path** | WARNING | DENY/ESCALATE policy on a READ-ONLY verb | Remove READ-ONLY verbs from DENY policies — they are fast-pathed as ALLOW |

### Grade scale

| Grade | Meaning |
|---|---|
| **A** | 0 warnings, 0 errors — **required for merge** |
| **B** | 1-3 warnings, 0 errors |
| **C** | 4-6 warnings |
| **D** | 7-10 warnings |
| **F** | 11+ warnings or any error |

---

## DCO Sign-Off

By contributing, you certify that you have the right to submit the work under the CC-BY-SA-4.0 license.

Sign your commits with `Signed-off-by`. CI verifies the sign-off is present **and** that the email matches the commit author:

```bash
git commit -s -m "hub: add patient-discharge skill for healthcare"
```

See the full [Developer Certificate of Origin](DCO) for details.

---

## Style Guide

### Naming Conventions

- Verbs: `verb[-qualifier[-object]]` in kebab-case (`transfer-funds`, `kyc-verify`)
- Policies: `<descriptive-name>.guard.md` in kebab-case
- Agents: `<descriptive-name>.agent.md` in kebab-case
- Skills: `<descriptive-name>.skill.md` in kebab-case
- Souls: `<descriptive-name>.soul.md` in kebab-case
- Mappings: `<server-name>.mapping.yaml` in kebab-case

### Directory Structure

```
<type>/<sector>/<name>.<type>.md
mappings/<server-name>.mapping.yaml
```

### Sectors

`core`, `automotive`, `cybersecurity`, `education`, `energy-utilities`, `financial-services`, `healthcare`, `hospitality`, `human-resources`, `legal`, `logistics`, `manufacturing`, `media-entertainment`, `professional-services`, `public-sector`, `real-estate`, `retail-ecommerce`, `saas-tech`, `telecom`
