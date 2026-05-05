---
type: protocol
authority: A2_OPERATIONAL
status: ACTIVE
supersedes_mount_narrative: false
---

# ION mount contract (canonical operational order)

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

This file is the **single canonical mount and cycle law** for substantive ION work on this root.  
It sits **under** `ION/REPO_AUTHORITY.md` (repo authority) and **above** Cursor rules, work-cycle packets, and carrier guides, which **must remain subordinate** to it.

**Operational mount order is governed by this file** — other documents only refine surfaces.

## Preconditions

1. **Carrier starts UNMOUNTED** (no implicit Steward, no implicit Relay owner).
2. **Confirm shell root:** `pyproject.toml` and `ION/REPO_AUTHORITY.md` exist as siblings at the shell root.

## Required reads (before mount)

3. Read, in order:
   - `ION/REPO_AUTHORITY.md`
   - **this file** — `ION/02_architecture/ION_MOUNT_CONTRACT.md`
   - the selected carrier profile under `ION/03_registry/`
   - the selected carrier execution packet template under `ION/07_templates/carriers/`
   - the role boot/context package named by the active packet or spawn row

Former shell-root markdown files such as `AGENTS.md` and
`START_HERE_FOR_ANY_AGENT.md` are retired from hot mount authority. Contained
copies are historical evidence only; active carriers mount through this
contract, registry profiles, execution packet templates, active packets, and
role/context packages.

## Kernel trace (bounded)

4. Run status and carrier continuation through the carrier runtime:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier <carrier_id> --operator-message "<objective>" --json
   ```

   Then treat active packet validity, gates, spawn plan, and return-intake state as the gate before broad edits.

## Cycle order (mandatory)

5. **RELAY phase first** — Relay creates or validates the **WorkCycle packet** (intake, correlation, persona-visible briefing when mounted).
6. **STEWARD phase** — Steward makes the **route decision**.
7. **STEWARD defines `role_phase_sequence`** — ordered named ION role phases for this cycle.
8. **One carrier may traverse multiple role phases** — the same Cursor parent (or other declared carrier) may execute MASON, then NEMESIS, etc., in sequence **without** implying multiple identities at once; each phase is a **bounded mount** with its own WorkPacket / ContextPackage.
9. **Cursor subagents are optional** — Task slots are **carrier slots only**; they are not roles. Subagents are optional carrier slots, not roles; use only when the packet authorizes them.
10. **Each role phase receives:** WorkPacket / ContextPackage, active template, allowed paths, forbidden paths, validation, receipt requirement.
11. **Role outputs are proposals** until Steward integrates or rejects them.
12. **STEWARD integrates or rejects** proposals before closing authority on that batch.
13. **RELAY reports final state** after Steward closure for the batch (persona-visible path when Persona is mounted).

## Optional visible layer

14. **PERSONA** is an optional front layer when explicitly mounted; it does not replace RELAY or STEWARD law.

## Authority ceilings

15. **No production authority** on default mount.
16. **No live execution authority** on default mount.

## Context authority

17. **MINI/CAPSULE are not primary context authority** for carrier work; templates and bounded packets are.

## Cycle closure

18. Every cycle ends with **receipt / handoff / tests / next visible update** recorded per packet (signals, consolidation, or template-mandated paths).

## Subordination clause

All Cursor-facing docs and rules must defer operational sequencing to this contract.  
Do not invent parallel mount stories; extend here or patch narrowly with Steward review.
