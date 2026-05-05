### CONTEXT PROOF

Carrier stance: Codex-backed worker only; no ION, Steward, Relay, Persona, sovereign, production, or live-execution authority claimed.

Receipt read: `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T220220Z0000_codex_req_agent_2026_05_04t220209z0000_vizier_analyze_the_next_architecture_slic/context_receipt.json` lines 2-107 list required reads; sha256 `648adbfdda6b7561fdec5b5a5c6b8cae36759da98e91744cbf6005dc4ffb4152`.

Required path evidence:

| Path | Evidence |
|---|---|
| `.../codex_work_requests/2026-05-04T220209Z0000_agent_vizier...json` | lines 2-7 VIZIER/Codex owner; lines 23-31 no production/live; sha256 `374821cb4085125a3b381a7558063c05370836523e9d4de5410420cdd87695bc` |
| `.../agent_invocations/2026-05-04T220209Z0000_vizier...json` | lines 72-90 distinguish Sev, Braden, one core, proof-gated raw output; sha256 `76d4d371b814da7d17f7c995584c6667097ffea218a53927827c20258feafc7f` |
| `ION/03_registry/agent_roster_registry.yaml` | lines 58-81 VIZIER role, activation owner, write scope; sha256 `92f8852b1ebff1916c5313d6e82a6cd01569135f73f0ec7ce6a8f4aa3418f6d6` |
| `ION/03_registry/agent_context_system_registry.yaml` | lines 37-49 VIZIER context system and templates; sha256 `0c9e8d86b55bcf310f85adabbdee3d4d7947a24c0ce05680b608d29d5466fd12` |
| `ION/03_registry/codex_cli_carrier_profile.yaml` | lines 17-24 proof gates/return module; lines 28-43 return sections/forbidden claims; sha256 `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6` |
| `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md` | lines 48-68 required return; lines 71-78 forbidden actions; sha256 `463c8d944f4c29b1f0b9edc9dcdc23085d2ac39c4d2805bea1e21032cace3891` |
| `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md` | lines 27-42 one-core carrier invariant; lines 350-381 queue/broker slice; sha256 `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e` |
| `ION/04_packages/kernel/ion_codex_queue_runner.py` | lines 1-7 no second work system/arbitrary shell; lines 194-225 runner status; lines 690-797 proof-gated worker return; sha256 `09a4b2669c890d3d6f822e7607dcff6106d666f82d8ae378b0e802c6164fe545` |
| `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py` | lines 95-154 tools and forbidden capabilities; lines 1116-1179 task-return gates; sha256 `55576cfc878e83f3d743636007b85bfc16fad8b75359c4ceaa5f917940ff490f` |
| `ION/05_context/current/agent_context_systems/VIZIER.context_system.md` | lines 5-9 governed context system/lane; lines 39-41 return contract; sha256 `8593359184dce2cdd6f73a6b08e31e3549af4d8010610e7bf21231da0a80fa0e` |
| `ION/03_registry/boots/VIZIER.boot.md` | lines 61-78 lane and do-not-write boundaries; lines 111-121 governance stack; sha256 `b19c88cd11282d2586c8c87bccba0361fed5b94ffa08d9209c56e7307b89e62a` |
| `ION/03_registry/semantic_identities/VIZIER.semantic.yaml` | lines 1-15 identity and constraints; sha256 `cf88ff9874297ea3d6711457d0d79f7edd31f366202de077fb55f356bbdfc2aa` |
| `ION/07_templates/bindings/STEWARD__PROPOSAL.md` | lines 14-21 recommendation vs landed truth; lines 23-27 authority boundaries; sha256 `7c69b685df2085c71cd6ce131fc23bd492b40e311c9a1c4d09dc59033c24b8c6` |
| `ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md` | lines 41-47 template action; lines 59-68 context proof requirement; sha256 `931da654a6a9c1625da5e5348088c009004c09d2c70dda061d1534ae54437e6d` |
| `ION/03_registry/daimon_matrix.yaml` | lines 58-62 engagement; lines 85-89 governance stack; sha256 `604e0fe0908aee67320497cff61d89b5479eeed6f5ce85c14454a6814fa0e0bb` |
| `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` | lines 1-18 current request claimed; lines 74-101 prior accepted automation/broker work; sha256 `e111ab2f5260cdb746ee3ea362a478972815dfd126388940912f5f184c084a22` |
| `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json` | lines 27-53 carrier smoke ack; lines 105-128 Sev callsign acknowledgement; sha256 `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae` |
| `ION/04_packages/kernel/ion_carrier_task_return.py` | lines 229-249 context/template gate evaluation; lines 281-299 Steward queue only after acceptance; sha256 `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28` |
| `ION/04_packages/kernel/ion_carrier_continue.py` | lines 1-18 continuation loop owners; lines 401-413 carrier next actions; sha256 `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f` |
| `ION/03_registry/chatgpt_browser_carrier_profile.yaml` | lines 1-7 Sev callsign only; lines 18-33 allowed/forbidden capabilities; sha256 `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181` |
| `ION/04_packages/kernel/ion_cockpit_view_model.py` | lines 339-411 ChatGPT MCP/queue/agent summary; lines 414-499 cockpit projection; sha256 `cdcabe13a1233cc3e5e19a7b2724225ab8964b18952aff896769bf5a8618808c` |

### TEMPLATE ACTION PROOF

template_id: `ion.template.autonomous_loop.local_worker.v1`  
action_id: `codex_queue_runner_process_once`  
requested change: bounded VIZIER architecture proposal only.  
files changed: none.  
boundaries not crossed: no git push, no deployment, no secret access, no deletion, no production/live authority, no mutation outside repo, no raw Codex output promoted to ION state.

### VALIDATION

Read-only validation performed: `sha256sum`, `nl -ba`, `rg`, `git status --short -- ION`, and `git diff --stat -- ION`.

No tests were run because this packet asked for analysis/proposal and explicitly discouraged mutation. `git status --short -- ION` and `git diff --stat -- ION` produced no ION-path changes from this run.

### RESULT

Proposal: the next slice should be a heartbeat-backed Codex queue autorun supervisor over existing owners, not a new agent system.

Sev should operate as the delegated ChatGPT Browser control-plane carrier: inspect cockpit/queues, invoke agents, step swarm work, poll/ack carrier messages, and record decisions through MCP tools. Sev should not become ION identity, sovereign authority, Steward integration, or a direct shell. Braden remains the human sovereign gate; Steward remains the integration membrane; Codex remains backend execution.

Persistent autorun should be local and bounded. Add a runner loop around existing `process_codex_queue_once`, with a single lease/lock, one active run guard, heartbeat timestamps, stale-pid reconciliation, and proof-gated task-return intake. It should write only under existing runtime/run owners such as `chatgpt_connector/runtime/` and `codex_queue_runs/`, and keep `ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` as the queue source of truth.

Alerts should surface through existing cockpit and carrier-message/human-gate queues. Sev gets operational alerts: heartbeat stale, daemon stopped, proof blocked, queue backlog, adapter mismatch, transport down, active run stale. Braden gets only true authority gates: production/live authority, destructive lifecycle transition, credential/secrets access, broad shell/process control, repeated backend failure threshold, or unresolved release/audit contradiction.

Failure classification for this slice: `AGENT_INVOCATION_FAILURE` for role/broker/context compile failures; `BACKEND_CODEX_FAILURE` for Codex backend output/proof failures; `CARRIER_ADAPTER_FAILURE` for MCP/browser/transport/tool exposure mismatches; `DAEMON_FAILURE` for heartbeat, stale PID, lock, or autorun lifecycle failures; `ION_CORE_FAILURE` only if core queue/proof/template owners are broken.

Next implementation packet: implement `codex_queue_autorun_heartbeat` as the narrow first slice. Touch only `ion_codex_queue_runner.py`, `ion_chatgpt_browser_mcp_connector_contract.py` if status projection needs adjustment, `ion_cockpit_view_model.py`, and focused tests. Do not add browser start/stop authority yet; expose status first, require an explicit human/operator gate for persistent service start.