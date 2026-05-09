# ION Custom GPT Actions → Local ION Bridge Strategy

created_at: 2026-05-07
status: candidate_strategy_not_ion_state
carrier_context: ChatGPT Browser / Sev as coordinator, Custom GPT Actions as bounded API ingress, local ION daemon as policy/receipt membrane, Codex CLI as bounded local worker.

## Settlement

Custom GPT Actions should become the primary controlled ingress from this GPT into local ION.

They should not become filesystem authority, shell authority, production authority, Steward authority, or raw local daemon exposure.

The correct shape is:

```text
Custom GPT Action
→ public HTTPS bridge / tunnel endpoint
→ authenticated allowlisted gateway
→ localhost ION ChatOps daemon
→ ION action validation / packet materialization / queue / receipt
→ Codex CLI bounded worker lane
→ proof-bearing return
→ Steward/template gate
→ receipt / next context
```

## Current ION surfaces already present

The current root already contains the owners needed for this plan:

- `ION/04_packages/kernel/ion_chatops_bridge.py`
- `ION/03_registry/ion_chatops_action.schema.yaml`
- `ION/03_registry/ion_chatops_extension_policy.yaml`
- `ION/03_registry/ion_chatops_local_daemon_policy.yaml`
- `ION/09_integrations/local_daemon/ion_chatops_bridge/`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/`
- `ION/04_packages/kernel/ion_codex_queue_runner.py`
- `ION/04_packages/kernel/ion_agent_invocation_broker.py`
- `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json`
- `ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json`
- `ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json`
- `ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json`

## Public Action API vs local daemon API

Do not expose every daemon endpoint directly to the Custom GPT at first.

Use two layers:

### Layer 1 — Public GPT Action bridge

A small HTTPS API that ChatGPT can call.

Responsibilities:

- authenticate GPT Action requests;
- enforce domain/endpoint allowlist;
- validate payload schema before forwarding;
- add replay protection and request IDs;
- refuse production/live authority claims;
- refuse shell/delete/push/deploy/credential paths;
- write gateway receipts;
- forward only accepted calls to local daemon;
- normalize daemon responses for ChatGPT.

### Layer 2 — Local ION daemon

The existing localhost daemon remains the ION policy and materialization owner.

Responsibilities:

- validate `ion.chatops.action.v1`;
- write bounded actions and receipts;
- create Codex work packets;
- expose queue/status/context-pack surfaces;
- register sandbox returns;
- queue review packets;
- refuse forbidden intents.

## MVP action tools

Expose only these to the Custom GPT first:

| Operation | Risk | Purpose |
|---|---:|---|
| `ionBridgeHealth` | read | prove bridge and daemon liveness |
| `ionBridgePolicy` | read | show allowed/blocked capabilities |
| `ionGetContextPack` | read | load bounded carrier context |
| `ionGetCodexQueue` | read | inspect local Codex work queue |
| `ionGetAgentStatus` | read | inspect broker/runner state |
| `ionValidateAction` | read/validation | validate a proposed action without materializing it |
| `ionSubmitApprovedAction` | write-gated | submit an explicitly approved bounded action |
| `ionGetSandboxReturns` | read | inspect sandbox return inbox |
| `ionGetReceipt` | read | retrieve action/receipt evidence |

Everything else remains internal or extension-only until proven.

## Mutation model

All mutating requests should go through a single high-level action envelope rather than many raw mutation endpoints.

Supported MVP intents:

- `register_artifact`
- `write_file_draft`
- `create_codex_work_packet`
- `create_github_issue_draft`

Hard-gated intents:

- `delete_file`
- `overwrite_protected_file`
- `push_main`
- `access_credential`
- `production_deploy`
- `broad_shell`

## Authentication and approval

Use two different mechanisms:

1. **Transport authentication**  
   Secret API key / bearer token stored in the GPT Action configuration and public bridge environment. This is the real transport secret.

2. **ION approval evidence**  
   Human approval fields inside the action payload. This is governance evidence, not a transport secret.

Minimum request fields:

```text
request_id
created_at
actor.callsign = Sev
actor.carrier = chatgpt_browser
authority.human_sovereign = Braden
authority.requires_approval = true
authority.production_authority = false
authority.live_execution_authority = false
```

Add replay controls:

```text
nonce
created_at within short TTL
idempotency_key
duplicate action_id rejected
gateway receipt path
```

## Browser extension role after Actions

The extension remains useful, but its role changes.

Keep it for:

- visible cockpit overlay;
- local diagnostics;
- manual approval UI;
- artifact attachment and file picker flows;
- safe-mode/throttle protection;
- fallback YAML bridge when Actions are unavailable.

Do not require the extension for the core Action API path once the HTTPS bridge works.

## Codex CLI role

Codex CLI remains the bounded local worker carrier.

It should receive rendered work packets, not raw user wishes and not unrestricted shell authority.

Default path:

```text
create_codex_work_packet
→ ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE
→ ion_codex_queue_runner
→ codex exec --sandbox workspace-write
→ latest_return.md / events.jsonl
→ context/template proof gate
→ Steward integration
→ receipt
```

## Implementation phases

### Phase 0 — Keep the current root stable

- Do not mutate doctrine broadly.
- Do not replace ChatOps bridge.
- Do not expose shell.
- Keep current non-production/live-execution false boundaries.

### Phase 1 — Public Action gateway skeleton

Build a small server with:

- `/health`
- `/policy`
- `/context-pack`
- `/codex/queue`
- `/agent/status`
- `/actions/validate`
- `/actions/submit`
- `/sandbox/returns`
- `/receipts/{receipt_id}`

Bridge these to localhost daemon endpoints.

### Phase 2 — Custom GPT Action schema

Install a minimal OpenAPI schema into the GPT editor.

Use only the MVP operations above.

Set API key auth.

Use a placeholder public HTTPS server URL until the approved tunnel/host is chosen.

### Phase 3 — Read-only proof

From the GPT, prove:

- health works;
- policy loads;
- context pack loads;
- Codex queue loads;
- agent status loads.

Receipt everything.

### Phase 4 — Bounded write proof

Submit one harmless `register_artifact` action.

Then submit one `create_codex_work_packet` action.

Prove:

- action validated;
- daemon wrote action packet;
- daemon wrote receipt;
- Codex queue index updated;
- no forbidden paths touched;
- no shell executed from the GPT Action itself.

### Phase 5 — Codex worker loop

Run queue processing locally.

Require Codex return sections:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

Prove tests and return intake.

### Phase 6 — IDE/cockpit

Build the browser/local cockpit over the existing data surfaces:

- daemon health;
- active packet;
- role spawn plan;
- Codex queue;
- agent invocations;
- task returns;
- receipts;
- blocked gates;
- current context pack export;
- attachable artifacts.

## Non-goals for first build

```text
no arbitrary shell endpoint
no raw filesystem editor endpoint
no direct git push
no production deploy
no secret/vault access
no hidden background autonomous loop
no bypass of Braden approval
no bypass of Steward integration
no replacing ION templates/receipts with Action responses
```

## First Codex work packet to create locally

Objective:

Build the Custom GPT Action public bridge skeleton for local ION, reusing the existing ChatOps daemon and policy surfaces.

Allowed paths:

```text
ION/09_integrations/
ION/04_packages/kernel/
ION/03_registry/
ION/tests/
ION/05_context/current/chatops_bridge/
```

Required work:

1. Add a public bridge server module or integration wrapper.
2. Implement API-key auth and allowlisted forwarding to `127.0.0.1:8767`.
3. Expose the minimal Action API endpoints.
4. Add focused tests for auth rejection, health/policy pass-through, action validation, blocked production/live authority, and duplicate action protection.
5. Update the OpenAPI schema artifact.
6. Return context proof, template action proof, validation, result, and receipt paths.

## Strong rule

Actions can give us enough control to operate local ION only if every call remains a candidate state transition under ION law.

The API gives reach. ION gives authority.
