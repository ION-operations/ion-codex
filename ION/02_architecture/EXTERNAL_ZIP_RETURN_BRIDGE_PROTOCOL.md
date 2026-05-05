---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/07_templates/actions/PATCH_PACKAGE.md
  - ION/07_templates/actions/HANDOFF.md
  - ION/07_templates/actions/SIGNAL.md
  - ION/07_templates/actions/EXTERNAL_RETURN.md
  - ION/06_intelligence/research/2026-04-12_external_zip_return_bridge_provenance_note.md
---

# External Zip Return Bridge Protocol

## Purpose

Define the minimum current-phase law for browser or VM carriers that receive a bounded
workspace snapshot, work outside the live branch, and return bounded artifacts for
comparison and landing.

This bridge is a current-phase carrier over the already-landed generic external
execution bridge. It does not replace that bridge.

## Core law

1. The external snapshot is witness, not kernel truth.
2. Returned files or zips do not become live-branch truth directly.
3. The external carrier must receive one governing packet, explicit allowed targets, and
   a bound template set.
4. Returned work must re-enter the live branch as bounded artifacts.
5. The live branch owner performs comparison, validation, and landing.
6. No silent full-zip import or hidden merge is allowed.

## Required inputs to the external carrier

- one governing `TASK`, `ROLE_SESSION`, or `HANDOFF`
- one identified workspace snapshot or zip
- explicit allowed write targets
- bound template set
- exact expected output family

## Required returned artifact set

At minimum, the external carrier should return:

- one `EXTERNAL_RETURN` packet

and, when code or text changes are proposed:

- one `PATCH_PACKAGE`

plus, when needed:

- one `HANDOFF`
- one `SIGNAL`

## Landing law

Returned work should be processed in this order:

1. inspect the `EXTERNAL_RETURN` packet
2. inspect any `PATCH_PACKAGE` or companion artifacts
3. compare returned targets against live branch state
4. validate and land through the ordinary live branch owner

## Relationship to the generic external bridge

`EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md` remains the stronger generic law for
external execution boundaries.

This bridge only restates the browser or VM zip-carrier case that the generic bridge did
not standardize as a packet family in the live template stack.

## Current-phase default

browser ChatGPT remains external and unmounted by default even when this bridge is used.
The bridge standardizes return flow; it does not silently settle role mount.

## Non-goals

- no automatic sync daemon yet
- no direct governed-write application from an external zip
- no claim that an entire returned snapshot should replace the live branch wholesale
