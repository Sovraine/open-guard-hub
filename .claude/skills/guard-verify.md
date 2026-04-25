---
name: guard-verify
description: Verify the structure and quality of the OpenGuard Hub. Use to validate taxonomy structure, scan grade, naming conventions, cross-references, and content consistency. Run after any hub modification.
---

# Guard Verify

## Required Checks

### 1. Hub structure

```bash
# Verify core directories exist
test -d core
test -d sectors
test -d policies
test -d mappings
test -d agents
test -d souls
test -d skills

# Verify core verb files
for domain in common data-privacy kubernetes database cloud security audit-control change-management ai-ml; do
  test -f "core/$domain/_verbs.yaml" || echo "MISSING: core/$domain/_verbs.yaml"
done

# Verify sector files
for sector in $(ls sectors/); do
  test -f "sectors/$sector/_sector.yaml" || echo "MISSING: sectors/$sector/_sector.yaml"
done
```

### 2. Guard scan — Grade A required

```bash
sg guard scan .
```

### 3. Taxonomy validation

```bash
sg guard scan --taxonomy .
```

### 4. No self-certification

```bash
grep -r "certified: true" . --include="*.md" --include="*.yaml" -l && echo "FAIL: self-certification found" || echo "OK"
grep -rP "signature:\s+(?!null)" . --include="*.md" --include="*.yaml" -l && echo "FAIL: non-null signature found" || echo "OK"
```

### 5. License consistency

```bash
grep -r "license:" . --include="*.md" --include="*.yaml" | grep -v "CC-BY-SA-4.0" | grep -v ".claude/" | grep -v "spec/" && echo "WARN: non-CC-BY-SA-4.0 license found" || echo "OK"
```

### 6. Cross-references

For each agent file, verify:
- Referenced soul exists
- Referenced policies exist
- Referenced skills exist
- No overlap between allowed_verbs and denied_verbs

### 7. Body sections

Verify required headers per type:
- Policy: 5 headers
- Agent: 5 headers
- Soul: 4 headers
- Skill: 5 headers

## Full Command

```bash
sg guard scan . && sg guard scan --taxonomy . && echo "ALL CHECKS PASSED"
```

## Pre-Commit Checklist

- [ ] `sg guard scan .`: Grade A
- [ ] `sg guard scan --taxonomy .`: 0 blocking errors
- [ ] No `certified: true` in community files
- [ ] No non-null `signature` in community files
- [ ] All cross-references resolve
- [ ] All required body headers present
