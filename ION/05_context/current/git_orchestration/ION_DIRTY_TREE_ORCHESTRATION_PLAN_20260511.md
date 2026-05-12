# ION Dirty Tree Orchestration Plan - 2026-05-11

Status: candidate orchestration record  
Production authority: false  
Live execution authority: false  
GitHub push authority: false  
Direct `main` authority: false  
Prepared from local inspection only. No commit, push, reset, checkout, cleanup, or validation run was performed in this pass.

## Purpose

Define how to handle the current dirty tree without losing ION evidence, without blessing runtime noise as canonical source, and without pushing mixed live state as trusted ION state.

This is a management and settlement plan. It is not an acceptance receipt for the code, UI, runtime artifacts, queue returns, or generated evidence.

## Current Git Posture

Repo root inspected:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

Current branch:

```text
feature/codex-capsule-chat-active-root
```

Upstream:

```text
origin/feature/codex-capsule-chat-active-root
```

Remote:

```text
https://github.com/ION-operations/ION.git
```

Ahead/behind before this document was added:

```text
0 ahead / 0 behind
```

Local dirty tree before this document was added:

```text
tracked modified: 62
untracked: 639
```

This document itself adds one more untracked file unless later staged.

## Existing ION Git Doctrine Found

Primary policy surfaces inspected:

```text
README.md
CONTRIBUTING.md
.github/PULL_REQUEST_TEMPLATE.md
ION/REPO_AUTHORITY.md
ION/docs/PUBLIC_REPO_NAVIGATION_AND_CLEANUP_PLAN.md
ION/docs/GITHUB_BRANCHING_AND_LIVE_STATE_POLICY.md
ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md
ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml
ION/03_registry/ion_chatops_extension_policy.yaml
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/STATUS.json
```

Rules confirmed:

- GitHub is a collaboration and data plane, not ION runtime authority.
- `Commit = Receipt`, `Diff = Proposed state delta`, `Branch = Alternate work trajectory`, `Pull request = Candidate transition awaiting review`.
- `main` is stable public landing branch. No direct push by default.
- Scoped review lanes exist: `docs/*`, `work/*`, `agent/*`, `data-plane/*`.
- `volatile/live-YYYYMMDD-<topic>` is valid for public live-state mirrors, but must be marked `VOLATILE / NOT TRUSTED ION STATE`.
- Volatile branches may include still-settling code, docs, non-secret evidence, and useful generated artifacts.
- Volatile branches must not contain secrets, credentials, tokens, cookies, private browser profiles, private connector auth state, private tunnel material, or private production infrastructure config.
- ChatOps policy explicitly forbids `git_push`.
- Extension policy explicitly sets `git_push_allowed: false` and forbids `push_main`.
- Later Git intents such as `create_github_branch_plan`, `request_git_diff`, `commit_branch`, `push_scoped_branch`, and `open_pull_request` are blocked until policy, tests, and receipts exist.
- Pull requests must identify branch trust class, touched paths, validation, evidence, blockers, and ION boundaries.

## Current Dirty Tree Shape

Tracked modified stat:

```text
62 files changed, 48373 insertions(+), 6361 deletions(-)
```

Untracked top-level counts before this document:

```text
614 ION
13 workpackets
11 diffs
1 what_is_ion
```

Untracked `ION/05_context/current` counts:

```text
344 chatgpt_connector
57 custom_gpt_capsule_system
32 extension_queue_protocol_context_package
30 codex_solo
24 helixion_joc_rebuild
17 chatops_bridge
11 browser_perception
10 context_settlement
7 action_surface_cartography
5 agent_context_branches
4 action_gateway
1 portable_ion_page_companion
1 custom_gpt_factory
1 ai_assistant_work
```

Untracked `chatgpt_connector` counts:

```text
183 codex_work_requests
78 codex_queue_runs
33 carrier_messages
21 task_returns
15 carrier_message_acks
7 agent_invocations
4 capsule_messages
1 probes
1 DAIMON_COMPANION_AGENT_LANE_UI_001_STATE.md
1 BOUNDED_AGENT_INVOCATION_RELAY_V1_STATE.md
```

Specific duplicate/no-receipt risk:

```text
158 untracked files match b00_carrier_worker_spawn_contract_repair_001
```

Interpretation:

The dirty tree is mixed. It contains source changes, generated extension bundles, JOC UI candidate work, kernel queue/gateway changes, tests, context package materialization, current Capsule/Mini state updates, live queue state, task returns, carrier message ledgers, imported workpackets, imported diffs, and likely duplicate B00 no-receipt/action-spam artifacts.

## Tracked Modified Lane Classification

Lane A - source and integration implementation:

```text
ION/04_packages/kernel/ion_agent_invocation_broker.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py
ION/04_packages/kernel/ion_chatops_bridge.py
ION/04_packages/kernel/ion_cockpit_view_model.py
ION/04_packages/kernel/ion_codex_chat_assets_ui.py
ION/04_packages/kernel/ion_codex_chat_left_drawer_ui.py
ION/04_packages/kernel/ion_codex_chat_shell_ui.py
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/04_packages/kernel/ion_codex_solo_context.py
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/04_packages/kernel/ion_dual_codex_chat.py
ION/04_packages/kernel/ion_local_cockpit_app.py
ION/04_packages/kernel/ion_skill_activation.py
```

Lane B - policy, registry, OpenAPI, and package metadata:

```text
ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
ION/03_registry/ion_skill_registry.yaml
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/000_READ_FIRST_MOUNT_ORDER.md
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/001_GPT_INSTRUCTIONS_PASTE.md
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/001_GPT_INSTRUCTIONS_PASTE_8K.md
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/002_KNOWLEDGE_UPLOAD_MANIFEST.json
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/060_ACTION_SCHEMAS/ACTION_SELECTION_AND_PROOF_MAP.md
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/090_VALIDATION/PACKAGE_MANIFEST.json
ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/090_VALIDATION/V2_6_VALIDATION_REPORT.md
ION/09_integrations/custom_gpt_action_gateway/README.md
ION/09_integrations/custom_gpt_action_gateway/openapi.yaml
```

Lane C - extension implementation and generated dist:

```text
ION/09_integrations/browser_extension/ion_chatops_bridge/README.md
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/background.js
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/background.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
```

Lane D - JOC / cockpit UI candidate:

```text
ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx
ION/08_ui/joc_cockpit_shell/ion-runtime-cockpit.css
ION/08_ui/joc_cockpit_shell/ionRuntimeCockpitTypes.ts
```

Lane E - tests:

```text
ION/tests/test_codex_project_config_and_hook.py
ION/tests/test_kernel_ion_agent_invocation_broker.py
ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py
ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py
ION/tests/test_kernel_ion_chatops_bridge_policy.py
ION/tests/test_kernel_ion_cockpit_view_model.py
ION/tests/test_kernel_ion_codex_queue_runner.py
ION/tests/test_kernel_ion_codex_solo_context.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py
ION/tests/test_kernel_ion_local_cockpit_app.py
```

Lane F - active state and runtime ledgers:

```text
ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json
ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json
ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-09T004941Z0000_prepare_a_bounded_ion_work_packet_report_for_the_next_local_ion_codex_or_role_ag.json
ION/05_context/current/chatgpt_connector/runtime/agent_invocation_broker_state.json
ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json
ION/05_context/current/codex_capsule_chat/state.json
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/LONG_HORIZON.json
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/ROUTE.json
ION/05_context/current/codex_solo/STATUS.json
```

Lane F is the highest-risk tracked lane because it mixes useful current continuity with live mutable state. It should not be staged together with source code without an explicit evidence intent.

## Untracked Lane Classification

Lane G - new architecture and registry candidates:

```text
ION/02_architecture/*.md
ION/03_registry/*.yaml
ION/03_registry/*.json
```

Known themes:

```text
Codex carrier limits
dAimon/JOC automation lineage
DOM perception
Helixion/JOC master evolution
agent branch capsule protocol
bounded agent invocation and relay
ChatOps mode visibility
multi-agent context/workpacket settlement
portable ION page companion
```

Lane H - new kernel helpers:

```text
ION/04_packages/kernel/ion_bounded_agent_lane_smoke.py
ION/04_packages/kernel/ion_cockpit_service_manager.py
```

Lane I - new JOC React shell files:

```text
ION/08_ui/joc_cockpit_shell/CodexCapsuleChatWorkbenchPanel.tsx
ION/08_ui/joc_cockpit_shell/DocsProjectsPackagesPanel.tsx
ION/08_ui/joc_cockpit_shell/ExtensionMicroShellPanel.tsx
ION/08_ui/joc_cockpit_shell/HelixionDevelopmentPanel.tsx
ION/08_ui/joc_cockpit_shell/HelixionEvolutionPanel.tsx
ION/08_ui/joc_cockpit_shell/LocalCockpitApp.tsx
ION/08_ui/joc_cockpit_shell/QueueGatewayCockpitPanel.tsx
ION/08_ui/joc_cockpit_shell/ServiceConsolePanel.tsx
ION/08_ui/joc_cockpit_shell/index.html
ION/08_ui/joc_cockpit_shell/main.tsx
ION/08_ui/joc_cockpit_shell/package-lock.json
ION/08_ui/joc_cockpit_shell/package.json
ION/08_ui/joc_cockpit_shell/tsconfig.json
ION/08_ui/joc_cockpit_shell/vite.config.ts
```

Lane J - durable context packages and receipts:

```text
ION/05_context/current/action_surface_cartography/
ION/05_context/current/agent_context_branches/
ION/05_context/current/ai_assistant_work/
ION/05_context/current/browser_perception/
ION/05_context/current/custom_gpt_capsule_system/
ION/05_context/current/custom_gpt_factory/
ION/05_context/current/extension_queue_protocol_context_package/
ION/05_context/current/helixion_joc_rebuild/
ION/05_context/current/portable_ion_page_companion/
ION/05_context/current/context_settlement/
```

Lane K - live connector/runtime evidence:

```text
ION/05_context/current/action_gateway/receipts/
ION/05_context/current/chatgpt_connector/agent_invocations/
ION/05_context/current/chatgpt_connector/capsule_messages/
ION/05_context/current/chatgpt_connector/carrier_message_acks/
ION/05_context/current/chatgpt_connector/carrier_messages/
ION/05_context/current/chatgpt_connector/codex_queue_runs/
ION/05_context/current/chatgpt_connector/codex_work_requests/
ION/05_context/current/chatgpt_connector/task_returns/
```

Lane L - external/imported workpackets and diffs:

```text
workpackets/
diffs/
what_is_ion/
```

Lane M - quarantine/no-receipt duplicate lane:

```text
ION/05_context/current/chatgpt_connector/codex_work_requests/*b00_carrier_worker_spawn_contract_repair_001*
```

There are 158 untracked B00 spawn-contract repair files. This is almost certainly retry/action-spam/no-receipt residue. It should be summarized and quarantined before any public branch mirror, not staged as ordinary evidence.

## Recommended Branch and Commit Strategy

Do not commit everything together.

Do not use:

```bash
git add .
```

Do not push directly to `main`.

Do not push from ChatOps/extension automation. Current policy forbids it.

Recommended path:

```text
1. Preserve the current working tree locally.
2. Build a staged path manifest for each lane.
3. Commit source lanes separately from evidence lanes.
4. Use a volatile branch only if we need immediate public visibility of mixed live state.
5. Promote cleaned lanes into review branches only after path manifests and evidence are reviewed.
```

Suggested volatile branch if immediate visibility is needed:

```text
volatile/live-20260511-chatgpt-actions-joc-daimon
```

Required label for that branch/PR:

```text
VOLATILE / NOT TRUSTED ION STATE
```

Suggested eventual review branches:

```text
work/chatgpt-action-gateway-auto-accept
work/codex-worker-spawn-contract
work/helixion-joc-shell-candidate
data-plane/context-package-settlement-20260511
data-plane/chatgpt-connector-evidence-20260511
docs/daimon-joc-orchestration-protocols
```

## Proposed Commit Slices

Slice 1 - Action Gateway and extension auto-accept source

Scope:

```text
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/09_integrations/custom_gpt_action_gateway/README.md
ION/09_integrations/custom_gpt_action_gateway/openapi.yaml
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/background.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/background.js
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/09_integrations/browser_extension/ion_chatops_bridge/README.md
ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
ION/tests/test_kernel_ion_custom_gpt_action_gateway.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py
ION/tests/test_kernel_ion_chatops_bridge_policy.py
```

Status:

```text
candidate source slice
requires diff review and targeted validation before push
```

Slice 2 - Worker spawn contract, return-template enforcement, and timeout reliability

Scope:

```text
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py
ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py
ION/04_packages/kernel/ion_agent_invocation_broker.py
ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml
ION/tests/test_kernel_ion_codex_queue_runner.py
ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py
ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py
ION/tests/test_kernel_ion_agent_invocation_broker.py
```

Status:

```text
candidate source slice
aligns with C-088 and C-091 capsule entries
requires proof that worker returns lint locally before task-return intake
```

Slice 3 - Codex solo context and skill activation continuity

Scope:

```text
ION/04_packages/kernel/ion_codex_solo_context.py
ION/04_packages/kernel/ion_skill_activation.py
ION/03_registry/ion_skill_registry.yaml
ION/tests/test_codex_project_config_and_hook.py
ION/tests/test_kernel_ion_codex_solo_context.py
```

Optional evidence, only if intentionally included:

```text
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/LONG_HORIZON.json
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/ROUTE.json
ION/05_context/current/codex_solo/STATUS.json
```

Status:

```text
source and continuity mixed
context files require intentional evidence treatment
```

Slice 4 - Helixion/JOC cockpit UI candidate

Scope:

```text
ION/04_packages/kernel/ion_cockpit_view_model.py
ION/04_packages/kernel/ion_local_cockpit_app.py
ION/04_packages/kernel/ion_codex_chat_assets_ui.py
ION/04_packages/kernel/ion_codex_chat_left_drawer_ui.py
ION/04_packages/kernel/ion_codex_chat_shell_ui.py
ION/08_ui/joc_cockpit_shell/
ION/tests/test_kernel_ion_cockpit_view_model.py
ION/tests/test_kernel_ion_local_cockpit_app.py
```

Status:

```text
candidate UI slice
must remain marked candidate until visually reviewed against JOC drawer/page canon
```

Slice 5 - Bounded agent lane

Scope:

```text
ION/02_architecture/ION_BOUNDED_AGENT_INVOCATION_AND_RELAY_PROTOCOL.md
ION/03_registry/ion_agent_invocation_packet.schema.json
ION/03_registry/ion_agent_relay_message.schema.json
ION/03_registry/ion_agent_relay_response.schema.json
ION/03_registry/ion_bounded_agent_role_registry.yaml
ION/04_packages/kernel/ion_bounded_agent_lane_smoke.py
ION/05_context/current/chatgpt_connector/BOUNDED_AGENT_INVOCATION_RELAY_V1_STATE.md
ION/05_context/current/chatgpt_connector/DAIMON_COMPANION_AGENT_LANE_UI_001_STATE.md
```

Status:

```text
candidate protocol/source/evidence mixed
split implementation from runtime evidence when possible
```

Slice 6 - Durable product/context package lane

Scope:

```text
ION/02_architecture/CODEX_CARRIER_LIMITS_CONTEXT_PROTOCOL.md
ION/02_architecture/DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS.md
ION/02_architecture/DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN.md
ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md
ION/02_architecture/HELIXION_JOC_ORCHESTRATION_WORKFLOW_PROTOCOL.md
ION/02_architecture/ION_AGENT_BRANCH_CAPSULE_PROTOCOL_V0_1.md
ION/02_architecture/ION_CHATOPS_MODE_VISIBILITY_PROTOCOL.md
ION/02_architecture/ION_MULTI_AGENT_CONTEXT_AND_WORKPACKET_SETTLEMENT_PROTOCOL_V0_1.md
ION/02_architecture/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.md
ION/03_registry/browser_perception_agent_roster_proposal.yaml
ION/03_registry/browser_perception_domain_registry_proposal.yaml
ION/03_registry/codex_carrier_limits_registry.yaml
ION/03_registry/helixion_joc_evolution_registry.yaml
ION/03_registry/portable_ion_page_companion_registry.yaml
ION/05_context/current/action_surface_cartography/
ION/05_context/current/agent_context_branches/
ION/05_context/current/browser_perception/
ION/05_context/current/custom_gpt_capsule_system/
ION/05_context/current/custom_gpt_factory/
ION/05_context/current/extension_queue_protocol_context_package/
ION/05_context/current/helixion_joc_rebuild/
ION/05_context/current/portable_ion_page_companion/
ION/05_context/current/context_settlement/
```

Status:

```text
candidate context package lane
should be reviewed as doctrine/context, not source runtime
```

Slice 7 - Live runtime evidence lane

Scope:

```text
ION/05_context/current/action_gateway/receipts/
ION/05_context/current/chatgpt_connector/agent_invocations/
ION/05_context/current/chatgpt_connector/capsule_messages/
ION/05_context/current/chatgpt_connector/carrier_message_acks/
ION/05_context/current/chatgpt_connector/carrier_messages/
ION/05_context/current/chatgpt_connector/codex_queue_runs/
ION/05_context/current/chatgpt_connector/codex_work_requests/
ION/05_context/current/chatgpt_connector/task_returns/
ION/05_context/current/chatgpt_connector/runtime/
ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json
```

Status:

```text
evidence only
do not mix into source commits
do not push unless redacted/public-safe and intentionally marked volatile or evidence
```

Slice 8 - Imported diffs and workpackets

Scope:

```text
diffs/
workpackets/
what_is_ion/
```

Status:

```text
inbox/import lane
must be ingested or referenced by manifest before staging
```

## Quarantine Rules

Quarantine before staging:

```text
ION/05_context/current/chatgpt_connector/codex_work_requests/*b00_carrier_worker_spawn_contract_repair_001*
```

Reason:

```text
158 duplicate/no-receipt-like files exist.
```

Required handling:

```text
1. Select the canonical accepted or most complete request, if one exists.
2. Preserve one compact summary receipt for duplicate action/no-receipt behavior.
3. Mark the rest as local noise or move to an archive/quarantine lane only after explicit approval.
4. Do not stage all duplicates into source or context package commits.
```

## Candidate `.gitignore` Discussion

Current `.gitignore` already excludes common runtime/log/cache noise and explicitly allows browser extension `dist/`.

Do not blindly ignore all `ION/05_context/current/chatgpt_connector/` because some files are useful public evidence.

Candidate future ignore or archive policy:

```text
chatgpt_connector/codex_queue_runs/ -> usually local runtime evidence, commit only selected proof runs
chatgpt_connector/codex_work_requests/ -> commit only canonical packets or compact manifests
chatgpt_connector/carrier_messages/ -> commit only selected settlement/proof traces
chatgpt_connector/carrier_message_acks/ -> commit only selected settlement/proof traces
chatgpt_connector/task_returns/ -> commit accepted/proof-blocked returns only when intentionally evidence
```

Better than a broad ignore:

```text
generate a dated public-safe evidence manifest
commit the manifest plus selected receipts
keep bulk live residue local or volatile-only
```

## Secret and Safety Gate Before Any Push

Before any branch push or PR, run a bounded secret/public-safety scan over staged paths only.

Refuse staging if paths contain:

```text
tokens
cookies
credentials
private browser profiles
private connector auth state
live tunnel credentials
.env files
private production infrastructure config
```

This is especially important for:

```text
ION/05_context/current/chatgpt_connector/
ION/05_context/current/action_gateway/
workpackets/
diffs/
```

## Immediate Operational Recommendation

Current best move:

```text
do not push yet
do not commit a monolithic snapshot
do not clean or delete files yet
create staged path manifests per slice
review the source slices first
quarantine duplicate B00 no-receipt artifacts before evidence staging
```

If the operator needs GitHub visibility now:

```text
create volatile/live-20260511-chatgpt-actions-joc-daimon
commit only reviewed public-safe lanes
label it VOLATILE / NOT TRUSTED ION STATE
do not represent it as accepted ION state
```

If the operator wants clean promotion:

```text
prepare separate review branches for source, UI, context packages, and evidence
open PRs with branch trust class and evidence fields
preserve runtime residue locally until summarized
```

## Next Work Packet Recommendation

Recommended next packet:

```text
GIT_SETTLEMENT_001_STAGE_MANIFESTS_AND_QUARANTINE_PLAN
```

Objective:

```text
Build machine-readable stage manifests for each lane without staging files, identify duplicate/no-receipt artifacts, and propose exact commit boundaries.
```

Authority:

```text
analysis_only
no git add
no commit
no push
no delete
no reset
```

Outputs:

```text
ION/05_context/current/git_orchestration/GIT_STAGE_MANIFEST_SOURCE_AUTO_ACCEPT_20260511.json
ION/05_context/current/git_orchestration/GIT_STAGE_MANIFEST_WORKER_SPAWN_CONTRACT_20260511.json
ION/05_context/current/git_orchestration/GIT_STAGE_MANIFEST_JOC_UI_CANDIDATE_20260511.json
ION/05_context/current/git_orchestration/GIT_STAGE_MANIFEST_CONTEXT_PACKAGES_20260511.json
ION/05_context/current/git_orchestration/GIT_STAGE_MANIFEST_RUNTIME_EVIDENCE_20260511.json
ION/05_context/current/git_orchestration/GIT_QUARANTINE_DUPLICATE_B00_NO_RECEIPT_20260511.md
```

Stop condition:

```text
operator reviews manifests and approves exact staging/commit path
```

## Final Posture

The tree is recoverable, but it must be treated as a multi-lane ION settlement problem, not a normal dirty Git tree.

The source work appears separable into useful candidate slices. The dangerous part is the live runtime evidence and duplicate action residue. Those must be either summarized, quarantined, or placed on a clearly marked volatile branch, never mixed into a source commit by accident.
