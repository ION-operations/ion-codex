# Context Graph Substrate Implementation Plan

**Status:** Build plan / not yet executed  
**Date:** 2026-04-24  
**Purpose:** Convert the restored context graph law into a staged implementation path.

## Phase 0 — Ratify restoration posture

- Confirm the root sentence: ION is a living context graph materialized as an evented, template-instantiated file system.
- Confirm V3 and V4 are proposal/restoration surfaces, not already-ratified law.
- Assign review: Steward routes, Vizier synthesizes, Vice pressures contradiction, Nemesis audits safety, Mason estimates implementation, Scribe documents.

## Phase 1 — Witness-only event detection

Implement file scanning and classification without source graph mutation.

Deliverables:

- `TemplateCompletionEvent` model
- watch registry loader
- template classifier
- dry-run completion evaluator
- event witness writer
- refusal writer
- evented file projection index

Non-negotiable tests:

- unknown template does not emit actionable event;
- incomplete file emits blocked/refusal witness;
- valid known file emits one stable event id;
- unchanged re-scan is idempotent;
- witness event does not mutate source graph.

## Phase 2 — Reaction registry and bounded reaction selection

Implement reaction registry loading and allowed-reaction selection.

Deliverables:

- graph reaction registry loader;
- reaction selector;
- forbidden-effect checker;
- authority posture checker;
- reaction proposal receipt.

Non-negotiable tests:

- unregistered effect is refused;
- forbidden effect is refused;
- allowed reaction produces proposal only;
- reaction idempotence key is stable.

## Phase 3 — Projection writeback only

Allow index/projection updates, but not source graph mutation.

Deliverables:

- evented file index update;
- stale/incomplete projection marker;
- membrane projection hook candidate;
- index update receipts.

Non-negotiable tests:

- projection update cites event and receipt;
- projection does not claim source authority;
- stale markers are reversible by later valid event.

## Phase 4 — Source graph mutation proposal

Allow source graph mutation proposals, still subject to governed write / landing.

Deliverables:

- graph node create proposal;
- graph edge update proposal;
- graph writeback receipt;
- conflict/contradiction marker;
- registry delta proposal pathway.

Non-negotiable tests:

- graph mutation cannot occur without event + allowed reaction + receipt;
- contradiction cannot be deleted by edge update;
- registry mutation remains proposal until verdict.

## Phase 5 — Subagent fan-out binding

Bind event reactions to agent families and sub-specialist graph regions.

Deliverables:

- agent graph jurisdiction loader;
- fan-out request generator;
- fan-in settlement template binding;
- manager/subagent context package assembly.

Non-negotiable tests:

- event can request specialist but not silently activate arbitrary role;
- manager receives bounded settlement;
- subagent output writes back through receipt.

## Phase 6 — Full evented graph loop

A completed template file can lawfully produce graph reactions, schedule work, request specialists, update projections, and emit receipts without losing authority boundaries.

Exit condition:

ION can prove, by tests and receipts, that a template-completed file becomes an actionable event surface while incomplete/unknown/unauthorized files remain safe and visible.
