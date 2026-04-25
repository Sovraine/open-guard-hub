# Guard Hub Style Guide

## Verb Naming

Format: `verb[-qualifier[-object]]`

Rules:
1. kebab-case lowercase
2. Action verb first (never a noun)
3. Maximum 4 segments
4. No redundant prefixes
5. ONE canonical name per concept (no aliases)
6. Qualifier adds context when verb alone is ambiguous

Good: `transfer-funds`, `delete-tenant-data`, `approve-loan`
Bad: `funds-transfer`, `deleteTenantData`, `loan-approval`

## Risk Levels

| Level | Criteria |
|-------|----------|
| READ-ONLY | No mutation, no side-effect |
| LOW | Reversible mutation, limited scope, no sensitive data |
| MEDIUM | Reversible mutation but impacts a user/process |
| HIGH | Hard to reverse OR sensitive data OR financial impact |
| CRITICAL | Irreversible OR legal/criminal impact OR life risk OR security bypass |

## _verbs.yaml Format

Required fields per verb: `risk`, `description`
Optional: `reversible`, `regulatory_reference`, `requires_approval`, `examples`, `related`, `composed_of`

## _sector.yaml Format

Required: `name`, `display_name`, `status`, `inherits`, `sub_sectors`
Optional: `regulations`, `cross_cutting`, `overrides`
