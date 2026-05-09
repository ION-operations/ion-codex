carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    Read-only Codex CLI carrier loop proof-contract smoke for Sev after touched_paths prompt repair. Read the required context receipt paths, do not edit files, do not delete, do not push git, do not access secrets, and return the required proof sections with a non-empty touched_paths list naming repo-relative evidence paths inspected.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Reuse existing ION queue, task-return, carrier-message, and receipt owners."

required_context:
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T164636Z0000_read_only_codex_cli_carrier_loop_proof_contract_smoke_for_sev_after_touched_path.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/context_receipt.json"
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
  touched_paths_requirement: "Under TEMPLATE ACTION PROOF, include touched_paths as a non-empty YAML list. For read-only/no-edit work, list the work request, run packet, context receipt, or repo-relative source/status files inspected."
