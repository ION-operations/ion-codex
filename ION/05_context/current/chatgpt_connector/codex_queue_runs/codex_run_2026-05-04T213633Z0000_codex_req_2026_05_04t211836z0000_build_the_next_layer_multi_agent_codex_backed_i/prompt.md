carrier_mount:
  title: "ION Codex Queue Runner Work Packet"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    Build the next layer: multi-agent Codex-backed ION swarm control from Sev/GPT Browser over MCP. Do not create a separate agent system; build an ION agent invocation broker over existing owners: ion_codex_queue_runner.py, ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json, codex_work_requests, task_returns, carrier messages, agent_roster_registry.yaml, codex_cli_carrier_profile.yaml, CODEX_CLI_EXECUTION_PACKET.md, context/template proof gates, and full-carrier MCP parity protocol. Desired model: Sev calls ION to invoke a role/agent, ION compiles context/template/return contract, local runner invokes Codex CLI as backend execution substrate, return is captured/proof-gated/receipted, and cockpit/queue state records which role/backend/carrier did what. Design and implement the narrowest strong slice for swarm control. Candidate tools/surfaces: ion_agent_invoke, ion_agent_status, ion_agent_result, ion_agent_cancel, ion_agent_list, ion_agent_queue, ion_agent_spawn_plan, ion_swarm_status, ion_swarm_step_once. Support multiple role packets such as MASON, VIZIER, NEMESIS, STEWARD-review/proposal, TEMPLATE_CURATOR, CONTEXT_CARTOGRAPHER using existing role/context surfaces. Distinguish human sovereign Braden, Sev delegated operator carrier, ION core engine, Steward integration membrane, and Codex-backed workers. Ensure no raw Codex output becomes state without proof gates. Include failure classes: AGENT_INVOCATION_FAILURE, BACKEND_CODEX_FAILURE, CARRIER_ADAPTER_FAILURE, DAEMON_FAILURE, ION_CORE_FAILURE. Validate with kernel.ion_status, focused tests, tool manifest/audit, and at least one smoke invocation in prepare-only or bounded execution mode. Return with CONTEXT PROOF, TEMPLATE ACTION PROOF, touched paths, validations, new tools exposed if any, remaining blockers, and next lawful moves.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Reuse existing ION queue, task-return, carrier-message, and receipt owners."

required_context:
  work_request_path: "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T211836Z0000_build_the_next_layer_multi_agent_codex_backed_ion_swarm_control_from_sev_gpt_bro.json"
  context_receipt_path: "ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T213633Z0000_codex_req_2026_05_04t211836z0000_build_the_next_layer_multi_agent_codex_backed_i/context_receipt.json"
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
