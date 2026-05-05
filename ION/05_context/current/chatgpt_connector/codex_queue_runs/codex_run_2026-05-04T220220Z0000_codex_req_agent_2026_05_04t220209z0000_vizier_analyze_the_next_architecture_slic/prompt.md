carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    ION agent invocation for VIZIER (role.vizier) via Codex CLI backend.

Invariant: ION has one core engine mounted by all carriers. ChatGPT Browser/Sev is a full ION carrier target, not an observer-only lane.
Distinguish human sovereign Braden, Sev as delegated operator carrier/callsign, ION core engine, Steward integration membrane, and Codex-backed worker.
This is a role/context packet compiled by the ION agent invocation broker; it is not a separate agent system.

Invocation packet: ION/05_context/current/chatgpt_connector/agent_invocations/2026-05-04T220209Z0000_vizier_analyze_the_next_architecture_slice_for_ion_swarm_control_after_the_42_to.json
Requested mode: queued
Original objective: Analyze the next architecture slice for ION swarm control after the 42-tool MCP agent invocation broker and stale-runner reconciliation. Focus on how Sev should operate as delegated browser control-plane carrier, how persistent autorun/heartbeat should be added without creating duplicate authority, how alerts/gates should surface to Sev and Braden, and what the next implementation packet should be. Produce a bounded proposal only; do not mutate project files unless required by the invocation protocol.

Backend and proof rules:
- Mount the requested role only through the supplied boot/context/template evidence.
- Do not claim to be ION, sovereign authority, or production authority.
- Do not let raw Codex output become ION state except through the existing task-return proof gates.
- Return must include CONTEXT PROOF, TEMPLATE ACTION PROOF, VALIDATION, and RESULT sections.
- Classify failures as AGENT_INVOCATION_FAILURE, BACKEND_CODEX_FAILURE, CARRIER_ADAPTER_FAILURE, DAEMON_FAILURE, or ION_CORE_FAILURE.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Reuse existing ION queue, task-return, carrier-message, and receipt owners."

required_context:
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T220209Z0000_agent_vizier_analyze_the_next_architecture_slice_for_ion_swarm_control_after_the.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T220220Z0000_codex_req_agent_2026_05_04t220209z0000_vizier_analyze_the_next_architecture_slic/context_receipt.json"
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
