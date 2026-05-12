# EXTENSION_QUEUE_REGISTRY_PROTOCOL

Defines registry rows for every queue surfaced in extension cockpit.

Required queue types:
- `codex_work_queue`
- `browser_self_queue`
- `carrier_message_queue`
- `action_approval_receipt_queue`
- `agent_invocation_queue`
- `branch_carrier_message_queue`

Rules:
- Queue registry is descriptive view state, not authority state.
- Each queue row carries: queue_type, owner_path, source_of_truth_path, status, visibility_profile, redaction_profile.
- Registry rows include `agent_class_scope` with allowed classes: capsule_context_bound, full_ion_orchestration, codex_cli_worker, local_ops_daemon.
