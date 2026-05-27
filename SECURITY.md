# Security Policy

## Scope

OpenGuard Hub is a **content-only** repository containing governance policies (`.guard.md`), agent definitions (`.agent.md`), soul personas (`.soul.md`), skills (`.skill.md`), and MCP server mappings (`.mapping.yaml`). There is no executable code.

However, this content is downloaded and enforced at runtime by the Sovraine Guard daemon on user machines. **A malicious policy or mapping is a supply-chain attack.** We treat content integrity with the same severity as code integrity.

Security-relevant issues include:

- Policy injection that bypasses governance (e.g., broad ALLOW rules, priority escalation)
- Soul prompt injection that corrupts LLM-based governance debates
- Mapping manipulation that downgrades risk levels for dangerous operations
- CI/workflow compromise that allows malicious content to merge
- Symlink, binary, or Unicode attacks that evade review

## Supported versions

| Branch | Supported |
|--------|-----------|
| `main` | Yes |
| All other branches | No |

Only the `main` branch is consumed by production systems.

## Reporting a vulnerability

**Do not open a public issue for security vulnerabilities.**

Use [GitHub's private vulnerability reporting](https://github.com/Sovraine/open-guard-hub/security/advisories/new) to submit a report. This ensures the issue stays private until a fix is ready.

When reporting, please include:

1. Which file(s) are affected
2. The type of issue (content injection, CI bypass, supply-chain risk)
3. Steps to reproduce or a proof of concept
4. Potential impact on downstream consumers

## Response timeline

- **Acknowledgment**: within 48 hours
- **Triage and severity assessment**: within 7 days
- **Fix for CRITICAL/HIGH**: within 14 days
- **Coordinated disclosure**: 90 days from report

## Trust model

All community contributions are **untrusted by default**:

- `certified: false` and `signature: null` are enforced by CI
- `author: community` is required for external contributions
- Priority is capped at 500 (Sovraine-signed policies use 501-999)
- Content is scanned by 105+ automated checks before merge
- Human review is required for all pull requests

Sovraine-signed content uses cryptographic signatures verified by the runtime daemon. Community content operates at lower priority and cannot override signed policies.

## Recognition

We credit security researchers who responsibly disclose vulnerabilities, unless they prefer to remain anonymous. Reporters will be acknowledged in the fix commit and release notes.
