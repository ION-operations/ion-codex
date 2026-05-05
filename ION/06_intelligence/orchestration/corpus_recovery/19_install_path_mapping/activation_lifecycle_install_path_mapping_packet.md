---
type: install_path_mapping_packet
authority: A1_CANONICAL
status: ACTIVE
created: 2026-04-14T12:15:00-04:00
---

# Activation/lifecycle install-path mapping packet

## Purpose

The activation/lifecycle joint promotion candidate is now mature enough to require a concrete install-path map.
This packet names where the candidate would land if later promoted into active architecture, what it would neighbor,
what it must not silently replace, and what staged order would keep promotion lawful.

This packet is **not** an installation.
It is a bounded path map for future thaw review.

## Scope

Covered:
- likely active-architecture target paths
- relation to current architecture surfaces
- non-replacement boundaries
- staged promotion sequence
- current remaining blockers after install-path clarification

Not covered:
- final ratification
- direct edits under `ION/02_architecture/`
- executor-specific implementation code changes
- reclassification of historical law as current law

## Candidate surfaces under consideration

Review-layer source set:
- `15_quarantined_active_law_review/drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- `15_quarantined_active_law_review/drafts/EXECUTOR_LIFECYCLE_PROTOCOL.review_draft.md`
- `15_quarantined_active_law_review/drafts/ACTIVATION_LIFECYCLE_INTERFACE.review_note.md`

## Proposed active landing paths

Primary candidate installs:
- `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md`

Supporting orientation / registry follow-ons after promotion:
- `ION/SYSTEM_MAP.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/README.md`
- `ION/STATUS.md`
- `ION/03_registry/...` surfaces only if canonical object names or lifecycle states are later ratified for registry use

## Active neighbors

The candidate would sit adjacent to, but not replace:
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md`
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `ION/02_architecture/MANUAL_AUTOMATION_EQUIVALENCE_PROTOCOL.md`
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

## Non-replacement law

Promotion must not silently imply any of the following false moves:
- scheduler law now decides enactment permission
- lifecycle law now replaces capability law
- continuation / takeover now become retroactive activation authority
- settlement now rewrites whether activation was lawful
- carrier shells now become authority-bearing simply because they can invoke execution

## Staged promotion order

1. Maintain review-layer drafts as the source of truth until thaw review closes.
2. Ratify the install-path map as a promotion prerequisite.
3. Promote `ACTIVATION_AUTHORITY_PROTOCOL.md` and `EXECUTOR_LIFECYCLE_PROTOCOL.md` together or not at all.
4. Update root maps and orchestration indexes in the same bounded packet.
5. Defer any registry/object formalization until active law text stabilizes under review.

## Remaining blockers after mapping

Install-path clarification reduces ambiguity, but the set is still not thaw-ready until:
- counterexample findings are reconciled against the landing paths
- carrier-crossing and receipt/settlement examples are explicitly judged install-compatible
- active-architecture adjacency language is reviewed against existing scheduler, continuation, and settlement law
- a bounded thaw-readiness reassessment is written

## Current judgment

The activation/lifecycle set now has:
- draft law
- seam review
- promotion-candidate framing
- counterexample pressure
- carrier-crossing examples
- receipt/settlement examples
- install-path mapping

That is enough to support a **bounded thaw-readiness reassessment packet**, but not enough to install active law yet.
