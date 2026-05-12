# Bounded Agent Invocation Relay V1 State

Status: candidate implementation packet.

The Action Gateway exposes a bounded agent lane for ChatGPT Browser / ION:

- `POST /agent/invoke`
- `GET /agent/status`
- `GET /agent/relay/pending`
- `POST /agent/relay/respond`
- `POST /agent/control`
- `GET /agent/receipts/recent`
- `POST /agent/settle`

Authority remains bounded: no production authority, no unrestricted live execution, no credentials, no broad shell, no destructive deletion, no protected overwrite, no push_main, and no silent authority expansion.

Artifacts live under `ION/05_context/current/chatgpt_connector/agent_invocations/{invocation_id}/`.
