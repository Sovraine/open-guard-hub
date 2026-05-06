# Agents & Skills — open-guard-hub

Claude Code agents and skills for AI-assisted hub contribution.

## Agents

| Agent | Description |
|-------|-------------|
| [guard-hub](.claude/agents/guard-hub.md) | Taxonomy, policies, and mappings specialist |
| [hub-contributor](.claude/agents/hub-contributor.md) | Guides contributors through creating hub artifacts |

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| [contributor-onboard](.claude/skills/contributor-onboard.md) | `/contributor-onboard` | Interactive setup guide for new contributors |
| [hub-contribution-check](.claude/skills/hub-contribution-check.md) | `/hub-contribution-check` | Pre-flight validation before pushing |
| [guard-policy-create](.claude/skills/guard-policy-create.md) | `/guard-policy-create` | Scaffold a .guard.md policy |
| [guard-agent-create](.claude/skills/guard-agent-create.md) | `/guard-agent-create` | Scaffold an .agent.md agent |
| [guard-skill-create](.claude/skills/guard-skill-create.md) | `/guard-skill-create` | Scaffold a .skill.md skill |
| [guard-soul-create](.claude/skills/guard-soul-create.md) | `/guard-soul-create` | Scaffold a .soul.md soul |
| [guard-mapping-create](.claude/skills/guard-mapping-create.md) | `/guard-mapping-create` | Scaffold a .mapping.yaml mapping |
| [guard-scan-taxonomy](.claude/skills/guard-scan-taxonomy.md) | `/guard-scan-taxonomy` | Validate taxonomy consistency |
| [guard-verify](.claude/skills/guard-verify.md) | `/guard-verify` | Verify hub structure and quality |
| [review-hub-pr](.claude/skills/review-hub-pr.md) | `/review-hub-pr` | Review a hub PR (taxonomy, body, cross-refs) |

## Quick Start

```
# In Claude Code, type:
/contributor-onboard

# To create a new policy:
/guard-policy-create

# Before pushing:
/hub-contribution-check
```
