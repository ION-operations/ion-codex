# ION Supabase Operating Runtime Protocol v0.1

Status: candidate architecture protocol.

## Purpose

The Supabase operating runtime is a typed read/query/status plane for ION
cockpit, GPT-001, Sev/ION PRO, future agents, and local automation adapters. It
is not the accepted-state authority and it is not the local working tree.

## Source Truth

```text
local repo + Git history: schema/source truth
ION receipts + settlement: accepted-state decision lane
Supabase: indexed operational visibility and typed runtime operation layer
Google Drive: package/drop mirror only
ChatGPT/GPT Actions: bounded carrier interface, not DB owner
```

## Managed Schema

The initial schema is `ion_ops`.

Tables:

```text
ion_ops.automation_events
ion_ops.carrier_mount_receipts
ion_ops.service_health_snapshots
```

Views:

```text
ion_ops.v_current_carrier_mounts
ion_ops.v_latest_service_health
ion_ops.v_recent_automation_events
ion_ops.v_cockpit_overview
```

Typed RPC:

```text
ion_ops.ion_ops_rpc_authority
ion_ops.ion_ops_record_automation_event
ion_ops.ion_ops_record_service_health_snapshot
ion_ops.ion_ops_record_carrier_mount_receipt
```

## Authority Model

Supabase rows are evidence and operating telemetry.

They may show:

```text
service health
carrier mount state
automation events
queue/receipt summaries
cockpit overview state
```

They must not claim:

```text
production deployment
accepted state
secret authority
unrestricted action authority
direct ChatGPT mutation authority
```

## RLS Layers

```text
001_initial_ion_ops.sql
  Enables RLS and keeps base schema private by default.

002_dev_private_cockpit_read_policies.sql
  Adds broad authenticated read for Braden's private cockpit.
  This is not a public/multi-user policy.

003_ion_ops_authority_and_rpc.sql
  Adds typed RPC operations with authority guards.
```

## Typed Operation Rules

AI/runtime writes must use typed operations rather than direct table mutation.

The current RPC authority defaults are:

```text
production_authority: false
live_execution_authority: false
accepted_state_authority: false
accepted_state_claim_default: false
direct_table_write_for_authenticated: false
chatgpt_direct_db_mutation: false
```

RPCs must reject payloads that attempt:

```text
accepted_state_claim: true
accepted_state_authority: true
production_authority: true
live_execution_authority: true
```

## Adapter Plan

Implement a local adapter in a later packet.

Adapter responsibilities:

```text
1. Read local ION receipts/state.
2. Normalize rows for ion_ops tables.
3. Upsert through typed RPCs with idempotency keys.
4. Record local write receipts.
5. Refuse writes without explicit Supabase destination configuration.
6. Redact secrets before transport.
7. Report sync status back to ION cockpit.
```

Recommended adapter file:

```text
ION/04_packages/kernel/ion_supabase_operating_runtime.py
```

Recommended commands:

```text
ion_supabase_push_service_health
ion_supabase_push_carrier_mount
ion_supabase_push_automation_event
ion_supabase_sync_status
```

## Write Boundaries

Allowed future writer:

```text
local ION adapter with operator-managed Supabase credentials
```

Allowed AI lane:

```text
typed RPC calls only, under explicit authority guard and receipts
```

Not allowed:

```text
ChatGPT live Action direct DB table mutation
browser extension direct service_role access
committed .env.local
printed service_role key
automatic accepted-state promotion from Supabase rows
```

## Row Identity

Every write should carry one stable id:

```text
automation_events.event_id
carrier_mount_receipts.receipt_id
service_health_snapshots.snapshot_id
```

Where retries are possible, use:

```text
idempotency_key
correlation_id
packet_id
context_instance_id
branch_id
```

## Cockpit Use

Cockpit should read from views first:

```text
v_cockpit_overview
v_latest_service_health
v_current_carrier_mounts
v_recent_automation_events
```

If Supabase is unavailable, cockpit must degrade to local receipt/state view
instead of failing the local app.

## Non-claims

This protocol does not deploy production, expose secrets, re-enable direct
ChatGPT DB mutation, or make Supabase an accepted-state authority.
