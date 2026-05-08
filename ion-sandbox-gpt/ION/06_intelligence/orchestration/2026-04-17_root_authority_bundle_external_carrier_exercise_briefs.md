---
type: orchestration_verification
authority: A3_OPERATIONAL
created: 2026-04-17T22:24:58-04:00
status: ACTIVE
purpose: Record the q004 hardening packet that emits lawful browser and Claude external exercise briefs, materializes fillable external return stubs, and ingests completed external returns while refusing false external receipts
connections:
  - ION/06_intelligence/decisions/2026-04-17_root_authority_carrier_export_bundle_canonicalization_decision.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_EXERCISE_BRIEF.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_EXERCISE_BRIEF.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_RETURN_STUB.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_RETURN_STUB.md
  - ION/04_packages/kernel/root_authority_bundle.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_root_authority_bundle.py
  - ION/tests/test_root_authority_bundle_cli.py
---

# Root-authority bundle external carrier exercise briefs

## Purpose

Close one truthfulness gap in q004.

After the current-carrier receipt landed, the operator surface could still have
been used to stamp a browser or Claude carrier key without any actual external
proof. That would have turned q004 into a parity theater surface.

This packet hardens the bundle in four ways:

- durable bundle exercise receipts are now limited to the proven
  `cursor_codex` current-carrier posture
- browser and Claude now receive explicit external exercise briefs instead of
  fake receipts
- browser and Claude now also receive fillable `EXTERNAL_RETURN` stubs bound to
  those briefs so the return path uses an already-ratified branch template
- completed browser and Claude returns can now be ingested as durable
  q004-scoped external-return receipts without claiming external parity beyond
  the cited carrier, and each ingested return is archived as an immutable
  witness copy in kernel
  history
- the bundle no longer freezes host-absolute root terms and now validates from
  a relocated extract

## Landed surfaces

- `ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_EXERCISE_BRIEF.md`
- `ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_EXERCISE_BRIEF.md`
- `ION/05_context/exports/2026-04-17_root_authority_bundle/BROWSER_CHATGPT_EXTERNAL_RETURN_STUB.md`
- `ION/05_context/exports/2026-04-17_root_authority_bundle/CLAUDE_CODE_EXTERNAL_RETURN_STUB.md`

The operator CLI now supports:

- `python -m kernel bundle --workspace-root .. --format json materialize-external-exercise-brief --carrier-key browser_chatgpt`
- `python -m kernel bundle --workspace-root .. --format json materialize-external-exercise-brief --carrier-key claude_code`
- `python -m kernel bundle --workspace-root .. --format json materialize-external-return-stub --carrier-key browser_chatgpt`
- `python -m kernel bundle --workspace-root .. --format json materialize-external-return-stub --carrier-key claude_code`
- `python -m kernel bundle --workspace-root .. --format json record-external-return --carrier-key browser_chatgpt --input <completed_external_return_packet>`
- `python -m kernel bundle --workspace-root .. --format json record-external-return --carrier-key claude_code --input <completed_external_return_packet>`

## What the briefs do

Each brief binds the external carrier to:

- `START_HERE.md`
- the carrier-specific read-mode file
- the retained dual-center settlement anchors
- the current forward-path handoff
- an explicit return contract naming the four path classes that must be
  distinguished correctly

Each return stub then binds the external carrier to the branch’s existing
`EXTERNAL_RETURN` template and pre-wires:

- the governing brief packet
- the live q004 decision
- the orchestration note for the external exercise packet
- the reintegration queue as one explicit landing target

Each completed return can now be ingested into the kernel store as:

- one durable `root_authority_bundle_external_return_receipt`
- one archived packet copy under `root_authority_bundle_external_return_packets/`

## What they do not do

These briefs, stubs, and receipt-ingestion surfaces do not prove external parity.

They only prepare the next lawful packet so browser or Claude execution can be
performed without informal oral tradition and without ambiguous success
criteria.
