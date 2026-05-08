---
type: canonicalization_decision
template: CANONICALIZATION_DECISION
created: 2026-04-17T00:00:00-04:00
status: WORKING
scope: root_authority_carrier_export_bundle
decision_class: export_bundle
connections:
  - ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_packaged_root_nested_path_disambiguation_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_retained_dual_center_settlement_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_external_transport_shell_current_phase_disposition_decision.md
  - ION/03_registry/reintegration/canonicalization_queue.yaml
  - ION/03_registry/reintegration/root_manifest.yaml
  - ION/03_registry/reintegration/authority_registry.yaml
  - ION/03_registry/reintegration/duplicate_competition_registry.yaml
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BUNDLE_MANIFEST.yaml
  - ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CURSOR_CODEX_READ_MODE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_READ_MODE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_READ_MODE.md
  - ION/06_intelligence/orchestration/2026-04-17_root_authority_bundle_modeled_carrier_read_test.md
  - ION/06_intelligence/orchestration/2026-04-17_root_authority_bundle_current_carrier_exercise_receipt.md
  - ION/06_intelligence/orchestration/2026-04-17_root_authority_bundle_external_carrier_exercise_briefs.md
  - ION/06_intelligence/orchestration/2026-04-17_post_reintegration_canonicalization_state_forward_path_and_codex_handoff.md
  - ION/04_packages/kernel/root_authority_bundle.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_root_authority_bundle.py
  - ION/tests/test_root_authority_bundle_cli.py
  - ION/05_context/history/kernel_store/root_authority_bundle_exercise_receipts/root-authority-bundle-exercise-cursor-codex-2026-04-17t18-03-49-04-00.json
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_EXERCISE_BRIEF.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_EXERCISE_BRIEF.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_RETURN_STUB.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_RETURN_STUB.md
  - ION/REPO_AUTHORITY.md
  - /home/sev/ION - Production/_opus_composer_bridge/50_opus_assessments/001_reintegration_assessment_after_codex_q001.md
---

# Canonicalization Decision: Root-Authority Carrier Export Bundle

## Purpose

Close q004 far enough that fresh carriers stop landing on two real roots plus
one misleading nested path without adjudication.

This packet does not decide final single-root settlement. It emits the first
carrier-facing startup bundle for the current split-center period.

## Scope

In scope:

1. one shared root-authority startup surface
2. explicit per-carrier read modes for Cursor/Codex, browser ChatGPT, and
   Claude Code
3. explicit supersession of raw STATUS-first onboarding during the current
   reintegration phase

Out of scope:

- final single-root ratification
- production-surface code promotion
- broader canon-foundry exports beyond root authority

## Evidence considered

Primary decision inputs:

- `ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md`
- `ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md`
- `ION/06_intelligence/decisions/2026-04-17_packaged_root_nested_path_disambiguation_canonicalization_decision.md`
- `ION/03_registry/reintegration/canonicalization_queue.yaml`
- `ION/03_registry/reintegration/root_manifest.yaml`
- `ION/03_registry/reintegration/authority_registry.yaml`

Carrier/read-mode guidance:

- `ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/04_canon_foundry_operating_model_and_registry_stack.md`
- `/home/sev/ION - Production/_opus_composer_bridge/50_opus_assessments/001_reintegration_assessment_after_codex_q001.md`

## Decision

### 1. Emit a generated carrier-facing root-authority bundle now

The current split-center period now has one explicit generated startup bundle at:

`ION/05_context/exports/2026-04-17_root_authority_bundle/`

This bundle is the correct first onboarding surface for carriers entering the
workspace-level reintegration question.

### 2. Shared startup rule

For fresh carrier onboarding to the split-center question, use:

- `ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md`

before either `STATUS.md` surface.

This is a **startup supersession rule**, not a claim that the STATUS files are
useless. They remain projection surfaces, but they are no longer the cleanest
first answer to workspace root authority.

### 3. Bundle truth model

The bundle must keep the current root truth explicit:

- packaged current-generation root = provisional primary reintegration center
- top-level production root = retained live extraction center
- embedded residue lane = internal packaged witness lane, not a root

The bundle must not compress those three objects into one ambiguous `ION/`.

### 4. Per-carrier read modes

The bundle now defines three carrier-specific read modes:

- Cursor/Codex = rich filesystem mode with direct registry and decision access
- browser ChatGPT = compressed bundle-first mode with narrow anchor expansion
- Claude Code = file-first but bounded mode with the bundle as the mandatory
  entry surface

These are working read modes, not final canon policy forever.

### 5. STATUS handling rule

During the current split-center period:

- do not use packaged `STATUS.md` or top-level production `STATUS.md` as the
  first onboarding surface for carrier startup
- use the bundle first
- read STATUS only after the bundle has named the active root partition

### 6. Why this packet is enough for now

The goal of q004 is not to solve the workspace permanently. It is to stop
carrier drift while the workspace remains in retained dual-center settlement.

This packet is therefore successful if:

- a fresh carrier can name the three relevant path classes correctly
- a fresh carrier knows which root to start from
- a fresh carrier knows when to consult the top-level production root
- and a fresh carrier does not infer a second runnable root from `ION/ION/`

## Export contents

The emitted bundle contains:

- `BUNDLE_MANIFEST.yaml`
- `START_HERE.md`
- `CURSOR_CODEX_READ_MODE.md`
- `BROWSER_CHATGPT_READ_MODE.md`
- `CLAUDE_CODE_READ_MODE.md`

The emitted bundle now also carries support surfaces for the next external
parity packet:

- `BROWSER_CHATGPT_EXTERNAL_EXERCISE_BRIEF.md`
- `CLAUDE_CODE_EXTERNAL_EXERCISE_BRIEF.md`
- `BROWSER_CHATGPT_EXTERNAL_RETURN_STUB.md`
- `CLAUDE_CODE_EXTERNAL_RETURN_STUB.md`

## Confidence and unresolved contradictions

Confidence: **high** that a carrier-facing export bundle is now the correct
stable startup surface after q001, q003, q005, and q006, and that the current
bundle is materially hardened by static tests, an operator CLI surface, and one
durable current-carrier exercise receipt.

Confidence: **high** that raw STATUS-first onboarding is inferior to the bundle
during the current split-center period.

Confidence: **medium** that these three read modes are the final right
partition; later carriers may justify more nuance.

Confidence: **high** that external parity should not be claimed through the
durable receipt path until one real external exercise lands, and that refusing
non-current-carrier receipts while emitting explicit external exercise briefs
and `EXTERNAL_RETURN` stubs, then ingesting completed external returns only as
carrier-specific witness receipts with archived packet copies, is the correct
current hardening move.

Confidence: **high** that the root-authority bundle should not freeze
host-specific roots. The emitted root terms are now portable and the bundle
validates from a relocated extract rather than only from the originating host
path.

Unresolved contradictions that must remain visible:

- q003 maps production surfaces but does not yet promote them
- the bundle is generated onboarding truth, not final single-root canon
- the bundle is now proven for the current branch-local editable-install
  carrier posture, but not yet for live external carriers beyond that path

## Required follow-up

1. Mark q004 as current-carrier exercised with receipt in the queue.
2. Treat the bundle as the current stable startup surface for the retained
   dual-center settlement.
3. Use the emitted browser/Claude exercise briefs and external return stubs for
   the next external-carrier packet, then ingest any completed return through
   `bundle record-external-return` rather than stamping unsupported durable
   parity receipts.
4. Reopen bundle work only if live external-carrier exercise exposes a gap not
   covered by the current modeled/read-tested/current-carrier proof stack.
