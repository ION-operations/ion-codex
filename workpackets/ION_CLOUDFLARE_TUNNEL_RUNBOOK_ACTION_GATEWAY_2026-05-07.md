# ION Cloudflare Tunnel Runbook — Custom GPT Action Gateway

created_at: 2026-05-07
status: candidate_runbook_not_ion_state
production_authority: false
live_execution_authority: false

## Target

Expose only the ION Custom GPT Action Gateway to the public internet for GPT Actions.

Target mapping:

```text
https://ion-actions.<approved-domain>
→ http://127.0.0.1:8777
```

Do not expose:

```text
http://127.0.0.1:8767  # existing ChatOps daemon
raw Codex CLI
raw shell
database/filesystem paths
development server with broad endpoints
```

## Local services

Terminal 1 — existing ChatOps daemon:

```bash
cd "<ION shell root>"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatops_bridge \
  --ion-root . --host 127.0.0.1 --port 8767 --serve
```

Terminal 2 — new Action Gateway:

```bash
cd "<ION shell root>"
export ION_ACTION_GATEWAY_TOKEN="<operator-generated-secret>"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_custom_gpt_action_gateway \
  --ion-root . --host 127.0.0.1 --port 8777 --serve
```

## Cloudflare route

Create or update a published application route:

```text
Public hostname: ion-actions.<approved-domain>
Service URL: http://127.0.0.1:8777
```

## Minimal external smoke

Unauthenticated health:

```bash
curl -s https://ion-actions.<approved-domain>/health | jq .
```

Protected read must fail without token:

```bash
curl -i https://ion-actions.<approved-domain>/policy
```

Protected read must succeed with token:

```bash
curl -s -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" \
  https://ion-actions.<approved-domain>/policy | jq .
```

Dry-run validation:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  --data @sample_validate_register_artifact.json \
  https://ion-actions.<approved-domain>/actions/validate | jq .
```

Submit without approval evidence must refuse:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  --data @sample_validate_register_artifact.json \
  https://ion-actions.<approved-domain>/actions/submit | jq .
```

## Hardening checklist

```text
- token generated outside repo
- no token committed
- Cloudflare hostname points to 8777, not 8767
- WAF/rate limiting enabled for POST paths if available
- logs checked for token redaction
- receipts checked for auth redaction
- submit refuses missing idempotency
- submit refuses hard-gated intents
- submit refuses production_authority=true
- submit refuses live_execution_authority=true
```

## GPT Builder installation

```text
1. GPT editor → Actions → Create new action.
2. Paste OpenAPI schema from ION/09_integrations/custom_gpt_action_gateway/openapi.yaml.
3. Configure Bearer/API-key auth using ION_ACTION_GATEWAY_TOKEN.
4. Test ionGatewayHealth.
5. Test ionGatewayPolicy.
6. Test ionGatewayContextPack.
7. Test ionGatewayValidateAction with harmless register_artifact.
8. Do not test submit until local receipts are confirmed.
```

## Receipt target

Record tunnel and GPT Builder test receipts under:

```text
ION/05_context/current/action_gateway/receipts/
```
