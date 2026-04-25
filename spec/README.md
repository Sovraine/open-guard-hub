<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# OpenGuard Specification (OGS)

The OpenGuard Specification defines the file formats used by the OpenGuard Hub to describe AI agent governance artifacts.

## Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| [GuardFile](guardfile.md) | `.guard.md` | Policy defining governance rules for agent actions |
| [Agent](agent.md) | `.agent.md` | Agent identity, capabilities, and governance constraints |
| [Soul](soul.md) | `.soul.md` | Agent persona and system prompt template |
| [Skill](skill.md) | `.skill.md` | Atomic capability with mapped verbs and side effects |
| [Mapping](mapping.md) | `.mapping.yaml` | Translation from MCP server tools to canonical verbs |
| [Taxonomy](taxonomy.md) | `_verbs.yaml` / `_sector.yaml` | Action verb definitions and sector organization |

## Design Principles

1. **YAML frontmatter + Markdown body** — machine-readable metadata with human-readable documentation
2. **Taxonomy-first** — every action references a canonical verb; the mapping is the only translator
3. **Fail-closed** — unknown actions default to WARN; HIGH/CRITICAL default to DENY without explicit policy
4. **No aliases** — one canonical name per concept; MCP mappings translate tool names to verbs
5. **Graduated trust** — community (unsigned) → validated (reviewed) → certified (audited + Ed25519 signed)

## License

This specification is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
