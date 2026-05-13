# ION Work Packet — Guarded Macro Automation MVP

## Status

`PROPOSED_WORK_PACKET`

## Objective

Implement the first safe layer of browser DOM macro automation for ChatGPT composer controls.

The goal is not full autonomy. The goal is visible, approval-gated, logged DOM assistance.

## Automation Law

```text
visible target
-> preview
-> explicit approval
-> stale-target check
-> execute
-> log
-> receipt if ION state is touched
```

## Scope

Implement safe macros first:

```text
focus composer
insert approved text into composer
copy latest assistant response
copy selected code block
scroll to message number
open extension panel/tab
highlight attach/send/mic controls
```

Implement approval-required macros only as previewable actions:

```text
click send
open attach file picker
submit valid YAML action
enqueue Codex work
submit sandbox return
```

Do not implement silent send/upload.

## DOM Target Model

Each macro target should carry:

```text
target_id
target_kind
selector/heuristic source
bounding box
visible state
enabled/disabled state
last_seen_at
stale_after_ms
risk_level
```

Before execution, re-check:

```text
target still exists
target visible
target not disabled
target bounds sufficiently unchanged
active tab/window still expected
user approval matches target
```

## Risk Levels

### Safe

```text
focus input
insert text
copy text
scroll
open/close ION panel
```

### Approval Required

```text
click send
click attach
submit YAML
queue Codex
submit artifact
```

### Forbidden In MVP

```text
silent send
silent file upload
silent daemon mutation
apply patch
git commit/push
delete/archive state
```

## UI

Automation tab should show:

```text
detected controls
available macros
risk level
preview
last run
last failure
approval required badge
```

Composer controls may receive colored halos, but halos indicate availability only, not permission.

## Acceptance Criteria

```text
safe macros work without console errors
approval-required macros show preview before execution
send click is never silent
attach click is never silent
stale target detection blocks execution
Automation tab logs success/failure
Diagnostics tab shows target registry
existing extension behavior remains intact
```

## Validation

```text
focus composer
insert approved test text
copy a code block
scroll to numbered message
try stale target scenario by rerendering page before approval
confirm execution is blocked
confirm send requires explicit approval
```

## Authority Boundary

Allowed:

```text
DOM assistance
approved local UI action
logs
```

Forbidden:

```text
unapproved send
unapproved upload
unapproved daemon mutation
background autonomous browser operation
production/deployment authority
