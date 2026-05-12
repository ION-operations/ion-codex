# B04_CHATOPS_INLINE_ACTION_FALSE_POSITIVE_001

packet_id: B04_CHATOPS_INLINE_ACTION_FALSE_POSITIVE_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_B04_FALSE_POSITIVE_FIX_CANDIDATE
created: 2026-05-11
phase: extension_micro_shell_mode_visibility
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Prevent documentation and inline mentions of `ion_action:` from entering `ERROR_BLOCKED` mode while preserving detection of complete YAML action packets.

## Problem

The extension correctly detected and submitted real action packets, but ordinary documentation examples could still enter the scan path:

```text
Inline/documentation mention
-> candidateBlocks
-> parseIonActionYamlWithDiagnostics
-> missing/incomplete packet
-> YAML blocked locally / ERROR_BLOCKED
```

This created false operator alarm when browser GPTs discussed `ion_action:` as text.

## Implemented Behavior

Inline mention:

```text
"trigger another small `ion_action:` test"
```

Result:

```text
no action validation
no ERROR_BLOCKED mode
silent ignore as documentation text
```

Documentation snippet:

```text
ion_action:
  schema: ion.chatops.action.v1
  action_id: ...
  intent: ...
```

Result:

```text
no action validation
no ERROR_BLOCKED mode
silent ignore as incomplete documentation example
```

Concrete full action packet:

```text
ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-...
  intent: create_codex_work_packet
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
```

Result:

```text
DETECTED / approval flow preserved
```

## Implementation Notes

Added structural prefilter:

```text
isIonActionPacketCandidateText
```

The scan path now requires these concrete markers before parse/validation:

```text
schema: ion.chatops.action.v1
action_id: non-empty and not "..."
intent: non-empty and not "..."
actor marker or callsign/carrier marker
authority marker or human_sovereign/requires_approval/production_authority marker
```

The DOM registry annotation path uses the same prefilter, so documentation snippets do not get marked as blocked YAML badges.

## Additional Safety Fix

The smoke harness exposed a stale drop-target visibility edge. `visibleDropRect` now rejects non-body targets outside the viewport or smaller than an actionable target, so hidden calibrated drop targets are not treated as usable.

## Validation

```text
node --check ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
git diff --check scoped to changed extension/B04 files
unzip -t ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_inline_false_positive_20260511.zip
```

The smoke simulation now covers:

```text
inline ion_action mention ignored
documentation snippet ignored
assistant container action still detected
rendered code block action still detected
page fallback still splits multiple concrete action blocks
DOM registry still marks concrete YAML valid
safe mode still blocks candidate sends
```

## Touched Paths

```text
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_INLINE_ACTION_FALSE_POSITIVE_001.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_INLINE_ACTION_FALSE_POSITIVE_001_RECEIPT.json
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_inline_false_positive_20260511.zip
```

## Package Artifact

```text
zip_path: ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_inline_false_positive_20260511.zip
zip_sha256: b21f502f08764b8e1b952e4fa62e177ac8173e13e9cc822f398fa3e0db44a54f
zip_entries: 23
```

## Acceptance Boundary

Accepted:

```text
B04 false-positive fix candidate
inline/documentation mention filtering
concrete action YAML detection preserved
```

Not claimed:

```text
production authority
live execution authority
complete UI canon
silent browser send
```
