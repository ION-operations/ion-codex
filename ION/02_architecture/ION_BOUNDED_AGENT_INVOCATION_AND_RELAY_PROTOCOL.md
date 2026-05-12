# ION Bounded Agent Invocation and Relay Protocol

## Purpose

This protocol defines the first governed lane for ChatGPT Browser / ION to invoke named local ION agents through the Action Gateway and existing Codex queue infrastructure. The lane creates bounded role-session workers with explicit context, authority, proof, relay, and settlement requirements.

This is bounded agent invocation, not free autonomy. Tool availability is not authority. Agent output remains candidate state until proof, settlement, and receipt.

## Non-claims

- Production authority remains false.
- Live unrestricted execution authority remains false.
- No credential access, production deploy, push_main, broad shell, destructive deletion, or protected overwrite is granted.
- Browser/page automation remains observe/plan/preview/ask/receipt, not unrestricted control.

## Invocation packet

Schema file: `ION/03_registry/ion_agent_invocation_packet.schema.json`.

Required fields are `schema_id`, `idempotency_key`, `agent_role`, `objective`, and `authority`. The authority block must keep `production_authority=false` and `live_execution_authority=false`. Local writes are limited to `none`, `gated`, or `bounded`, with path scope validation.

## Supported v1 roles

Registry file: `ION/03_registry/ion_bounded_agent_role_registry.yaml`.

V1 supports `role.context_cartographer`, `role.runtime_cartographer`, `role.canon_librarian`, `role.template_curator`, `role.scribe`, and `role.nemesis_reviewer`. Each role has a display name, authority ceiling, default read zones, write posture, relay policy, and settlement target.

## Gateway endpoints

- `POST /agent/invoke`: validate packet, enforce idempotency, create capsule context, enqueue a bounded work request, and receipt the transition.
- `GET /agent/status`: return active/queued/known invocation state, evidence refs, relay posture, proof posture, and a legacy ChatOps status witness.
- `GET /agent/relay/pending`: return relay questions waiting for ChatGPT or operator.
- `POST /agent/relay/respond`: record a ChatGPT/operator relay response and make the invocation eligible to continue when allowed.
- `POST /agent/control`: pause, resume, or cancel safe invocation states.
- `GET /agent/receipts/recent`: surface recent invocation, relay, control, and settlement receipts.
- `POST /agent/settle`: record terminal accepted/blocked/deferred/rejected/failed settlement with proof references and receipts.

## Capsule context artifact

Each invocation creates:

`ION/05_context/current/chatgpt_connector/agent_invocations/{invocation_id}/capsule_context.json`

The capsule contains the objective, role, context refs, inline summary, required reads, forbidden reads, authority posture, source posture, generated time, and checksum. It is a bounded working world, not full memory.

## Queue integration

The invocation lane writes compatible Codex work requests under the existing ChatGPT connector queue root and appends queue records to `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json`. New queue fields are additive: `invocation_id`, `agent_role`, `capsule_context_path`, `relay_policy`, `authority_ceiling`, and `settlement_target`.

## State machine

V1 uses these visible states: `QUEUED`, `VALIDATING`, `RUNNING`, `WAITING_FOR_CHATGPT`, `WAITING_FOR_OPERATOR`, `BLOCKED`, `TERMINAL_ACCEPTED`, `TERMINAL_BLOCKED`, `TERMINAL_FAILED`, and `CANCELLED`. `PAUSED` is also supported as a safe control state.

## Relay loop

Relay schema files are `ION/03_registry/ion_agent_relay_message.schema.json` and `ION/03_registry/ion_agent_relay_response.schema.json`. Relay messages are durable JSON objects under each invocation. ChatGPT may answer context, route, knowledge, and non-authority settlement questions. Operator approval is required for authority expansion or sensitive actions. Relay never silently widens authority.

## Receipts

Important transitions write receipts under:

`ION/05_context/current/chatgpt_connector/agent_invocations/{invocation_id}/receipts/`

Minimum events include `agent_invocation_validated`, `capsule_context_created`, `agent_invocation_enqueued`, `relay_created`, `relay_answered`, `agent_invocation_paused`, `agent_invocation_resumed`, `worker_terminal`, `settlement_recorded`, and `blocked_or_refused` where applicable. Accepted settlement requires at least one proof, task return, or evidence reference.

## dAimon / JOC companion mapping

The browser companion should render this lane as a compressed JOC micro-shell: top status bar, mode rail, work surface, right evidence drawer, and bottom receipt timeline. Required surfaces are active invocation, queue state, relay questions, pause/resume/cancel controls, authority posture, proof/receipt rail, and blocked-capability warnings. Older JOC and local automation protocols are architecture witnesses for visible plans, dry runs, traces, and consent boundaries.

## Tests

Targeted tests cover valid invocation, idempotency, policy refusals, capsule creation, queue records, status, relay read/respond, receipts, and gateway policy/OpenAPI exposure.

## Known blockers and next packets

- Live gateway processes must be restarted or reloaded before new routes are available in a running server.
- Worker continuation after relay is represented by durable state and queue eligibility; deeper runner-level resume semantics can be expanded in a follow-up packet.
- Extension UI wiring should consume the new endpoints in a separate dAimon companion packet.
