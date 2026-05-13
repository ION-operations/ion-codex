# ION Supabase Event Mirror

Status: candidate local adapter for `PCKT-ION-SUPABASE-EVENT-MIRROR-001`.

The Supabase event mirror sends selected local ION operational evidence to the
`ion_ops` Supabase schema through typed RPC functions only. Supabase is an
operational mirror, not source truth.

## Adapter

```text
ION/04_packages/kernel/ion_supabase_event_mirror.py
```

Supported RPCs:

```text
ion_ops.record_automation_event
ion_ops.record_service_health_snapshot
ion_ops.record_carrier_mount_receipt
```

The adapter does not perform direct table writes.

## Local environment

Load credentials outside Git:

```sh
cd "/home/sev/ION - Production/ION_CODEX FULL"
set -a
source .env.supabase.local
set +a
```

Required for non-dry-run calls:

```text
SUPABASE_URL
SUPABASE_KEY
SUPABASE_SCHEMA=ion_ops
```

`SUPABASE_KEY` should be a key appropriate for the RPC lane. Do not commit
`.env.supabase.local` and do not print keys in logs.

`SUPABASE_SCHEMA` defaults to `ion_ops`. The Supabase dashboard must expose the
`ion_ops` schema under Project Settings -> API -> Data API / Exposed schemas.
The adapter keeps clean RPC names and routes them through PostgREST schema
profile headers:

```text
Content-Profile: ion_ops
Accept-Profile: ion_ops
```

Do not move the functions to `public` to make RPC calls work. The intended
runtime boundary is the separate `ion_ops` schema plus RLS and typed RPCs.

## Dry-run example

```sh
PYTHONPATH=ION/04_packages python3 -m kernel.ion_supabase_event_mirror \
  --event-json /path/to/event.json \
  --dry-run \
  --json
```

Dry-run validates the payload and writes a local receipt without calling
Supabase.

## Input shapes

Automation event:

```json
{
  "kind": "automation_event",
  "event_type": "queue_status",
  "title": "Queue status mirrored",
  "summary": "Local ION queue state was mirrored as operational evidence.",
  "payload": {
    "accepted_state_claim": false
  }
}
```

Service health snapshot:

```json
{
  "kind": "service_health_snapshot",
  "service_name": "ION MCP preview",
  "status": "healthy",
  "host": "127.0.0.1",
  "port": 8765,
  "production_authority": false,
  "live_execution_authority": false
}
```

Carrier mount receipt:

```json
{
  "kind": "carrier_mount_receipt",
  "agent_tag": "codex_local_ion_mason",
  "carrier_type": "local_codex_cli",
  "context_instance_id": "ctx_example",
  "authority": {
    "production_authority": false,
    "live_execution_authority": false,
    "accepted_state_authority": false
  }
}
```

## Guardrails

The adapter rejects payloads containing:

```text
accepted_state_claim: true
accepted_state_authority: true
production_authority: true
live_execution_authority: true
```

Local receipts are written under:

```text
ION/05_context/current/supabase_event_mirror/receipts/
```

Those receipts are local evidence. They do not make Supabase accepted state.

## Non-claims

This adapter does not deploy production, reset the database, bypass RLS, commit
secrets, or make Supabase the source of truth.
