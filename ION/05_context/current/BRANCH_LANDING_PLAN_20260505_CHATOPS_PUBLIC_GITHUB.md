# Branch Landing Plan - ChatOps, Public Docs, Sandbox Return, JOC Restoration

created_at: 2026-05-05T14:58:21Z
branch: docs/github-public-data-plane-policy
production_authority: false
live_execution_authority: false
git_push_authority: false

## Context Proof

root_confirmed:
- `/home/sev/ION - Production/ION_CODEX`
- `pyproject.toml` present
- `ION/REPO_AUTHORITY.md` present

operator_confirmation:
- Braden confirmed the new ChatOps extension top-bar placement is live-acceptable after reload.

queue_hygiene:
- Receipt: `ION/05_context/current/chatgpt_connector/queue_hygiene/2026-05-05T145821Z_chatops_public_landing_queue_hygiene.json`
- Stale runner-active requests before cleanup: 8
- Stale runner-active requests after cleanup: 0
- No request packets were deleted.

## Landing Slices

### Slice A - Public README and Docs

Purpose:
- Make the public GitHub landing page concise and serious.
- Move ontology-heavy material into `ION/docs/`.

Primary paths:
- `README.md`
- `ION/docs/README.md`
- `ION/docs/ION_FUNDAMENTALS.md`
- `ION/docs/TEMPLATE_LAW.md`
- `ION/docs/CONTEXT_SYSTEM.md`
- `ION/docs/AGENTS_ROLES_CARRIERS.md`

Landing note:
- Avoid hardcoded test counts in public prose unless generated immediately before commit.

### Slice B - Sandbox Return Runtime

Purpose:
- Add first-class ChatGPT sandbox return intake as inbox evidence, not accepted source state.
- Add daemon endpoints and cockpit projection support.

Primary paths:
- `ION/02_architecture/ION_CHATGPT_SANDBOX_RETURN_INTAKE_PROTOCOL.md`
- `ION/03_registry/ion_chatgpt_sandbox_return.schema.json`
- `ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py`
- `ION/04_packages/kernel/ion_chatops_bridge.py`
- `ION/04_packages/kernel/ion_cockpit_view_model.py`
- `ION/tests/test_kernel_ion_chatgpt_sandbox_return_intake.py`
- `ION/tests/test_kernel_ion_chatops_bridge_policy.py`
- `ION/tests/test_kernel_ion_cockpit_view_model.py`
- `ION/03_registry/ion_chatops_extension_policy.yaml`
- `ION/03_registry/ion_chatops_local_daemon_policy.yaml`

Landing note:
- This is runtime code, not public-doc polish.
- Keep separate from README-only review.

### Slice C - ChatOps Browser Extension Topbar and Sandbox UI

Purpose:
- Keep the ChatOps extension within the ChatGPT top bar.
- Respect left rail/drawer, right Memory/Share/more controls, and narrower screen widths.
- Expose Agent/Packages/Sandbox controls without blocking chat input.

Primary paths:
- `ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/src/background.ts`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/dist/background.js`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/README.md`
- `ION/09_integrations/local_daemon/ion_chatops_bridge/README.md`

Manual proof:
- Braden confirmed the new extension placement after reload.

### Slice D - JOC Cockpit Restoration

Purpose:
- Restore missing direct imports used by `JocCockpitShell.tsx` from the local prior ION/Cursor tree.
- Preserve the current shell; do not replace it with the older shell.

Primary paths:
- `ION/08_ui/joc_cockpit_shell/AutomationOverlayPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/CognitiveExplorerPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/DispatchAuthorizationPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/DryRunDispatchHandoffPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/GovernorVerdictRail.tsx`
- `ION/08_ui/joc_cockpit_shell/InfiniteContextCommandPalette.tsx`
- `ION/08_ui/joc_cockpit_shell/MissionDispatchRouterPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/ModelRouteMatrixPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/OperatorApprovalQueuePanel.tsx`
- `ION/08_ui/joc_cockpit_shell/ReactiveOsStreamPanel.tsx`
- `ION/08_ui/joc_cockpit_shell/dispatch-authorization.css`
- `ION/08_ui/joc_cockpit_shell/dispatchAuthorizationTypes.ts`
- `ION/08_ui/joc_cockpit_shell/icons.tsx`
- `ION/08_ui/joc_cockpit_shell/joc-cockpit.css`
- `ION/08_ui/joc_cockpit_shell/operator-approval.css`
- `ION/08_ui/joc_cockpit_shell/operatorApprovalTypes.ts`
- `ION/08_ui/joc_cockpit_shell/projectionFixtures.ts`
- `ION/08_ui/joc_cockpit_shell/reactiveTypes.ts`

Validation note:
- Local import resolution is clean.
- There is no standalone `ION/08_ui` TypeScript build target yet.

### Slice E - Generated Runtime Receipts and Package Manifests

Purpose:
- Preserve operational evidence without mixing it into public/docs commits.

Primary paths:
- `ION/05_context/current/TRUNK_FILE_MANIFEST_BASELINE_V118.json`
- `ION/05_context/current/TRUNK_FILE_MANIFEST_POSTPATCH_V118.json`
- `ION/05_context/current/TRUNK_PRESERVATION_REPORT_V118.json`
- `ION/05_context/current/chatops_bridge/receipts/chatops_bridge_operation_20260505t044017z_export_safe_full_zip.json`
- `ION/05_context/current/chatgpt_connector/queue_hygiene/2026-05-05T145821Z_chatops_public_landing_queue_hygiene.json`
- `ION/05_context/current/BRANCH_LANDING_PLAN_20260505_CHATOPS_PUBLIC_GITHUB.md`

Landing note:
- Review generated artifacts separately. They may be evidence, not product source.

## Required Validation Before Push

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_queue_runner --ion-root . --json
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q -p no:cacheprovider
```

Expected minimum:
- `ion_status` verdict: `ION_STATUS_READY`
- `ion_codex_queue_runner` queued request count: `0` before a new smoke packet is intentionally created
- browser parser smoke: `ok: true`
- Python suite: pass

## Next Lawful Moves

1. Stage and commit Slice A alone if the next goal is public GitHub readability.
2. Stage and commit Slice B only after reviewing runtime diffs.
3. Stage and commit Slice C after the live extension placement proof remains acceptable across left drawer open/closed.
4. Stage and commit Slice D after deciding whether to add a real JOC TypeScript build harness.
5. Keep Slice E as evidence or move it into a deliberate evidence commit; do not mix it silently into public docs.
6. Create one fresh browser ChatOps `create_codex_work_packet` smoke after the queue is clean, then run one bounded queue-runner cycle.
