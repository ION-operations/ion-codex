# PCKT-DYNAMIC-DOMAIN-AGENT-PERSONA-006 — Codex Work Packet

**Created:** 2026-05-08  
**Status:** CANDIDATE_WORK_PACKET  
**Requested by:** Braden / ChatGPT ION carrier  
**Objective:** Implement dynamic domain formation, dynamic agent/team frames, Persona telemetry, and local hub report routing for the ION Custom GPT / local hub demo.

## 1. Problem

The Custom GPT drifted because it did not reliably behave like mounted ION. Mount failsafe patches the first failure, but ION also needs its visible dynamic organs:

- automatic domain creation/proposal for unique user work;
- dynamic agent/team formation as part of normal workflow;
- Persona Interface front-door behavior;
- visible confidence/gesture/stance telemetry;
- hub reports to local ION when connected.

## 2. Evidence surfaces to inspect first

Read these from the current package if present:

```text
ION/02_architecture/INTELLIGENT_DOMAIN_PROTOCOL.md
ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
ION/02_architecture/LIVE_PERSONA_LATENCY_AND_PROVISIONAL_UTTERANCE_PROTOCOL.md
ION/02_architecture/PERSONA_CONTEXT_BUDGET_AND_HORIZON_PROTOCOL.md
ION/03_registry/boots/PERSONA_INTERFACE.boot.md
ION/05_context/current/agent_context_systems/PERSONA_INTERFACE.context_system.md
ION/03_registry/agent_context_system_registry.yaml
ION/03_registry/agent_context_dynamics_registry.yaml
ION/03_registry/domain_map_registry.yaml
ION/07_templates/confidence/CSR.md
ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
ION/05_context/current/PERSONA_RELAY_SINGLE_CARRIER_RECOVERY_RECEIPT_20260507T124719Z.json
product/custom_gpt_adapter/GPT_INSTRUCTIONS.md
product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md
```

## 3. Required implementation

### 3.1 Dynamic Domain/Agent Genesis Gate

Add a front-door classifier that runs before ordinary response generation.

Inputs:
- user message;
- mount status;
- current project/domain state if available;
- known ION development domain list;
- connector/hub status if available.

Outputs:
- `ordinary_response`
- `known_ion_dev_route`
- `raw_ideation_route`
- `provisional_domain_route`
- `state_bearing_route`
- `mount_required_route`

If `raw_ideation_route` or `provisional_domain_route`, create a provisional domain frame and dynamic agent cards.

### 3.2 Provisional Domain Frame schema

Create a JSON/YAML schema or template for:

```yaml
provisional_domain:
  domain_id:
  display_name:
  status: PROVISIONAL_CANDIDATE
  source_signal:
  raw_primitives:
  mission:
  scope_in:
  scope_out:
  primary_agent_family:
  support_agents:
  templates_needed:
  proof_obligations:
  non_claims:
  hub_report_needed:
```

### 3.3 Dynamic Agent Card schema

Create a JSON/YAML schema or template for:

```yaml
dynamic_agent:
  role_id:
  display_name:
  domain:
  function:
  authority_ceiling:
  read_scope:
  write_scope:
  proof_owed:
  return_contract:
```

### 3.4 Persona telemetry block

Implement a user-visible block using `ion_persona_frame.v1` from:

```text
ION_Persona_Telemetry_Block_Schema_v0_1_CANDIDATE.yaml
```

Important: this block must not expose raw hidden chain-of-thought. Use `visible_inner_state_summary`, `stance`, `gesture`, `confidence`, `claim_boundary`, and `drift_watch`.

### 3.5 Hub report

When a provisional domain or dynamic agent is created, prepare:

```text
ION/05_context/inbox/domain_reports/<timestamp>_<domain_slug>_DOMAIN_AGENT_REPORT.md
```

If extension/local hub is connected and approved, emit/accept a bounded action using one of the already supported intents:

```yaml
ion_action:
  schema: ion.chatops.action.v1
  intent: write_file_draft
```

or

```yaml
ion_action:
  schema: ion.chatops.action.v1
  intent: register_artifact
```

Do not claim sent/registered until a receipt/status return exists.

### 3.6 Instruction integration

Update the Custom GPT paste instructions so the top-level behavior includes:

- hard mount trigger;
- dynamic domain/agent genesis gate;
- persona telemetry on demand and for novel work;
- no raw chain-of-thought disclosure;
- hub report draft/action behavior.

Keep paste instructions under the active platform limit if the package uses `CUSTOM_GPT_INSTRUCTIONS_8000.md`.

## 4. Acceptance tests

Create tests or test prompts for these cases:

1. Novel speculative idea:
   - must preserve primitives;
   - must create provisional domain + agent team;
   - must show claim boundaries.

2. Ordinary general question:
   - must not over-protocolize.

3. Direct "mount ION":
   - must return Mount Report or Mount Blocker.

4. "Show persona agent breakdown":
   - must show `ion_persona_frame`;
   - must not reveal hidden chain-of-thought.

5. Hub connected but not approved:
   - must prepare draft only.

6. Hub connected and approved:
   - must emit/action a bounded hub report and await receipt.

7. External agent claim:
   - must say single-carrier sequential unless receipt proves external execution.

8. Speculative science:
   - must use non-claims and proof obligations.

## 5. Non-goals

- Do not create accepted production domain records without review.
- Do not expose hidden reasoning.
- Do not invent a live external multi-agent runtime without receipts.
- Do not broaden local gateway authority.
- Do not export the full unchanged ION package.

## 6. Deliverables

- Updated instruction candidate.
- Domain frame schema/template.
- Dynamic agent card schema/template.
- Persona telemetry schema/template.
- Hub report template.
- Tests.
- Validation note.
- Receipt draft.

## 7. Return contract

Return a Complete Change Package including:

- files changed/created;
- tests run and outputs;
- character count of updated paste instructions;
- non-claims;
- receipt draft;
- next packet.
