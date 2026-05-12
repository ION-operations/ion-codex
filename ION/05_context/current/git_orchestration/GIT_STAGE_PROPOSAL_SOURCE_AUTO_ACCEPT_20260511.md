# Source Auto-Accept Stage Proposal - 2026-05-11

Status: candidate stage proposal, not staged  
Production authority: false  
Live execution authority: false  
Git add authority: false  
Git commit authority: false  
Git push authority: false  

## Scope

This lane covers the governed Action Gateway auto-accept controls and browser-extension top-bar/native-action confirm behavior. It excludes runtime evidence, JOC UI work, context-package settlement, and B00 duplicate/no-receipt residue.

## Exact Path Count

`18` paths.

## Candidate Command - Not Executed

```bash
git add --pathspec-from-file=ION/05_context/current/git_orchestration/GIT_STAGE_PATHSPEC_SOURCE_AUTO_ACCEPT_20260511.txt
git diff --cached --stat
git diff --cached
git commit -m "Add governed Action auto-accept controls"
```

Do not run these until the operator approves this exact lane. Do not push from ChatOps/extension automation.

## Required Gates

- Operator approval of exact paths.
- Confirm generated `dist/` files intentionally travel with `src/` files.
- Staged diff review after `git add`.
- Staged secret/public-safety scan before commit.
- Targeted validation only if requested.

## Paths

- `M` `ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml`
- `M` `ION/04_packages/kernel/ion_chatops_bridge.py`
- `M` `ION/04_packages/kernel/ion_custom_gpt_action_gateway.py`
- `??` `ION/09_integrations/browser_extension/ion_chatops_bridge/AGENT_INVOCATION_LANE_CONTRACT.json`
- `??` `ION/09_integrations/browser_extension/ion_chatops_bridge/QUEUE_PACK_AUTHORING.md`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/README.md`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/dist/background.js`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js`
- `??` `ION/09_integrations/browser_extension/ion_chatops_bridge/examples/ION_QUEUE_PACK_EXAMPLE.json`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/src/background.ts`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts`
- `M` `ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js`
- `M` `ION/09_integrations/custom_gpt_action_gateway/README.md`
- `M` `ION/09_integrations/custom_gpt_action_gateway/openapi.yaml`
- `M` `ION/tests/test_kernel_ion_chatops_bridge_policy.py`
- `M` `ION/tests/test_kernel_ion_custom_gpt_action_gateway.py`
- `M` `ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py`
