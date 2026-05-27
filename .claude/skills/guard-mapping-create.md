---
name: guard-mapping-create
description: Create an MCP mapping (.mapping.yaml) to translate MCP server tools into canonical Guard verbs. The mapping is the ONLY translator — no aliases in the taxonomy. Use to scaffold, write and validate mappings.
---

# Guard Mapping Create

## Principle

The MCP mapping is the **only translator** between MCP tool names and the canonical verbs of the Guard taxonomy. There are NO aliases in the taxonomy.

```
MCP tool "send_money"  →  Mapping  →  transfer-funds  →  Policy evaluated
MCP tool "wire"        →  Mapping  →  transfer-funds  →  Policy evaluated
MCP tool "query"       →  Mapping  →  SELECT/INSERT/UPDATE/DELETE (parse SQL)
```

## Location

```
mappings/<server-name>.mapping.yaml
```

## Schema .mapping.yaml

```yaml
# mappings/postgresql.mapping.yaml
mcp_server:
  name: mcp-postgresql
  version: ">=1.0"
  repository: "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres"
  transport: stdio                   # stdio | sse | streamable-http

mappings:
  - tool: query
    description: "Execute SQL query"
    action_from: params.sql          # Dynamic parsing from param
    target_from: params.sql          # Dynamic parsing from param
    parser: sql                      # Specialized parser (sql, json, params)
    risk_default: HIGH               # If the parser fails
    examples:
      - input: { sql: "SELECT * FROM users" }
        action: SELECT
        target: users
        risk: READ-ONLY
      - input: { sql: "DROP TABLE users" }
        action: DROP
        target: users
        risk: CRITICAL

  - tool: list_tables
    action: list
    target: tables
    risk: READ-ONLY
    description: "List all database tables"
```

## Specialized Parsers

| Parser | When | What it does |
|--------|------|--------------|
| `sql` | Database tools (query, execute) | Parses SQL → extracts verb (SELECT/INSERT/UPDATE/DELETE/DROP) + table |
| `params` | Default | Extracts action + target from MCP parameters |
| `json` | API tools | Parses JSON body → extracts the operation |

## Static vs Dynamic Mapping

| Type | When | Fields |
|------|------|--------|
| **Static** | 1 tool = 1 fixed action | `action: "scale"`, `target_from: "params.deployment"` |
| **Dynamic** | 1 tool = N possible actions | `action_from: "params.sql"`, `parser: "sql"` |

## Scaffold

```bash
sg guard init-mapping mcp-postgresql

# Generates:
# mappings/postgresql.mapping.yaml
# with all discovered tools, action/target set to "TODO"
```

## Validation

```bash
sg guard scan .                          # Always scan from repo root (subdirectory scan produces false GUARD-070)
```

### Checks

- [ ] Each mapped `action` exists in the taxonomy (canonical verb)
- [ ] Each `risk` is >= the taxonomy risk for that verb
- [ ] `parser` is a known parser (sql, params, json)
- [ ] `target_from` references an existing param of the MCP tool
- [ ] No MCP server tool without a mapping (100% coverage)
- [ ] `mcp_server.name` is unique in the Hub

## Trust Levels

| Level | Who did it | Guarantee |
|-------|-----------|-----------|
| **Community** | Contributor | None. Best-effort. CC-BY-SA. |
| **Validated** (Pro) | Sovraine review | Mapping correct, risk levels valid |
| **Certified** (Business+) | Sovraine audit | + MCP server audited, Guard server-side, Ed25519 signed |

## When an MCP Tool Has No Mapping

The unmapped action → verb `_unknown` → verdict WARN (by default) or DENY (if configured fail-closed).
