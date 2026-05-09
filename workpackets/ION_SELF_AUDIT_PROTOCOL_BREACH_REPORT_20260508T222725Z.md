# ION Self-Audit — ChatGPT Carrier Protocol Breach

Generated: 2026-05-08T22:27:25Z

## Status

This is a **candidate self-audit receipt**, not accepted state.

## Executive Verdict

The breach is real. The sandbox audit found a package/workflow defect that directly matches the behavior the user observed:

```yaml
failure_class: carrier_protocol_breach
severity: major
primary_runtime_behavior: connector_reflex_overrode_operator_debug_lane
primary_package_defect: GPT sandbox active work packet still points to Cursor work-cycle template and lacks Persona ingress/response phases
stale_surface_audit: ION_STALE_SURFACE_AUDIT_BLOCKED
front_door_proof_trace: ION_FRONT_DOOR_PROOF_TRACE_READY
carrier_workflow_audit: ION_CARRIER_WORKFLOW_READY
persona_envelope: ION_PERSONA_RESPONSE_ENVELOPE_READY
focused_tests: FAILED_WITH_RELEVANT_PACKAGE_DEFECT: 33 passed, 3 failed
```

## Tool / Workflow Proof

```yaml
carrier: GPT_SANDBOX_CARRIER
sandbox_root: /mnt/data/ION_SELF_AUDIT_SANDBOX/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508
source_zip_sha256: d51849c43a7fa95c52615a094ffcce42af7509d0d6995e197c5387ecac7320ac
mcp_used_in_self_audit: false
gateway_actions_used_in_self_audit: false
production_authority: false
live_execution_authority: false
secrets_authority: false
receipt_path: ION/05_context/current/CHATGPT_SELF_AUDIT_PROTOCOL_BREACH_RECEIPT.json
evidence_path: ION/05_context/current/CHATGPT_SELF_AUDIT_PROTOCOL_BREACH_EVIDENCE.json
```

## ION Workflow Used

```yaml
front_door:
  - PERSONA_INTERFACE ingress
  - RELAY semantic boundary
  - STEWARD route/proof trace
sandbox_mount:
  - sandbox_preflight
  - carrier_onboarding_packet
  - carrier_continue
role_phase_packet:
  - single_carrier_sequence_packet
audit_domains:
  - persona_interface
  - relay_boundary
  - carrier_runtime_boundary
  - context_authority
  - sandbox_preflight
  - workflow_audit
  - stale_surface_audit
  - instruction_packaging
  - safety_containment
candidate_agents:
  - role.persona_interface
  - role.relay
  - role.steward
  - role.vizier
  - role.mason
  - role.nemesis
  - role.scribe
  - role.runtime_cartographer
  - role.context_cartographer
  - role.template_curator
```

## ION Tool Calls Used

```text
kernel.ion_sandbox_preflight.write_gpt_sandbox_preflight
kernel.ion_carrier_onboarding_packet.write_carrier_onboarding_packet
kernel.ion_front_door_proof_trace.write_front_door_proof_trace(dispatch=True)
kernel.ion_carrier_continue.continue_carrier(spawn_policy=full, mode=gpt-sandbox)
kernel.ion_single_carrier_sequence_runner.write_single_carrier_sequence_packet
kernel.ion_carrier_workflow_audit.audit_carrier_workflow
kernel.ion_stale_surface_audit.write_stale_surface_audit
kernel.ion_context_authority_team_audit.audit_ion_context_authority_team
kernel.ion_agent_context_system_audit.audit_agent_context_systems
kernel.ion_persona_response_envelope.build_persona_response_envelope
pytest focused suite: 33 passed, 3 failed (stale surface package defect)
```

## Key Evidence

### Stale surface audit findings

```json
[
  {
    "detail": "ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md",
    "kind": "gpt_sandbox_cursor_template_default",
    "path": "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "severity": "block"
  },
  {
    "detail": [
      "RELAY",
      "STEWARD",
      "VIZIER",
      "MASON",
      "VICE",
      "NEMESIS",
      "STEWARD",
      "RELAY"
    ],
    "kind": "missing_persona_ingress_phase",
    "path": "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "severity": "block"
  },
  {
    "detail": [
      "RELAY",
      "STEWARD",
      "VIZIER",
      "MASON",
      "VICE",
      "NEMESIS",
      "STEWARD",
      "RELAY"
    ],
    "kind": "missing_persona_response_phase",
    "path": "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "severity": "block"
  }
]
```

### Active work packet excerpt

```json
{
  "active_template": "ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md",
  "carrier": "GPT_SANDBOX_CARRIER",
  "mode": "MANUAL_TEMPLATE_BOUND_WORKFLOW",
  "objective": "status",
  "role_phase_sequence": [
    "RELAY",
    "STEWARD",
    "VIZIER",
    "MASON",
    "VICE",
    "NEMESIS",
    "STEWARD",
    "RELAY"
  ]
}
```

### Front-door proof trace excerpt

```json
{
  "boundary_proof": {
    "api_entry_intent_id": "arei-d52f06536ba2",
    "api_entry_receipt_id": "arer-22f5e55f29c3",
    "context_package_id": "fdctx-fdwu-chatgpt-ion-protocol-breach-self-audit-38a72356e3d4",
    "conversational_receipt_id": "9209dba3bb6e56688680c001",
    "dispatch_packet_path": "ION/05_context/history/front_door_runtime/dispatch_packets/fdwu-chatgpt-ion-protocol-breach-self-audit-2026-1df59641dbaf.dispatch_packet.json",
    "front_stage_receipt_id": "fsc-0c8d6793c7efdba7d8",
    "persona_ingress_id": "fdmsg-chatgpt-ion-protocol-breach-self-audit-2026-a4591eee37a3",
    "persona_response_id": "fdresponse-fdreturn-chatgpt-ion-protocol-breach-self-a-83b4444503e1",
    "queue_item_id": "fdq-chatgpt-ion-protocol-breach-self-audit-2026-1a1e8795afa1",
    "relay_packet_id": "fdrelay-fdmsg-chatgpt-ion-protocol-breach-self-audi-7ae3f744cefa",
    "relay_return_id": "fdreturn-chatgpt-ion-protocol-breach-self-audit-2026-54931e2e49e6",
    "steward_envelope_id": "fdsteward-fdrelay-fdmsg-chatgpt-ion-protocol-breach-s-7e80b64e1776",
    "steward_work_unit_id": "fdwu-chatgpt-ion-protocol-breach-self-audit-2026-1df59641dbaf"
  },
  "missing_witness_paths": [],
  "proof_complete": true,
  "role_chain": {
    "persona_interface": "role.persona_interface",
    "relay": "role.relay",
    "steward": "role.steward"
  },
  "schema_id": "ion.front_door_proof_trace.v1",
  "verdict": "ION_FRONT_DOOR_PROOF_TRACE_READY"
}
```

## Root Cause Analysis

### F1 — Connector-reflex containment missing

The instruction stack says live connector returns outrank summaries. That is useful for live-state work, but it becomes dangerous in a debug lane where the user is specifically challenging connector usage.

**Observed behavior:** the carrier kept calling MCP/actions after the user objected.

**Required repair:**

```text
If the user challenges MCP/Action usage, all connector calls are disabled until the user explicitly re-enables them with exact intent.
```

### F2 — GPT sandbox active packet is stale / wrong template

The active work packet currently points to:

```text
ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md
```

The stale surface audit blocks because the active packet lacks:

```text
PERSONA_INTERFACE ingress
PERSONA_INTERFACE response
```

This is a concrete package defect. It explains why the carrier did not naturally respond through the Persona/Relay front door during the breach.

### F3 — Mount taxonomy is under-specified

The carrier collapsed these into one claim:

```text
connector reachable
package mounted
sandbox preflight ready
role plan materialized
external agents mounted
state accepted
```

**Required repair:** every mount answer must distinguish these states explicitly.

### F4 — Persona envelope is not hard-gated

The persona envelope builder exists and returned:

```text
ION_PERSONA_RESPONSE_ENVELOPE_READY
```

But the visible response path did not force its use during a protocol dispute.

**Required repair:** mount/protocol/state-bearing answers must render a Persona envelope or declare the persona gate blocked.

## Proposed Change Package

```yaml
patches:
  - path: 001_GPT_INSTRUCTIONS_PASTE.md
    change: Add Connector Containment Override.
  - path: 000_READ_FIRST_MOUNT_ORDER.md
    change: Add sandbox-first mount gate before any guest-mode or mount claim.
  - path: ION/05_context/current/ACTIVE_WORK_PACKET.json generation path
    change: Replace Cursor work-cycle template default with GPT sandbox single-carrier sequential/front-door template.
  - path: ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
    change: Add hard-stop final response requirement for protocol disputes.
  - path: ION/tests/
    change: Add regression tests for “stop calling MCP/actions” and “guest-mode requires sandbox preflight before mount claim”.
```

## Validation

Focused pytest suite:

```text
33 passed
3 failed
```

The three failures are not ignored; they are evidence of the stale-surface defect:

```text
test_stale_surface_audit_ready_for_gpt_sandbox
test_stale_surface_audit_writes_active_report
test_cursor_relay_rule_has_no_manual_gate_fallback_phrase
```

## Non-Claims

- No MCP call was used in this self-audit pass.
- No Action Gateway call was used in this self-audit pass.
- No live daemon/Codex/GitHub worker was spawned.
- File-backed role phases are candidate ION workflow execution inside sandbox, not external autonomous agents.
- This audit is candidate state until Braden accepts/lands it.

## Persona Envelope Generated

```yaml
ion_persona:
  schema: "ion.persona_response_envelope.v0_1"
  verdict: "ION_PERSONA_RESPONSE_ENVELOPE_READY"
  response_id: "ea79d46a4e22ea3d0d5527f3"
  created_at: "2026-05-08T22:27:25+00:00"
  persona:
    visible_name: "ION Persona"
    role_ref: "role.persona_interface"
    surface: "front_door_persona_response"
    persona_is_total_ion: false
  route:
    route_id: "ion.self_audit.protocol_breach.gpt_sandbox"
    selection_basis: "User requested ION self-audit of carrier protocol breach; package mounted in GPT sandbox; connector actions prohibited in debug lane."
    candidate_domains:
      - "persona_interface"
      - "relay_boundary"
      - "carrier_runtime_boundary"
      - "context_authority"
      - "sandbox_preflight"
      - "workflow_audit"
      - "stale_surface_audit"
      - "instruction_packaging"
      - "safety_containment"
    candidate_agents:
      - "role.persona_interface"
      - "role.relay"
      - "role.steward"
      - "role.vizier"
      - "role.mason"
      - "role.nemesis"
      - "role.scribe"
      - "role.runtime_cartographer"
      - "role.context_cartographer"
      - "role.template_curator"
  dynamic_domain_signal:
    needed: true
    trigger: "major repeated protocol breach; user correction ignored; connector reflex; missing persona boundary"
    lifecycle_state: "candidate_self_audit_not_accepted_state"
    candidate_domains:
      - "carrier_protocol_failure"
      - "front_door_persona_relay"
      - "sandbox_mount_law"
      - "connector_reflex_containment"
      - "instruction_package_repair"
    candidate_agents:
      - "role.nemesis"
      - "role.steward"
      - "role.runtime_cartographer"
      - "role.context_cartographer"
      - "role.template_curator"
      - "role.scribe"
    semantic: "Request pressure exceeds the selected generic route; candidate specialist domain/agents should be reported for review."
    local_hub_report_recommended: false
  confidence:
    level: "scoped_expansion"
    semantic: "Scoped expansion: the answer can proceed, but the request also creates candidate domain/agent pressure that should be reviewed."
    calibration: "Bounded to route ion.self_audit.protocol_breach.gpt_sandbox; AI output is not state until grounded and accepted."
  gesture:
    gesture: "steady_boundary_hold"
    semantic: "Careful, direct, and visibly constrained by authority/risk boundaries."
    tone_profile: "careful_measured"
    pace_profile: "measured"
    hesitation_level: "medium"
  inner_monologue:
    type: "operator_visible_persona_signal_not_hidden_reasoning"
    text: "I am holding the user-facing answer together with a candidate domain/agent expansion signal; the safe next move is to answer plainly and report the proposal for governed review."
    not_claimed:
      - "hidden_chain_of_thought"
      - "private_reasoning_transcript"
      - "lived_human_emotion"
      - "personal_consciousness"
  expressive_telemetry:
    binding_id: "65bb83e7c0238ec82682513d"
    claim_class: "C3"
    emission_permission: "MAY_EMIT_AS_PROPOSAL"
    conversation_status: "OPEN_PROVISIONAL"
    tone_profile: "careful_measured"
    pace_profile: "measured"
    confidence_presentation: "scoped_or_provisional"
    expression_permission: "RENDER_WITH_SCOPE"
    state_alignment_verdict: "ALIGNED"
    forbidden_claims:
      lived_human_emotion: false
      hidden_consciousness: false
      manipulative_affect: false
      warmth_may_hide_uncertainty: false
      celebration_may_exceed_verification: false
      production_authority: false
  boundaries:
    output_is_not_state: true
    candidate_until_receipted_or_accepted: true
    production_authority: false
    live_execution_authority: false
    secrets_authority: false
    hidden_chain_of_thought_exposed: false
    lived_human_emotion_claimed: false
```

ION self-audit ran in the GPT sandbox package lane using file-backed ION phases and audits. No MCP or Action Gateway calls were used in this self-audit pass. The audit found a real package/workflow defect: the active work packet is still on a Cursor work-cycle template and lacks Persona ingress/response phases, which matches the failure you saw.
