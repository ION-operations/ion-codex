# dAimon Companion Action Gateway Visibility Setup

Status: candidate setup receipt
Date: 2026-05-10

## Purpose

Give the dAimon Companion Custom GPT explicit, read-only visibility into the
local dAimon project without granting broad filesystem, secret, deployment, or
live execution authority.

## Action Route

- OpenAPI source: `ION/09_integrations/custom_gpt_action_gateway/openapi.yaml`
- Public gateway: `https://ion-actions.helixion.net`
- Operation: `ionGatewayDaimonVisibility`
- HTTP route: `GET /projects/daimon/visibility`
- Auth: existing Action Gateway bearer token configuration

## What The GPT Can See

- dAimon repo presence and curated receipt artifact inventory.
- Current dAimon claim/proof status from demo evidence receipts.
- Existing connector surfaces for the ION MCP connector and Action Gateway.
- Cloud Run URL/auth mode, Google project/location, Agent Engine resource and
  service account identity, and MongoDB database/collection names.
- Google user-access readiness blockers and recommended next actions.

## Explicit Non-Claims

- This does not expose `.env`, tokens, MongoDB URIs, passwords, or raw service
  account JSON.
- This does not grant production authority, live execution authority, deploy
  authority, accepted-state authority, or arbitrary local file access.
- Custom GPT visibility over dAimon receipts is not permission to mutate
  dAimon, Google Cloud, MongoDB, or local ION files.

## Builder Setup Note

Refresh or re-import the Action schema in the Custom GPT builder from
`ION/09_integrations/custom_gpt_action_gateway/openapi.yaml`, then test the
`ionGatewayDaimonVisibility` operation with the existing gateway bearer auth.
The operation should be used only when the operator asks for dAimon project
status, proof, connection visibility, or setup diagnostics.
