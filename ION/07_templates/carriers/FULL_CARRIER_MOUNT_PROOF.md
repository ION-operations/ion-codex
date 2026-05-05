# Full Carrier Mount Proof

## Carrier

- carrier_id:
- host_family:
- adapter_surface:
- target_parity_level:
- production_authority: false
- live_execution_authority: false

## Core Invariant

ION has one core engine. The carrier mounts the same ION packet, role, template,
proof-gate, receipt, and state engine as every other carrier.

## Root And Context Proof

- shell_root:
- `pyproject.toml` present:
- `ION/REPO_AUTHORITY.md` present:
- `ION/02_architecture/ION_MOUNT_CONTRACT.md` read:
- selected carrier profile:
- current operating packet:
- active work packet:
- execution packet template:

## Adapter Capability Proof

| capability_class | adapter_tool_or_surface | proof_path_or_command | verdict |
|---|---|---|---|
| mount_and_context | | | |
| status_and_state_visibility | | | |
| work_packet_creation | | | |
| file_artifact_transfer | | | |
| carrier_to_carrier_comms | | | |
| task_return_and_integration | | | |
| command_test_process_git | | | |

## Failure Classification

For every missing or failed capability, classify one:

```text
ION_CORE_FAILURE
CARRIER_ADAPTER_FAILURE
TRANSPORT_FAILURE
AUTH_OR_CONFIRMATION_FAILURE
CAPABILITY_NOT_YET_IMPLEMENTED
POLICY_BLOCK_WORKING_AS_DESIGNED
```

## Receipt Requirements

- action receipt template:
- task-return proof gate:
- no-silent-loss receipt:
- containment or rollback receipt when target already exists:
- human gate receipt for production/live authority:

## Verdict

FULL_CARRIER_MOUNT_PROOF_ACCEPTED / FULL_CARRIER_MOUNT_PROOF_BLOCKED
