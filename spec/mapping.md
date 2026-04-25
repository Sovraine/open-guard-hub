<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Mapping Specification (`.mapping.yaml`)

A Mapping translates MCP server tool names into canonical Guard taxonomy verbs. The mapping is the **only translator** — there are no aliases in the taxonomy.

## Principle

```
MCP tool "send_money"  →  Mapping  →  transfer-funds  →  Policy evaluated
MCP tool "wire"        →  Mapping  →  transfer-funds  →  Policy evaluated
MCP tool "query"       →  Mapping  →  SELECT/INSERT/UPDATE/DELETE (parse SQL)
```

## Format

Pure YAML (no Markdown body).

## Schema

```yaml
mcp_server:
  name: mcp-server-name             # MCP server identifier
  version: ">=1.0"                   # Minimum version
  repository: "https://..."          # Source repository URL
  transport: stdio                   # stdio | sse | streamable-http

mappings:
  - tool: tool_name                  # MCP tool name
    action: verb                     # Static: canonical taxonomy verb
    # OR
    action_from: params.field        # Dynamic: parse action from param
    target_from: params.field        # Extract target from param
    parser: sql                      # Specialized parser (sql, json, params)
    risk: READ-ONLY                  # Risk level for static mappings
    risk_default: HIGH               # Default risk if parser fails
    description: "What this tool does"
    context_from:                    # Optional: additional context params
      type: resource_type
    examples:                        # For dynamic mappings
      - input: { sql: "SELECT * FROM users" }
        action: SELECT
        target: users
        risk: READ-ONLY
```

### Required Fields (per mapping entry)

| Field | Type | Description |
|-------|------|-------------|
| `tool` | string | MCP tool name |
| `action` or `action_from` | string | Static verb or dynamic extraction path |
| `risk` or `risk_default` | enum | Risk level |
| `description` | string | What the tool does |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `target_from` | string | Parameter path for target extraction |
| `parser` | string | `sql`, `json`, or `params` |
| `context_from` | object | Additional context parameters |
| `examples` | list | Input/output examples for dynamic mappings |

## Mapping Types

| Type | When | Fields |
|------|------|--------|
| **Static** | 1 tool = 1 fixed action | `action`, `risk` |
| **Dynamic** | 1 tool = N possible actions | `action_from`, `parser`, `risk_default` |

## Specialized Parsers

| Parser | When | What it does |
|--------|------|--------------|
| `sql` | Database tools | Parses SQL → extracts verb + table |
| `params` | Default | Extracts action + target from MCP parameters |
| `json` | API tools | Parses JSON body → extracts operation |

## Trust Levels

| Level | Who | Guarantee |
|-------|-----|-----------|
| **Community** | Contributor | Best-effort. CC-BY-SA. |
| **Validated** | Sovraine review | Mapping correct, risk levels valid |
| **Certified** | Sovraine audit | + MCP server audited, Ed25519 signed |

## Unmapped Tools

When an MCP tool has no mapping, the action resolves to verb `_unknown` → verdict WARN (default) or DENY (if configured fail-closed).

## Validation Rules

- Each mapped `action` must exist in the taxonomy
- Each `risk` must be >= the taxonomy risk for that verb
- `parser` must be a known parser
- `mcp_server.name` must be unique in the hub
- All tools should be mapped (100% coverage recommended)

## Example

```yaml
mcp_server:
  name: mcp-filesystem
  version: ">=1.0"
  transport: stdio

mappings:
  - tool: read_file
    action: read
    target_from: params.path
    risk: READ-ONLY
    description: "Read file contents"

  - tool: write_file
    action: update
    target_from: params.path
    risk: HIGH
    description: "Write to a file"

  - tool: delete_file
    action: delete
    target_from: params.path
    risk: HIGH
    description: "Delete a file"

  - tool: list_directory
    action: list
    target_from: params.path
    risk: READ-ONLY
    description: "List directory contents"
```
