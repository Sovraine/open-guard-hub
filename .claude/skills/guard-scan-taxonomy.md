---
name: guard-scan-taxonomy
description: Validate the consistency of the Guard Hub taxonomy. Use to check duplicates, orphans, naming conventions, risk levels, overrides, CRITICAL coverage, inheritance, cross-cutting. Knows the 18 sectors, ~66 sub-sectors, the _verbs.yaml and _sector.yaml format.
---

# Guard Scan Taxonomy

## Hub Structure

```
.
├── core/                          # Technical, cross-sector
│   ├── common/_verbs.yaml         # ~28 universal CRUD verbs
│   ├── data-privacy/_verbs.yaml   # 16 verbs, auto-inherited by ALL
│   ├── audit-control/_verbs.yaml  # 11 verbs, regulated sectors
│   ├── change-management/_verbs.yaml # 10 verbs, production envs
│   ├── kubernetes/_verbs.yaml     # ~20 verbs
│   ├── database/_verbs.yaml       # ~18 verbs
│   ├── cloud/_verbs.yaml          # ~16 verbs
│   ├── security/_verbs.yaml       # ~18 verbs
│   ├── ai-ml/_verbs.yaml          # ~17 verbs
│   └── .../
└── sectors/
    ├── financial-services/
    │   ├── _sector.yaml
    │   ├── banking/_verbs.yaml
    │   ├── insurance/_verbs.yaml
    │   └── .../
    └── (18 sectors total)
```

## _verbs.yaml Schema

```yaml
taxonomy_version: "2026.03.1"    # Date-based versioning
sub_sector: banking               # Sub-sector name
sector: financial-services         # Parent sector

verbs:
  transfer-funds:
    risk: HIGH                     # READ-ONLY | LOW | MEDIUM | HIGH | CRITICAL
    description: "Transfer money between accounts"
    reversible: false              # bool
    requires_approval: false       # bool (hint, not enforced)
    regulatory_reference: "PSD2"   # free string
    composed_of: []                # documentary, ignored by runtime
    deprecated: false              # if true, use: must be filled in
    use: null                      # canonical replacement verb
    examples:
      - "Agent transfers 500 EUR from account A to B"
    related:
      - transfer-funds-international
```

## _sector.yaml Schema

```yaml
name: financial-services
display_name: "Financial Services"
status: STABLE                     # STABLE | BETA
regulations:
  - DORA
  - MiFID_II
  - PSD2
  - Basel_III
  - AML_6AMLD
cross_cutting:
  - core/data-privacy              # auto-inherited
  - core/audit-control             # regulated sector
  - core/change-management         # production env
inherits:
  - core/common                    # always
overrides:
  delete: { risk: CRITICAL }       # override of core/common default risk
  export: { risk: CRITICAL }
  execute: { risk: CRITICAL }
  share: { risk: HIGH }
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
Rules:
1. kebab-case lowercase
2. Action verb first (NEVER a noun)
3. Max 4 segments
4. No redundant prefixes (not "do-transfer", just "transfer")
5. ONE canonical name per concept (NO aliases)
6. The MCP mapping is the ONLY translator
```

## Risk Levels — Criteria

| Level | Criteria | Examples |
|-------|----------|----------|
| READ-ONLY | No mutation, no side-effect | read, list, search, SELECT, EXPLAIN |
| LOW | Reversible mutation, limited scope, no sensitive data | tag, comment, schedule, VACUUM |
| MEDIUM | Reversible mutation but impacts a user/process | update, cancel, import |
| HIGH | Difficult to reverse OR sensitive data OR financial impact | delete, execute, transfer-funds |
| CRITICAL | Irreversible OR legal/criminal impact OR life-threatening risk | DROP, kyc-override, declare-death |

## Inheritance

```
core/data-privacy/        → ALL sectors (auto)
core/common/              → ALL sectors (auto)
core/audit-control/       → regulated sectors (declared in _sector.yaml cross_cutting)
core/change-management/   → production envs (declared in _sector.yaml cross_cutting)
sectors/X/                → sectors/X/sub-sector/ (auto)
sectors/X/sub-sector/     → can override parent risk level (explicit in _sector.yaml overrides)
```

## Reserved Verbs

| Verb | Meaning | Default verdict |
|------|---------|-----------------|
| `_unknown` | Action not matched in taxonomy | WARN |
| `_any` | Wildcard — matches any action | — |
| `_override` | Explicit bypass (admin) | ESCALATE_HUMAN |

These verbs MUST NOT appear in _verbs.yaml files.

## Validation Checks (sg guard scan --taxonomy .)

### 1. Naming (BLOCKING)
- [ ] All verbs are kebab-case lowercase
- [ ] All verbs start with an action verb
- [ ] Max 4 segments per verb
- [ ] No reserved verb (_unknown, _any, _override) in _verbs.yaml

### 2. Duplicates (BLOCKING)
- [ ] No identical verb in two sub-sectors of the same sector
- [ ] No sub-sector verb identical to a core/common verb (must be an explicit override)

### 3. Risk Coherence (WARNING)
- [ ] Verb marked `reversible: false` → risk >= HIGH
- [ ] Verb marked `requires_approval: true` → risk >= HIGH
- [ ] Risk override in _sector.yaml never goes below core risk without justification
- [ ] Verb `deprecated: true` has a filled `use` field

### 4. CRITICAL Coverage (WARNING)
- [ ] Each CRITICAL verb is covered by at least one .guard.md policy
- [ ] Each CRITICAL verb has `reversible: false` or a justification in description

### 5. Structure (BLOCKING)
- [ ] Each sector in sectors/ has a _sector.yaml
- [ ] Each sub-sector in _sector.yaml has a _verbs.yaml
- [ ] taxonomy_version present in each _verbs.yaml
- [ ] cross_cutting in _sector.yaml references existing core/ paths

### 6. Inheritance (WARNING)
- [ ] Overrides in _sector.yaml only target verbs that exist in core/common
- [ ] cross_cutting does not reference a sector (only core/)
- [ ] inherits contains at minimum core/common

## 18 Sectors

| # | Sector | Status | Regulations |
|---|--------|--------|-------------|
| 1 | financial-services | STABLE | DORA, MiFID II, PSD2, Basel III, AML/CFT |
| 2 | healthcare | STABLE | HIPAA, GDPR, MDR, GxP |
| 3 | legal | STABLE | Professional secrecy, GDPR |
| 4 | human-resources | STABLE | Labor law, GDPR |
| 5 | retail-ecommerce | BETA | PCI-DSS |
| 6 | logistics | BETA | Customs, transport safety |
| 7 | energy-utilities | BETA | NERC CIP, EU Energy |
| 8 | telecom | BETA | ePrivacy, BEREC |
| 9 | manufacturing | BETA | ISO 9001, REACH |
| 10 | real-estate | BETA | Property law |
| 11 | automotive | BETA | UNECE, ISO 26262 |
| 12 | public-sector | BETA | FOIA, classification |
| 13 | media-entertainment | BETA | Copyright, DMCA |
| 14 | education | BETA | FERPA, COPPA |
| 15 | hospitality | BETA | PCI-DSS, health safety |
| 16 | professional-services | STABLE | SOX, ISQM |
| 17 | saas-tech | STABLE | SOC2, GDPR, CCPA |
| 18 | cybersecurity | BETA | NIS2, ISO 27001 |
