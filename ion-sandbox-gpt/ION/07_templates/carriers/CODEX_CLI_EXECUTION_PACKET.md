# Codex CLI Execution Packet

## Carrier

- carrier_id: `CODEX_CLI_CARRIER`
- host_family: `codex_cli`
- starting_level: `L1_TOOL_ASSISTED`
- bounded_execution_level: `L2_BOUNDED_EXECUTION`
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
- chatgpt_connector_codex_work_request:
- operator_message:
- objective:

## Required Context Reads

- `ION/REPO_AUTHORITY.md`
- `ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md`
- `ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md`
- `ION/03_registry/codex_cli_carrier_profile.yaml`
- `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md`
- active packet/context package for the task
- files directly affected by the requested change

## Recommended Invocation Record

```text
codex_command:
prompt_path:
return_path:
event_log_path:
sandbox_mode:
approval_mode:
```

## Required Return

```text
### CONTEXT PROOF
- root confirmed:
- carrier profile used:
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
- Do not run unbounded host mutation.
- Do not push to git or deploy without explicit human gate.
- Do not summarize unaccepted worker returns as current truth.
- Do not attach receipts to UI bubbles by recency.
