# ION ChatOps Mode Visibility Protocol

protocol_id: ION_CHATOPS_MODE_VISIBILITY_PROTOCOL
status: candidate_doctrine
accepted_state: ACCEPTED_AS_UI_BEHAVIOR_DISCOVERY
created: 2026-05-11
production_authority: false
live_execution_authority: false
secrets_authority: false

## Purpose

ION ChatOps browser-carrier UI has transient operational modes. Some surfaces should appear only during high-signal states, but the operator must always be able to tell which mode is active, why it activated, and what happened when it ended.

This protocol formalizes the observed behavior without promoting it to complete UI canon or a full mode manager.

## Mode Taxonomy

| Mode | Meaning | Operator Signal |
|---|---|---|
| `IDLE_MONITORING` | Extension is watching ChatGPT for `ion_action` blocks. | Minimal rail, neutral mode badge. |
| `DETECTED` | Candidate YAML/action block was found and local validation is beginning. | Working tone, action detail available. |
| `APPROVAL_REQUIRED` | Action or bounded bridge operation requires operator approval. | Amber/orange tone, approval controls prominent. |
| `APPROVAL_MODAL` | Operator review modal is open. | Modal shows action id, intent, risk, target, receipts. |
| `SUBMITTING` | Approved packet is being submitted to the local bridge/gateway. | Working tone, send/submission state visible. |
| `RECEIPTED` | Receipt or queued result returned. | Green/success tone, last-action memory preserved. |
| `ERROR_BLOCKED` | Parse, validation, refusal, gateway, or bridge failure occurred. | Red/error tone with refusal or blocker detail. |
| `INSPECTOR_CALIBRATION` | Manual DOM/capture/anchor calibration mode is active. | Calibration tone and overlay/capture controls visible. |

## UI Behavior Table

| State | Should Appear | Should Persist After Return |
|---|---|---|
| Idle | Minimal rail, queue/context rails | Last mode badge and status tab memory |
| Detected | Captured block outline, action summary | Last detected action id if available |
| Approval | Amber rail/modal, approval details | Approval outcome |
| Submitting | Working indicator | Submission status |
| Receipted | Green success, receipt path, queue target | Last action, receipt, queue target |
| Blocked | Red error detail | Last blocked action/status |
| Inspector | Outlines, anchor/capture previews | Calibration status, not permanent authority |

## Mode Transition Log Contract

The extension SHOULD keep a compact mode memory:

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

The mode memory is a UI witness only. It is not accepted state by itself; receipt paths, queue paths, and local daemon/gateway responses remain the proof surfaces.

## Last-Action Display

The operator-facing rail SHOULD show a small persistent mode badge. When an action receipts or queues successfully, the badge SHOULD read in plain language such as:

```text
Last action queued
```

The Status tab SHOULD expose the full structured memory block.

## Pin/Unpin Capture Overlay Option

Capture, DOM, attach, drop-zone, and tab-anchor outlines are high-signal and should stay transient by default. A future pinned overlay option may allow the operator to keep them visible during calibration, but it must be explicit, reversible, and labeled as `INSPECTOR_CALIBRATION`.

No pinned overlay is canon until implemented with visible operator control and receipt.

## Operator Explanation Labels

Labels should describe the mode, not hidden implementation:

```text
Monitoring
Detected
Approval
Review
Submitting
Receipted
Blocked
Calibration
```

Avoid implying production authority, live execution authority, secrets authority, or silent browser send.

## Amber Approval Canon Note

The observed amber/orange approval state is accepted as behavior discovery:

```text
Normal mode -> action detected -> approval/capture mode -> operator approves -> receipt/queue lands -> UI returns toward normal monitoring.
```

This is not yet accepted as complete UI canon or a fully implemented mode manager.
