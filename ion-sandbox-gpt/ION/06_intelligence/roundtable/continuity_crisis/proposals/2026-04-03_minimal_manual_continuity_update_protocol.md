---
type: proposal
authority: A3_OPERATIONAL
template: SYSTEM_EVOLUTION
from: Codex
created: 2026-04-03T12:28:54-04:00
status: PROPOSED
ratification: NOT_RATIFIED
responding_to:
  - ION/06_intelligence/roundtable/continuity_crisis/references/2026-04-03_codex_continuity_dependency_register.md
  - ION/06_intelligence/roundtable/continuity_crisis/synthesis/2026-04-03_ion_core_and_continuity_synthesis.md
  - ION/06_intelligence/research/2026-04-03_builder_continuity_roundtable.md
---

# Proposed Minimal Manual Continuity Update Protocol

## Purpose

This proposal exists to supply the thinnest explicit update-obligation layer the
active `ION/` root currently lacks.

It is meant for Phase 0B manual operation.
It is not a full restored template stack.

---

## Protocol

### Step 1: Load lawful source state first

Before meaningful work:

1. read your boot document
2. read your private `MINI.md`
3. read your private `CAPSULE.md` if it exists
4. read the task packet or governing artifact for the current work
5. read any specifically routed supporting files

Do not begin from root projections as if they were your source continuity.

### Step 2: Establish a PRE checkpoint

Before mutating your continuity:

1. ensure your private lane has a `history/` directory
2. if `MINI.md` exists, copy it to `history/{timestamp}_PRE_MINI.md`
3. if `CAPSULE.md` exists, copy it to `history/{timestamp}_PRE_CAPSULE.md`

If no continuity file exists yet, create the initial file in your own lane and
record that this was an initialization rather than a mutation.

### Step 3: Perform one bounded work unit

The work unit must produce at least one visible artifact:

- a research note,
- audit note,
- decision/proposal,
- code/output artifact,
- or other lawful public result.

The work unit should stay bounded enough that the resulting continuity delta is
legible.

### Step 4: Update private continuity

At completion, update:

1. your private `CAPSULE.md`
   - what was done
   - what changed
   - what remains unresolved
2. your private `MINI.md`
   - current mission
   - now
   - next
   - exact route/load set for the next turn

### Step 5: Emit public visibility

After updating private continuity:

1. emit or update at least one public artifact
2. emit a signal pointing to that artifact

If the work is leadership-sensitive, review-sensitive, or roundtable-sensitive,
the public artifact must be sufficient for another role to inspect without
access to hidden chat state.

### Step 6: Handle projections honestly

If you are not the currently designated projection curator, do not update root
projection surfaces.

If you are the currently designated projection curator, either:

1. update the relevant projection explicitly as a projection, or
2. record that projection update was intentionally deferred

Never silently treat a projection update as source continuity.

### Step 7: Trigger review or audit when required

If the work touches continuity law, architecture, doctrine, release posture, or
other review-sensitive surfaces:

1. route the result to the relevant review lane
2. do not silently self-ratify

### Step 8: Pass the chat-death test

At the end of the work unit, the role should be able to lose the chat and
resume from:

1. boot document
2. private `MINI.md`
3. private `CAPSULE.md`
4. emitted public artifact(s)
5. signals/task packet

If that is not true, the work unit is not yet a clean continuity event.

---

## Minimal Invariants

1. Source continuity is private.
2. Every meaningful work unit leaves both private and public traces.
3. History exists before mutation, not after regret.
4. Projections are never confused with source.
5. A fresh chat must be able to resume.

## Open Questions

1. Is this thin enough for immediate use, or does the table want explicit PRE
   and POST capsule formatting before accepting it?
2. Should signal emission be mandatory for every work unit, or only for
   cross-role relevant work?
3. Should the first proof loop require a designated projection curator, or can
   projection update be deferred entirely?
