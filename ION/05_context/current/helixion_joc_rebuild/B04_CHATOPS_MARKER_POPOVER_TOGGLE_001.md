# B04_CHATOPS_MARKER_POPOVER_TOGGLE_001

packet_id: B04_CHATOPS_MARKER_POPOVER_TOGGLE_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_B04_MARKER_POPOVER_TOGGLE_CANDIDATE
created: 2026-05-11
phase: extension_micro_shell_dom_perception
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Make DOM perception marker circles behave as toggles. Clicking a marker once opens its data popover; clicking the same marker again closes it.

## Implemented Behavior

```text
click marker A -> opens marker A detail
click marker A again -> closes marker A detail
click marker B while marker A is open -> closes A and opens B
keyboard Enter/Space on a focused marker uses the same toggle path
```

## Safety Boundary

This only changes the diagnostic UI:

```text
no browser automation authority change
no click-zone execution change
no production authority
no live execution authority
no silent browser send
```

## Validation

```text
node --check ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
unzip -t ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_marker_popover_toggle_20260511.zip
```

## Touched Paths

```text
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_MARKER_POPOVER_TOGGLE_001.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_MARKER_POPOVER_TOGGLE_001_RECEIPT.json
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_marker_popover_toggle_20260511.zip
```

## Package Artifact

```text
zip_path: ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_marker_popover_toggle_20260511.zip
zip_sha256: 3bbbc61a2567d179de434e88e1a4eeb0752282d695d5af88a60ac807268598f2
zip_entries: 23
```
