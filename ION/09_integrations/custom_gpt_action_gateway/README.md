# ION Custom GPT Action Gateway

Status: draft non-production. Production authority and live execution authority
are false.

This Action is explicit-use only. It is not the default ION mount path. Do not
use it to boot the uploaded sandbox/package, answer from files, satisfy
`/guest-mode`, satisfy `/what is ION?`, or start first-time context. Use it only
when the user asks for live gateway/local hub status, queue/receipt reads,
validation, submit, or a connector-backed draft.

## Local Launch

```bash
export ION_ACTION_GATEWAY_TOKEN="<operator-generated-secret>"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_custom_gpt_action_gateway \
  --ion-root . --host 127.0.0.1 --port 8777 --serve
```

The existing ChatOps daemon may remain on `127.0.0.1:8767`. Do not expose the
raw daemon publicly.

## Cloudflare Route

```text
https://ion-actions.helixion.net -> http://127.0.0.1:8777
```

## Auth

Protected routes require:

```text
Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN
```

The gateway also supports `ION_ACTION_GATEWAY_TOKEN_SHA256` so the raw token can
remain outside repo state.

## Endpoints

```text
GET  /health
GET  /openapi.yaml
GET  /policy
GET  /context-pack
GET  /codex/queue
GET  /agent/status
GET  /projects/daimon/visibility
GET  /receipts/recent
POST /actions/validate
POST /actions/submit
```

`/projects/daimon/visibility` gives a Custom GPT read-only visibility into the
dAimon project through curated receipt artifacts only. It exposes proof status,
known connector surfaces, Cloud Run/Agent Engine/MongoDB names, artifact
inventory, and current blockers. It does not expose `.env`, secrets, tokens,
MongoDB URIs, raw service account JSON, or mutation authority.

`/actions/submit` requires a mutating idempotency key and Braden approval
evidence before routing to the existing ChatOps owner.

## Refusals

The gateway returns structured refusal classes including auth failure,
idempotency failure, hard-gated intent, production/live authority refusal,
approval failure, schema failure, owner refusal, and Steward gate required.

## Custom GPT Setup

1. Add `openapi.yaml` as the Custom GPT Action schema, or import it from
   `https://ion-actions.helixion.net/openapi.yaml`.
2. Configure bearer/API-key auth with the gateway token.
3. Test health, policy, context pack, queue reads, and dAimon visibility during
   explicit connector setup or diagnostics only.
4. Use validate before submit.
5. Submit only after explicit Braden approval evidence is present.
