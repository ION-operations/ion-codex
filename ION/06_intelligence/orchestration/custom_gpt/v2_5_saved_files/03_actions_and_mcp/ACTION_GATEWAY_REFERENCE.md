# ION Action Gateway Reference

## Purpose

The ION Action Gateway is the Custom GPT Action surface for bounded reads,
validation, queue/status inspection, receipts, and approval-gated action submit.

It is not a password login endpoint and not a raw local shell.

## Base URL

```text
https://ion-actions.helixion.net
```

## Privacy Policy URL

```text
https://helixion.net/privacy
```

## Auth

Protected routes require Action auth configured in the GPT Builder. User
passwords, API keys, and local secrets must not be pasted into chat.

## Main Endpoints

```text
GET  /health
GET  /policy
GET  /context-pack
GET  /codex/queue
GET  /agent/status
GET  /receipts/recent
POST /actions/validate
POST /actions/submit
```

## GPT Use

Use Gateway reads to check policy, context, Codex queue, agent status, and
receipts. Use `/actions/validate` before any submit. Use `/actions/submit` only
when the request is approved and the required idempotency/approval evidence
exists.

## Refusal Classes To Respect

If the Gateway returns auth, schema, idempotency, policy, approval, hard-gate,
owner, Steward-gate, production, or live-authority refusal, treat that refusal
as law for the current turn. Do not route around it in chat.

## Non-Claims

Gateway health means the surface is reachable. It does not prove production
readiness, live execution authority, or accepted state.
