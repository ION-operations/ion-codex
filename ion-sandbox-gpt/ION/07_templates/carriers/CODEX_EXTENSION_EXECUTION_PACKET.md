# Codex Extension Execution Packet

## Carrier

- carrier_id: `CODEX_EXTENSION_CARRIER`
- host_family: `codex_extension`
- starting_level: `L1_TOOL_ASSISTED`
- production_authority: `false`
- live_execution_authority: `false`

## Shell Root Proof

- shell_root:
- `pyproject.toml` present:
- `ION/REPO_AUTHORITY.md` present:

## Active ION Packet

- active_work_packet:
- active_turn_packet:
- active_spawn_plan:
- operator_message:
- objective:

## Required Context Reads

- `ION/REPO_AUTHORITY.md`
- `ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md`
- `ION/03_registry/codex_extension_carrier_profile.yaml`
- `ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md`
- active packet/context package for the task
- files directly affected by the requested change

## Required Return

```text
### CONTEXT PROOF
- root confirmed:
- files read:
- active packet/context package used:
- assumptions:

### TEMPLATE ACTION PROOF
- requested change:
- files changed:
- tests run:
- receipts/view models emitted:
- boundaries not crossed:

### RESULT
- implementation result:
- remaining blockers:
- next lawful move:
```

## Forbidden

- Do not claim ION identity.
- Do not claim STEWARD/RELAY/PERSONA authority.
- Do not claim host subagents unless the host exposes and records them.
- Do not summarize unaccepted worker returns as current truth.
- Do not attach receipts to UI bubbles by recency.
