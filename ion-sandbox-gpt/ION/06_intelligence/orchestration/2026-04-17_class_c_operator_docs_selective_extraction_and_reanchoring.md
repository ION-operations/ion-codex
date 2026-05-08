---
type: execution_note
authority: A3_OPERATIONAL
created: 2026-04-17T00:00:00-04:00
status: ACTIVE
purpose: Record the landed Class C selective extraction and re-anchoring packet for operator docs
connections:
  - ION/docs/README.md
  - ION/docs/PRODUCTION_RUNBOOK.md
  - ION/docs/O1_RATIFICATION_CHECKLIST.md
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/06_intelligence/orchestration/2026-04-17_branch_root_shell_vs_content_root_clarification.md
  - ION/06_intelligence/orchestration/2026-04-17_external_service_shell_vs_runtime_entry_clarification.md
  - /home/sev/ION - Production/ION/docs/README.md
  - /home/sev/ION - Production/ION/docs/PRODUCTION_RUNBOOK.md
  - /home/sev/ION - Production/ION/docs/O1_RATIFICATION_CHECKLIST.md
---

# Class C operator docs selective extraction and re-anchoring

## Purpose

This packet lands the low-risk Class C portion of q003:

- extract the highest-signal top-level production operator docs
- re-anchor them to the extracted branch shell-root/content-root reality
- avoid silently importing the broader production docs/program stack
- avoid smuggling in the optional external transport shell as if it were branch
  startup law

## Landed surfaces

The following docs now exist in the extracted branch:

- `ION/docs/README.md`
- `ION/docs/PRODUCTION_RUNBOOK.md`
- `ION/docs/O1_RATIFICATION_CHECKLIST.md`

## Re-anchoring decisions

### 1. Docs hub

The new `ION/docs/README.md` is not a clone of the retained production docs hub.
It explicitly names this lane as a selective extraction and points back to the
core startup law surfaces (`REPO_AUTHORITY`, `CANONICAL_WORKFLOW`,
`AGENT_CONTRACT`) instead of trying to become a replacement authority center.

### 2. Production runbook

The new runbook keeps only the parts that remain truthful for the extracted
branch:

- shell-root editable install
- branch-local `kernel` verification
- branch-local pytest posture

It deliberately does **not** claim that `ion-preflight`, `ion-api`, or the
`ion_*_mcp` shells are already active in this branch.

### 3. Ratification checklist

The new O1 checklist is a re-anchored witness map, not a replay of the older
production-root gate. It preserves the older O1/T31/T32 spine as evidence while
making clear that the extracted branch already has its own later ratification
record and acceptance evidence bundle.

## What was intentionally not imported

This packet does not import:

- `docs/program/`
- broader production-root program indexing
- transport-shell startup assumptions
- the top-level production external API/MCP service family

Those remain outside this low-risk Class C extraction.

## Execution judgment after this packet

The extracted branch now has:

- explicit shell-root/content-root law
- explicit external transport-shell versus internal runtime-entry law
- explicit re-anchored operator docs for install / verify / ratification witness use

That means split-center operator drift is reduced without widening into the
optional transport-shell packet.

## Next unresolved packet

The next unresolved q003-class question is no longer operator docs.

It is whether the retained top-level production external transport shell should:

- remain retained witness/support-only, or
- be opened as a later bounded promotion packet on its own terms

That decision should be made deliberately, not by drift.
