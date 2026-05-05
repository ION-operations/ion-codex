# ION Work Packet — DOM Action Registry And YAML Annotation

## Status

`PROPOSED_WORK_PACKET`

## Objective

Add a DOM action registry that detects ChatGPT composer controls, messages, code blocks, and valid ION YAML blocks, then annotates them with ION-aware affordances.

This packet creates visibility and addressability. It does not execute high-risk actions.

## Scope

Implement:

```text
composer control detection
message numbering
code block numbering
YAML block validation markers
duplicate YAML/action detection support
automation-availability halos
copy-to-extension action hooks
diagnostics for detected DOM elements
```

## Composer Controls To Detect

Detect and track these when available:

```text
composer input
send button
attach/add file button
microphone / dictate button
thinking/model controls
voice mode controls
file chips
```

Add non-invasive visual affordance halos indicating automation availability.

Halos must not imply execution authority.

## Message And Code Annotation

For visible conversation messages:

```text
assign stable-ish visible sequence number
show small ION badge/number
track assistant/user role if detectable
```

For code blocks:

```text
assign code block sequence number
detect language if available
detect YAML
validate possible ion_action YAML
show valid/invalid marker
show duplicate-risk marker if same YAML appears multiple times
add copy-to-extension affordance
```

## YAML Protocol Behavior

Detect YAML blocks that appear to be ION actions.

For valid blocks:

```text
mark block as ION-valid
assign sequence number
show action type
show approval-needed status
offer queue/preview action using existing approval path
```

For invalid blocks:

```text
mark as invalid
show reason in Diagnostics or tooltip
do not submit
```

For duplicates:

```text
show duplicate warning
prevent accidental duplicate ingestion unless explicitly approved
```

## Acceptance Criteria

```text
messages receive visible ION sequence labels
code blocks receive visible ION sequence labels
valid ION YAML blocks are marked
invalid YAML blocks are not submitted
duplicate YAML blocks are detected or flagged
composer controls receive visual automation-availability halos
Diagnostics tab lists detected controls/messages/code/YAML counts
no send/upload/daemon mutation occurs without existing approval path
```

## Validation

Manual validation:

```text
open chat with multiple user/assistant messages
create multiple code blocks
create valid ion_action YAML block
create invalid YAML block
copy/repeat a YAML block
confirm numbering and duplicate warnings
confirm existing copy button remains usable
check console for errors
```

## Authority Boundary

Allowed:

```text
read and annotate DOM
copy text into extension preview
send valid YAML to existing approval modal only after user action
```

Forbidden:

```text
silent submission
silent send click
silent file upload
silent daemon mutation
patch application
Git push
```
