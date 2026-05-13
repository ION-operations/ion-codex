# ION Action Gateway Supabase Actions

Status: candidate operating guide for `PCKT-ION-GPT001-ACTION-SUPABASE-COCKPIT-SETUP-001`.

GPT-001 should connect to the ION Action Gateway, not directly to Supabase.
Supabase secrets stay local to the gateway process.

## Action schema

Use:

```text
ION/07_templates/actions/ION_SUPABASE_ACTIONS_OPENAPI_V0_1.yaml
```

Server:

```text
https://ion-actions.helixion.net
```

Authentication:

```text
Bearer token for ION Action Gateway
```

Do not put Supabase URL, service keys, secret keys, database passwords, or JWT
secrets in Custom GPT Action settings.

## Local environment

The local Action Gateway process needs:

```text
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY or SUPABASE_SECRET_KEY
SUPABASE_SCHEMA=ion_ops
ION_ACTION_GATEWAY_TOKEN or ION_ACTION_GATEWAY_TOKEN_SHA256
```

The GPT only receives the Action Gateway token. The gateway uses local backend
environment to call Supabase.

## Read endpoints

```text
GET /supabase/cockpit/overview
GET /supabase/events/recent?limit=20
GET /supabase/service-health/latest
GET /supabase/carrier-mounts/current
```

Read endpoints use Supabase REST with:

```text
Accept-Profile: ion_ops
```

Responses are gateway envelopes with:

```text
ok
data
route
tool
production_authority: false
live_execution_authority: false
accepted_state_claim: false
```

## Write endpoints

```text
POST /supabase/events/record
POST /supabase/service-health/record
POST /supabase/carrier-mounts/record
```

Writes go through:

```text
ION/04_packages/kernel/ion_supabase_event_mirror.py
```

They call typed RPCs:

```text
ion_ops.record_automation_event
ion_ops.record_service_health_snapshot
ion_ops.record_carrier_mount_receipt
```

The gateway returns the local receipt path and remote row id when available.

## Rejections

The write lane rejects:

```text
accepted_state_claim=true
accepted_state_authority=true
production_authority=true
live_execution_authority=true
```

Supabase remains an operational mirror. It does not make accepted ION state.

## Local smoke

Health:

```sh
curl -fsS http://127.0.0.1:8777/health
```

Read recent events:

```sh
curl -fsS \
  -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" \
  "http://127.0.0.1:8777/supabase/events/recent?limit=5"
```

Record a safe smoke event:

```sh
curl -fsS \
  -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "action_gateway_supabase_event_record_smoke",
    "severity": "notice",
    "source_system": "ion_action_gateway",
    "agent_tag": "codex_local_ion_mason",
    "packet_id": "PCKT-ION-GPT001-ACTION-SUPABASE-COCKPIT-SETUP-001",
    "title": "Action Gateway Supabase write smoke",
    "accepted_state_claim": false,
    "settlement_required": true
  }' \
  http://127.0.0.1:8777/supabase/events/record
```

## Non-claims

This lane does not deploy production, expose Supabase secrets, connect GPT
Actions directly to Supabase, reset the database, start queue workers, or claim
accepted ION state.
