# ION Custom GPT Action Gateway Protocol

created_at: 2026-05-07
status: DRAFT_NON_PRODUCTION
production_authority: false
live_execution_authority: false

## Purpose

The ION Custom GPT Action Gateway is a public-facing local API membrane for
Custom GPT Actions. It exists to receive bounded HTTPS action calls, validate
them, and route them into existing ION ChatOps, Codex queue, proof, receipt, and
Steward-facing owners.

The gateway is transport, not authority.

## Boundary

Cloudflare Tunnel may expose only the gateway service, not the raw ChatOps
daemon, raw Codex CLI, shell commands, local filesystems, credentials, git push,
or production deployment surfaces.

The intended mapping is:

```text
Custom GPT Action
-> public HTTPS tunnel
-> local ION Action Gateway on 127.0.0.1:8777
-> existing ION ChatOps / queue / proof / receipt owners
```

## Authority

The gateway always carries:

```text
production_authority: false
live_execution_authority: false
```

Custom GPT Action approval is not Steward integration. Cloudflare
authentication is not ION authority. A gateway receipt is evidence of ingress
and routing, not canon acceptance.

## Mutation Rule

Mutations must route through existing ION owners:

```text
validate -> existing ChatOps action validation
submit -> existing ChatOps submit path
Codex work -> existing ChatGPT connector Codex queue owner
Codex output -> proposal until proof-gated
```

Codex output remains proposal until the existing context proof and template
action gates accept it and Steward integration reviews it.

## Refusals

The gateway must refuse missing or invalid auth, missing idempotency keys,
replayed idempotency keys, oversized payloads, unsupported endpoints, hard-gated
intents, production authority, live execution authority, missing operator
approval evidence, invalid approval evidence, and owner refusals.

## Non-Goals

The gateway does not create a new queue, a new agent system, a shell endpoint, a
credential store, a production deploy lane, or a replacement for Steward
integration.
