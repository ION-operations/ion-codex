---
type: proposal
authority: A3_OPERATIONAL
template: PROPOSAL
created: 2026-04-17T00:00:00-04:00
status: PROPOSED
topic: Canon foundry operating model, registry stack, and generated runtime-canon exports for ION
responding_to:
  - ION/06_intelligence/orchestration/corpus_recovery/00_program/atlas_work_gating_protocol.md
  - ION/06_intelligence/orchestration/corpus_recovery/11_grand_picture/era2_controlled_reintegration.md
  - ION/06_intelligence/orchestration/2026-04-17_reintegration_state_and_canonical_root_assessment.md
---

# Proposed Canon Foundry Operating Model and Registry Stack

## Purpose

This proposal defines how the reintegration program should operate mechanically.
Its central claim is simple: the project should not try to solve the estate with
one giant markdown summary or one flattened mega-folder. It should build a
foundry that preserves root identity, adjudicates authority explicitly, and
exports smaller generated canon surfaces to real carriers.

## Proposal

The canon foundry should be built as an embedded ION subsystem, not as a new
competing root. Its logical layers should be:

root manifests and source identity, evidence/lineage registries, adjudication
records, archive/tombstone records, and generated runtime-canon exports.

The key correction to many older consolidation instincts is this: the project
should mirror identity and adjudicate over it, not flatten difference away.

## Why not flatten

Flattening all files into one undifferentiated folder feels attractive because it
promises a single field the AI can "see." In practice it would damage exactly
the distinctions the project now most needs.

It would erase which root a file came from, blur the difference between active
and witness matter, make near-duplicates harder rather than easier to compare,
and encourage false authority because location would no longer encode lineage.

The estate does not need less difference. It needs difference rendered legible
and governable.

## Logical architecture

The foundry should operate through five logical layers.

The first layer is source identity. This is where roots, branch families, and
adjacent universes are named and classified before any promotion claim is made.

The second layer is evidence and lineage. This is where subsystem fingerprints,
competing candidates, lineage edges, loss/regression notes, and misread risks
are stored.

The third layer is adjudication. This is where the project records explicit
canonicalization decisions, promotion candidates, witness retentions, and
deferrals.

The fourth layer is archive witness disposition. This is where retired,
superseded, or witness-only artifacts are preserved with explicit reasons rather
than left as ambient stale residue.

The fifth layer is generated runtime canon. This is where smaller operational
surfaces are emitted for carriers such as Cursor, browser ChatGPT, Codex, or
future external workers.

## Recommended physical posture inside ION

The foundry should begin inside the existing stronger package rather than as a
new top-level rival root. In other words, use the current `corpus_recovery`
spine as the seed rather than inventing a new parallel universe.

The safest initial physical pattern is:

- keep authored recovery/foundry analysis under `06_intelligence/orchestration/corpus_recovery/`
- keep machine-readable registries in a future registry tier, likely under
  `03_registry/reintegration/` or another clearly named sub-registry
- keep generated carrier exports under a future export layer, likely under
  `05_context/exports/` or an equivalent explicitly-generated area
- keep archive-witness/tombstone records in a dedicated witness/disposition lane

The important point is not the exact folder name. The important point is that
the foundry must not masquerade as the active executable center until its own
outputs are explicitly promoted.

## Initial registry stack

The minimum registry stack should include the following.

`root_manifest.yaml` should say what major roots exist, what class each root
belongs to, what its rough status is, and where its evidence surfaces live.

`source_roots.yaml` should go a little deeper and describe root family, path,
local availability, extraction status, and whether the root is live, mirror,
archive, or external witness.

`lineage_registry.yaml` should capture which lines descend from or continue which
other lines, where the evidence is weak, and where sibling rather than parent
relations are more truthful.

`authority_registry.yaml` should capture which root or surface currently has the
best claim over a subsystem, and whether that claim is active, provisional,
historical, or merely evidentiary.

`module_registry.yaml` should capture high-value subsystems and where they live
across roots.

`subsystem_fingerprint_registry.yaml` should record the recognizable subsystem
clusters that recur across roots and therefore need competition handling.

`duplicate_competition_registry.yaml` should explicitly record competing files or
subsystem variants rather than making duplicate handling an implicit intuition.

`canonicalization_queue.yaml` should hold unresolved items that need a formal
decision.

`retired_artifacts_registry.yaml` should hold retired and superseded artifacts
with reasons.

`true_names_registry.yaml` should record semantic identity questions such as
Steward versus Codex versus carrier aliases and similar future identity repairs.

`route_map_registry.yaml` should record how generated exports and carrier
surfaces should be read.

## Minimum field grammar

The fields do not need to be baroque. A smaller disciplined grammar is better.

The most useful foundational fields appear to be:

- `id`
- `path`
- `root`
- `family`
- `kind`
- `status`
- `authority_class`
- `canonicality`
- `confidence`
- `supersedes`
- `superseded_by`
- `depends_on`
- `witnesses`
- `contradicts`
- `belongs_in`
- `notes`

If this small grammar is preserved, the foundry can answer the essential
questions without requiring a new ontology for every pass.

## Generated runtime-canon exports

The foundry’s purpose is not just to remember. It is to emit compact operational
truth.

That means it should generate different export surfaces for different carriers.

The browser/ChatGPT side should consume smaller bundles such as operator start,
current posture, authority map, open questions, placement queue, and maybe one
current bounded packet. The point there is not filesystem richness but bounded
clarity.

Cursor and Codex should consume a somewhat richer active surface: authority map,
lineage map, module registry, system map, glossary, and explicit ignore rules so
the carrier does not wander through witness mass by default.

Claude Code or other file-first carriers should similarly receive the smaller
generated canon plus explicit read order, not the entire estate as unmediated
startup truth.

## Relation to existing template law

The foundry should not create its own parallel template regime. It should build
on the current-phase template bridge already present in the stronger branch.

That is why the present suite only introduced two narrowly justified support
templates:

- `SYSTEM_LINEAGE_PROFILE`
- `CANONICALIZATION_DECISION`

General synthesis, proposal, and evidence work can continue to ride the existing
`RESEARCH`, `PROPOSAL`, and `EVIDENCE` templates.

In the future, the foundry may need narrower support templates such as
retirement tombstones, placement decisions, or export-bundle manifests. But
those should be added only when a real recurring need exists, not by speculative
catalog expansion.

## Tombstones and witness disposition

The archive side of the foundry must be explicit. The project has suffered
repeatedly from stale surfaces that remain visible but do not clearly say why
they are stale or what superseded them.

So archive witness handling should eventually produce explicit tombstone or
disposition records. Each such record should say:

- origin root
- prior path
- current status
- retirement reason
- superseded_by, if any
- retained evidentiary value

This matters because the correct contrast is not active versus deleted. The
correct contrast is active versus witness-retained versus retired-versus-
superseded.

## Human review points

The foundry should stay human-auditable at several points.

Root classification should remain reviewable because misclassifying a root as
primary, supporting, or wrapper changes later interpretation heavily.

Subsystem competition judgments should remain reviewable because many clusters
will look similar while preserving different strengths.

Generated runtime-canon exports should remain reviewable because the final
carrier bundle is where many subtle authority mistakes become startup truth.

## Risks / edge cases

The biggest risk is building too much registry before proving the first few
high-value adjudications. If that happens, the foundry becomes another document
growth engine rather than a control mechanism.

The second risk is confusing "generated canon" with "final canon." Generated
surfaces are operational conveniences over an adjudicated state; they are not
magically higher truth just because they are compact.

The third risk is letting the foundry silently own questions that still belong
to the live era board. The current selected lane is still Lane C runtime/session
review-entry. The foundry supports that lane and the broader root question, but
it does not silently replace the board.

## Open questions

The main open question is whether the initial foundry registries should live
only in orchestration space until the root-authority problem is resolved, or
whether a small sub-registry under `03_registry/` should begin immediately.

The second is what the first generated export bundle should target: browser
ChatGPT, Cursor/Codex, or a root-authority adjudication packet first.

The third is whether source-mirror copying is ever needed or whether manifest
references to the existing roots are sufficient for the current era. My present
judgment is that manifests should come first and copying should be delayed until
a concrete quarantine or promotion need demands it.
