<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Taxonomy Specification

The taxonomy defines the canonical vocabulary of action verbs organized by sector. Every verb referenced in policies, agents, or skills must exist in the taxonomy.

## Structure

```
core/                              # Technical, cross-sector
├── common/_verbs.yaml             # ~28 universal CRUD verbs
├── data-privacy/_verbs.yaml       # 16 verbs (auto-inherited by ALL sectors)
├── audit-control/_verbs.yaml      # 11 verbs (regulated sectors)
├── change-management/_verbs.yaml  # 10 verbs (production environments)
├── kubernetes/_verbs.yaml
├── database/_verbs.yaml
├── cloud/_verbs.yaml
├── security/_verbs.yaml
└── ai-ml/_verbs.yaml

sectors/
├── <sector>/
│   ├── _sector.yaml               # Sector metadata, overrides
│   ├── <sub-sector>/_verbs.yaml   # Sub-sector specific verbs
│   └── ...
└── (18 sectors)
```

## Verb File Schema (`_verbs.yaml`)

```yaml
taxonomy_version: "2026.03.1"       # Date-based versioning
sub_sector: banking                  # Sub-sector name
sector: financial-services           # Parent sector

verbs:
  transfer-funds:
    risk: HIGH                       # READ-ONLY | LOW | MEDIUM | HIGH | CRITICAL
    description: "Transfer money between accounts"
    reversible: false                # boolean
    requires_approval: false         # boolean (hint, not enforced)
    regulatory_reference: "PSD2"     # free string
    composed_of: []                  # documentary, ignored by runtime
    deprecated: false                # if true, `use` must be set
    use: null                        # canonical replacement verb
    examples:
      - "Agent transfers 500 EUR from account A to B"
    related:
      - transfer-funds-international
```

### Required Verb Fields

| Field | Type | Description |
|-------|------|-------------|
| `risk` | enum | `READ-ONLY`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `description` | string | What the verb does |

### Optional Verb Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `reversible` | boolean | `true` | Whether the action can be undone |
| `requires_approval` | boolean | `false` | Hint for governance (not enforced) |
| `regulatory_reference` | string | — | Relevant regulation |
| `composed_of` | list[string] | `[]` | Sub-actions (documentary) |
| `deprecated` | boolean | `false` | If true, `use` must point to replacement |
| `use` | string\|null | `null` | Canonical replacement verb |
| `examples` | list[string] | `[]` | Usage examples |
| `related` | list[string] | `[]` | Related verbs |

## Sector File Schema (`_sector.yaml`)

```yaml
name: financial-services
display_name: "Financial Services"
status: STABLE                       # STABLE | BETA
regulations:
  - DORA
  - MiFID_II
  - PSD2
cross_cutting:
  - core/data-privacy                # auto-inherited
  - core/audit-control               # regulated sector
  - core/change-management           # production env
inherits:
  - core/common                      # always required
overrides:
  delete: { risk: CRITICAL }         # override core/common default risk
  export: { risk: CRITICAL }
sub_sectors:
  - banking
  - insurance
  - asset-management
  - payments
  - crypto
```

## Naming Convention

```
Format: verb[-qualifier[-object]]
```

Rules:
1. **kebab-case lowercase** only
2. **Action verb first** (never a noun)
3. **Max 4 segments**
4. **No redundant prefixes** (not `do-transfer`, just `transfer`)
5. **ONE canonical name** per concept (no aliases)
6. The **MCP mapping is the only translator**

Correct: `transfer-funds`, `delete-namespace`, `override-clinical-alert`
Incorrect: `money-transfer` (noun-first), `do-transfer` (redundant), `send-money` (alias)

## Risk Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| `READ-ONLY` | No mutation, no side-effect | `read`, `list`, `search`, `SELECT` |
| `LOW` | Reversible mutation, limited scope | `tag`, `comment`, `schedule` |
| `MEDIUM` | Reversible but impacts a user/process | `update`, `cancel`, `import` |
| `HIGH` | Difficult to reverse OR sensitive data OR financial | `delete`, `execute`, `transfer-funds` |
| `CRITICAL` | Irreversible OR legal/criminal OR life-threatening | `DROP`, `kyc-override`, `declare-death` |

## Inheritance

```
core/data-privacy/        → ALL sectors (automatic)
core/common/              → ALL sectors (automatic)
core/audit-control/       → regulated sectors (declared in _sector.yaml cross_cutting)
core/change-management/   → production envs (declared in _sector.yaml cross_cutting)
sectors/X/                → sectors/X/sub-sector/ (automatic)
```

Sectors can override core verb risk levels via `overrides` in `_sector.yaml`. An override can only increase risk, not decrease it.

## Reserved Verbs

| Verb | Meaning | Default Verdict |
|------|---------|-----------------|
| `_unknown` | Action not matched in taxonomy | WARN |
| `_any` | Wildcard — matches any action | — |
| `_override` | Explicit admin bypass | ESCALATE_HUMAN |

These verbs **must not** appear in `_verbs.yaml` files.

## 18 Sectors

| Sector | Status | Regulations |
|--------|--------|-------------|
| financial-services | STABLE | DORA, MiFID II, PSD2, Basel III |
| healthcare | STABLE | HIPAA, GDPR, MDR, GxP |
| legal | STABLE | Professional secrecy, GDPR |
| human-resources | STABLE | Labor law, GDPR |
| professional-services | STABLE | SOX, ISQM |
| saas-tech | STABLE | SOC2, GDPR, CCPA |
| cybersecurity | BETA | NIS2, ISO 27001 |
| retail-ecommerce | BETA | PCI-DSS |
| logistics | BETA | Customs, transport safety |
| energy-utilities | BETA | NERC CIP, EU Energy |
| telecom | BETA | ePrivacy, BEREC |
| manufacturing | BETA | ISO 9001, REACH |
| real-estate | BETA | Property law |
| automotive | BETA | UNECE, ISO 26262 |
| public-sector | BETA | FOIA, classification |
| media-entertainment | BETA | Copyright, DMCA |
| education | BETA | FERPA, COPPA |
| hospitality | BETA | PCI-DSS, health safety |

## 3 Cross-Cutting Domains

| Domain | Verb Count | Inherited by |
|--------|-----------|-------------|
| data-privacy | 16 | ALL sectors |
| audit-control | 11 | Regulated sectors |
| change-management | 10 | Production environments |
