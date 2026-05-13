# ION Supabase Operating Runtime Setup

Status: candidate setup guide for repo-managed Supabase operating state.

This guide moves the manually bootstrapped `ion_ops` Supabase schema into
source-controlled migrations. The local repo remains the source of truth for
schema evolution. SQL Editor changes should be treated as emergency/manual
bootstrap only and then reconciled back into migrations.

## Current Manual Bootstrap State

The following state was created manually before this migration packet:

```text
schema: ion_ops
tables:
  ion_ops.automation_events
  ion_ops.carrier_mount_receipts
  ion_ops.service_health_snapshots
views:
  ion_ops.v_current_carrier_mounts
  ion_ops.v_latest_service_health
  ion_ops.v_recent_automation_events
  ion_ops.v_cockpit_overview
RLS: enabled on all three tables
seed rows: automation event, service health snapshots, carrier mount receipts
```

## Repo-managed Files

```text
supabase/migrations/001_initial_ion_ops.sql
supabase/migrations/002_dev_private_cockpit_read_policies.sql
supabase/migrations/003_ion_ops_authority_and_rpc.sql
supabase/migrations/004_ion_ops_api_grants.sql
supabase/migrations/005_ion_ops_cockpit_readmodel_fixes.sql
supabase/seed/001_ion_ops_bootstrap_seed.sql
supabase/tests/validate_initial_ion_ops_sql.py
ION/02_architecture/ION_SUPABASE_OPERATING_RUNTIME_PROTOCOL_V0_1.md
```

## Migration Layers

```text
001_initial_ion_ops.sql
  Base schema, tables, indexes, triggers, RLS enablement, service writer posture, views.

002_dev_private_cockpit_read_policies.sql
  Broad authenticated read policies for Braden's private cockpit only.
  Replace before public or multi-user deployment.

003_ion_ops_authority_and_rpc.sql
  Typed RPC operation layer for safe AI/runtime writes.
  Rejects accepted-state, production, and live-execution authority claims.

004_ion_ops_api_grants.sql
  API grant layer for backend-only local ION adapter writes through typed RPCs.
  Does not grant anon execute on write RPCs.

005_ion_ops_cockpit_readmodel_fixes.sql
  Cockpit readmodel repair layer. Ensures v_recent_automation_events exposes
  created_at for PostgREST ordering and gives v_cockpit_overview richer event
  identity/status fields for the first cockpit data source.
```

## Apply Order

Use the Supabase CLI when available:

```sh
supabase db push
```

For local-only review without a Supabase project connection:

```sh
python3 supabase/tests/validate_initial_ion_ops_sql.py
```

If the CLI is not configured yet, the migrations can be pasted into Supabase SQL
Editor in numeric order as a transitional measure, but files in
`supabase/migrations/` remain the canonical schema source.

## Development Seed

The seed file is intentionally separate:

```text
supabase/seed/001_ion_ops_bootstrap_seed.sql
```

Apply it only for development/bootstrap recreation. It is replay-safe through
`on conflict`, but its rows are not production truth and do not claim accepted
ION state.

## Secrets Boundary

Do not commit:

```text
.env
.env.local
service_role keys
JWT secrets
database passwords
Supabase access tokens
```

Local adapter code should read credentials from operator-managed environment
variables only. ChatGPT Action/MCP lanes must not receive or print Supabase
service credentials.

## RLS and RPC Posture

The base migration enables RLS on all base tables. Direct authenticated table
writes are not granted.

Current layered policy intent:

```text
anon: no explicit access
authenticated: private cockpit read via 002, authority-introspection RPC only
service_role: backend/operator adapter typed RPC writes via 003/004
```

The typed RPC functions in `003` are the safe AI/runtime write surface:

```text
ion_ops.record_automation_event
ion_ops.record_service_health_snapshot
ion_ops.record_carrier_mount_receipt
ion_ops.ion_ops_rpc_authority
```

Those RPCs reject:

```text
accepted_state_claim: true
accepted_state_authority: true
production_authority: true
live_execution_authority: true
```

Material writes should go through a local ION adapter or approved backend lane,
not direct browser table writes.

## Cockpit Readmodels

The first cockpit read surface is Supabase-backed but remains an operational
mirror. It should never be treated as accepted ION state.

Primary views:

```text
ion_ops.v_current_carrier_mounts
ion_ops.v_latest_service_health
ion_ops.v_recent_automation_events
ion_ops.v_cockpit_overview
```

`005_ion_ops_cockpit_readmodel_fixes.sql` ensures recent events expose:

```text
occurred_at
created_at
event_id
event_type
severity
carrier_id
agent_tag
branch_id
packet_id
title
summary
accepted_state_claim
settlement_required
```

Cockpit clients may order recent automation events by:

```text
created_at desc, occurred_at desc
```

## First Adapter Targets

The first repo-managed adapter should write through RPCs:

```text
service_health_snapshots from local service probes
carrier_mount_receipts from mount receipt helper output
automation_events from receipts, queue events, and settlement status
```

The adapter must preserve ION posture:

```text
production_authority: false unless explicitly granted by future protocol
accepted_state_claim: false unless settlement grants it through a future migration
direct ChatGPT DB mutation: false
```

## Operator Notes

Before applying to a real Supabase project, confirm whether the current manual
schema should be replaced, diffed, or treated as already equivalent. If manual
tables contain rows worth preserving, export them before destructive resets.
