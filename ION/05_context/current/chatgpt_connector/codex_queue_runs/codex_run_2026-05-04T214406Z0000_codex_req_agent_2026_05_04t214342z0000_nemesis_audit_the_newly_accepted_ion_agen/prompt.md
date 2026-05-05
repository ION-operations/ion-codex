carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    ION agent invocation for NEMESIS (role.nemesis) via Codex CLI backend.

Invariant: ION has one core engine mounted by all carriers. ChatGPT Browser/Sev is a full ION carrier target, not an observer-only lane.
Distinguish human sovereign Braden, Sev as delegated operator carrier/callsign, ION core engine, Steward integration membrane, and Codex-backed worker.
This is a role/context packet compiled by the ION agent invocation broker; it is not a separate agent system.

Invocation packet: ION/05_context/current/chatgpt_connector/agent_invocations/2026-05-04T214342Z0000_nemesis_audit_the_newly_accepted_ion_agent_invocation_broker_and_codex_queue_run.json
Requested mode: queued
Original objective: Audit the newly accepted ION agent invocation broker and Codex queue runner slice. Focus on whether Sev/GPT Browser can invoke Codex-backed role agents without creating a parallel agent authority, whether proof-gated intake remains intact, whether blocked runner state from the earlier process-once return is fully reconciled, and what the next safe swarm-control step should be. Do not mutate code unless explicitly required by the audit surface; produce findings and next lawful moves.

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
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T214342Z0000_agent_nemesis_audit_the_newly_accepted_ion_agent_invocation_broker_and_codex_que.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T214406Z0000_codex_req_agent_2026_05_04t214342z0000_nemesis_audit_the_newly_accepted_ion_agen/context_receipt.json"
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
