---
name: escalate-infra-deploy
version: "1.0.0"
domain: core/common
description: Escalate deployments, destructive ops, and SQL execution on cloud infrastructure MCP servers
schema_version: 1
match:
  servers: ["netlify", "vercel", "cloudflare", "supabase", "salesforce", "circleci"]
  actions: ["create", "update", "execute", "delete", "_detect"]
  min_risk: HIGH
verdict: ESCALATE_HUMAN
severity: HIGH
priority: 85
author: sovraine
license: CC-BY-SA-4.0
tags: [infra, deploy, cloud, ci-cd, safety]
signature: null
certified: false
---

## What it does

Requires human approval before deploying, executing pipelines, deleting resources, or running SQL on cloud infrastructure platforms.

## Why it exists

Cloud infrastructure actions affect live production systems. Deploying to Netlify/Vercel pushes code to the internet. Deleting Cloudflare KV namespaces, D1 databases, or R2 buckets destroys stored data. Executing SQL via Supabase or Cloudflare D1 can modify or delete production data. Running CI/CD pipelines triggers build and deploy chains. Purchasing a domain (Vercel) is an irreversible financial commitment.

## What gets blocked

- `create`, `update`, `execute`, `delete`, `_detect` actions on Netlify, Vercel, Cloudflare, Supabase, Salesforce, and CircleCI servers with risk >= HIGH
- Site deployments, database deletions, SQL execution, and CI/CD pipeline runs
- Domain purchases on Vercel (CRITICAL, irreversible)

## Servers covered

- **Netlify** — `deploy_site`, `deploy_site_remotely`, `manage_env_vars`, `update_visitor_access_controls`
- **Vercel** — `deploy_to_vercel`, `buy_domain` (CRITICAL)
- **Cloudflare** — `kv_namespace_delete`, `d1_database_query`, `d1_database_delete`, `r2_bucket_delete`, `hyperdrive_config_delete`
- **Supabase** — `create_project`, `pause_project`, `delete_branch`, `merge_branch`, `reset_branch`, `apply_migration`, `execute_sql`, `deploy_edge_function`
- **Salesforce** — `create_scratch_org`, `delete_org`, `deploy_metadata`, `assign_permission_set`
- **CircleCI** — `run_pipeline`, `run_rollback_pipeline` (CRITICAL), `rerun_workflow`

## What is still allowed

- All `read` and `list` actions (viewing projects, deployments, logs, domains)
- `search` actions (searching documentation)
- `update` on non-destructive resources (project names, form settings)

## How to override

A human operator must confirm the action with: target resource, environment, and acknowledgment of production impact. The confirmation is recorded in the audit log.
