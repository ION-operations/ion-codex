# Connection Surface Manifest v2.6.7

status: candidate_connector_surface_manifest
revision: v2_6_7_daimon_codex_capsule_queue_relay

## Purpose

Document the proven local connection surfaces for the ChatGPT -> ION MCP ->
Codex Capsule -> Codex queue -> proof-return loop.

## Surfaces

| Surface | Type | Direction | Primary use | Guardrails |
| --- | --- | --- | --- | --- |
| `ion_codex_capsule_chat_status` | MCP tool | GPT -> Capsule | Read lane state and recent turn posture | Read-only; no state acceptance claim |
| `ion_codex_capsule_message_send` | MCP tool | GPT -> Capsule | Send bounded operator/GPT message into Capsule lane | Message packet only; not accepted state |
| `ion_codex_capsule_message_poll` | MCP tool | GPT <- Capsule | Poll Capsule response/progress without queue mutation | Read-only polling |
| `ion_codex_capsule_sync_to_queue` | MCP tool | Capsule -> Queue | Create bounded queue packet from Capsule message when requested | Requires explicit objective; candidate packet only |
| `ion_codex_work_queue` | MCP tool | GPT -> Queue | Read queue entries/status | Read-only queue inspection |
| `ion_codex_queue_process_once` | MCP tool | GPT -> Queue runner | Execute one bounded queue cycle | Bounded one-shot; no blanket live authority |
| `ion_codex_runner_reconcile` | MCP tool | GPT -> Queue runner | Lawful stale-runner recovery and cleanup | Recovery only; no hidden mutation |
| `ion_codex_worker_live_status` | MCP tool | GPT -> Worker telemetry | Live bounded worker telemetry for active/last run | Telemetry is observation, not acceptance |
| `ion_daemon_status` | MCP tool | GPT -> Runtime | Daemon/runtime status sanity check | Status only |
| `/cockpit/worker` | HTTP view | User/GPT visible | Human-readable worker panel | Derived telemetry; non-authoritative alone |
| `/cockpit/worker/model.json` | HTTP view | User/GPT visible | Machine-readable worker telemetry projection | Projection only; confirm with receipts |

## Proof Gate Rule

Raw Codex output is candidate work only. It is not accepted state until
context proof and template action proof gates are satisfied and a return path
records acceptance/receipt.

## Non-Claims

- Surface availability does not equal production authority.
- Telemetry visibility does not equal state acceptance.
- Queue execution does not bypass proof-gated task return workflow.
