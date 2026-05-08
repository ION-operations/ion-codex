# ION Single-Carrier Sequential Packet

schema_id: ion.single_carrier_sequence_packet.v1
template_id: ion.template.single_carrier_sequential_runtime.v1
sequence_id: scseq-4e716a45c88e82ed15
created_at: 2026-05-08T19:31:48+00:00
carrier: GPT_SANDBOX_CARRIER
objective: write sequence packet test
production_authority: false
live_execution_authority: false

## Runtime law

One capable LLM carrier executes the ION role chain sequentially. This packet
does not spawn external agents and does not grant production authority.

Required baseline sequence:

```text
PERSONA_INTERFACE ingress
→ RELAY
→ STEWARD
→ VIZIER
→ MASON
→ NEMESIS / VICE when required
→ SCRIBE
→ STEWARD FINAL
→ PERSONA_INTERFACE response
→ RECEIPT / NEXT STATE
```

## Active packet

- active work packet: `ION/05_context/current/ACTIVE_WORK_PACKET.json`
- sequence receipt candidate: `ION/05_context/current/single_carrier_sequences/scseq-4e716a45c88e82ed15/SINGLE_CARRIER_SEQUENCE_RECEIPT.json`
- packet path: `ION/05_context/current/single_carrier_sequences/scseq-4e716a45c88e82ed15/SINGLE_CARRIER_SEQUENTIAL_PACKET.md`
- GPT sandbox preflight verdict: `ION_GPT_SANDBOX_PREFLIGHT_READY`

## Required context reads

The carrier must include evidence for these paths in `### CONTEXT PROOF`:

- `ION/REPO_AUTHORITY.md`
- `ION/02_architecture/ION_MOUNT_CONTRACT.md`
- `ION/02_architecture/SINGLE_CARRIER_SEQUENTIAL_RUNTIME_PROTOCOL.md`
- `ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md`
- `ION/07_templates/receipts/SINGLE_CARRIER_SEQUENCE_RECEIPT.md`
- `ION/03_registry/gpt_sandbox_carrier_profile.yaml`
- `ION/02_architecture/ION_GPT_SANDBOX_ENVIRONMENT_CONTRACT.md`
- `ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md`
- `ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md`
- `ION/03_registry/boots/PERSONA_INTERFACE.boot.md`
- `ION/03_registry/boots/RELAY.boot.md`
- `ION/03_registry/boots/STEWARD.boot.md`
- `ION/03_registry/boots/VIZIER.boot.md`
- `ION/03_registry/boots/MASON.boot.md`
- `ION/03_registry/boots/SCRIBE.boot.md`

## Phase order

1. `PERSONA_INTERFACE_INGRESS` — role `PERSONA_INTERFACE` — Receive human language, preserve intent, and render it into ION-admissible intent without overexposing machinery.
2. `RELAY` — role `RELAY` — Preserve signal integrity and package the intent for Steward/internal routing.
3. `STEWARD` — role `STEWARD` — Classify authority, decide route, and prevent output from becoming state without review.
4. `VIZIER` — role `VIZIER` — Strategic route analysis and context-aware sequencing.
5. `MASON` — role `MASON` — Implementation or concrete construction phase within sandbox limits.
6. `NEMESIS_OR_VICE_REVIEW` — role `NEMESIS_OR_VICE` — Risk/adversarial review; explicitly mark not required only with reason.
7. `SCRIBE` — role `SCRIBE` — Documentation and receipt synthesis.
8. `STEWARD_FINAL` — role `STEWARD` — Final integration recommendation; still proposal-only unless separately accepted.
9. `PERSONA_INTERFACE_RESPONSE` — role `PERSONA_INTERFACE` — Render the internal result back to the user clearly, hiding machinery unless useful/requested.

## Role surface status

### MASON surfaces
- `ION/03_registry/boots/MASON.boot.md` — present
- `ION/05_context/current/agent_context_systems/MASON.context_system.md` — present
### NEMESIS_OR_VICE surfaces
- `ION/03_registry/boots/NEMESIS.boot.md` — present
- `ION/03_registry/semantic_identities/NEMESIS.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/NEMESIS.context_system.md` — present
- `ION/03_registry/boots/VICE.boot.md` — present
- `ION/03_registry/semantic_identities/VICE.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/VICE.context_system.md` — present
### PERSONA_INTERFACE surfaces
- `ION/03_registry/boots/PERSONA_INTERFACE.boot.md` — present
- `ION/03_registry/semantic_identities/PERSONA_INTERFACE.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/PERSONA_INTERFACE.context_system.md` — present
- `ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md` — present
- `ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md` — present
### RELAY surfaces
- `ION/03_registry/boots/RELAY.boot.md` — present
- `ION/03_registry/semantic_identities/RELAY.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/RELAY.context_system.md` — present
- `ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md` — present
### SCRIBE surfaces
- `ION/03_registry/boots/SCRIBE.boot.md` — present
- `ION/05_context/current/agent_context_systems/SCRIBE.context_system.md` — present
### STEWARD surfaces
- `ION/03_registry/boots/STEWARD.boot.md` — present
- `ION/03_registry/semantic_identities/STEWARD.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/STEWARD.context_system.md` — present
### VIZIER surfaces
- `ION/03_registry/boots/VIZIER.boot.md` — present
- `ION/03_registry/semantic_identities/VIZIER.semantic.yaml` — present
- `ION/05_context/current/agent_context_systems/VIZIER.context_system.md` — present

## Missing required surfaces

```json
[]
```

## Required carrier output shape

Copy the following headings into the carrier return and fill each section. The
return is a candidate until Steward/human review accepts it.

### CONTEXT PROOF

- Mention every required context path read.
- Include line/heading/excerpt/hash evidence, not a generic acknowledgement.

### TEMPLATE ACTION PROOF

template_id: ion.template.single_carrier_sequential_runtime.v1
action_id: scseq-4e716a45c88e82ed15
result: <candidate_result>
touched_paths:
  - ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_RECEIPT.json

### ROLE PHASE: PERSONA_INTERFACE_INGRESS

- role: `PERSONA_INTERFACE`
- required: `true`
- return:


### ROLE PHASE: RELAY

- role: `RELAY`
- required: `true`
- return:


### ROLE PHASE: STEWARD

- role: `STEWARD`
- required: `true`
- return:


### ROLE PHASE: VIZIER

- role: `VIZIER`
- required: `true`
- return:


### ROLE PHASE: MASON

- role: `MASON`
- required: `true`
- return:


### ROLE PHASE: NEMESIS_OR_VICE_REVIEW

- role: `NEMESIS_OR_VICE`
- required: `true`
- return:


### ROLE PHASE: SCRIBE

- role: `SCRIBE`
- required: `true`
- return:


### ROLE PHASE: STEWARD_FINAL

- role: `STEWARD`
- required: `true`
- return:


### ROLE PHASE: PERSONA_INTERFACE_RESPONSE

- role: `PERSONA_INTERFACE`
- required: `true`
- return:


## Final response rule

Only the `PERSONA_INTERFACE_RESPONSE` phase is user-facing. Internal machinery
may be summarized only when useful or requested.
