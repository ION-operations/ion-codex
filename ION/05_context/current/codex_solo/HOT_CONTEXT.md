# Codex Solo HOT_CONTEXT

generated_at: 2026-05-08T21:30:44+00:00
witness_policy: Capsule is the minimum working context. Mini is a lookup/receipt index for capsule history. Neither overrides current repo authority, tests, receipts, or explicit operator instructions.
production_authority: false
live_execution_authority: false

## MINIMUM WORKING CAPSULE

# Codex Solo Capsule

> Minimum working context for the standalone Codex chat lane. Load this before general Codex work. Mini is only lookup/index; detailed work stays in normal artifacts.

| # | Date | Summary | Evidence | Status |
|---|------|---------|----------|--------|
| C-001 | 2026-05-07 | Implemented capsule-first Codex solo context: Capsule is minimum working context; Mini is lookup/receipt index. | `ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md` | IMPLEMENTED |
| C-002 | 2026-05-07 | Implemented multi-horizon Codex solo context: long-horizon capsule epochs and explicit context package selector. | `ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/05_context/current/codex_solo/LONG_HORIZON.json, ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json` | IMPLEMENTED |
| C-003 | 2026-05-07 | Implemented project-scoped Codex CLI capsule boot setup with read-only session hook, optional local ION MCP read/status tools, and explicit post receipt helper. | `.codex/config.toml, .codex/hooks/ion_session_start_context.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_codex_project_config_and_hook.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md` | IMPLEMENTED |
| C-004 | 2026-05-07 | Implemented Codex CLI model moves and Mini auto-post for dual chat | `ION/04_packages/kernel/ion_codex_model_moves.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_queue_runner.py, ION/03_registry/codex_cli_model_move_policy.yaml, ION/tests/test_kernel_ion_codex_model_moves.py` | IMPLEMENTED |
| C-005 | 2026-05-07 | Implemented public cockpit login with signed sessions, permission tokens, and Google OAuth hooks | `ION/04_packages/kernel/ion_public_cockpit_auth.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py, ION/tests/test_kernel_ion_public_cockpit_auth.py, ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md` | IMPLEMENTED |
| C-006 | 2026-05-07 | Updated cockpit login password and pre-allowed crinkedart Google account | `/home/sev/.config/systemd/user/ion-mcp-preview.service.d/cockpit-token.conf, ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py, ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py` | IMPLEMENTED |
| C-007 | 2026-05-07 | Rebuilt dual Codex chat into JOC-style cockpit workbench with command rail and context drawers | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CLI_CARRIER_AND_COCKPIT_PASS_20260507.md` | IMPLEMENTED |
| C-008 | 2026-05-07 | Added Codex Capsule Operating Protocol: Capsule ION is the minified fallback/basic ops kernel while full ION Codex CLI chat is rebuilt. | `ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md, ION/04_packages/kernel/ion_codex_solo_context.py` | CORRECTED |
| C-009 | 2026-05-07 | Corrected Codex chat product direction to one Capsule Codex chat with bounded full-ION comms adapter. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md, ION/tests/test_kernel_ion_dual_codex_chat.py` | CORRECTED |
| C-010 | 2026-05-07 | Added opt-in chat execution bridge from Codex Capsule chat turns to existing Codex work queue. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_local_cockpit_app.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md, ION/tests/test_kernel_ion_dual_codex_chat.py` | IMPLEMENTED |
| C-011 | 2026-05-07 | Wrote Codex Capsule Chat app UI orchestration for a chat-first JOC/ION-inspired app. | `ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md, ION/04_packages/kernel/ion_codex_solo_context.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_kernel_ion_dual_codex_chat.py` | PLANNED |
| C-012 | 2026-05-07 | Implemented chat-first Codex Capsule app UI model and Python-rendered shell. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-013 | 2026-05-07 | Added Codex return/proof hydration into the Codex Capsule chat timeline. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-014 | 2026-05-07 | Added transparent per-turn trace and agent broker visibility to Codex Capsule chat. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CAPSULE_TRACE_AND_AGENT_TRANSPARENCY_ORCHESTRATION_20260507.md, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-015 | 2026-05-07 | Corrected Codex chat UI language and composer flow after operator confusion. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CHAT_UI_RECOVERY_ORCHESTRATION_20260507.md, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | CORRECTED |
| C-016 | 2026-05-07 | Extracted active Codex Chat app shell into dedicated UI renderer module. | `ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CHAT_APP_SHELL_COMPONENTIZATION_20260507.md, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-017 | 2026-05-07 | Removed obsolete in-file Codex chat HTML/CSS renderer blocks after UI extraction. | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CHAT_APP_SHELL_COMPONENTIZATION_20260507.md, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-018 | 2026-05-07 | Improved Codex Chat Timeline and Agents drawers from existing trace and broker data. | `ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/CODEX_CHAT_TIMELINE_AGENTS_DRAWER_PASS_20260507.md, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-019 | 2026-05-08 | Implemented ION skill activation layer for Codex Chat: skills activate workflows while templates remain proof gates. | `ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md, ION/03_registry/ion_skill_registry.yaml, ION/04_packages/kernel/ion_skill_activation.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/tests/test_kernel_ion_skill_activation.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/05_context/current/codex_cli/CODEX_SKILL_ACTIVATION_IMPLEMENTATION_20260507.md` | IMPLEMENTED |
| C-020 | 2026-05-08 | Implemented Codex Chat Engine core: response modes, native ION lenses, GPT-5.5 chat route, and queue metadata handoff. | `ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md, ION/03_registry/ion_native_lens_registry.yaml, ION/04_packages/kernel/ion_codex_chat_engine.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py, ION/04_packages/kernel/ion_codex_queue_runner.py, ION/tests/test_kernel_ion_codex_chat_engine.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_queue_runner.py, ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py, ION/05_context/current/codex_cli/CODEX_CHAT_ENGINE_IMPLEMENTATION_20260508.md` | IMPLEMENTED |
| C-021 | 2026-05-08 | Implemented ION Codex Chat Engine layer: user turns now route through context mount, skill activation, native lenses, model move, response mode, and existing Codex queue carrier metadata. | `ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md, ION/03_registry/ion_native_lens_registry.yaml, ION/04_packages/kernel/ion_codex_chat_engine.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py, ION/04_packages/kernel/ion_codex_queue_runner.py, ION/tests/test_kernel_ion_codex_chat_engine.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_queue_runner.py, ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py, ION/05_context/current/codex_cli/CODEX_CHAT_ENGINE_IMPLEMENTATION_20260508.md` | IMPLEMENTED |
| C-022 | 2026-05-08 | Planned next Codex Chat step: real GPT-5.5 Codex CLI response carrier for respond-only chat turns under the existing Capsule/skill/native-lens engine. | `ION/05_context/current/codex_cli/CODEX_CHAT_RESPONSE_CARRIER_ORCHESTRATION_20260508.md, ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_queue_runner.py` | PLANNED |
| C-023 | 2026-05-08 | Implemented Codex Chat response carrier: respond-only chat turns can use Codex CLI final messages under the Capsule/skill/native-lens engine, with fallback, trace events, artifacts, and drift detection. | `ION/04_packages/kernel/ion_codex_chat_response_carrier.py, ION/tests/test_kernel_ion_codex_chat_response_carrier.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/05_context/current/codex_cli/CODEX_CHAT_RESPONSE_CARRIER_IMPLEMENTATION_20260508.md, ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T140124Z968157_live_carrier_smoke_reply_with_one_concise_sentence_naming_the_current_ca/run.json, ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T140124Z968157_live_carrier_smoke_reply_with_one_concise_sentence_naming_the_current_ca/latest_r` | IMPLEMENTED |
| C-024 | 2026-05-08 | Enabled Codex Chat response carrier in the user service and verified authenticated cockpit chat turn captured a real GPT-5.5 Codex final message with no unexpected worktree drift. | `ION/05_context/current/codex_cli/CODEX_CHAT_RESPONSE_CARRIER_SERVICE_ENABLEMENT_20260508.md, /home/sev/.config/systemd/user/ion-mcp-preview.service.d/cockpit-token.conf, ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T143135Z679115_authenticated_cockpit_carrier_smoke_answer_in_one_concise_sentence_with_/run.json, ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T143135Z679115_authenticated_cockpit_carrier_smoke_answer_in_one_concise_sentence_with_/latest_r` | IMPLEMENTED |
| C-025 | 2026-05-08 | Fixed cockpit chat pending-state UX: optimistic user bubble, Codex loading bubble, textarea clear, disabled submit controls, duplicate-submit guard, JSON fetch response handling, and execution-status rendering. | `ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py, ION/05_context/current/codex_cli/CODEX_CHAT_PENDING_STATE_UX_FIX_20260508.md` | IMPLEMENTED |
| C-026 | 2026-05-08 | Installed Playwright package and added opt-in live cockpit browser smoke proving chat submit clears immediately, shows pending Codex response state, blocks duplicate submit, and captures the real response carrier output. | `ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json, ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py, ION/05_context/current/codex_cli/CODEX_CHAT_PENDING_STATE_UX_FIX_20260508.md` | IMPLEMENTED |
| C-027 | 2026-05-08 | Planned the next Codex Capsule Chat rewrite around JOC shell regions, Victus Contextual Matryoshka, Echo Forge evented chat traces, protocol manifest routing, and smart context visualization. | `ION/05_context/current/codex_cli/CODEX_CHAT_JOC_CONTEXT_VISUALIZATION_ORCHESTRATION_20260508.md, /home/sev/ION - Production/AIM-ION/packages/joc/plans/01-architecture-and-layout.md, /home/sev/ION - Production/AIM-ION/packages/joc/plans/09-context-node-graph-visualization.md, /home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/XRayMessage.tsx, /home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/stream.ts, /home/sev/ION - Production/operation-victus/victus/context_assembler.py, /home/sev/ION - Production/operation-victus/victus/memory_bus.py` | PLANNED |
| C-028 | 2026-05-08 | Implemented Codex Chat Phase 0 memory visualization projection: memory strata, context route edges, protocol manifest summary, carrier phase events, token budget summary, redaction, model/UI drawer exposure, and tests. | `ION/04_packages/kernel/ion_codex_chat_memory_visualization.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json, ION/05_context/current/codex_cli/CODEX_CHAT_JOC_CONTEXT_VISUALIZATION_ORCHESTRATION_20260508.md` | IMPLEMENTED |
| C-029 | 2026-05-08 | Implemented Codex Chat Phase 1 shell component split: app facade, shell, main chat, right inspector, timeline, memory visualization drawer, shared helpers, and CSS/JS assets split into focused modules while preserving co | `ION/04_packages/kernel/ion_codex_chat_app_ui.py, ION/04_packages/kernel/ion_codex_chat_shell_ui.py, ION/04_packages/kernel/ion_codex_chat_main_ui.py, ION/04_packages/kernel/ion_codex_chat_right_inspector_ui.py, ION/04_packages/kernel/ion_codex_chat_timeline_ui.py, ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/04_packages/kernel/ion_codex_chat_ui_common.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-030 | 2026-05-08 | Implemented Codex Chat Phase 2 JOC shell behavior: top page tabs, page-local left drawer, main work-surface pages, right icon rail, inspector tab panels, bottom timeline filters, client-side shell toggles, and preserved  | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_shell_ui.py, ION/04_packages/kernel/ion_codex_chat_left_drawer_ui.py, ION/04_packages/kernel/ion_codex_chat_right_inspector_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json, ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json` | IMPLEMENTED |
| C-031 | 2026-05-08 | Implemented Codex Chat Phase 3 smart context visualization: selected-turn context, memory strata, Contextual Matryoshka layers, route graph, compaction timeline, protocol manifest, and UI-safe budget surface. | `ION/04_packages/kernel/ion_codex_chat_memory_visualization.py, ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json` | IMPLEMENTED |
| C-032 | 2026-05-08 | Verified Codex Chat Phase 3 smart context visualization through restarted local cockpit service and live Playwright cockpit smoke. | `ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json, ION/05_context/current/codex_solo/history/codex_solo_post_20260508T155446+0000.json` | VERIFIED |
| C-033 | 2026-05-08 | Added and passed live Playwright JOC shell smoke for Codex Chat: shell regions, top page switch, left drawer, right inspector, context memory page, timeline filter, and composer restoration. | `ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json, ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json` | VERIFIED |
| C-034 | 2026-05-08 | Implemented selected-message and route graph interaction for Codex Chat: chat turns, memory segments, and route edges are selectable; selected-node panel updates; connected context is highlighted; live Playwright shell s | `ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_main_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-035 | 2026-05-08 | Improved Codex Chat route graph usability: edge-type filters, route row metadata, selected node turn/source fields, and live browser coverage for compressed route filtering. | `ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-036 | 2026-05-08 | Implemented source-ref drilldown and compact selected-turn trace linking in Codex Chat: source refs and carrier phase events are selectable, update the selected-node panel, and highlight related visible context; live Pla | `ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-037 | 2026-05-08 | Persisted Codex Chat context inspector selection across reloads: memory, route, source, and trace selections now store in browser state/hash and restore before default selection; live cockpit smoke verifies trace restora | `ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-038 | 2026-05-08 | Added grouped source-reference drilldown and route edge summaries to Codex Chat: source refs now expose grouped filters and lanes, route graph shows type counts before detailed edges, and live cockpit smoke covers the fi | `ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py, ION/04_packages/kernel/ion_codex_chat_assets_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_cockpit_playwright_smoke.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-039 | 2026-05-08 | Improved Codex Chat response-carrier prompt quality: mounted Hot Context and context package selector, removed hard-coded root assumption, strengthened direct-answer continuity rules, and verified with live cockpit chat  | `ION/04_packages/kernel/ion_codex_chat_response_carrier.py, ION/tests/test_kernel_ion_codex_chat_response_carrier.py, ION/tests/test_kernel_ion_codex_chat_engine.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json` | VERIFIED |
| C-040 | 2026-05-08 | Added response-run observability to Codex Chat: recent response carrier run packets are projected into the active model and Evidence/Runs inspector with prompt, return, event, stdout, stderr, model, and status refs; live | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_right_inspector_ui.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json` | VERIFIED |
| C-041 | 2026-05-08 | Preserved first ION custom-GPT user-handling case study: added v0.2 governed-continuity draft, evidence index with local v2.4 pack SHA/file count, benchmark rubric, and user-handling trial index. | `ION/06_intelligence/research/user_handling_trials/2026-05-08_ion_first_custom_gpt_user_handling_case_study_v0_2.md, ION/06_intelligence/evidence/user_handling_trials/2026-05-08_ion_first_custom_gpt_user_handling_evidence_index.json, ION/06_intelligence/research/user_handling_trials/2026-05-08_ion_prompt_burden_continuity_benchmark_v0_1.md, ION/06_intelligence/research/user_handling_trials/README.md` | VERIFIED |
| C-042 | 2026-05-08 | Imported sandbox package v1.4 AI Assistant Work candidate lane into active root, documented package diff, preserved evidence index, patched validator -S path bootstrap, and locally validated candidate suite. | `ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_diff.md, ION/06_intelligence/evidence/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_evidence_index.json, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ACTIVE_ROOT_CANDIDATE_IMPORT_RECEIPT_20260508T174843Z.json, ION/05_context/current/ai_assistant_work/AI_ASSISTANT_WORK_STATE_INDEX_V0_5.json, ION/tests/test_kernel_ai_assistant_work_template_instances.py` | VERIFIED |
| C-043 | 2026-05-08 | Reviewed AI Assistant Work route compiler next packet and mapped candidate routes to active Codex chat skills, native lenses, Custom GPT/MCP/product lanes, and next compiler implementation target. | `ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_20260508T175230Z.md, ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_RECEIPT_20260508T175340Z.json, ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_diff.md` | VERIFIED |
| C-044 | 2026-05-08 | Implemented candidate-only Assistant Work route compiler and wired route metadata into Codex chat engine, queued objectives, turn traces, UI model drawers, and right inspector. | `ION/04_packages/kernel/ion_assistant_work_route_compiler.py, ION/tests/test_kernel_ion_assistant_work_route_compiler.py, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_IMPLEMENTATION_RECEIPT_20260508T181926Z.json, ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_diff.md` | done |
| C-045 | 2026-05-08 | Documented Phase 4 product reconciliation matrix across Codex Capsule Chat, Action Gateway, MCP Action, data-zip Custom GPT product, local cockpit, and full ION pipeline. | `ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_phase4_product_reconciliation_matrix.md, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_PHASE4_PRODUCT_RECONCILIATION_RECEIPT_20260508T182228Z.json, ION/06_intelligence/evidence/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_evidence_index.json` | VERIFIED |
| C-046 | 2026-05-08 | Added candidate Assistant Work route metadata to Action Gateway validate-only responses; held MCP route tool for explicit tool-policy/schema gate. | `ION/04_packages/kernel/ion_custom_gpt_action_gateway.py, ION/tests/test_kernel_ion_custom_gpt_action_gateway.py, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_GATEWAY_ROUTE_METADATA_RECEIPT_20260508T182713Z.json, ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_phase4_product_reconciliation_matrix.md` | VERIFIED |
| C-047 | 2026-05-08 | Planned candidate-domain operation ladder for assistant-work surfaces: candidate domains/agents/templates/routes may operate under containment for classification, proof shaping, route preview, trace display, and diagnost | `ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_candidate_domain_operation_protocol_plan.md, ION/05_context/current/ai_assistant_work/next/AI_ASSISTANT_WORK_NEXT_PACKET_CANDIDATE_DOMAIN_OPERATION_PROTOCOL_20260508T183906Z.json, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_CANDIDATE_DOMAIN_OPERATION_PLAN_RECEIPT_20260508T184123Z.json` | PLANNED |
| C-048 | 2026-05-08 | Implemented candidate-domain lifecycle gate: added provisional protocol, candidate lifecycle registry, scorecards, promotion proposal draft, and route compiler filtering for inactive/rejected/archived/draft routes. | `ION/02_architecture/ION_CANDIDATE_DOMAIN_OPERATION_PROTOCOL.md, ION/05_context/current/ai_assistant_work/candidate_lifecycle/CANDIDATE_DOMAIN_LIFECYCLE_REGISTRY_V0_1.yaml, ION/04_packages/kernel/ion_assistant_work_route_compiler.py, ION/tests/test_kernel_ion_assistant_work_route_compiler.py, ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_CANDIDATE_DOMAIN_LIFECYCLE_IMPLEMENTATION_RECEIPT_20260508T185104Z.json` | IMPLEMENTED |
| C-049 | 2026-05-08 | Formalized root source lanes for workpackets, diffs, and ION_sandbox: added lane READMEs, machine-readable indexes, consolidated source-lane policy, receipt, and git hygiene for sandbox snapshots. | `workpackets/README.md, workpackets/WORKPACKET_INDEX_20260508T190626Z.json, diffs/README.md, diffs/DIFF_INDEX_20260508T190626Z.json, ION_sandbox/README.md, ION_sandbox/ION_SANDBOX_INDEX_20260508T190626Z.json, ION/05_context/current/source_lanes/ION_ROOT_SOURCE_LANE_POLICY_20260508T190626Z.md, ION/05_context/current/source_lanes/receipts/ION_ROOT_SOURCE_LANE_FORMALIZATION_RECEIPT_20260508T190626Z.json` | IMPLEMENTED |
| C-050 | 2026-05-08 | Documented GitHub release strategy for ION_sandbox: recommend a dedicated release/ion-sandbox-gpt-v1 branch with curated product root, after cache cleanup, metadata repair, Cursor test-boundary decision, focused tests, s | `ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_ion_sandbox_github_release_strategy.md, ION/05_context/current/source_lanes/receipts/ION_SANDBOX_GITHUB_RELEASE_STRATEGY_RECEIPT_20260508T191612Z.json, ION_sandbox/ION_SANDBOX_INDEX_20260508T190626Z.json` | PLANNED |
| C-051 | 2026-05-08 | Prepared sanitized ion-sandbox-gpt release root from ION_sandbox snapshot: repaired active GPT sandbox packet, release metadata, Cursor optional test boundary, passed focused release tests, secret scan clean, generated c | `ion-sandbox-gpt/RELEASE_MANIFEST.json, ion-sandbox-gpt/RELEASE_READINESS.md, ion-sandbox-gpt/VALIDATION_REPORT.json, ion-sandbox-gpt/ION/05_context/current/ACTIVE_WORK_PACKET.json, ion-sandbox-gpt/ION/tests/test_kernel_ion_stale_surface_audit.py, ION/05_context/current/source_lanes/receipts/ION_SANDBOX_GPT_RELEASE_ROOT_PREP_RECEIPT_20260508T192928Z.json` | IMPLEMENTED |
| C-052 | 2026-05-08 | Published release/ion-sandbox-gpt-v1 to GitHub with curated ion-sandbox-gpt release root, candidate-domain/source-lane documentation, release validation proof, and branch-push receipt. First release commit dda4a89541cc85 | `ion-sandbox-gpt/RELEASE_MANIFEST.json, ion-sandbox-gpt/RELEASE_READINESS.md, ion-sandbox-gpt/VALIDATION_REPORT.json, ION/05_context/current/source_lanes/receipts/ION_SANDBOX_GPT_RELEASE_BRANCH_PUSH_RECEIPT_20260508T193825Z.json` | PUBLISHED |
| C-053 | 2026-05-08 | Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context system, chat engine, response carrier, JOC-style shell modules, model move policy, skill/lens registries, candida | `ION/04_packages/kernel/ion_dual_codex_chat.py, ION/04_packages/kernel/ion_codex_chat_engine.py, ION/04_packages/kernel/ion_codex_chat_response_carrier.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_ACTIVE_ROOT_BRANCH_PUSH_RECEIPT_20260508T201115Z.json, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_chat_engine.py` | PUBLISHED |

## MINI LOOKUP INDEX

CODEX SOLO MINI INDEX | 2026-05-08T20:12:02+00:00

ROLE: lookup/receipt index; Capsule is the minimum working context.
ACTIVE_CAPSULE: ION/05_context/current/codex_solo/CAPSULE.md
HOT_CONTEXT: ION/05_context/current/codex_solo/HOT_CONTEXT.md
LONG_HORIZON: ION/05_context/current/codex_solo/LONG_HORIZON.json
PACKAGES: ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
HISTORY: ION/05_context/current/codex_solo/history

MISSION: Codex Capsule Chat active-root branch publication
PHASE: feature branch pushed
LAST_RECEIPT: Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context system, chat engine, response carrier, JOC-style shell modules, model mov
BLOCKER: None
NEXT: Review/open GitHub PR https://github.com/ION-operations/ION/pull/new/feature/codex-capsule-chat-active-root and decide merge order relative to sandbox GPT release branch.

ACTIVE_TEMPLATE: codex_capsule_chat_branch_publish

CAPSULE_LOOKUP:
- C-049 2026-05-08 IMPLEMENTED: Formalized root source lanes for workpackets, diffs, and ION_sandbox: added lane READMEs, machine-readable ind
- C-050 2026-05-08 PLANNED: Documented GitHub release strategy for ION_sandbox: recommend a dedicated release/ion-sandbox-gpt-v1 branch wi
- C-051 2026-05-08 IMPLEMENTED: Prepared sanitized ion-sandbox-gpt release root from ION_sandbox snapshot: repaired active GPT sandbox packet,
- C-052 2026-05-08 PUBLISHED: Published release/ion-sandbox-gpt-v1 to GitHub with curated ion-sandbox-gpt release root, candidate-domain/sou
- C-053 2026-05-08 PUBLISHED: Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context sys

ROUTE_INDEX: ION/05_context/current/codex_solo/ROUTE.json validates active refs.
POLICY: Capsule is the minimum working context. Mini is a lookup/receipt index for capsule history. Neither overrides current repo authority, tests, receipts, or explicit operator instructions.


## LONG HORIZON CAPSULE INDEX

{
  "capsule_entry_count": 53,
  "epoch_count": 6,
  "latest_epochs": [
    {
      "date_end": "2026-05-07",
      "date_start": "2026-05-07",
      "epoch_id": "E-001",
      "evidence_refs": [
        "ION/04_packages/kernel/ion_codex_solo_context.py",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/tests/test_kernel_ion_codex_solo_context.py",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md",
        "ION/05_context/current/codex_solo/LONG_HORIZON.json",
        "ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json",
        ".codex/config.toml",
        ".codex/hooks/ion_session_start_context.py",
        "ION/tests/test_codex_project_config_and_hook.py",
        "ION/04_packages/kernel/ion_codex_model_moves.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/03_registry/codex_cli_model_move_policy.yaml",
        "ION/tests/test_kernel_ion_codex_model_moves.py",
        "ION/04_packages/kernel/ion_public_cockpit_auth.py",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py",
        "ION/tests/test_kernel_ion_public_cockpit_auth.py",
        "ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py",
        "/home/sev/.config/systemd/user/ion-mcp-preview.service.d/cockpit-token.conf"
      ],
      "row_count": 10,
      "row_end": "C-010",
      "row_start": "C-001",
      "status_counts": {
        "CORRECTED": 2,
        "IMPLEMENTED": 8
      },
      "summaries": [
        {
          "date": "2026-05-07",
          "id": "C-006",
          "status": "IMPLEMENTED",
          "summary": "Updated cockpit login password and pre-allowed crinkedart Google account"
        },
        {
          "date": "2026-05-07",
          "id": "C-007",
          "status": "IMPLEMENTED",
          "summary": "Rebuilt dual Codex chat into JOC-style cockpit workbench with command rail and context drawers"
        },
        {
          "date": "2026-05-07",
          "id": "C-008",
          "status": "CORRECTED",
          "summary": "Added Codex Capsule Operating Protocol: Capsule ION is the minified fallback/basic ops kernel while full ION Codex CLI chat is rebuilt."
        },
        {
          "date": "2026-05-07",
          "id": "C-009",
          "status": "CORRECTED",
          "summary": "Corrected Codex chat product direction to one Capsule Codex chat with bounded full-ION comms adapter."
        },
        {
          "date": "2026-05-07",
          "id": "C-010",
          "status": "IMPLEMENTED",
          "summary": "Added opt-in chat execution bridge from Codex Capsule chat turns to existing Codex work queue."
        }
      ]
    },
    {
      "date_end": "2026-05-08",
      "date_start": "2026-05-07",
      "epoch_id": "E-002",
      "evidence_refs": [
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md",
        "ION/04_packages/kernel/ion_codex_solo_context.py",
        "ION/tests/test_kernel_ion_codex_solo_context.py",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_TRACE_AND_AGENT_TRANSPARENCY_ORCHESTRATION_20260507.md",
        "ION/05_context/current/codex_cli/CODEX_CHAT_UI_RECOVERY_ORCHESTRATION_20260507.md",
        "ION/04_packages/kernel/ion_codex_chat_app_ui.py",
        "ION/05_context/current/codex_cli/CODEX_CHAT_APP_SHELL_COMPONENTIZATION_20260507.md",
        "ION/05_context/current/codex_cli/CODEX_CHAT_TIMELINE_AGENTS_DRAWER_PASS_20260507.md",
        "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md",
        "ION/03_registry/ion_skill_registry.yaml",
        "ION/04_packages/kernel/ion_skill_activation.py",
        "ION/tests/test_kernel_ion_skill_activation.py",
        "ION/05_context/current/codex_cli/CODEX_SKILL_ACTIVATION_IMPLEMENTATION_20260507.md",
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md",
        "ION/03_registry/ion_native_lens_registry.yaml",
        "ION/04_packages/kernel/ion_codex_chat_engine.py",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py"
      ],
      "row_count": 10,
      "row_end": "C-020",
      "row_start": "C-011",
      "status_counts": {
        "CORRECTED": 1,
        "IMPLEMENTED": 8,
        "PLANNED": 1
      },
      "summaries": [
        {
          "date": "2026-05-07",
          "id": "C-016",
          "status": "IMPLEMENTED",
          "summary": "Extracted active Codex Chat app shell into dedicated UI renderer module."
        },
        {
          "date": "2026-05-07",
          "id": "C-017",
          "status": "IMPLEMENTED",
          "summary": "Removed obsolete in-file Codex chat HTML/CSS renderer blocks after UI extraction."
        },
        {
          "date": "2026-05-07",
          "id": "C-018",
          "status": "IMPLEMENTED",
          "summary": "Improved Codex Chat Timeline and Agents drawers from existing trace and broker data."
        },
        {
          "date": "2026-05-08",
          "id": "C-019",
          "status": "IMPLEMENTED",
          "summary": "Implemented ION skill activation layer for Codex Chat: skills activate workflows while templates remain proof gates."
        },
        {
          "date": "2026-05-08",
          "id": "C-020",
          "status": "IMPLEMENTED",
          "summary": "Implemented Codex Chat Engine core: response modes, native ION lenses, GPT-5.5 chat route, and queue metadata handoff."
        }
      ]
    },
    {
      "date_end": "2026-05-08",
      "date_start": "2026-05-08",
      "epoch_id": "E-003",
      "evidence_refs": [
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md",
        "ION/03_registry/ion_native_lens_registry.yaml",
        "ION/04_packages/kernel/ion_codex_chat_engine.py",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/04_packages/kernel/ion_codex_chat_app_ui.py",
        "ION/04_packages/kernel/ion_codex_solo_context.py",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/tests/test_kernel_ion_codex_chat_engine.py",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/tests/test_kernel_ion_codex_queue_runner.py",
        "ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py",
        "ION/05_context/current/codex_cli/CODEX_CHAT_ENGINE_IMPLEMENTATION_20260508.md",
        "ION/05_context/current/codex_cli/CODEX_CHAT_RESPONSE_CARRIER_ORCHESTRATION_20260508.md",
        "ION/04_packages/kernel/ion_codex_chat_response_carrier.py",
        "ION/tests/test_kernel_ion_codex_chat_response_carrier.py",
        "ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md",
        "ION/05_context/current/codex_cli/CODEX_CHAT_RESPONSE_CARRIER_IMPLEMENTATION_20260508.md",
        "ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T140124Z968157_live_carrier_smoke_reply_with_one_concise_sentence_naming_the_current_ca/run.json",
        "ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T140124Z968157_live_carrier_smoke_reply_with_one_concise_sentence_naming_the_current_ca/latest_r"
      ],
      "row_count": 10,
      "row_end": "C-030",
      "row_start": "C-021",
      "status_counts": {
        "IMPLEMENTED": 8,
        "PLANNED": 2
      },
      "summaries": [
        {
          "date": "2026-05-08",
          "id": "C-026",
          "status": "IMPLEMENTED",
          "summary": "Installed Playwright package and added opt-in live cockpit browser smoke proving chat submit clears immediately, shows pending Codex response state, blocks duplicate submit, and ca"
        },
        {
          "date": "2026-05-08",
          "id": "C-027",
          "status": "PLANNED",
          "summary": "Planned the next Codex Capsule Chat rewrite around JOC shell regions, Victus Contextual Matryoshka, Echo Forge evented chat traces, protocol manifest routing, and smart context vis"
        },
        {
          "date": "2026-05-08",
          "id": "C-028",
          "status": "IMPLEMENTED",
          "summary": "Implemented Codex Chat Phase 0 memory visualization projection: memory strata, context route edges, protocol manifest summary, carrier phase events, token budget summary, redaction"
        },
        {
          "date": "2026-05-08",
          "id": "C-029",
          "status": "IMPLEMENTED",
          "summary": "Implemented Codex Chat Phase 1 shell component split: app facade, shell, main chat, right inspector, timeline, memory visualization drawer, shared helpers, and CSS/JS assets split "
        },
        {
          "date": "2026-05-08",
          "id": "C-030",
          "status": "IMPLEMENTED",
          "summary": "Implemented Codex Chat Phase 2 JOC shell behavior: top page tabs, page-local left drawer, main work-surface pages, right icon rail, inspector tab panels, bottom timeline filters, c"
        }
      ]
    },
    {
      "date_end": "2026-05-08",
      "date_start": "2026-05-08",
      "epoch_id": "E-004",
      "evidence_refs": [
        "ION/04_packages/kernel/ion_codex_chat_memory_visualization.py",
        "ION/04_packages/kernel/ion_codex_chat_memory_visualization_ui.py",
        "ION/04_packages/kernel/ion_codex_chat_assets_ui.py",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/05_context/current/ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json",
        "ION/tests/test_kernel_ion_cockpit_playwright_smoke.py",
        "ION/05_context/current/codex_cli/playwright_cockpit_pending_smoke_latest.json",
        "ION/05_context/current/codex_solo/history/codex_solo_post_20260508T155446+0000.json",
        "ION/05_context/current/codex_cli/playwright_cockpit_shell_smoke_latest.json",
        "ION/04_packages/kernel/ion_codex_chat_main_ui.py",
        "ION/04_packages/kernel/ion_codex_chat_response_carrier.py",
        "ION/tests/test_kernel_ion_codex_chat_response_carrier.py",
        "ION/tests/test_kernel_ion_codex_chat_engine.py",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/04_packages/kernel/ion_codex_chat_right_inspector_ui.py"
      ],
      "row_count": 10,
      "row_end": "C-040",
      "row_start": "C-031",
      "status_counts": {
        "IMPLEMENTED": 1,
        "VERIFIED": 9
      },
      "summaries": [
        {
          "date": "2026-05-08",
          "id": "C-036",
          "status": "VERIFIED",
          "summary": "Implemented source-ref drilldown and compact selected-turn trace linking in Codex Chat: source refs and carrier phase events are selectable, update the selected-node panel, and hig"
        },
        {
          "date": "2026-05-08",
          "id": "C-037",
          "status": "VERIFIED",
          "summary": "Persisted Codex Chat context inspector selection across reloads: memory, route, source, and trace selections now store in browser state/hash and restore before default selection; l"
        },
        {
          "date": "2026-05-08",
          "id": "C-038",
          "status": "VERIFIED",
          "summary": "Added grouped source-reference drilldown and route edge summaries to Codex Chat: source refs now expose grouped filters and lanes, route graph shows type counts before detailed edg"
        },
        {
          "date": "2026-05-08",
          "id": "C-039",
          "status": "VERIFIED",
          "summary": "Improved Codex Chat response-carrier prompt quality: mounted Hot Context and context package selector, removed hard-coded root assumption, strengthened direct-answer continuity rul"
        },
        {
          "date": "2026-05-08",
          "id": "C-040",
          "status": "VERIFIED",
          "summary": "Added response-run observability to Codex Chat: recent response carrier run packets are projected into the active model and Evidence/Runs inspector with prompt, return, event, stdo"
        }
      ]
    },
    {
      "date_end": "2026-05-08",
      "date_start": "2026-05-08",
      "epoch_id": "E-005",
      "evidence_refs": [
        "ION/06_intelligence/research/user_handling_trials/2026-05-08_ion_first_custom_gpt_user_handling_case_study_v0_2.md",
        "ION/06_intelligence/evidence/user_handling_trials/2026-05-08_ion_first_custom_gpt_user_handling_evidence_index.json",
        "ION/06_intelligence/research/user_handling_trials/2026-05-08_ion_prompt_burden_continuity_benchmark_v0_1.md",
        "ION/06_intelligence/research/user_handling_trials/README.md",
        "ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_diff.md",
        "ION/06_intelligence/evidence/sandbox_agent_package_evolution/2026-05-08_sandbox_agent_package_v1_4_ai_assistant_work_evidence_index.json",
        "ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ACTIVE_ROOT_CANDIDATE_IMPORT_RECEIPT_20260508T174843Z.json",
        "ION/05_context/current/ai_assistant_work/AI_ASSISTANT_WORK_STATE_INDEX_V0_5.json",
        "ION/tests/test_kernel_ai_assistant_work_template_instances.py",
        "ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_20260508T175230Z.md",
        "ION/05_context/current/ai_assistant_work/route_compiler/AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json",
        "ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_REVIEW_RECEIPT_20260508T175340Z.json",
        "ION/04_packages/kernel/ion_assistant_work_route_compiler.py",
        "ION/tests/test_kernel_ion_assistant_work_route_compiler.py",
        "ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_ROUTE_COMPILER_IMPLEMENTATION_RECEIPT_20260508T181926Z.json",
        "ION/06_intelligence/research/sandbox_agent_package_evolution/2026-05-08_phase4_product_reconciliation_matrix.md",
        "ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_PHASE4_PRODUCT_RECONCILIATION_RECEIPT_20260508T182228Z.json",
        "ION/04_packages/kernel/ion_custom_gpt_action_gateway.py",
        "ION/tests/test_kernel_ion_custom_gpt_action_gateway.py",
        "ION/05_context/current/ai_assistant_work/receipts/AI_ASSISTANT_WORK_GATEWAY_ROUTE_METADATA_RECEIPT_20260508T182713Z.json"
      ],
      "row_count": 10,
      "row_end": "C-050",
      "row_start": "C-041",
      "status_counts": {
        "IMPLEMENTED": 2,
        "PLANNED": 2,
        "VERIFIED": 5,
        "done": 1
      },
      "summaries": [
        {
          "date": "2026-05-08",
          "id": "C-046",
          "status": "VERIFIED",
          "summary": "Added candidate Assistant Work route metadata to Action Gateway validate-only responses; held MCP route tool for explicit tool-policy/schema gate."
        },
        {
          "date": "2026-05-08",
          "id": "C-047",
          "status": "PLANNED",
          "summary": "Planned candidate-domain operation ladder for assistant-work surfaces: candidate domains/agents/templates/routes may operate under containment for classification, proof shaping, ro"
        },
        {
          "date": "2026-05-08",
          "id": "C-048",
          "status": "IMPLEMENTED",
          "summary": "Implemented candidate-domain lifecycle gate: added provisional protocol, candidate lifecycle registry, scorecards, promotion proposal draft, and route compiler filtering for inacti"
        },
        {
          "date": "2026-05-08",
          "id": "C-049",
          "status": "IMPLEMENTED",
          "summary": "Formalized root source lanes for workpackets, diffs, and ION_sandbox: added lane READMEs, machine-readable indexes, consolidated source-lane policy, receipt, and git hygiene for sa"
        },
        {
          "date": "2026-05-08",
          "id": "C-050",
          "status": "PLANNED",
          "summary": "Documented GitHub release strategy for ION_sandbox: recommend a dedicated release/ion-sandbox-gpt-v1 branch with curated product root, after cache cleanup, metadata repair, Cursor "
        }
      ]
    },
    {
      "date_end": "2026-05-08",
      "date_start": "2026-05-08",
      "epoch_id": "E-006",
      "evidence_refs": [
        "ion-sandbox-gpt/RELEASE_MANIFEST.json",
        "ion-sandbox-gpt/RELEASE_READINESS.md",
        "ion-sandbox-gpt/VALIDATION_REPORT.json",
        "ion-sandbox-gpt/ION/05_context/current/ACTIVE_WORK_PACKET.json",
        "ion-sandbox-gpt/ION/tests/test_kernel_ion_stale_surface_audit.py",
        "ION/05_context/current/source_lanes/receipts/ION_SANDBOX_GPT_RELEASE_ROOT_PREP_RECEIPT_20260508T192928Z.json",
        "ION/05_context/current/source_lanes/receipts/ION_SANDBOX_GPT_RELEASE_BRANCH_PUSH_RECEIPT_20260508T193825Z.json",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/04_packages/kernel/ion_codex_chat_engine.py",
        "ION/04_packages/kernel/ion_codex_chat_response_carrier.py",
        "ION/04_packages/kernel/ion_codex_solo_context.py",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_ACTIVE_ROOT_BRANCH_PUSH_RECEIPT_20260508T201115Z.json",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/tests/test_kernel_ion_codex_chat_engine.py"
      ],
      "row_count": 3,
      "row_end": "C-053",
      "row_start": "C-051",
      "status_counts": {
        "IMPLEMENTED": 1,
        "PUBLISHED": 2
      },
      "summaries": [
        {
          "date": "2026-05-08",
          "id": "C-051",
          "status": "IMPLEMENTED",
          "summary": "Prepared sanitized ion-sandbox-gpt release root from ION_sandbox snapshot: repaired active GPT sandbox packet, release metadata, Cursor optional test boundary, passed focused relea"
        },
        {
          "date": "2026-05-08",
          "id": "C-052",
          "status": "PUBLISHED",
          "summary": "Published release/ion-sandbox-gpt-v1 to GitHub with curated ion-sandbox-gpt release root, candidate-domain/source-lane documentation, release validation proof, and branch-push rece"
        },
        {
          "date": "2026-05-08",
          "id": "C-053",
          "status": "PUBLISHED",
          "summary": "Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context system, chat engine, response carrier, JOC-style shell modules, model mov"
        }
      ]
    }
  ],
  "path": "ION/05_context/current/codex_solo/LONG_HORIZON.json"
}

## CONTEXT PACKAGE SELECTOR

{
  "packages": [
    {
      "context_type": "active_short_horizon",
      "load_policy": "always_inline_first",
      "package_id": "minimum_working_capsule",
      "path_refs": [
        "ION/05_context/current/codex_solo/CAPSULE.md"
      ],
      "window": {
        "kind": "line_tail",
        "max_lines": 80
      }
    },
    {
      "context_type": "receipt_lookup",
      "load_policy": "index_only_not_primary_prompt",
      "package_id": "mini_lookup_index",
      "path_refs": [
        "ION/05_context/current/codex_solo/MINI.md"
      ],
      "window": {
        "kind": "recent_capsule_rows",
        "max_rows": 5
      }
    },
    {
      "context_type": "compressed_long_horizon",
      "load_policy": "load_when_older_continuity_or_prior_decisions_matter",
      "package_id": "long_horizon_capsule_index",
      "path_refs": [
        "ION/05_context/current/codex_solo/LONG_HORIZON.json"
      ],
      "window": {
        "epoch_count": 6,
        "epoch_size_rows": 10,
        "hot_context_recent_epochs": 6,
        "kind": "epoch_summary"
      }
    },
    {
      "context_type": "authority_and_policy",
      "load_policy": "always_available_by_route_hash",
      "package_id": "active_authority_package",
      "path_refs": [
        "ION/REPO_AUTHORITY.md",
        "ION/03_registry/agent_context_system_registry.yaml",
        "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md"
      ],
      "window": {
        "kind": "route_excerpt",
        "max_chars_per_file": 1600
      }
    },
    {
      "context_type": "current_objective",
      "load_policy": "injected_per_queue_or_chat_turn",
      "package_id": "mission_active_package",
      "path_refs": [
        "ION/05_context/current/codex_solo/HOT_CONTEXT.md"
      ],
      "window": {
        "capsule_first": true,
        "kind": "compiled_hot_context"
      }
    },
    {
      "context_type": "route_deeper",
      "load_policy": "use_when_hot_context_is_insufficient",
      "package_id": "route_depth_package",
      "path_refs": [
        "ION/05_context/current/codex_solo/ROUTE.json",
        "ION/05_context/current/codex_solo/CAPSULE.md",
        "ION/05_context/current/codex_solo/MINI.md",
        "ION/05_context/current/codex_solo/LONG_HORIZON.json",
        "ION/REPO_AUTHORITY.md",
        "ION/03_registry/agent_context_system_registry.yaml",
        "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md",
        "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md",
        "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md",
        "ION/03_registry/ion_skill_registry.yaml",
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md",
        "ION/03_registry/ion_native_lens_registry.yaml",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md"
      ],
      "window": {
        "kind": "validate_before_queue",
        "required_missing": []
      }
    },
    {
      "context_type": "proof_and_receipts",
      "load_policy": "use_for_verification_or_claims_about_completed_work",
      "package_id": "evidence_receipt_package",
      "path_refs": [
        "ION/05_context/current/codex_solo/history"
      ],
      "window": {
        "kind": "latest_checkpoint_plus_named_evidence",
        "source": "capsule_row_evidence_refs"
      }
    },
    {
      "context_type": "recovery",
      "load_policy": "use_when_context_drift_or_old_build_comparison_is_requested",
      "package_id": "recovery_package",
      "path_refs": [
        "ION/05_context/current/codex_solo/history",
        "ION/05_context/current/codex_solo/LONG_HORIZON.json"
      ],
      "window": {
        "kind": "explicit_operator_or_blocker_triggered"
      }
    }
  ],
  "path": "ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json",
  "selected_by_default": [
    "minimum_working_capsule",
    "mini_lookup_index",
    "long_horizon_capsule_index",
    "active_authority_package",
    "mission_active_package",
    "route_depth_package"
  ]
}

## ROUTE VALIDATION

{
  "entries": [
    {
      "bytes": 29280,
      "classification": "codex_solo_minimum_working_context",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/codex_solo/CAPSULE.md",
      "repo_relative": true,
      "required": true,
      "sha256": "26c7fd472d6d5d8205c8d7f36b606287bc4d4883f08c09456af82df6c0ef44d3",
      "why": "Minimum context the standalone Codex lane must always carry."
    },
    {
      "bytes": 1952,
      "classification": "codex_solo_lookup_receipt_index",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/codex_solo/MINI.md",
      "repo_relative": true,
      "required": true,
      "sha256": "0077dc437a4b124a47a037f9df2310e6d285846b3f6172284f76828c481a0927",
      "why": "Lookup index and receipt summary for capsule history."
    },
    {
      "bytes": 37840,
      "classification": "codex_solo_long_horizon_index",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/codex_solo/LONG_HORIZON.json",
      "repo_relative": true,
      "required": true,
      "sha256": "520646e3fd91e985acff2a66d390902b2607af500ce71c8336a8ba9cabdf35bd",
      "why": "Compressed long-horizon capsule index for older continuity lookup."
    },
    {
      "bytes": 9259,
      "classification": "active_repo_authority",
      "exists": true,
      "is_file": true,
      "path": "ION/REPO_AUTHORITY.md",
      "repo_relative": true,
      "required": true,
      "sha256": "804ed8430fc53e551d254af063ec414646a1c1bf94ceeec51c31769fa41aca1e",
      "why": "Active root authority boundary."
    },
    {
      "bytes": 9343,
      "classification": "active_context_policy",
      "exists": true,
      "is_file": true,
      "path": "ION/03_registry/agent_context_system_registry.yaml",
      "repo_relative": true,
      "required": true,
      "sha256": "0c9e8d86b55bcf310f85adabbdee3d4d7947a24c0ce05680b608d29d5466fd12",
      "why": "Current Mini/Capsule witness policy and active context-system registry."
    },
    {
      "bytes": 1098,
      "classification": "active_lead_context",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md",
      "repo_relative": true,
      "required": true,
      "sha256": "3dcbd1f7f1c81c30a9d02f66deffdc5d0c9466df4347946030a3a1cf6721cd4c",
      "why": "Current lead-dev operating posture."
    },
    {
      "bytes": 10713,
      "classification": "codex_solo_design",
      "exists": true,
      "is_file": true,
      "path": "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md",
      "repo_relative": true,
      "required": true,
      "sha256": "4e92263b324a31489cd6be3c375ad0654b94493db87f46ff5ccda7985ea15e47",
      "why": "Research basis for this single-agent context lane."
    },
    {
      "bytes": 6081,
      "classification": "codex_capsule_operating_kernel",
      "exists": true,
      "is_file": true,
      "path": "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md",
      "repo_relative": true,
      "required": true,
      "sha256": "b76326e484b8c61395f15109c444352a968a3ef6ce58fee4983019ad024abffa",
      "why": "Small ION operating kernel for Codex fallback/basic ops."
    },
    {
      "bytes": 4015,
      "classification": "codex_skill_activation_governance",
      "exists": true,
      "is_file": true,
      "path": "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md",
      "repo_relative": true,
      "required": true,
      "sha256": "cc3207616a001e71116e7262968f3b7b6b932d819bbd52b69be31d5923a67c94",
      "why": "Defines skills as activation control while templates remain proof law."
    },
    {
      "bytes": 9803,
      "classification": "codex_skill_activation_registry",
      "exists": true,
      "is_file": true,
      "path": "ION/03_registry/ion_skill_registry.yaml",
      "repo_relative": true,
      "required": true,
      "sha256": "bc64b6fdbe8805c22dc3ec5faee2ec765ca2f2184e9333f4591c5c1aa83dcdb1",
      "why": "Active skill registry for Codex chat, ION handoff, recovery, template curation, and receipts."
    },
    {
      "bytes": 3401,
      "classification": "codex_chat_engine_protocol",
      "exists": true,
      "is_file": true,
      "path": "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md",
      "repo_relative": true,
      "required": true,
      "sha256": "3b8176c08c0524d6befef8d1434d3af23e3dc8a90aed88ee496119f7b4751d1c",
      "why": "Defines the chat-quality engine under the UI: context, skills, native lenses, model route, and response contract."
    },
    {
      "bytes": 5076,
      "classification": "codex_chat_native_lens_registry",
      "exists": true,
      "is_file": true,
      "path": "ION/03_registry/ion_native_lens_registry.yaml",
      "repo_relative": true,
      "required": true,
      "sha256": "4121707156f13446addccbf19c1b26af087fc7520cd80ca1f8e50cac2b6a437d",
      "why": "Maps ION native roles into chat-engine lenses without making them user-facing chores."
    },
    {
      "bytes": 3312,
      "classification": "codex_capsule_chat_rebuild_orchestration",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md",
      "repo_relative": true,
      "required": true,
      "sha256": "d214747d7a4dd3c9e4585f2345eabad1e98513485bc43c7c4d3a922f5af54439",
      "why": "Active product correction: one Capsule Codex chat with bounded full-ION comms."
    },
    {
      "bytes": 8550,
      "classification": "codex_capsule_chat_ui_orchestration",
      "exists": true,
      "is_file": true,
      "path": "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md",
      "repo_relative": true,
      "required": true,
      "sha256": "050112e9456f270894f796468b1009a60dc646eba731e38ac543548867b9cb29",
      "why": "Chat-first app UI orchestration using JOC/ION drawers and Capsule context."
    }
  ],
  "findings": [],
  "live_execution_authority": false,
  "ok": true,
  "production_authority": false,
  "route_path": "ION/05_context/current/codex_solo/ROUTE.json",
  "schema_id": "ion.codex_solo_route_validation.v1"
}

## ROUTE EXCERPTS

### ION/05_context/current/codex_solo/CAPSULE.md

# Codex Solo Capsule

> Minimum working context for the standalone Codex chat lane. Load this before general Codex work. Mini is only lookup/index; detailed work stays in normal artifacts.

| # | Date | Summary | Evidence | Status |
|---|------|---------|----------|--------|
| C-001 | 2026-05-07 | Implemented capsule-first Codex solo context: Capsule is minimum working context; Mini is lookup/receipt index. | `ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md` | IMPLEMENTED |
| C-002 | 2026-05-07 | Implemented multi-horizon Codex solo context: long-horizon capsule epochs and explicit context package selector. | `ION/04_packages/kernel/ion_codex_solo_context.py, ION/04_packages/kernel/ion_dual_codex_chat.py, ION/tests/test_kernel_ion_codex_solo_context.py, ION/tests/test_kernel_ion_dual_codex_chat.py, ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md, ION/05_context/current/codex_solo/LONG_HORIZON.json, ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json` | IMPLEMENTED |
| C-003 | 2026-05-07 | Implemented project-scoped Codex CLI capsule boot setup with read-only session hook, optional local ION MCP read/status tools, and explicit post receipt helper. | `.codex/config.toml, .codex/hooks/ion_session_start_context.py, ION/04_packages/kernel/ion_codex_solo_context.py, ION/test

### ION/05_context/current/codex_solo/MINI.md

CODEX SOLO MINI INDEX | 2026-05-08T20:12:02+00:00

ROLE: lookup/receipt index; Capsule is the minimum working context.
ACTIVE_CAPSULE: ION/05_context/current/codex_solo/CAPSULE.md
HOT_CONTEXT: ION/05_context/current/codex_solo/HOT_CONTEXT.md
LONG_HORIZON: ION/05_context/current/codex_solo/LONG_HORIZON.json
PACKAGES: ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
HISTORY: ION/05_context/current/codex_solo/history

MISSION: Codex Capsule Chat active-root branch publication
PHASE: feature branch pushed
LAST_RECEIPT: Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context system, chat engine, response carrier, JOC-style shell modules, model mov
BLOCKER: None
NEXT: Review/open GitHub PR https://github.com/ION-operations/ION/pull/new/feature/codex-capsule-chat-active-root and decide merge order relative to sandbox GPT release branch.

ACTIVE_TEMPLATE: codex_capsule_chat_branch_publish

CAPSULE_LOOKUP:
- C-049 2026-05-08 IMPLEMENTED: Formalized root source lanes for workpackets, diffs, and ION_sandbox: added lane READMEs, machine-readable ind
- C-050 2026-05-08 PLANNED: Documented GitHub release strategy for ION_sandbox: recommend a dedicated release/ion-sandbox-gpt-v1 branch wi
- C-051 2026-05-08 IMPLEMENTED: Prepared sanitized ion-sandbox-gpt release root from ION_sandbox snapshot: repaired active GPT sandbox packet,
- C-052 2026-05-08 PUBLISHED: Published release/ion-sandbox-gpt-v1 to GitHub with curated ion-sandbox-gpt release root, candidate-domain/sou
- C-053 2026-05-08 PUBLISHED: Published feature/codex-capsule-cha

### ION/05_context/current/codex_solo/LONG_HORIZON.json

{
  "capsule_entry_count": 53,
  "epoch_count": 6,
  "epoch_size_rows": 10,
  "epochs": [
    {
      "date_end": "2026-05-07",
      "date_start": "2026-05-07",
      "epoch_id": "E-001",
      "evidence_refs": [
        "ION/04_packages/kernel/ion_codex_solo_context.py",
        "ION/04_packages/kernel/ion_dual_codex_chat.py",
        "ION/tests/test_kernel_ion_codex_solo_context.py",
        "ION/tests/test_kernel_ion_dual_codex_chat.py",
        "ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md",
        "ION/05_context/current/codex_solo/LONG_HORIZON.json",
        "ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json",
        ".codex/config.toml",
        ".codex/hooks/ion_session_start_context.py",
        "ION/tests/test_codex_project_config_and_hook.py",
        "ION/04_packages/kernel/ion_codex_model_moves.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/03_registry/codex_cli_model_move_policy.yaml",
        "ION/tests/test_kernel_ion_codex_model_moves.py",
        "ION/04_packages/kernel/ion_public_cockpit_auth.py",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py",
        "ION/tests/test_kernel_ion_public_cockpit_auth.py",
        "ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py",
        "/home/sev/.config/systemd/user/ion-mcp-preview.service.d/cockpit-token.conf"
      ],
      "row_count": 10,
      "row_end": "C-010",
      "row_start": "C-001",
      "status_counts": {
        "CO

### ION/REPO_AUTHORITY.md

---
type: repo_authority
authority: A1_CANONICAL
created: 2026-04-13T16:20:00-04:00
status: ACTIVE
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION Repo Authority

This file answers one startup question only:

**What is authoritative in this repository right now?**

## Canonical root

The canonical content root in this repository is **this `ION/` directory
itself**.

Use these root assumptions:

- package root: `ION/04_packages/kernel/`
- test root: `ION/tests/`
- doctrine root: `ION/01_doctrine/`
- architecture root: `ION/02_architecture/`
- registry root: `ION/03_registry/`
- templates root: `ION/07_templates/`

## Shell-root distinction

This extracted branch also has a **shell root** one level above this content
root:

`.`

That shell root carries:

- `pyproject.toml`
- editable-install semantics
- pytest configuration for `ION/tests`

Practical rule:

- use the **content root** for ordinary reading and code navigation
- use the **shell root** for package-aware commands such as editable install
  and pytest runs that rely on `pyproject.toml`

## Cursor carrier lane (IDE / local Steward mount)

For Cursor-as-carrier work aligned with `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
and `.cursor/rules/ion-carrier-mount.mdc`:

- **Cursor** is chassis/carrier; **ION roles** are mounted identities (boots + bounded packets).
- The **Cursor parent chat** is an available carrier by default; it operates as **task-scoped local STEWARD carrier** for orchestration only after explicit mount with bounded mission, this `ION/REPO_AUTHOR

### ION/03_registry/agent_context_system_registry.yaml

registry_id: ion.agent_context_system_registry.v1
status: ACTIVE_OPERATIONAL
rank: A2_CONTEXT_AUTHORITY
created: 2026-04-28
primary_protocol: ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
primary_index: ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md
primary_templates:
  - ION/07_templates/context/AGENT_CONTEXT_SYSTEM_CARD.md
  - ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md
  - ION/07_templates/context/AGENT_CONTEXT_PACKAGE_INDEX.md
context_authority_team:
  - role.ionologist
  - role.context_cartographer
  - role.runtime_cartographer
  - role.canon_librarian
  - role.template_curator
legacy_surfaces_policy:
  mini_capsule_status: STANDING_CONTINUITY_WITNESS_NOT_PRIMARY_CONTEXT_AUTHORITY
  boot_status: IDENTITY_AND_LAW_INPUT_NOT_COMPLETE_CONTEXT_PACKAGE
  root_projection_status: UI_OR_OPERATOR_PROJECTION_NOT_AGENT_PRIVATE_CONTEXT_SOURCE
  required_package_phrase: MINI/CAPSULE are witness inputs, not primary context authority. The active package is the operative context for this run.
agents:
  - role_id: role.steward
    display_name: STEWARD
    context_system_card: ION/05_context/current/agent_context_systems/STEWARD.context_system.md
    base_sources:
      - ION/03_registry/boots/STEWARD.boot.md
      - ION/03_registry/semantic_identities/STEWARD.semantic.yaml
      - ION/agents/steward/MINI.md
      - ION/agents/steward/CAPSULE.md
    package_strategy: orchestration and integration package with current cycle plan, authority map, carrier limits, and acceptance gates
    default_active_package_class: MISSION_ACTIVE_CONTEXT_P

### ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md

# LEAD DEV Active Operating Context V105

```yaml
schema_id: ion.lead_dev_active_operating_context.v105
created_at: 2026-05-02T20:58:20+00:00
production_authority: false
```

## True north

Make ION fully operational by proving every core system as wired runtime rather than preserving it as disconnected doctrine, plans, or isolated tests.

## Current branch truth

V105 audited 14 core systems: 3 ready surfaces, 11 partial/disconnected surfaces, 0 missing surfaces, and 0 blocking missing-surface findings.

## Active priority

1. Lifecycle-aware full/compact/forensic packaging.
2. JOC/front-door telemetry triad: lane timeline, receipt hydration mapper, debug overlay.
3. Carrier mount proof for ChatGPT browser, Cursor IDE, and Codex extension in Cursor.
4. Front-door Relay -> Steward -> Persona runtime proof.
5. Bounded worker adapter only after the above gates.

## Operational discipline

Do not invent new doctrine where existing ION systems already exist. First inspect, map, and wire. Every future pass should update the V105 cartography or supersede it with a newer generated audit.

### ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md

---
type: research
authority: A3_OPERATIONAL
template: RESEARCH
created: 2026-05-07
status: ACTIVE_RESEARCH
scope: codex_single_agent_context_lane
production_authority: false
live_execution_authority: false
---

# Codex Single-Agent Mini/Capsule Research

## Purpose

Research the older Mini/Capsule systems and define a simpler, bulletproof context
system for the standalone Codex chat lane that will sit beside the full ION chat.

This is not the Relay -> Steward -> multi-agent ION workflow. This is the smaller
single-agent continuity pattern that worked well in SOS, AETHER, AIMOS, and early
ION-BUILD, adapted with current ION guardrails.

## Evidence Read

Primary old-system evidence:

- `/home/sev/ION - Production/SOS/02_architecture/CONTEXT_PROTOCOL.md`
- `/home/sev/ION - Production/SOS/05_context/MINI.md`
- `/home/sev/ION - Production/SOS/05_context/CAPSULE.md`
- `/home/sev/ION - Production/AETHER-OS-V4/context/MINI.md`
- `/home/sev/ION - Production/AETHER-OS-V4/context/CAPSULE.md`
- `/home/sev/ION - Production/ION-BUILD/context/MINI.md`
- `/home/sev/ION - Production/ION-BUILD/context/CAPSULE.md`
- `/home/sev/ION - Production/ION-BUILD/context/MINI.compiled.md`
- `/home/sev/ION - Production/ION-BUILD/tools/capsule-compiler.js`
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/.agent/workflows/mini.md`
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/.agent/comms/capsules/codex/2026-03-13.md`
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/.agent/comms/capsules/opus/2026-03-17_1440_PRE_capsule-naming-redesign.md`
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/.agent/comms/capsules/opus/2026-03-17_1445_POST_cap

### ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md

---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE_PROVISIONAL
scope: codex_capsule_fallback_operating_kernel
production_authority: false
live_execution_authority: false
---

# Codex Capsule Operating Protocol

## Purpose

This protocol defines the small ION operating kernel for Codex CLI and Codex
chat carriers while the full ION Codex CLI system is still being built.

The capsule system is not a replacement for full ION. It is the fallback and
basic-ops layer that lets one capable Codex carrier stay oriented, bounded,
evidence-aware, and recoverable across long work.

## Operating Split

```text
Full ION
-> user-facing Persona chat
-> Relay / Steward / role workflow
-> Codex CLI bounded worker packets
-> proof gates
-> Steward integration
-> receipts and next context

Capsule ION
-> one Codex carrier
-> Capsule as minimum working context
-> Mini as pasteable lookup/receipt brief
-> explicit mode declaration
-> bounded plan / work / verification
-> capsule post receipt
```

The full path remains the target architecture. The capsule path preserves useful
work when full orchestration, UI, agents, actions, or services are incomplete,
blocked, or too heavy for the current step.

## Context Stack

Codex must treat these as the natural starting stack for serious ION work:

1. Active root proof: `pyproject.toml` and `ION/REPO_AUTHORITY.md`.
2. `ION/05_context/current/codex_solo/HOT_CONTEXT.md`.
3. `ION/05_context/current/codex_solo/CAPSULE.md`.
4. `ION/05_context/current/codex_solo/MINI.md`.
5. The active workpacket, protocol, test, or so

### ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md

---
protocol_id: ion.skill_activation_protocol.v1
status: ACTIVE_PROVISIONAL
rank: A3_OPERATIONAL
created: 2026-05-07
scope: codex_cli_capsule_and_full_ion_skill_activation
production_authority: false
live_execution_authority: false
---

# ION Skill Activation Protocol

## Purpose

Skills are the controlled activation layer for ION workflows. A skill may mount
context, choose a model move, choose a reasoning posture, select templates, and
route work through the correct carrier surface. A skill does not make output
lawful by itself.

Templates remain the proof contract. A completed action becomes admissible only
when the relevant template proof, validation evidence, and receipt/acceptance
gate are present.

```text
operator intent
-> skill selection
-> context mount
-> authority check
-> model/thinking route
-> template activation
-> bounded work or response
-> template action proof
-> validation
-> receipt / Capsule update
-> UI projection
```

## Definitions

**Skill**: user/Codex-facing reusable workflow activator. It answers when and
how a workflow should run.

**Template**: governed artifact/proof contract. It defines required sections,
authority boundaries, evidence expectations, validation, and receipt shape.

**Binding**: role-specific discipline for using a shared template. A binding
refines a template for a role; it does not replace the template.

**Capsule**: minimum working context for Codex solo work.

**Mini**: pasteable lookup and receipt index. Mini is not the primary prompt
source and is not authority.

## Authority Rule

A skill may never grant:

- producti

### ION/03_registry/ion_skill_registry.yaml

schema_id: ion.skill_registry.v1
status: ACTIVE_PROVISIONAL
authority_scope: A3_OPERATIONAL_SKILL_ACTIVATION
protocol: ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md
production_authority: false
live_execution_authority: false
secrets_authority: false
principle: "Skills activate workflows; templates govern proof."
default_context_mount:
  required_packages:
    - minimum_working_capsule
    - mini_lookup_index
    - active_authority_package
    - mission_active_package
  route_deeper_packages:
    - route_depth_package
    - evidence_receipt_package
    - recovery_package
global_proof_contract:
  context_proof_required: true
  template_action_proof_required_for_mutation: true
  receipt_required_for_material_work: true
  state_acceptance_requires_steward_or_human_gate: true
skills:
  - skill_id: codex-chat-answer
    display_name: Codex Chat Answer
    class: user_visible
    purpose: "Answer normal operator chat using Capsule context without queuing Codex work."
    trigger_summary: "Default for respond-only Codex chat."
    selection_priority: 40
    model_stage_id: persona_response
    preferred_model: gpt-5.5
    default_reasoning_effort: medium
    activates_templates:
      - ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md
    template_bindings: []
    context_mount:
      required_packages:
        - minimum_working_capsule
        - mini_lookup_index
        - mission_active_package
      route_deeper_packages:
        - active_authority_package
        - route_depth_package
    allowed_authority:
      read_context: true
      queue_work: false
      write_f

### ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md

---
protocol_id: ion.codex_chat_engine_protocol.v1
status: ACTIVE_PROVISIONAL
rank: A3_OPERATIONAL
created: 2026-05-08
scope: codex_chat_engine_capsule_skill_native_routing
production_authority: false
live_execution_authority: false
---

# ION Codex Chat Engine Protocol

## Purpose

The Codex Chat Engine turns a normal operator message into a high-quality chat
response path without making the operator manage ION internals. It is the
functional core under the UI.

The UI renders the engine. The engine does not render the UI.

## Target

The quality target is ChatGPT-browser-level conversation or better, integrated
with ION context, skills, templates, model moves, native lenses, proof gates,
and receipts.

```text
operator message
-> context mount
-> skill activation
-> ION native lens selection
-> model/thinking route
-> response mode
-> direct answer or existing Codex queue / full ION handoff
-> proof and receipt hydration
-> Capsule settlement when material
```

## Response Modes

The engine may select:

- `answer`: produce a normal useful assistant response;
- `clarify`: ask a concise question only when needed;
- `plan`: produce an executable plan without editing;
- `queue_work`: send bounded work to the existing Codex queue;
- `recover`: stop drift, inspect evidence, and repair orientation;
- `ion_handoff`: route into the full ION Relay/Steward workflow.

## Native Lenses

ION natives are not extra chatbots for every turn. They are lenses or workflow
routes selected only when useful.

- Persona: user-facing continuity and clarity.
- Relay: intent normalization and packet

### ION/03_registry/ion_native_lens_registry.yaml

schema_id: ion.native_lens_registry.v1
status: ACTIVE_PROVISIONAL
authority_scope: A3_OPERATIONAL_CHAT_ROUTING
protocol: ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md
production_authority: false
live_execution_authority: false
secrets_authority: false
default_lenses:
  - persona
  - context_cartographer
lenses:
  - lens_id: persona
    display_name: Persona
    role_id: role.persona_interface
    purpose: "Final user-facing clarity, tone, continuity, and concise answer shape."
    use_when:
      - normal_chat
      - final_response
    model_stage_id: persona_response
    template_refs:
      - ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md
  - lens_id: relay
    display_name: Relay
    role_id: role.relay
    purpose: "Normalize messy operator language into bounded intent and handoff shape."
    use_when:
      - ion_handoff
      - ambiguous_intent
    model_stage_id: relay_ingress
    template_refs:
      - ION/07_templates/bindings/RELAY__HANDOFF.md
  - lens_id: steward
    display_name: Steward
    role_id: role.steward
    purpose: "Authority, risk, route legitimacy, and acceptance boundary."
    use_when:
      - recovery
      - high_risk
      - ion_handoff
      - mutation
    model_stage_id: steward_route
    template_refs:
      - ION/07_templates/bindings/STEWARD__TASK.md
      - ION/07_templates/bindings/STEWARD__STATUS_REPORT.md
  - lens_id: vizier
    display_name: Vizier
    role_id: role.vizier
    purpose: "Architecture, system design, dependencies, and plan depth."
    use_when:
      - architecture
      - plan
    model_stage_id

### ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md

---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Capsule Chat Rebuild Orchestration

## Correction

The product target is not a forced two-chat app.

The target is one primary Codex CLI chat mounted through the Capsule/Mini/HOT_CONTEXT system. Full ION already has its own Relay/Steward/workflow communication surfaces, so the Capsule chat should interoperate with those existing surfaces rather than duplicate them.

## Product Shape

```text
Operator
-> Codex Capsule Chat
-> Capsule / Mini / HOT_CONTEXT / route packages
-> bounded Codex CLI work packets when work needs execution
-> receipts / task returns / Capsule post

Codex Capsule Chat
<-> existing ION comms / queue / receipt owners
<-> full ION Persona / Relay / Steward workflow
```

## Non-Negotiables

- The primary UI behavior is normal chat: user message in, visible assistant response out.
- Queue, pin, lane, receipt, and model routing concepts are support surfaces, not required user chores.
- Capsule context is opt-in for the Codex Capsule chat/profile.
- Do not globally inject Capsule into every Codex CLI instance.
- Do not create a second ION queue, second agent system, or parallel truth surface.
- Full ION communication remains owned by existing Relay/Steward/workflow queues and receipts.

## Implementation Phases

1. Correct the current chat projection from dual-chat-first to single Capsule-chat-first.
2. Keep bounded queue/memory/comms functions available as backend capabilities, but remove

### ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md

---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Chat App UI Orchestration

## Purpose

Build the proper user-facing Codex Chat app: a local web chat that feels
closer to Codex IDE / ChatGPT browser chat than a terminal, while using ION/JOC
for context, evidence, receipts, model routing, and operator visibility.

The app is not a second ION, not a second agent system, and not a replacement
for full ION Persona / Relay / Steward. It is the polished front door for Codex,
with Capsule operating as background context.

## Research Basis

Local evidence already supports this direction:

- `workpackets/ION_LOCAL_CODEX_IDE_MVP_PACKET_2026-05-07.md` says the IDE is a
  front door/cockpit over existing ION owners, not a second ION.
- `workpackets/ION_ACTIONS_CODEX_IDE_FULL_EXECUTION_PLAN_2026-05-07.md` says
  the IDE/cockpit should expose owner status and create packets/validation
  requests, not directly mutate canonical state.
- `ION/03_registry/joc_cockpit_layout_manifest.yaml` defines the JOC zones:
  top bar, left rail, main work surface, right inspector, bottom timeline.
- `ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx` shows the JOC shell pattern:
  top nav, icon rail, maintained work surface, receipt inspector, runtime
  stream.
- `ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md`
  establishes the corrected product target: one Capsule Codex chat with bounded
  full-ION comms.

## Product Judgment

The primary scre
