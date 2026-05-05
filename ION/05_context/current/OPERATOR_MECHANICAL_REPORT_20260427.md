KERNEL_CALL:
- command: PYTHONPATH=ION/04_packages python3 -m kernel.ion_carrier_onboard --ion-root ION --carrier cursor --objective "Mechanical carrier: kernel packet then assigned role passes only; no chat route" --write-current --json
- success: true
- stdout/stderr or JSON: ION/05_context/current/LAST_KERNEL_ONBOARD_RAW.json (full JSON; also wrote ACTIVE_WORK_PACKET.json)

PACKET:
- role_phase_sequence: steward(required) -> vizier(required) -> mason(required) -> vice(optional) -> nemesis(optional) — see JSON field `role_phase_sequence`
- active_template: ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md
- next_lawful_action: After required_read_order, run: python3 -m kernel implementation "Mechanical carrier: kernel packet then assigned role passes only; no chat route"; require required_surfaces_ok: True in the printed trace. Then execute the first role pass (steward) using only required_reads for that pass.
- allowed_paths: ["ION/**"]
- forbidden_paths: ["secrets/**", "**/.env", "**/*credentials*", "production live execution outside bounded packet"]
- validation_commands: ["test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md", "python3 -m kernel implementation \"Mechanical carrier: kernel packet then assigned role passes only; no chat route\""]
- return_contract: Carrier returns a proposal: findings, touched paths, diffs or patch intent, risks, and receipt fields per ION_WORK_PACKET_TEMPLATE until Steward integrates.

ROLE_PASSES:
- role: steward | carrier/task: Cursor Task explore readonly | packet: ION/STEWARD/READ_ONLY pass1 from ACTIVE packet | result: PROPOSAL (Task agent 221f0357-d12e-445f-8468-2005757b9e63)
- role: vizier | carrier/task: Cursor Task explore readonly | packet: ION/VIZIER/READ_ONLY pass2 from ACTIVE packet | result: PROPOSAL (Task agent 2c4acfa4-482d-4bc0-86c4-d59f0b3f41eb)
- role: mason | carrier/task: Cursor Task explore readonly | packet: ION/MASON/READ_ONLY pass3 from ACTIVE packet | result: PROPOSAL (Task agent 9a408ee2-6f98-4556-b70f-55635ff53ea1)
- role: vice | carrier/task: Cursor Task explore readonly | packet: ION/VICE/READ_ONLY pass4 from ACTIVE packet | result: PROPOSAL (Task agent 2f30785e-49e5-4819-b89a-cb2ca07df491)
- role: nemesis | carrier/task: Cursor Task explore readonly | packet: ION/NEMESIS/READ_ONLY pass5 from ACTIVE packet | result: PROPOSAL (Task agent d5f61f69-da1d-46b6-8f85-4406e26916f0)

INTEGRATION:
- status: PENDING — proposals not merged; no Steward integration receipt written
- receipt/report path: this file; kernel trace ION/05_context/current/LAST_KERNEL_TRACE.txt; onboard JSON ION/05_context/current/LAST_KERNEL_ONBOARD_RAW.json; ACTIVE_WORK_PACKET.json refreshed same objective
