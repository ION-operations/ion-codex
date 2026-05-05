# Cursor agent handoff — 2026-04-28

Read this before doing substantive ION work. This chat is ending; this file is the continuity bridge.

## 1. Authoritative workspace root (shell root)

**Treat the Cursor workspace folder as the ION shell root:**

`/home/sev/ION - Production/ION most recent/CURSOR- ION`

Expected at that root: `pyproject.toml`, `AGENTS.md`, `.cursor/`, `ION/`, `ION/REPO_AUTHORITY.md`.

**Do not** assume the old nested path is still the live tree:

`…/IONcursorbuild/ION_MASTER_CURRENT_3_V69_HANDOFF_PACKAGE_ASSEMBLY_PLAN_AND_CHECKSUM_PREVIEW_FULL_PROJECT_20260426/ION MASTER CURRENT/`

That layout was **lifted** to the workspace root, then the old `IONcursorbuild` tree was **moved to archive** (see below). If you still see the deep path in editor tabs, **reload the window** and open the workspace at `CURSOR- ION` only.

## 2. What was reorganized (2026-04-28)

- The full contents of the former `ION MASTER CURRENT` shell were **rsync’d** into `CURSOR- ION` (merge into workspace root).
- **`IONcursorbuild/`** was moved to:
  - `_archive/IONcursorbuild_nested_handoff_20260426/`
  (full duplicate of the old nested handoff; safe to delete after human confirms nothing needed from it.)
- Loose carrier / handoff artifacts were moved to:
  - `_archive/carrier_packages/`
  (includes e.g. `ION_CARRIER_RUNTIME_FOUNDATION_PACKAGE_20260428/`, related zips, overlay zips, `IONcursorbuild2.zip`.)

## 3. High-risk cleanup the human approved (same day)

On the shell **before** the lift (now reflected at workspace root), the following were removed intentionally (external non-git backups exist):

- `.git` under that shell (workspace root may have **no** git until `git init` is run again).
- Nested mistake tree `ION/ION/` (small set of history/signal files).
- Duplicate `ION/pyproject.toml` (identical to root `pyproject.toml`; only root file kept).
- Extract residue folder `ION_CARRIER_RUNTIME_FOUNDATION_FIX_20260428/` under shell root.
- Stray `.zip` in shell root, `.pytest_cache/`, `__pycache__/`, `*.pyc` under that tree.
- Entire duplicate project: **`IONmcp/`** (including its `ION MASTER CURRENT`).

## 4. Carrier runtime foundation (already merged + fix)

- **Foundation package** was applied from folder `ION_CARRIER_RUNTIME_FOUNDATION_PACKAGE_20260428` (zip not required on disk).
- **Fix package** `ION_CARRIER_RUNTIME_FOUNDATION_FIX_20260428.zip` was unzipped and merged; it added among other things:
  - `ION/07_templates/carriers/CARRIER_UPGRADE_REQUEST.md`
  - `--write-current` on `kernel.ion_carrier_onboard` (alias for `--force` refresh of `ACTIVE_WORK_PACKET.json`)
  - `test_kernel_ion_carrier_onboard.py` fixes (minimal repo layout, subprocess `PYTHONPATH`).

**Lawful carrier cycle** (see root `AGENTS.md` and `.cursor/rules/ion-carrier-runtime-foundation.mdc`):

1. `kernel.ion_carrier_onboard` → `ION/05_context/current/ACTIVE_WORK_PACKET.json`
2. `kernel.ion_cycle_runner` → `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`
3. Execute only `spawn: true` rows in the spawn plan; do not infer spawns from chat.

## 5. Commands that should work from workspace root

```bash
cd "/home/sev/ION - Production/ION most recent/CURSOR- ION"
export PYTHONPATH=ION/04_packages
python3 -m pytest -q ION/tests/test_kernel_ion_carrier_onboard.py ION/tests/test_kernel_ion_cycle_runner.py
python3 -m kernel.ion_carrier_onboard --ion-root ION --carrier cursor --objective "…" --write-current --json
python3 -m kernel.ion_cycle_runner --ion-root ION --carrier cursor --workstream implementation --objective "…" --spawn-policy required --write-current --json
```

`pyproject.toml` already sets `pythonpath = ["ION/04_packages"]` for pytest when run from root.

## 6. Cursor / rules

- **AlwaysApply rule:** `.cursor/rules/ion-carrier-runtime-foundation.mdc`
- **Session hook:** `.cursor/hooks.json` runs `python3 .cursor/hooks/ion_session_start_persona_mount.py` on session start; keep it fast and non-blocking.

## 7. Do not regress

- Do not revive **MINI/CAPSULE** or sibling/archive roots as primary authority unless doctrine explicitly says so.
- Do not fake STEWARD / RELAY / PERSONA voice in agent output.
- Do not treat removed `IONmcp/` or `_archive/` trees as the live shell without human direction.

## 8. Optional follow-ups for the human or next agent

- `git init` (and `.gitignore`) at workspace root when version control is wanted again.
- Delete `_archive/IONcursorbuild_nested_handoff_20260426/` after confirming no unique files remain (saves duplicate disk).

## 9. Full test suite and root-authority bundle (2026-04-28)

- `pytest ION/tests` is green from workspace root (`PYTHONPATH` set via `pyproject.toml` / `.vscode/settings.json`).
- After removal of the mistaken `ION/ION/` tree, the **root authority bundle** (`ION/05_context/exports/2026-04-17_root_authority_bundle/`) was updated so `embedded_residue_lane` and `START_HERE.md` reference **`ION/05_context`** only; backticks must not reintroduce non-existent `ION/ION/…` paths or `build_snapshot` will mark the bundle invalid.
- **Meta carrier** `capability_registry.json` includes the six capabilities required by `test_meta_carrier_minimal.py` (`active_work_packet`, `active_role_spawn_plan`, `kernel_implementation_trace`, `python_toolchain`, `host_subagent`, `mcp_runtime`).
- `ion_carrier_onboard` exports `resolve_shell_root_from_ion_root` and `CarrierOnboardError` with `.code` for legacy tests.

## 10. Carrier-shaped Cursor surface (2026-04-28)

- **Session start hook** (`.cursor/hooks.json` → `ion_session_start_persona_mount.py`) runs **`ion_carrier_onboard`** then **`ion_cycle_runner`** with a fixed bootstrap objective, writes both JSON files, and injects a **spawn schedule** listing only `spawn=true` rows (procedural text only).
- **VS Code / Cursor tasks** (`.vscode/tasks.json`): kernel pytest shortcuts; **onboard**; **cycle runner**; **onboard then cycle (one prompt, write both)**; echo paths for active packet / spawn plan.
- **Settings** (`.vscode/settings.json`): `PYTHONPATH` in integrated terminals; Pylance `extraPaths`; pytest cwd; `_archive` excluded from search/watch.
- **Rule pointer:** `.cursor/rules/ion-carrier-runtime-foundation.mdc` documents tasks + hook.

---

**Handoff status:** workspace flattened to `CURSOR- ION`; carrier foundation + fix applied; aggressive duplicate and `.git` cleanup completed per human approval; full `ION/tests` passing; next agent should work only from this root unless told otherwise.
