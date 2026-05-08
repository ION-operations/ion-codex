# ChatGPT Browser Connector Session Packet

## Carrier

- carrier_id: `CHATGPT_BROWSER_CARRIER`
- host_family: `chatgpt_browser`
- starting_level: `L1_COORDINATION_WITH_BOUNDED_CONNECTOR`
- production_authority: `false`
- live_execution_authority: `false`

## Shell Root Proof

- shell_root:
- `pyproject.toml` present:
- `ION/REPO_AUTHORITY.md` present:

## Correct Onboarding Sources

- current_operating_packet:
- carrier_profile:
- mount_contract:
- active_carrier_onboarding_packet:
- active_work_packet:
- active_carrier_turn_packet:
- active_role_spawn_plan:
- active_task_return_ledger:

## Single-Carrier Sandbox Fallback

If no connector, daemon, Cursor, Codex, or worker surface is available or authorized, `CHATGPT_BROWSER_CARRIER` remains a valid single LLM carrier. Scheduled `spawn=true` rows are executed sequentially in the same chat as bounded role-phase mounts: load the row's ContextPackage, return `### CONTEXT PROOF` and `### TEMPLATE ACTION PROOF`, record the return, then continue to the next row. Do not claim separate external workers or agents were spawned.

## Allowed Connector Operations

- read bounded ION state
- read current operating packet
- read active packets by allowlist
- request Codex work packets
- queue operator messages with bounded write confirmation
- record ChatGPT decisions as receipts
- submit task returns only with context proof and template-action proof

## Forbidden Connector Operations

- arbitrary shell
- arbitrary file write
- direct delete
- git push
- credential access
- provider API calls
- browser/computer control
- unbounded local filesystem access
- accepting unproofed worker output as current truth

## Required Return

```text
### CONTEXT PROOF
- root confirmed:
- current operating packet read:
- carrier profile read:
- mount contract read:
- active packets/context surfaces used:
- assumptions:

### TEMPLATE ACTION PROOF
- requested change:
- files changed:
- tests run:
- receipts/view models emitted:
- boundaries not crossed:

### RESULT
- implementation result:
- validation result:
- remaining blockers:
- next lawful move:
```
