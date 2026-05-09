carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    Final read-only Codex CLI carrier proof-contract smoke for Sev after exact TEMPLATE ACTION PROOF prompt repair. Read the required context receipt paths, do not edit files, do not delete, do not push git, do not access secrets, and return CONTEXT PROOF, TEMPLATE ACTION PROOF, VALIDATION, and RESULT. In TEMPLATE ACTION PROOF include template_id, action_id, result, and a non-empty touched_paths YAML list of repo-relative evidence paths inspected.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Reuse existing ION queue, task-return, carrier-message, and receipt owners."

required_context:
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T165019Z0000_final_read_only_codex_cli_carrier_proof_contract_smoke_for_sev_after_exact_templ.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/context_receipt.json"
  instruction: "Read the work request and every required path in the context receipt before writing."

return_contract:
  required_sections:
    - "### CONTEXT PROOF"
    - "### TEMPLATE ACTION PROOF"
    - "### VALIDATION"
    - "### RESULT"
  template_id: "ion.template.autonomous_loop.local_worker.v1"
  action_id_hint: "codex_queue_runner_process_once"
  template_action_proof_exact_shape: |
    ### TEMPLATE ACTION PROOF
    template_id: ion.template.autonomous_loop.local_worker.v1
    action_id: codex_queue_runner_process_once
    result: <one-line result>
    touched_paths:
      - <repo-relative evidence or changed path>
  context_proof_requirement: "Mention every required context path with line/excerpt/sha256 evidence."
  result_requirement: "State touched paths, tests, remaining blockers, and next lawful moves."
  touched_paths_requirement: "Under TEMPLATE ACTION PROOF, include touched_paths as a non-empty YAML list. For read-only/no-edit work, list the work request, run packet, context receipt, or repo-relative source/status files inspected."
  proof_rejection_warning: "Do not omit template_id, action_id, result, or touched_paths; [] and none are not accepted for touched_paths."
