# dAimon Companion Agent Lane UI 001 State

Status: candidate implementation.

The browser extension companion now has a minimal bounded-agent lane surface in the Agent panel:

- Bounded Lane -> `GET /agent/status` through the Action Gateway.
- Relays -> `GET /agent/relay/pending` through the Action Gateway.
- Receipts -> `GET /agent/receipts/recent?limit=12` through the Action Gateway.

The background worker also defines approval-gated message handlers for:

- `POST /agent/invoke`
- `POST /agent/relay/respond`
- `POST /agent/control`

This is a data/control contract only. It does not grant production authority, unrestricted live execution, credentials, broad shell, destructive deletion, push_main, or unsafe browser control.
