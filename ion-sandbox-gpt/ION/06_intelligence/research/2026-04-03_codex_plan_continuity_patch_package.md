---
type: research
from: Codex
authority: A3_OPERATIONAL
created: 2026-04-03T13:43:16-04:00
status: FILED
subject: Minimal PLAN.md continuity patch package
responding_to:
  - ION/PLAN.md
  - ION/06_intelligence/research/2026-04-03_codex_plan_surface_drift_note.md
  - ION/06_intelligence/roundtable/continuity_crisis/synthesis/2026-04-03_continuity_law_candidate.md
  - ION/06_intelligence/roundtable/continuity_crisis/synthesis/2026-04-03_continuity_recovery_conditions.md
  - ION/06_intelligence/decisions/relay_vestige_continuity_class.md
---

# Codex PLAN Continuity Patch Package

## Purpose

This package gives Vizier a minimal, low-risk continuity correction for `ION/PLAN.md`
without reopening the broader roadmap, kernel, or daemon sections.

The target is narrow:

- stop the plan from teaching root shared continuity as universal source continuity
- align the plan with the current source/projection split
- preserve the new supervisor-role exception for lane-native continuity

## Scope boundary

This package intentionally does **not** attempt to rewrite the entire plan.

It should only affect:

1. the continuity bullets inside `EXECUTION MODE DECLARATION`
2. the section currently titled `CANONICAL SHARED-STATE MAP`

## Replacement A — continuity bullets under EXECUTION MODE DECLARATION

Replace the continuity-specific bullets in that section with:

```md
- All agents are IDE-resident chat sessions or Vizier-dispatched subagents.
- Source continuity is role-owned and loaded first.
- Core task roles use `ION/agents/{role}/MINI.md` and `ION/agents/{role}/CAPSULE.md` as source continuity.
- Supervisor roles may use lane-native private continuity when the lane itself is the stable private state family (currently Relay and Vestige).
- Root `ION/MINI.md`, `ION/CAPSULE.md`, and `ION/STATUS.md` are shared projections or temporary manual substitutes during recovery, not universal raw continuity.
- Interchange happens through `ION/05_context/inbox/`, `ION/05_context/signals/`, public intelligence artifacts, and explicit handoff/review packets.
- No daemon/autonomous mode is active during consolidation.
- When the daemon is built (Phase 3), it will use its own state surfaces (`system_ledger.json`, `active_routes.json`) per Mode B — those are separate from IDE continuity.
```

## Replacement B — replace CANONICAL SHARED-STATE MAP

Replace the entire section with:

```md
## CANONICAL CONTINUITY AND COORDINATION MAP

These are the active continuity and coordination surfaces in the unified root during
manual recovery and IDE-native operation.

| Surface | Canonical Location | Owner | Purpose |
|---------|-------------------|-------|---------|
| Core role private routing | `ION/agents/{role}/MINI.md` | Owning role | Source routing continuity for core task roles |
| Core role private work log | `ION/agents/{role}/CAPSULE.md` | Owning role | Source work continuity for core task roles |
| Supervisor role private continuity | Role-owned lane continuity family (for example `ION/06_intelligence/relay/relay/` or `ION/06_intelligence/archaeology/vestige/`) | Owning role | Source continuity for lane-native supervisor roles |
| Routing projection | `ION/MINI.md` | Vizier | Shared operator projection / temporary manual substitute |
| Work projection | `ION/CAPSULE.md` | Vizier | Shared operator projection / temporary manual substitute |
| Status projection | `ION/STATUS.md` | Vizier | Coordination projection / temporary manual substitute |
| Master plan | `ION/PLAN.md` | Vizier | System plan |
| Task inbox | `ION/05_context/inbox/` | Vizier creates, agents consume | Task dispatch |
| Signal bus | `ION/05_context/signals/` | Any agent may emit own signals | Machine-readable public events |
| Constitution | `ION/01_doctrine/SOVEREIGN_CONSTITUTION.md` | Sovereign only | Supreme law (PROVISIONAL until T32) |
| Kernel | `ION/01_doctrine/SOVEREIGN_KERNEL.md` | Sovereign only | Operational physics (PROVISIONAL until T32) |
| Registry | `ION/03_registry/agent_registry.json` | Sovereign only | Agent identities (PROVISIONAL until T32) |
| Templates | `ION/07_templates/` | Sovereign only | Template registry |
| Intelligence | `ION/06_intelligence/` | Agents write in their own lanes, all read | Evidence, research, audits, decisions, specs |

No role treats root `ION/MINI.md`, `ION/CAPSULE.md`, or `ION/STATUS.md` as its private
continuity source. Public interchange happens through inbox, signals, and visible
artifacts rather than cross-role continuity access.
```

## Why this wording

- It matches the continuity law candidate and recovery conditions closely enough to
  stop active teaching drift.
- It preserves the lane-native supervisor decision for Relay and Vestige instead of
  forcing a false universal `ION/agents/*` statement.
- It does not prematurely settle the future compiled-projection path.

## Non-goals

- not a full `ION/PLAN.md` revision
- not a ratification artifact by itself
- not a patch to `CONTINUITY_ARCHITECTURE.md`

## Follow-on after patch

Once the plan is corrected, the next stale high-authority surfaces should be reviewed
in order:

1. `ION/02_architecture/CONTINUITY_ARCHITECTURE.md` for the supervisor-role exception
2. any remaining boot docs that still front-load root projections
3. template surfaces that still imply shared-root append/update behavior
