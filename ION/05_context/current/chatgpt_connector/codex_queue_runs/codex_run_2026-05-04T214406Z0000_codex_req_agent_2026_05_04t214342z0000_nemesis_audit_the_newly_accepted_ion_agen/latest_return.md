### CONTEXT PROOF

Audit root: `/home/sev/ION - Production/ION_CODEX`. I did not claim ION/Steward/Relay/Persona/sovereign authority.

Required context read ledger:

| Path | Line/excerpt proof | sha256 |
|---|---|---|
| `...codex_work_requests/2026-05-04T214342Z0000_agent_nemesis...que.json` | lines 23-25 require proof-gated return; lines 99-103 require sections | `1dca576684d36a96e5c454df8c1786009fddf942c492715ee1f8cced5e8393fa` |
| `...codex_queue_runs/.../context_receipt.json` | lines 2-103 list every required read | `8c6dab269c2d0efa68849b90aa58cd11797abfa7518e09d6fe746d54a8d84a98` |
| `...agent_invocations/2026-05-04T214342Z0000_nemesis...json` | lines 87-92 one core/raw-output policy; lines 160-164 schema/status | `b5a8cc098d87096aab07a504067dbed728f9a409fc4792c7640406ca466eb78f` |
| `ION/03_registry/agent_roster_registry.yaml` | lines 113-140 define Nemesis audit lane/no source landing | `92f8852b1ebff1916c5313d6e82a6cd01569135f73f0ec7ce6a8f4aa3418f6d6` |
| `ION/03_registry/agent_context_system_registry.yaml` | lines 17-21 MINI/CAPSULE not primary; lines 63-75 Nemesis package | `0c9e8d86b55bcf310f85adabbdee3d4d7947a24c0ce05680b608d29d5466fd12` |
| `ION/03_registry/codex_cli_carrier_profile.yaml` | lines 15-21 no self-upgrade/proof gates; lines 28-31 return sections | `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6` |
| `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md` | lines 48-69 required return; lines 71-78 forbidden claims/actions | `463c8d944f4c29b1f0b9edc9dcdc23085d2ac39c4d2805bea1e21032cace3891` |
| `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md` | lines 27-42 one-core invariant; lines 363-381 agent broker slice | `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e` |
| `ION/04_packages/kernel/ion_codex_queue_runner.py` | lines 1-6 bounded owner; lines 551-565 submit through task-return intake | `ce8eb142fe50890c56fa90f6adbc916898c16f109fd860620336d648bfdb8a0b` |
| `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py` | lines 125-141 bounded tools; lines 1116-1178 task-return gate path | `a4b2d46aa5e6ec6aafbbd13c1d074a1df97733746a30f88308a530c2caff136d` |
| `ION/05_context/current/agent_context_systems/NEMESIS.context_system.md` | lines 5, 20, 28, 42 define governed audit/no overreach | `685127814d47c9312b944de43c33a4f0e8d0301ca4e19be03a7a4e6b2d041382` |
| `ION/03_registry/boots/NEMESIS.boot.md` | lines 27-29 no code/doctrine/commands; lines 53-61 do-not-write scope | `5c163168bb48c7001f3119b66b7141cb4bf99875d72ab7a1e334612707ebca83` |
| `ION/03_registry/semantic_identities/NEMESIS.semantic.yaml` | lines 5, 12-13 evidence-bound findings/no review upgrade | `526aee20b0bcfaf3be7a082e904fbcad2efa44d7067860fe3f36ce5f2818f099` |
| `ION/07_templates/bindings/NEMESIS__AUDIT.md` | lines 18-28 findings first/no mutation | `03ee57926749f1639c57c2b9ba46ed6c986dd28b9f6332bb4673b8e748bff6d6` |
| `ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md` | lines 59-68 context proof requirement | `931da654a6a9c1625da5e5348088c009004c09d2c70dda061d1534ae54437e6d` |
| `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` | lines 7-17 current Nemesis claimed state; lines 43-57 prior accepted return | `8ae147d6e5da88783891149607c630bc6063ea5ccf0deef11d7738844b4ca14f` |
| `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json` | lines 107-108 Sev callsign is not authority | `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae` |
| `ION/04_packages/kernel/ion_carrier_task_return.py` | lines 229-245 combine context/template gates before Steward review | `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28` |
| `ION/04_packages/kernel/ion_carrier_continue.py` | lines 401-414 require proof-gated task returns | `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f` |
| `ION/03_registry/chatgpt_browser_carrier_profile.yaml` | lines 4-7 Sev is carrier callsign only; lines 49-60 forbidden claims | `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181` |
| `ION/04_packages/kernel/ion_cockpit_view_model.py` | lines 383-406 project broker/runner into cockpit | `cdcabe13a1233cc3e5e19a7b2724225ab8964b18952aff896769bf5a8618808c` |

### TEMPLATE ACTION PROOF

template_id: `ion.template.autonomous_loop.local_worker.v1`  
action_id: `codex_queue_runner_process_once`

Files changed: none. This was a read-only audit.

Boundaries held: no git push, no deploy, no deletion, no secrets access, no source mutation. Role was mounted only through the supplied Nemesis boot/context/semantic/template evidence.

### VALIDATION

Ran focused read-only/status validation:

- `pytest ION/tests/test_kernel_ion_agent_invocation_broker.py ION/tests/test_kernel_ion_codex_queue_runner.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py ION/tests/test_kernel_ion_full_carrier_capability_audit.py -q -p no:cacheprovider`: `24 passed`.
- `kernel.ion_agent_invocation_broker --json`: broker reports `ION_AGENT_INVOCATION_BROKER_READY`, owner paths present, `no_parallel_agent_system_created: true`.
- `ps -fp 82526` and `/proc/82526`: no durable active process found during cross-check.
- Pure proof-gate probe: `evaluate_context_proof_return(receipt={...empty...})` accepted, which exposes a real intake weakness.

### RESULT

Findings:

1. High, `CARRIER_ADAPTER_FAILURE` with possible `ION_CORE_FAILURE` risk: proof-gated intake is not fully intact against an empty supplied context receipt. `ion_submit_task_return` only requires `context_receipt` to be a mapping, and `ion_context_proof_gate.py` accepts empty `required_paths` if the proof section is nonempty. The accepted repair return at `2026-05-04T214229Z0000_task_return.json` also shows `required_paths: []`. Raw output still goes through gates in the normal runner path, but the connector intake can be weakened by caller-supplied empty receipt data.

2. High, `DAEMON_FAILURE`: current runner state is not fully reconciled. The active queue still has the Nemesis request as `CLAIMED_BY_CODEX_QUEUE_RUNNER`, and run.json still says `CODEX_CLI_RUNNING` with pid `82526`, but no durable process/latest_return exists. The runner status uses PID existence only, so PID reuse can produce a false active signal.

3. Medium, `AGENT_INVOCATION_FAILURE`: failure-class vocabulary is split. Agent broker packets require `BACKEND_CODEX_FAILURE`, while queue runner status advertises `CODEX_CLI_FAILURE`. That should be normalized at the agent broker boundary.

4. Low, `AGENT_INVOCATION_FAILURE`: declared Nemesis context paths remain missing (`ION/agents/nemesis/MINI.md`, `ION/07_templates/reports/AUDIT.md`). Not a blocker for this bounded audit because the packet explicitly supplied operative evidence, but it blocks claiming full Nemesis continuity completeness.

Answer to core audit question: Sev/GPT Browser can invoke Codex-backed role agents without creating a parallel agent authority in the current design. The broker reuses existing queue, task-return, carrier-message, registry, and template owners. Do not start another queued swarm step yet. Next lawful move is a narrow reconciliation patch: bind task-return intake to the recorded run/work-request context receipt, reject empty receipts for work-request submissions, add stale active-run reconciliation with command/run-path verification, normalize backend failure classes, then run a prepare-only smoke before any bounded execution.