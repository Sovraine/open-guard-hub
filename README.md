# OpenGuard Hub

Community registry of governance artifacts for AI agent actions.

The OpenGuard Hub provides a **shared taxonomy** of action verbs, **security policies**, **agent definitions**, and **MCP server mappings** that any AI agent framework can use to enforce governance at runtime.

## What's Inside

| Directory | Content | Count |
|-----------|---------|-------|
| `core/` | Cross-sector verb definitions | 9 domains |
| `sectors/` | Industry-specific verbs | 18 sectors |
| `policies/` | Governance policies (`.guard.md`) | 56 |
| `mappings/` | MCP server action mappings (`.mapping.yaml`) | 102 |
| `agents/` | Agent definitions (`.agent.md`) | 16 |
| `souls/` | Agent personas (`.soul.md`) | 16 |
| `skills/` | Atomic capabilities (`.skill.md`) | 7 |
| `gates/` | Kubernetes admission policies | 13 |
| `spec/` | OGS format specification | 7 docs |

## Quick Start

```bash
# 1. Clone the hub
git clone https://github.com/Sovraine/openguard-hub.git
cd openguard-hub

# 2. Download the sg binary (macOS ARM64)
curl -sL https://github.com/Sovraine/open-guard-cli/releases/latest/download/sg-darwin-arm64 -o sg
chmod +x sg

# 3. Validate the hub
./sg guard scan .
```

## 18 Industry Sectors

| Sector | Status | | Sector | Status |
|--------|--------|-|--------|--------|
| financial-services | STABLE | | retail-ecommerce | BETA |
| healthcare | STABLE | | logistics | BETA |
| legal | STABLE | | energy-utilities | BETA |
| human-resources | STABLE | | telecom | BETA |
| professional-services | STABLE | | manufacturing | BETA |
| saas-tech | STABLE | | real-estate | BETA |
| cybersecurity | BETA | | automotive | BETA |
| public-sector | BETA | | media-entertainment | BETA |
| education | BETA | | hospitality | BETA |

## OGS Specification

The [OpenGuard Specification](spec/) defines the file formats:

- [GuardFile](spec/guardfile.md) — `.guard.md` policy format
- [Agent](spec/agent.md) — `.agent.md` agent definition
- [Soul](spec/soul.md) — `.soul.md` persona/system prompt
- [Skill](spec/skill.md) — `.skill.md` capability definition
- [Mapping](spec/mapping.md) — `.mapping.yaml` MCP tool translation
- [Taxonomy](spec/taxonomy.md) — `_verbs.yaml` / `_sector.yaml` format

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

**Using Claude Code?** Type `/contributor-onboard` for an interactive guide, or `/guard-policy-create` to scaffold a new policy. See [AGENTS.md](AGENTS.md) for all available AI-assisted skills.

## License

Hub content is licensed under [CC-BY-SA-4.0](LICENSE).
OGS specification is licensed under [CC-BY-4.0](spec/README.md).

---

Built by [Sovraine](https://sovraine.com) — AI agent safety governance.
