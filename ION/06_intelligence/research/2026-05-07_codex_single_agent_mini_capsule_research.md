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
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/.agent/comms/capsules/opus/2026-03-17_1445_POST_capsule-naming-redesign.md`
- `/home/sev/AIMOS - Builds/AIM-OS-GIT/canon/agents/ONBOARDING_PACKAGE.md`

Current ION evidence:

- `ION/03_registry/agent_context_system_registry.yaml`
- `ION/04_packages/kernel/capsule_manager.py`
- `ION/02_architecture/ACTIVATION_SUMMARY_HANDOFF_CAPSULE_MATERIALIZATION_PROTOCOL.md`
- `ION/06_intelligence/roundtable/continuity_crisis/proposals/2026-04-03_minimal_manual_continuity_update_protocol.md`

## What Worked Best

The strongest single-agent design was SOS Mode A:

- `MINI.md` is routing state, not a novel or full memory.
- `MINI.md` has a hard size limit: 30 lines.
- It carries only mission, phase, now, blocker, next, active template, and route.
- The new session reads `MINI.md` first, then follows the route list.
- `CAPSULE.md` is append-only work history.
- Capsule entries stay one line and point to detailed artifacts elsewhere.
- Before updating capsule state, the old file is copied into `history/`.
- The manual IDE-agent surface is separated from daemon/swarm state.

This separation matters. The old SOS protocol explicitly split:

- Mode A: human plus IDE agent, durable state through manual Mini/Capsule updates.
- Mode B: headless agents, fresh compiled context package, automated ledger/signals.

For the new Codex chat lane, we want Mode A. We do not want the full ION worker
pipeline in this lane.

## What Failed Or Drifted

The old systems also show failure modes:

- Early ION-BUILD `CAPSULE.md` became too large and too narrative.
- The old Codex private `MINI.md` grew to tens of thousands of bytes and stopped
  being a mini routing state.
- Root projections were sometimes confused with true private continuity.
- PRE/POST capsule text could become performative if not tied to filesystem state.
- Cross-root routes appeared in old mini files, which can confuse active project
  identity.

Current ION already corrected part of this: the active registry says
Mini/Capsule are witness inputs, not primary context authority. For the solo
Codex lane, that rule should be preserved, but softened into practical language:

```text
Mini/Capsule guides continuity. It does not override current repo authority,
tests, receipts, or explicit operator instructions.
```

## Target Design: Codex Solo Context Capsule

Create one standalone context surface for the general Codex chat lane:

```text
ION/05_context/current/codex_solo/
  MINI.md
  CAPSULE.md
  STATUS.json
  ROUTE.json
  HOT_CONTEXT.md
  history/
    YYYYMMDD_HHMMSS_PRE_MINI.md
    YYYYMMDD_HHMMSS_PRE_CAPSULE.md
    YYYYMMDD_HHMMSS_POST.json
```

`MINI.md`:

- Human-readable.
- Maximum 30 lines.
- Updated after a meaningful work unit, not every message.
- Contains only mission, phase, now, blocker, next, active template, route.
- Route entries must be repo-relative unless explicitly marked external witness.

`CAPSULE.md`:

- Human-readable append-only ledger.
- One table row per work unit.
- No long prose.
- Detailed notes live in `ION/06_intelligence/research/`, `ION/docs/`, tests,
  receipts, or other normal artifacts.

`STATUS.json`:

- Machine-readable current state.
- Derived from `MINI.md`, `CAPSULE.md`, latest turns, and verification.
- Includes `production_authority=false` and `live_execution_authority=false`.

`ROUTE.json`:

- Machine-readable route set.
- Each path has `path`, `required`, `classification`, `sha256`, `exists`.
- Missing required route entries block queueing until repaired.

`HOT_CONTEXT.md`:

- Compiled, bounded, generated context package for the single Codex lane.
- Generated from MINI route, capsule tail, pinned memory, current workpackets,
  and selected current ION guardrails.
- It is input context, not state.

## Boot Protocol

For the standalone Codex chat:

1. Resolve active root as `/home/sev/ION - Production/ION_CODEX FULL`.
2. Read `ION/05_context/current/codex_solo/MINI.md`.
3. Read `ION/05_context/current/codex_solo/CAPSULE.md`.
4. Read every required path in `ROUTE.json`.
5. Read current ION guardrails:
   - `ION/REPO_AUTHORITY.md`
   - `ION/03_registry/agent_context_system_registry.yaml`
   - `ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md`
6. Build `HOT_CONTEXT.md`.
7. Start the chat lane from that context.

If `MINI.md` does not exist yet, initialize it from the current work objective and
the current ION guardrails. Do not search other ION roots except as explicitly
marked historical witness.

## Work Unit Protocol

One Codex solo work unit should do this:

1. PRE checkpoint:
   - copy current `MINI.md` and `CAPSULE.md` to `history/`
   - write a small PRE JSON record
2. Work:
   - inspect files
   - modify only active root files
   - run focused checks when relevant
3. POST checkpoint:
   - append one row to `CAPSULE.md`
   - update `MINI.md` with the next route
   - update `STATUS.json` and `ROUTE.json`
   - compile `HOT_CONTEXT.md`

No hidden memory claim is allowed. If memory matters, it is either in the capsule
ledger, a pinned memory file, or a named artifact path.

## Improvements From Current ION

Use these current ION ideas, but keep them small:

- Authority ceiling in every machine-readable state file.
- Route entries have existence and hash checks.
- Context package is compiled, not improvised.
- Mini/Capsule is witness continuity, not repo law.
- Proof/test paths are first-class fields.
- External historical roots are marked `historical_witness` and never silently
  treated as active project roots.
- Queueing Codex work carries the current route set and capsule checkpoint.

Do not import the full current ION context-window machinery into this lane yet.
That would recreate the complexity the solo chat is meant to avoid.

## 2026-05-07 Correction: Capsule-First Evolution

Sev clarified the later evolution of this pattern:

- `CAPSULE.md` is the minimum working context the AI should carry.
- `MINI.md` is not what the AI primarily works from.
- `MINI.md` is a receipt and lookup summary for finding past capsule rows,
  capsule snapshots, route data, and evidence paths.
- `HOT_CONTEXT.md` should therefore load Capsule first, Mini second, then
  route validation and excerpts.

This is still not a claim that Mini/Capsule outranks ION repo authority. The
correct boundary is: Capsule is the solo lane's minimum continuity context;
Mini indexes that continuity; current repo authority, tests, receipts, and
explicit operator instructions still outrank both.

## 2026-05-07 Implementation Addendum: Multi-Horizon Spine

The approved implementation extends the capsule-first lane with explicit rolling
windows and package selection:

- `CAPSULE.md` remains the active short-horizon context.
- `MINI.md` indexes recent receipts and lookup paths.
- `LONG_HORIZON.json` groups older capsule rows into compressed epochs.
- `CONTEXT_PACKAGES.json` names the available context package types: minimum
  capsule, Mini lookup, long-horizon capsule index, active authority, mission,
  route-depth, evidence/receipt, and recovery.
- `HOT_CONTEXT.md` loads Capsule first, then Mini, then long-horizon summary,
  package selector, route validation, and route excerpts.

Default rolling windows:

```text
active capsule context: 80 lines
Mini lookup: 5 recent capsule rows
long-horizon epoch: 10 capsule rows
hot-context epoch window: 6 recent epochs
route excerpt: 1600 chars per file
```

## UI Implication

The two-chat app should have:

- Left or primary lane: full ION chat, showing Relay/Steward/Persona pipeline.
- Side lane: Codex solo chat, showing Capsule first, Mini lookup index, Route, Hot Context,
  pinned memory, and recent proof artifacts.

The Codex solo lane should feel like a practical engineering assistant:

- current task
- next step
- route files
- memory pins
- queue/run/test buttons
- no ceremony unless a proof gate requires it

## Implementation Recommendation

Implement the Codex solo lane before deepening the full ION chat UI:

1. Add `kernel/ion_codex_solo_context.py`.
2. Add helpers:
   - `load_codex_solo_state(root)`
   - `initialize_codex_solo_context(root)`
   - `compile_codex_solo_hot_context(root)`
   - `record_codex_solo_pre(root, ...)`
   - `record_codex_solo_post(root, ...)`
   - `validate_codex_solo_route(root)`
3. Wire the general Codex chat lane to these helpers.
4. Add tests that prove:
   - MINI hard limit is enforced.
   - CAPSULE entries stay append-only.
   - route paths are repo-relative unless marked historical witness.
   - missing required route entries block queue packets.
   - HOT_CONTEXT is generated from explicit paths only.
5. Leave the full ION lane on the existing pipeline model.

## Bottom Line

The best old system was simple, with Sev's capsule-first correction:

```text
CAPSULE is the minimum working context.
MINI indexes capsule history and receipt lookup.
PRE/POST snapshots make chat death survivable.
Everything detailed lives in normal files.
```

For the standalone Codex chat, rebuild that exact shape with current ION safety:
explicit active root, route validation, hashes, no hidden state, and no confusion
between witness continuity and authoritative repo state.
