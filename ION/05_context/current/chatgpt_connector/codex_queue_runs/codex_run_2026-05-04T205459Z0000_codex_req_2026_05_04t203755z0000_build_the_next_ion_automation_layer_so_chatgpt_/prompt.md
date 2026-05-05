carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    Build the next ION automation layer so ChatGPT Browser can operate the local ION/Codex carrier loop from MCP without the operator manually relaying 'proceed' to Codex. Treat this as full carrier parity infrastructure, not a restricted observer lane. First inspect existing owners before writing: ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json, chatgpt_connector/codex_work_requests, chatgpt_connector/task_returns, carrier message queue, ion_carrier_task_return, ion_carrier_continue, MCP connector implementation, full-carrier parity protocol, carrier profiles, cockpit/status projection, and any existing daemon/loop/autonomous loop/supervisor surfaces. Reuse existing queue/task-return/carrier-message owners; do not invent a parallel work system. Desired outcome: a local ION carrier daemon/supervisor or runner that can poll queued Codex work requests, invoke Codex CLI or the appropriate local carrier command non-interactively with the packet context, capture stdout/stderr/result, enforce CONTEXT PROOF and TEMPLATE ACTION PROOF return format, submit/record task returns, update queue status, emit receipts, expose daemon status through MCP/cockpit, and classify failures as CARRIER_ADAPTER_FAILURE, CODEX_CLI_FAILURE, DAEMON_FAILURE, or ION_CORE_FAILURE. Also propose MCP tools if needed: ion_daemon_status, ion_daemon_start, ion_daemon_stop, ion_codex_queue_process_once, ion_codex_queue_autorun_status, ion_codex_queue_autorun_start, ion_codex_queue_autorun_stop. Implement the narrowest useful slice if safe: at minimum queue-process-once or daemon-status plus tests; ideally an autorun loop that processes QUEUED_FOR_CODEX_CARRIER packets without user relay. Validate with kernel.ion_status, focused tests, full-carrier capability audit, and a smoke work request if possible. Return with CONTEXT PROOF, TEMPLATE ACTION PROOF, touched paths, validation, whether manual 'proceed' is still required, remaining blockers, and next lawful moves.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Reuse existing ION queue, task-return, carrier-message, and receipt owners."

required_context:
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T203755Z0000_build_the_next_ion_automation_layer_so_chatgpt_browser_can_operate_the_local_ion.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T205459Z0000_codex_req_2026_05_04t203755z0000_build_the_next_ion_automation_layer_so_chatgpt_/context_receipt.json"
  instruction: "Read the work request and every required path in the context receipt before writing."

return_contract:
  required_sections:
    - "### CONTEXT PROOF"
    - "### TEMPLATE ACTION PROOF"
    - "### VALIDATION"
    - "### RESULT"
  template_id: "ion.template.autonomous_loop.local_worker.v1"
  action_id_hint: "codex_queue_runner_process_once"
  context_proof_requirement: "Mention every required context path with line/excerpt/sha256 evidence."
  result_requirement: "State touched paths, tests, remaining blockers, and next lawful moves."
