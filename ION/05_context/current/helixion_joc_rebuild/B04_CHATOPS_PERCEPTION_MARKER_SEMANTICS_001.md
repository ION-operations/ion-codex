# B04_CHATOPS_PERCEPTION_MARKER_SEMANTICS_001

packet_id: B04_CHATOPS_PERCEPTION_MARKER_SEMANTICS_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_B04_PERCEPTION_MARKER_UI_CANDIDATE
created: 2026-05-11
phase: extension_micro_shell_dom_perception
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Make the browser extension's DOM perception markers coherent for the operator. The circular info markers and colored borders should explain what the extension sees without making the page feel randomly tagged.

## Problem

Manual refresh can surface many circular markers and colored borders across the ChatGPT page:

```text
messages
code blocks
concrete YAML action candidates
composer controls
send / attach / voice controls
source chips
uploaded assets
drop / attach / tabs anchor previews
DOM inspector outlines
```

Before this packet, the markers were useful but not fully semantic. Some appeared grey, some colored, and the visual strength did not clearly separate low-signal page reading from high-signal automation-adjacent targets.

## Implemented Behavior

Marker visibility:

```text
low-signal markers -> dim by default
nearby hover/focus -> marker brightens
high-signal markers -> remain visible
```

High-signal markers include:

```text
locally valid ION YAML action candidates
locally blocked concrete action-like YAML
send button / approval-sensitive controls
```

Marker color semantics:

```text
grey   -> readable message chunk
blue   -> code/source/drop surface
green  -> attach/asset or locally valid candidate
amber  -> send/high-signal approval or locally blocked candidate
violet -> duplicate action candidate
```

Popover detail now explains:

```text
type
role
category
status
meaning
rect
selector
text excerpt
```

## Extension Reading Model

The extension now distinguishes page perception surfaces as:

```text
read_chunk
code_chunk
action_yaml
click_zone
text_entry_zone
source_or_attachment_surface
page_marker
```

This keeps the circle buttons from acting as generic decoration. A dot is now a compact handle for the exact thing the extension thinks it can read, inspect, or route through an operator-visible workflow.

## Border / Outline Doctrine

Subtle borders show broad reading zones:

```text
message chunks
code blocks
composer controls
source/attachment surfaces
```

Strong preview borders remain reserved for active calibration or action-adjacent surfaces:

```text
green attach preview
blue drop zone preview
orange tabs anchor preview
pink selected inspector anchor
```

## Safety Boundary

These markers are visual and diagnostic only:

```text
no automatic click
no silent send
no production authority
no live execution authority
no accepted state without receipt
```

## Validation

```text
node --check ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
unzip -t ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_perception_markers_20260511.zip
```

The smoke simulation still confirms:

```text
valid YAML action packet detected
inline ion_action mention ignored
documentation snippet ignored
assistant container action detected
rendered code block action detected
safe mode blocks candidate send
DOM registry emits message/code/control marker stats
```

## Touched Paths

```text
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_PERCEPTION_MARKER_SEMANTICS_001.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_PERCEPTION_MARKER_SEMANTICS_001_RECEIPT.json
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_perception_markers_20260511.zip
```

## Package Artifact

```text
zip_path: ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_perception_markers_20260511.zip
zip_sha256: e3e0970d7b6eeecf9c0cc7026e0f204780c8040644e93fb9e67544180fea0f7a
zip_entries: 23
```

## Acceptance Boundary

Accepted:

```text
B04 perception-marker semantic UI candidate
circle marker hover/focus behavior
marker category/meaning popover fields
diagnostic marker legend
```

Not claimed:

```text
complete page perception canon
production authority
live execution authority
silent browser send
```
