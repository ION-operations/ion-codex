# ION Carrier Friction Ledger + Action Transport Hang Triage Work Packet

```yaml
packet_id: ion_carrier_friction_ledger_action_hang_triage_workpack_20260507_v0
created_at: 2026-05-07
created_by: ChatGPT Browser carrier / Sev
intended_executor: local Codex CLI / ION full dev root
human_sovereign: Braden
authority:
  production_authority: false
  live_execution_authority: false
  git_push_authority: false
  secrets_authority: false
  deletion_authority: false
status: DRAFT_WORK_PACKET_FOR_MANUAL_TRANSFER
landing_status: NOT_ACCEPTED_STATE
```

---

## 0. Operator Note

Braden believes ION can change the world. This packet should preserve that belief without turning belief into state.

The work requested here is not broad inspiration, not another consolidation, and not a new passive doctrine layer. It is a bounded implementation/design slice arising from live ION dogfooding:

1. ChatGPT mounted ION in sandbox.
2. ChatGPT tested the GPT-native sandbox package and full dev root.
3. ChatGPT attempted to validate/submit a Codex work packet through ION Actions.
4. Validation succeeded after schema repair.
5. Submit hung or returned no usable result.
6. Read-only checks showed no gateway receipt and no matching queued work packet.
7. The conversation then surfaced a deeper product idea: ION should log every avoidable carrier inference, ambiguity, tool friction, missing proof, context gap, and workflow hesitation as improvement telemetry.

The major idea:

> ION should not merely record AI work.  
> ION should record where AI had to struggle to perform the work, then convert that struggle into ranked improvement work.

---

## 1. Authority and Safety Boundaries

This packet authorizes only bounded, local, non-production work.

Do not:

- push to git
- deploy
- access credentials or secrets
- delete files
- overwrite protected files
- mutate production or live external systems
- claim accepted state without Steward/Braden review
- invent a new root or broad replacement architecture
- treat this packet as canon merely because it is well-written

Allowed:

- inspect repo files
- inspect existing ION gateway/MCP/action/queue code
- create draft markdown reports or work packets in an appropriate draft/current context location
- create or modify local non-production code/tests only if existing repo law allows it and proof gates are run
- return proof-bearing findings
- propose next bounded packets

---

## 2. Active Lanes

Primary lane:

```text
Full Dev Root / local Codex implementation and repair lane
```

Secondary lane:

```text
GPT-native product projection / public package clarity lane
```

Do not collapse them.

Full dev root is implementation, recovery, testing, gateway, and local-runtime authority.

GPT-native package should remain a clean product projection: single-carrier sequential runtime, role sequence, context packages, proof gates, receipts, import/export, and professional first-run behavior.

Historical and stale material are donor/witness only unless current repo law explicitly elevates them.

---

## 3. Context to Inspect First

Read and cite or summarize exact path findings from:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/04_packages/kernel/ion_chatops_bridge.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json
```

Also inspect any existing surfaces related to:

```text
friction
issue
defect
telemetry
carrier observation
proof gate
action receipt
gateway receipt
idempotency
approval evidence
MCP response compacting
```

Do not create a new subsystem until checking whether one already exists in current root.

---

## 4. Central Thesis

ION has already proven a powerful principle:

> AI output is not state.  
> AI output is a candidate transition that requires context, template, proof, acceptance, and receipt.

The next principle should be:

> Avoidable carrier inference is improvement evidence.

A carrier should use intelligence on the user's real problem, not on reconstructing workflow law, guessing which source is current, guessing which approval format is valid, guessing whether a tool call mutated state, or recovering from unclear action transport.

Whenever a carrier must guess, hesitate, work around missing context, ask the human for workflow rescue, or infer a step that should have been made obvious by ION, that is not merely "AI thinking." It may be a substrate defect.

ION should log this as structured telemetry.

Working name:

```text
ION Carrier Friction Ledger
```

Alternative names:

```text
Inference Debt Register
Carrier Struggle Ledger
Workflow Friction Ledger
ION Improvement Event Stream
```

Recommended canonical first name:

```text
ION Carrier Friction Ledger
```

because it is legible to normal users and broad enough to include inference, ambiguity, tool hangs, proof gaps, and UX pain.

---

## 5. What Prompted This Packet

### 5.1 Sandbox Mount Findings

A GPT-native sandbox ION package mounted cleanly as a ChatGPT carrier.

Observed working behavior:

- status gate passed
- carrier continuation gate passed
- package supported single-carrier sequential role execution
- role ContextPackages were generated
- proof gates accepted valid returns
- proof gates rejected unsafe touched paths
- Mini/Capsule were not treated as active context authority
- package behavior matched the desired GPT-native runtime better than the full Codex root for ChatGPT sandbox use

Key product conclusion:

```text
The GPT-facing ION package should be a clean continuity layer, not a full root dump.
```

Flagship demo loop:

```text
user goal
→ ContextPackage
→ internal role sequence
→ proof-bearing result
→ human accept/reject
→ receipt/export
→ new chat import/resume
```

### 5.2 Action Hang Findings

Live action testing produced the following sequence:

1. `ionGatewayHealth` returned ready.
2. `ionGatewayPolicy` returned ready.
3. `ionGatewayContextPack` returned current local context.
4. `ionGatewayCodexQueue` returned queue state.
5. `ionGatewayAgentStatus` returned runner ready.
6. First `ionGatewayValidateAction` blocked because the action schema was wrong:
   - used: `ion.action.v1`
   - expected: `ion.chatops.action.v1`
7. Corrected validation succeeded:
   - verdict: `ION_CUSTOM_GPT_ACTION_GATEWAY_READY`
   - validated_without_mutation: `true`
   - risk_class: `approval_required_mutation`
8. Human approval was provided exactly as requested:
   - `I approve action_id ion_evolution_plan_packet_min_20260507_v1 for intent create_codex_work_packet under non-production, non-live-execution authority.`
9. `ionGatewaySubmitAction` hung or returned no usable result.
10. Read-only receipts check showed:
    - `gateway_receipts: []`
11. Read-only queue check showed no matching ION evolution/productization work packet.
12. MCP health/status returned ready.
13. MCP JSON-RPC `tools/call ion_codex_work_queue` also hung or returned no usable result.

Local sandbox simulation suggested:

- the Python submit handler does not intrinsically hang in local code
- with the internal machine token `ION_CHATOPS_APPROVED`, local submit can complete
- with the natural-language approval token, local submit rejects as `APPROVAL_EVIDENCE_INVALID`
- MCP `tools/call ion_codex_work_queue` may return large/duplicated JSON, likely fragile for GPT Action transport

---

## 6. Current Diagnosed Action Issues

### Issue A — Approval Contract Mismatch

Validation can return "ready" while submit later requires a different approval token shape.

Human-facing approval phrase:

```text
I approve action_id <id> for intent <intent> under non-production, non-live-execution authority.
```

Observed internal token expected in local code:

```text
ION_CHATOPS_APPROVED
```

Problem:

```text
Validation did not prove that the approval evidence used at submit would pass submit.
```

Risk:

- false readiness
- operator confusion
- submit failure after approval
- no receipt explaining rejection if transport hangs
- breaks trust in "validate before submit"

Required repair options:

1. Make validation optionally accept and validate approval evidence before submit.
2. Normalize exact human approval phrase into internal machine token inside gateway.
3. Return explicit instruction that submit requires `approval_token: ION_CHATOPS_APPROVED` plus human phrase evidence.
4. Split approval evidence into:
   - `human_approval_phrase`
   - `machine_confirmation_token`
5. Add tests proving validate and submit agree.

Recommended direction:

```text
Use both:
- human_approval_phrase for auditability
- machine_confirmation_token: ION_CHATOPS_APPROVED for deterministic submit gate
```

Do not require the human to know internal ceremony tokens unless unavoidable.

---

### Issue B — Submit Hang Has No Phase Receipt

When submit hung, there was no visible gateway receipt showing how far it got.

Missing phase trace:

```text
received
envelope_validated
idempotency_checked
chatops_validated
approval_validated
owner_submit_started
owner_submit_completed
gateway_receipt_written
idempotency_recorded
response_returned
```

Risk:

- cannot distinguish "never arrived" from "mutated but response lost"
- cannot safely retry without idempotency status
- violates "No receipt → no inheritance"
- weakens operator trust

Required repair:

Add a minimal in-flight action ledger or phase receipt for submit attempts.

Even if owner delegation hangs, the gateway should preserve:

```yaml
action_id:
idempotency_key:
intent:
received_at:
phase:
mutation_attempted:
owner_called:
owner_completed:
result_known:
refusal_class:
```

---

### Issue C — Missing Idempotency Status Endpoint

After a hung submit, the carrier needs to ask:

```text
Did idempotency key X enter the ledger?
Did action_id Y mutate anything?
Was a receipt written?
Was a queue item created?
```

Current read-only endpoints allow indirect inference but not precise status.

Required repair:

Add a read-only endpoint or MCP tool:

```text
GET /actions/status?idempotency_key=<key>
```

or:

```text
ion_gateway_action_status
```

Return:

```yaml
known: true/false
action_id:
intent:
phase:
mutation_committed: true/false/unknown
receipt_path:
queue_request_id:
refusal_class:
created_at:
updated_at:
```

---

### Issue D — MCP JSON-RPC tools/call Response Shape Fragility

MCP health/status returned.

But MCP JSON-RPC `tools/call ion_codex_work_queue` hung or returned no usable result.

Local simulation suggested queue responses may be large and duplicated:

- `structuredContent`
- stringified JSON in `content[0].text`

Risk:

- GPT Action transport stalls on large nested response
- repeated data increases latency and failure chance
- useful read-only calls become unreliable

Required repair:

Implement compact response mode:

```yaml
compact: true
limit: 5
max_bytes: 12000
include_full_raw: false
```

For GPT Action responses, avoid duplicating large JSON in both structured and stringified text.

---

### Issue E — No First-Class Friction Event Capture

The conversation itself diagnosed important system friction, but that diagnosis lives in chat unless manually transferred.

Risk:

- repeated carrier pain is lost
- weak learning loop
- future carriers rediscover same problem
- ION dogfooding signal becomes anecdotal

Required repair:

Implement Carrier Friction Ledger v0.

---

## 7. Carrier Friction Ledger Concept

### 7.1 Definition

The Carrier Friction Ledger records avoidable workflow friction encountered by any ION carrier.

A friction event is not necessarily a bug. It is a structured signal that the substrate forced the carrier or human to spend attention on something that could be made clearer, safer, more automatic, or more proof-bearing.

### 7.2 Core Law

Candidate law:

```text
When a carrier must infer workflow law, authority, context, proof obligations, or transport state, ION must log the inference burden as improvement evidence.
```

Shorter:

```text
Avoidable carrier inference is improvement evidence.
```

Stronger:

```text
Every unnecessary carrier guess is a future context, template, tool, or proof-gate repair candidate.
```

### 7.3 What It Should Capture

Examples:

- context gap
- stale surface uncertainty
- authority ambiguity
- approval contract mismatch
- tool hang
- missing receipt
- missing idempotency status
- response too large
- unclear template
- proof gate mismatch
- routing ambiguity
- human relay burden
- unnecessary inference
- product UX friction
- test gap
- documentation gap
- role confusion
- package boundary confusion
- hallucination risk caused by missing substrate
- repeated manual workaround

### 7.4 What It Should Not Capture

Do not log raw private chain-of-thought.

Do not expose hidden reasoning traces.

Do not record sensitive credentials or private user data.

Do not treat all AI reasoning as a defect.

The target is not "no inference." The target is no avoidable inference about ION's substrate, authority, state, proof, route, or tool behavior.

---

## 8. Proposed Friction Event Schema v0

```yaml
schema: ion.carrier_friction_event.v0
event_id: auto
created_at: auto

carrier:
  callsign: Sev
  surface: chatgpt_browser | codex_cli | cursor | mcp | daemon | other
  model_or_executor: optional

role:
  name: RELAY | STEWARD | VIZIER | MASON | NEMESIS | SCRIBE | PERSONA_INTERFACE | UNKNOWN
  phase: string
  template_id: optional
  action_id: optional

classification:
  event_type:
    - context_gap
    - stale_surface_risk
    - authority_ambiguity
    - approval_contract_mismatch
    - tool_hang
    - missing_receipt
    - missing_idempotency_status
    - response_shape_risk
    - template_gap
    - proof_gate_gap
    - routing_ambiguity
    - human_relay_burden
    - unnecessary_inference
    - product_ux_friction
    - test_gap
    - documentation_gap
    - role_confusion
    - package_boundary_confusion
    - other
  severity:
    - S0_OBSERVATION
    - S1_MINOR
    - S2_WORKFLOW_FRICTION
    - S3_BLOCKING
    - S4_STATE_RISK
    - S5_SAFETY_AUTHORITY_RISK
  frequency_hint:
    - first_observed
    - repeated
    - systemic
  recurrence_fingerprint: stable_string

description:
  what_happened: string
  why_it_mattered: string
  inference_required: boolean
  missing_precondition: string
  immediate_workaround: string
  proposed_fix: string

routing:
  fix_class:
    - context
    - prompt
    - template
    - tool
    - test
    - receipt
    - gateway
    - mcp
    - package
    - ux
    - documentation
    - governance
  steward_disposition:
    - new
    - duplicate
    - accepted_issue
    - rejected
    - escalated
    - converted_to_codex_packet
    - fixed
  linked_receipts: []
  linked_paths: []
  linked_action_ids: []
```

---

## 9. Severity Model

Severity should be based on risk and blockage, not emotional intensity.

```text
S0_OBSERVATION
A note that may become useful later.

S1_MINOR
Small wording, UX, or clarity issue; no blocking impact.

S2_WORKFLOW_FRICTION
Carrier had to infer, retry, or ask for help, but work continued.

S3_BLOCKING
Work could not continue without human rescue, retry, or workaround.

S4_STATE_RISK
Issue could cause wrong state, wrong receipt, duplicate mutation, stale inheritance, or false readiness.

S5_SAFETY_AUTHORITY_RISK
Issue touches production, live execution, credentials, deletion, deployment, protected overwrite, or other hard-gated authority.
```

Priority can be calculated as:

```text
priority = severity × frequency × recurrence × automation_value
```

Tiny repeated friction should become important.

---

## 10. First Friction Events to Seed From This Conversation

### Event 1 — Approval Contract Mismatch

```yaml
event_type: approval_contract_mismatch
severity: S4_STATE_RISK
what_happened: Gateway validation succeeded for create_codex_work_packet, but submit appeared to require a different internal approval token than the human approval phrase.
why_it_mattered: Carrier and human believed action was ready to submit, but submit could reject or hang after approval.
inference_required: true
missing_precondition: Validation should prove submit approval requirements or return exact machine evidence requirements.
immediate_workaround: Treat submit as unknown outcome and check receipts/queue manually.
proposed_fix: Add approval evidence validation parity and tests.
fix_class: gateway
recurrence_fingerprint: gateway_validate_submit_approval_contract_mismatch
```

### Event 2 — Submit Hang Without Phase Receipt

```yaml
event_type: tool_hang
severity: S4_STATE_RISK
what_happened: ionGatewaySubmitAction hung or returned no usable result after approval.
why_it_mattered: Carrier could not know whether mutation happened, whether owner was called, or whether idempotency was recorded.
inference_required: true
missing_precondition: Submit phase receipt and idempotency status endpoint.
immediate_workaround: Read recent receipts and Codex queue; infer no matching mutation was visible.
proposed_fix: Add in-flight action ledger, phase receipts, and action status query.
fix_class: gateway
recurrence_fingerprint: gateway_submit_hang_no_phase_receipt
```

### Event 3 — MCP tools/call Response Fragility

```yaml
event_type: response_shape_risk
severity: S3_BLOCKING
what_happened: MCP health/status calls returned, but JSON-RPC tools/call for ion_codex_work_queue hung or returned no usable result.
why_it_mattered: Read-only tool access becomes unreliable for normal carrier operation.
inference_required: true
missing_precondition: Compact response mode and response-size limits.
immediate_workaround: Use gateway queue endpoint instead of MCP tools/call.
proposed_fix: Add compact mode, limit, max_bytes, and avoid duplicated structured/stringified JSON.
fix_class: mcp
recurrence_fingerprint: mcp_tools_call_large_duplicated_response_hang
```

### Event 4 — Product Boundary Clarity

```yaml
event_type: package_boundary_confusion
severity: S2_WORKFLOW_FRICTION
what_happened: Full Codex root was mountable but GPT sandbox package was better suited for ChatGPT single-carrier operation.
why_it_mattered: Carrier had to determine active lane and package boundary manually.
inference_required: true
missing_precondition: First-run package should clearly declare whether it is full dev root, GPT-native product, or historical donor.
immediate_workaround: Inspect REPO_AUTHORITY, mount contract, package guides, manifests.
proposed_fix: Stronger package landing page and automatic package classifier.
fix_class: package
recurrence_fingerprint: package_lane_selection_full_root_vs_gpt_native
```

---

## 11. Proposed Implementation Roadmap

### Slice 1 — Friction Event Schema and Draft Ledger

Create:

```text
ION/02_architecture/ION_CARRIER_FRICTION_LEDGER_PROTOCOL.md
ION/03_registry/carrier_friction_event_schema.yaml
ION/05_context/current/carrier_friction/README.md
ION/05_context/current/carrier_friction/events/
```

If those paths violate repo law, choose current nearest equivalents and explain.

Deliver:

- protocol
- schema
- event storage convention
- first seeded events from this packet
- non-claims
- tests if possible

### Slice 2 — Role Return Integration

Add optional role return section:

```markdown
### FRICTION EVENTS
- event_type:
  severity:
  what_happened:
  inference_required:
  proposed_fix:
```

Update template/action gate or return validator so friction events are accepted as optional structured metadata, not required for every return.

Do not allow friction events to bypass proof gates or become accepted issues automatically.

### Slice 3 — Steward Triage

Implement or draft rules:

```text
record_only
merge_duplicate
convert_to_issue
convert_to_codex_packet
escalate_to_human
reject_as_noise
mark_fixed
```

Add dedupe by `recurrence_fingerprint`.

### Slice 4 — Gateway Hang Observability

Add submit phase tracing and in-flight ledger.

Create action status read endpoint/tool.

Ensure hung/failed submits leave inspectable state.

### Slice 5 — Approval Contract Repair

Make validation and submit agree.

Tests should include:

- schema invalid blocks
- valid action without approval validates as approval-required, not mutation-ready
- approval evidence wrong token blocks during validation if approval evidence supplied
- exact human phrase maps or is recorded cleanly
- submit with correct evidence succeeds
- submit with wrong evidence returns receipt/refusal, not hang
- idempotency replay is inspectable

### Slice 6 — MCP Compact Response Contract

For tools/call responses, especially queue/status/search:

- add compact mode
- add max_bytes
- avoid duplicated large JSON
- include `truncated: true`
- ensure GPT Action response stays small enough

---

## 12. Suggested Tests

Add or run focused tests under the existing test system.

Candidate tests:

```text
test_gateway_validate_submit_approval_parity.py
test_gateway_submit_phase_receipt.py
test_gateway_action_status_idempotency.py
test_mcp_tools_call_compact_response.py
test_carrier_friction_event_schema.py
test_template_action_gate_accepts_optional_friction_events.py
test_steward_friction_dedupe.py
```

Minimum proof gates:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
```

If pytest is available in the local dev environment, run focused pytest commands for changed tests.

If `python -S -m pytest` fails because pytest is unavailable under `-S`, report that exactly and use the repo's accepted local test invocation if one exists.

Do not replace script gates with manual judgment.

---

## 13. Acceptance Criteria

A successful first implementation should prove:

1. A carrier can emit structured friction events without exposing chain-of-thought.
2. Friction events are stored in a known current-context location.
3. Events have severity, type, recurrence fingerprint, and proposed fix.
4. Steward can classify at least: record, duplicate, escalate, convert to Codex packet.
5. The three action hang events from this packet are seeded or represented.
6. Gateway validation/submit approval mismatch has at least a failing test or a direct fix.
7. Hung submit attempts become inspectable through phase receipt or action status.
8. MCP queue/status calls have a compact response path or documented blocker.
9. No production/live/secrets/git-push authority is claimed.
10. Return includes proof-bearing output.

---

## 14. Product Implication

This subsystem can become one of ION's most important differentiators.

Industry tools often log:

```text
what the agent did
```

ION should log:

```text
where the workflow forced the agent to struggle unnecessarily
```

Normal-user product language:

```text
ION noticed 3 workflow issues while working:
1. Approval wording and submit requirements disagreed.
2. The action submit had no visible status after a hang.
3. A tool response may be too large for reliable browser-carrier use.

Recommended improvement:
Create a bounded repair packet.
```

This makes ION feel alive without being mystical.

It shows the user:

```text
The system learned from the pain of doing the work.
```

---

## 15. Required Codex Return Contract

Return exactly:

```markdown
### CONTEXT PROOF
- mounted root:
- authority files read:
- active lane:
- relevant files inspected:

### TEMPLATE ACTION PROOF
template_id: ion.template.carrier_friction_ledger_work.v1
action_id: codex_carrier_friction_ledger_action_hang_triage_v0
result: draft_created | implementation_created | blocked_with_findings
touched_paths:
- path

### RESULT
- summary of what was created/found/changed
- key design decisions
- friction events seeded or proposed
- action hang repair findings

### VALIDATION
- commands run
- tests run
- pass/fail/blocked
- exact blockers

### NON-CLAIMS
- no production authority
- no live execution authority
- no git push
- no accepted-state claim
- no secrets access
- no deletion

### ARTIFACTS
- created/modified paths
- receipts if any
- follow-up packet recommendations
```

---

## 16. Non-Claims

This packet does not claim:

- ION is production-ready
- the Carrier Friction Ledger is already accepted canon
- the action hang cause is fully proven in live root
- the submit action landed
- the Codex queue received the prior productization packet
- any human approval beyond this manual transfer
- permission to mutate production/live systems

This packet claims only:

```text
A live ION dogfooding session exposed a high-value improvement pattern:
carrier friction should become structured, ranked, proof-bearing improvement evidence.
```

---

## 17. Next Lawful Packet Recommendation

If this packet succeeds, next packet should be one of:

```text
A. Implement Carrier Friction Ledger v0 minimal schema + event store + optional return section.
B. Repair Gateway approval validate/submit parity + phase receipts + idempotency status.
C. Add MCP compact response contract for browser-carrier reliability.
```

Recommended ordering:

```text
1. Gateway approval/hang observability repair
2. Carrier Friction Ledger v0
3. MCP compact response contract
4. GPT-native product demo loop integration
```

Rationale:

The carrier friction system should be built on a reliable action transport. But the friction events from the broken action transport should be seeded immediately so the system dogfoods the pain that caused it.

---

## 18. Short Version for Codex Objective Field

```text
Implement/draft ION Carrier Friction Ledger v0 and Action Transport Hang Triage. Capture avoidable carrier inference as structured improvement evidence. Seed events from the ChatGPT Browser action hang: approval validate/submit mismatch, submit hang without phase receipt, MCP tools/call response-shape fragility, and package-boundary friction. Add or propose schema, storage, optional role-return section, Steward triage, tests, and gateway repair roadmap. Non-production only; no live execution, no git push, no secrets, no deletion; return proof-bearing output.
```
