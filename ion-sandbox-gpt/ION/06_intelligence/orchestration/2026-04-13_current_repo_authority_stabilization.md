---
type: orchestration_record
authority: A1_CANONICAL
created: 2026-04-13T16:35:00-04:00
status: ACTIVE
---

# Current repo authority stabilization

## Why this exists

The current recovered branch was executable and internally coherent, but its root startup surface still leaked an older extracted pathname:

`ION_Working_Branch_M16/ION`

That pathname was historically true during extraction and recovery, but inside the present repository it is now misleading at the exact moment a fresh executor asks the most important question:

**what is the active root here?**

This stabilization note resolves that ambiguity without rewriting older lineage records.

## Resolution

The current canonical runnable root is the present repository root:

`ION/`

The historical extracted pathname remains preserved only as a recovery alias.

## What changed

1. Added `ION/REPO_AUTHORITY.md` as the explicit root authority surface.
2. Updated `ION/README.md` so the root no longer presents the old extracted pathname as the live startup root.
3. Updated `ION/STATUS.md` and `ION/SYSTEM_MAP.md` so the new root authority surface participates in startup orientation.
4. Preserved older packet and handoff records unchanged, because they remain accurate as historical execution receipts.

## Governing rule after stabilization

- current repo startup should anchor on branch authority first
- executable center remains `ION/04_packages/kernel/` plus `ION/tests/`
- recovery and corpus-wide archaeology remain witness layers
- any promotion from wider-estate witness into current-root authority requires a new bounded packet

## Startup consequence

A fresh executor can now recover the current branch center from the repo root itself without needing to interpret historical extracted-path phrasing before understanding what is live.

## Non-goal

This note does not attempt a project-wide rewrite of all historical references to the earlier extracted pathname. Those references remain valid as time-bound recovery records.
