# B04_CHATOPS_MODE_VISIBILITY_001

packet_id: B04_CHATOPS_MODE_VISIBILITY_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_UI_BEHAVIOR_DISCOVERY
created: 2026-05-11
phase: extension_micro_shell_mode_visibility
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Make the extension's transient modes explicit, preserve the useful outline/capture behavior, and add mode memory so the operator can see what just happened after the UI returns toward normal monitoring.

## Source Discovery

Observed flow:

```text
Normal mode
-> action detected
-> approval/capture mode activates
-> operator approves
-> receipt/queue lands
-> UI returns toward normal mode
```

Current extension behavior already exposes mode-like statuses:

```text
Monitoring ChatGPT
ION action detected
Approval required
Approved, submitting
ION action submitted
Action rejected
YAML blocked locally
ION scan degraded
No action block found
```

## Implemented Outputs

- Added `ION_CHATOPS_MODE_MEMORY_V1` browser-local mode memory.
- Added explicit mode taxonomy classification in the bridge panel UI.
- Added a top-rail mode memory badge.
- Added full structured mode memory in the Status tab.
- Preserved existing outline/capture behavior.
- Added `queue_target` to action receipt summaries when bridge result data is available.
- Added `APPROVAL_MODAL` memory when approval dialogs open.

## Mode Taxonomy

```text
IDLE_MONITORING
DETECTED
APPROVAL_REQUIRED
APPROVAL_MODAL
SUBMITTING
RECEIPTED
ERROR_BLOCKED
INSPECTOR_CALIBRATION
```

## UI Behavior Table

| Mode | Top Rail | Status Tab | Persistence |
|---|---|---|---|
| `IDLE_MONITORING` | Neutral `MON` badge | Current monitoring text plus mode memory | Last non-idle mode remains |
| `DETECTED` | Blue `DET` badge | Action intent/id if parsed | Action id/intention preserved |
| `APPROVAL_REQUIRED` | Amber `APPR` badge | Approval status | Outcome preserved after modal |
| `APPROVAL_MODAL` | Amber `MODAL` badge | Modal detail | Operator review state recorded |
| `SUBMITTING` | Blue `SEND` badge | Submission status | Last action id retained |
| `RECEIPTED` | Green `RCPT` badge | Receipt and queue target | Last action queued display |
| `ERROR_BLOCKED` | Red `BLOCK` badge | Refusal/blocker detail | Last blocked status retained |
| `INSPECTOR_CALIBRATION` | Purple `CAL` badge | Calibration/capture status | Calibration state retained |

## Mode Transition Log

Mode memory shape:

```text
current_mode
last_mode
last_action
last_intent
last_receipt
last_queue_target
last_status
last_updated_at
```

Storage:

```text
browser localStorage key: ION_CHATOPS_MODE_MEMORY_V1
```

Proof posture:

```text
mode memory is UI witness only
receipt paths and queue/gateway responses remain proof
```

## Last-Action Receipt Display

Implemented display:

```text
top rail badge: RCPT / Last action queued
status tab: structured mode memory block
```

The badge opens the Status tab.

## Pin/Unpin Capture Overlay Option

Not yet implemented as a persistent control. Current behavior remains transient. This packet records the requirement:

```text
future option: explicit pin/unpin capture overlay toggle
mode label: INSPECTOR_CALIBRATION
default: unpinned transient overlays
authority: no silent page control, no send click
```

## Operator Explanation Labels

Current compact badge labels:

```text
MON, DET, APPR, MODAL, SEND, RCPT, BLOCK, CAL
```

Expanded Status tab labels preserve the full canonical mode names.

## Screenshot/Canon Note

The amber approval mode observed in ChatGPT is accepted as behavior discovery, not complete canon. A later visual canon pass should capture screenshots for:

```text
DETECTED
APPROVAL_REQUIRED
APPROVAL_MODAL
RECEIPTED
ERROR_BLOCKED
INSPECTOR_CALIBRATION
```

## Acceptance Boundary

Accepted:

```text
ACCEPTED_AS_UI_BEHAVIOR_DISCOVERY
implemented_candidate mode memory badge/status surface
```

Not accepted yet:

```text
complete UI canon
full mode manager
pinned capture overlay canon
production/live execution authority
```

## Touched Paths

```text
ION/02_architecture/ION_CHATOPS_MODE_VISIBILITY_PROTOCOL.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_MODE_VISIBILITY_001.md
ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
```
