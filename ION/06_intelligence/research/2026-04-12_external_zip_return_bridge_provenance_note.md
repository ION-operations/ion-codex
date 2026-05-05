---
type: research
from: Codex
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
topic: Provenance note for the current-phase external zip return bridge
connections:
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
  - ION/07_templates/actions/EXTERNAL_RETURN.md
  - ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md
  - ION/07_templates/actions/PATCH_PACKAGE.md
  - ION/tests/test_kernel_external_api_parity_scenario.py
  - /home/sev/ION - Production/AIM-ION/ide_orchestration/research/EXTERNAL_SYSTEMS_ANALYSIS_CHATGPT.md
---

# External Zip Return Bridge Provenance Note

## Why this exists

The live branch already had a generic external execution bridge, but it did not yet have
one explicit current-phase packet family for browser or VM zip returns.

## Historical and live sources searched

- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/04_packages/kernel/external_execution_bridge.py`
- `ION/07_templates/actions/PATCH_PACKAGE.md`
- `ION/07_templates/actions/HANDOFF.md`
- `ION/07_templates/actions/SIGNAL.md`
- `ION/tests/test_kernel_external_execution_bridge.py`
- `ION/tests/test_kernel_external_api_parity_scenario.py`
- `/home/sev/ION - Production/AIM-ION/ide_orchestration/research/EXTERNAL_SYSTEMS_ANALYSIS_CHATGPT.md`

## What was found

- The current root already defines truthful external boundary law.
- The current root already proves external export plus governed accept-return through the
  operator CLI scenario.
- The current template floor already has `PATCH_PACKAGE`, `HANDOFF`, and `SIGNAL`.
- The broader estate preserves ChatGPT browser as an external system with its own
  orchestration and context persistence characteristics.
- No exact active `EXTERNAL_RETURN` packet existed in the current root.

## What is reused directly

- external boundary law from `EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- live proof center from `test_kernel_external_api_parity_scenario.py`
- patch-return semantics from `PATCH_PACKAGE.md`

## What is restated for current phase

- the browser or VM zip-return carrier as a bounded packet family
- the rule that returned snapshots remain witness until compared and landed
- the explicit current-phase requirement for one `EXTERNAL_RETURN` packet at re-entry

## Why this remains provisional

- the branch still needs a real browser zip drill under this exact packet family
- the bridge is narrower than the generic external bridge and should remain current-phase
  until proved

## Non-claims

- This note does not claim browser ChatGPT is a mounted internal role.
- This note does not authorize whole-zip replacement of the live branch.
- This note does not replace the generic external bridge law.
