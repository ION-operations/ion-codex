---
type: execution_note
authority: A3_OPERATIONAL
created: 2026-04-17T00:00:00-04:00
status: ACTIVE
purpose: Record the modeled carrier read-test for the root-authority bundle and the small corrections required to make q004 a stable startup export for the current retained dual-center settlement
connections:
  - ION/06_intelligence/decisions/2026-04-17_root_authority_carrier_export_bundle_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_retained_dual_center_settlement_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_external_transport_shell_current_phase_disposition_decision.md
  - ION/06_intelligence/orchestration/2026-04-17_post_reintegration_canonicalization_state_forward_path_and_codex_handoff.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CURSOR_CODEX_READ_MODE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_READ_MODE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_READ_MODE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BUNDLE_MANIFEST.yaml
  - ION/03_registry/reintegration/canonicalization_queue.yaml
---

# Root-authority bundle modeled carrier read-test

## Purpose

q004 emitted the root-authority bundle and named read-testing across the
carrier modes as the next required follow-up.

This note records that modeled read-test and the bounded corrections required
to make the bundle stable for the current retained dual-center settlement.

## Method

Three modeled carrier passes were executed against the bundle:

1. Cursor / Codex rich-filesystem mode
2. browser ChatGPT compressed anchor-first mode
3. Claude Code file-first bounded mode

The read-test checked two things:

- whether the bundle and carrier read orders point to real anchor files
- whether a fresh carrier following those read orders can recover the current
  settled posture without silently falling back to older root projections

## Findings

### 1. Anchor existence passed

All bundle-local and branch-local anchor paths referenced in:

- `START_HERE.md`
- `CURSOR_CODEX_READ_MODE.md`
- `BROWSER_CHATGPT_READ_MODE.md`
- `CLAUDE_CODE_READ_MODE.md`
- `BUNDLE_MANIFEST.yaml`

resolved successfully during the read-test.

### 2. The startup bundle itself already carried the right top-level answer

`START_HERE.md` already stated the current truthful posture correctly:

- packaged current-generation shell root
- packaged current-generation content root
- top-level production retained secondary root
- embedded residue lane
- single-root ratification not authorized

So the shared startup surface was already materially correct.

### 3. The carrier-specific deepening paths needed one correction

The read modes were slightly too narrow after later packets landed.

They did not all carry the same deeper anchors for:

- q005 retained dual-center settlement
- the post-reintegration forward-path reset

That meant a fresh carrier could recover center from `START_HERE.md`, but not
always expand into the same later evidence chain without extra local judgment.

## Corrections landed

The following bounded corrections now land with this note:

- q005 settlement anchor added to carrier read paths where needed
- post-reintegration handoff added as the current forward-path anchor
- current-phase external transport-shell disposition added to the shared bundle
  anchors
- bundle manifest updated to reflect read-tested stable startup-export status
- q004 queue/control surfaces updated to reflect read-tested stability rather
  than merely emitted status

## Result

q004 should now be treated as:

- stable startup export for the current retained dual-center settlement
- read-tested across the named modeled carrier modes
- still not equivalent to live external service execution proof

That last distinction matters. This packet proves startup recovery and anchor
coherence, not end-to-end execution inside external carrier runtimes.

## What remains out of scope

This read-test does not prove:

- real browser-chat or Claude-host runtime execution
- future single-root canon
- promotion of the retained top-level production external transport shell

Those remain separate bounded questions.
