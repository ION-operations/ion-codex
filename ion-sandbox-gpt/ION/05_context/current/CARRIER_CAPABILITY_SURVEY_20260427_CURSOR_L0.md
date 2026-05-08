# CARRIER_CAPABILITY_SURVEY — filled instance (2026-04-27, Cursor, L0 mount test)

## Session instance — L0 mount test — 2026-04-27 — Cursor (external host)

- Session ID: `L0-MOUNT-TEST-20260427`
- Host: Cursor (external AI session; no trusted prior ION role)

### Copy from `ACTIVE_WORK_PACKET.json` (cited from disk)

- `shell_root`: `/home/sev/ION - Production/ION most recent/CURSOR- ION/IONcursorbuild/ION_MASTER_CURRENT_3_V69_HANDOFF_PACKAGE_ASSEMBLY_PLAN_AND_CHECKSUM_PREVIEW_FULL_PROJECT_20260426/ION MASTER CURRENT`
- `objective`: `install deterministic carrier cycle runner so Cursor executes spawn=true role passes only`
- `workstream`: `implementation`
- `carrier`: `cursor`
- `validation_commands`:
  1. `test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md`
  2. `python3 -m kernel implementation "install deterministic carrier cycle runner so Cursor executes spawn=true role passes only"`
- `visible_report_target`: `ION/05_context/signals and relay lane per workstream closure`
- `next_lawful_action`: After `required_read_order`, run `python3 -m kernel implementation` with the above objective; require `required_surfaces_ok: True` in the printed trace; then execute first role pass (steward) using only required reads for that pass.
- Active work packet file exists: **yes** — `ION/05_context/current/ACTIVE_WORK_PACKET.json`

### Spawn plan (L3)

- `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`: **yes** (on disk; objective inside file is `test deterministic spawn plan` — **not identical** to current `ACTIVE_WORK_PACKET` objective; treat as stale plan until runner re-run for current packet).
- `spawn: true` roles from that file (verbatim): steward, vizier, mason

### Host proofs (this session only)

| Capability | Claim | Evidence path |
|------------|-------|-----------------|
| File read | yes | `ION/REPO_AUTHORITY.md`; `ION/04_agents/carriers/META_CARRIER_EVOLUTION_PROTOCOL.md`; `ION/03_registry/capabilities/capability_registry.json` — read via host; see `reports/ION_L0_CARRIER_MOUNT_TEST.md` |
| File write under `ION/**` | **only after** this append + report write | `ION/05_context/current/CARRIER_CAPABILITY_SURVEY_20260427_CURSOR_L0.md` (this file); `reports/ION_L0_CARRIER_MOUNT_TEST.md` |
| Shell | **unproven this turn** | — |
| Python / pytest | **unproven this turn** | — |
| `ion_carrier_onboard` | **unproven this turn** (not executed here) | — |
| `ion_cycle_runner` | **unproven this turn** (not executed here) | — |
| Host subagents | **not used this turn** | — |

### Requested level

- Current operating level: **L0** (Manual Carrier) until decision artifact exists.
- Requested level: **L1** (tool-assisted: bounded read + single report write for mount test only). **Not** requesting L2 (no subagent proof filed this turn).

### Upgrade gate

- `ION/05_context/signals/CARRIER_LEVEL_DECISION.json`: **no** (not present at survey time).
- **No self-approval** — remain **L0** for any capability that lacks file-backed proof per registry.
