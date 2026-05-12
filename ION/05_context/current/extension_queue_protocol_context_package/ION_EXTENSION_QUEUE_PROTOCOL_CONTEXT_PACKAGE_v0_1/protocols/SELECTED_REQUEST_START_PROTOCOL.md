# SELECTED_REQUEST_START_PROTOCOL

Start actions:
- `start_queue_head`
- `start_selected_request`

Rules:
- UI must distinguish both actions explicitly.
- Safe default for branch work is `start_selected_request`.
- `start_selected_request` requires selected request id/path to be present.
- Preflight panel must show: queue_type, request_id, request_path, agent_class, context_binding, authority, expected_proof.
