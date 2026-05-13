# ION Work Packet — ChatGPT DOM Cockpit Shell

## Status

`PROPOSED_WORK_PACKET`

## Objective

Implement the first bounded slice of the ChatGPT DOM cockpit evolution for the ION browser extension.

The extension should move from a floating top panel toward a native-feeling ChatGPT composer cockpit:

```text
Status | Action | Agent | Packages | Sandbox | Automation | Artifacts | Diagnostics | Logs
```

The tabs should visually attach to the lower ChatGPT composer pill and open panels upward from that composer area.

## Scope

Implement:

```text
composer anchor discovery
composer-relative tab rail
upward expanding panel
tab open / close / switch behavior
top one-line status rail
anchor health diagnostics
resize / rerender tracking
fail-closed fallback
```

Do not implement macro execution in this packet.

Do not implement file upload automation in this packet.

Do not apply repo-wide architectural rewrites.

## Existing Surfaces

Expected current extension surfaces:

```text
ION/09_integrations/browser_extension/ion_chatops_bridge/
  src/content.ts
  src/approval_ui.ts
  src/background.ts
  src/schema.ts
  dist/content.js
  dist/background.js
  manifest.json
```

## Design Requirements

### Composer anchoring

Detect the ChatGPT composer/input pill by robust heuristics, not brittle single class names.

Prefer a strategy such as:

```text
find textarea/contenteditable composer
walk to rounded composer container
confirm visible bounds
confirm contains send / attach / mic controls when available
track via ResizeObserver and MutationObserver
```

### Cockpit rail

Render an ION-owned overlay container positioned relative to the composer bounds.

Tabs:

```text
Status
Action
Agent
Packages
Sandbox
Automation
Artifacts
Diagnostics
Logs
```

Behavior:

```text
click closed tab -> open panel
click active tab -> close panel
click different tab -> switch panel
escape -> close panel
lost anchor -> hide / degraded mode
```

### Panel

Panel expands upward from composer area.

Panel should adapt to:

```text
composer grows with long text
dictation/voice mode expands composer
file chips change composer height
window resize
visual viewport shifts
ChatGPT rerenders
```

### Top status rail

Replace or minimize the old floating panel into a subtle top status rail:

```text
green/yellow/red dot
ION ChatOps
short status text
latest warning/error
```

The full details move to lower cockpit tabs.

## Acceptance Criteria

```text
extension reloads without console errors
composer cockpit appears visually attached to ChatGPT composer pill
tabs open upward panels and close/switch correctly
panel tracks composer resizing and page rerenders
top status rail renders as one-line status surface
existing YAML scan and approval modal behavior still works
Diagnostics tab reports anchor health and failure state
no automatic clicks or file uploads are introduced
```

## Validation

Run or perform:

```text
extension build / compile if available
manual Chrome extension reload
open ChatGPT chat
confirm cockpit rail
type long input
toggle dictation/voice if available
attach/detach file chips if available
resize window
check console for errors
verify existing YAML detection still works
```

## Authority Boundary

This packet may change browser extension UI code.

It may not:

```text
send chat messages automatically
upload files automatically
invoke Codex automatically
mutate ION state without existing approval path
depend on secrets
change Git/GitHub behavior
```
