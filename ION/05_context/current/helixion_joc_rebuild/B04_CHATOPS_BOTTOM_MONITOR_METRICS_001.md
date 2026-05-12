# B04_CHATOPS_BOTTOM_MONITOR_METRICS_001

packet_id: B04_CHATOPS_BOTTOM_MONITOR_METRICS_001
status: implemented_candidate
accepted_state: ACCEPTED_AS_B04_BOTTOM_MONITOR_METRICS_CANDIDATE
created: 2026-05-11
phase: extension_micro_shell_operator_monitor
production_authority: false
live_execution_authority: false
secrets_authority: false

## Goal

Upgrade the bottom diagnostics strip from a narrow pressure readout into a compact operator monitor for the ChatGPT page and ION extension surfaces.

## Source Evidence

```text
operator request: bottom bar diagnostics should show AI message counts, connected actions, and other useful status
active UI: ION ChatOps browser extension lower monitor strip beside the ChatGPT composer
UI protocol: bottom timeline/monitor surface; dense metrics, hover detail, no monolithic dashboard
```

## Implemented Behavior

```text
Msgs A/U
  Counts loaded assistant and user conversation items visible in the page DOM.

Loaded tokens
  Keeps the visible transcript estimate and tier reference percentages.

Actions
  Shows detected ION action candidates and hover detail for valid, blocked, duplicate, and code block counts.

Queue
  Shows unsent queue count, file queue count when present, active waiting/sending count in hover detail, pause state, and send availability.

Conn
  Shows whether the extension sees send, output, or no-send state, plus selected source count. Hover detail includes composer controls, source chips, and uploaded attachments.

Lag and DOM
  Preserved browser pressure metrics for event-loop lag, long task lag, and DOM element count.
```

## Shell Zones

```text
BOTTOM_TIMELINE: compact monitor strip
RIGHT_INSPECTOR: existing Queue and diagnostics panels keep details
TOP_BAR: unchanged context/project surfaces
LEFT_ICON_RAIL: unchanged future extension utility surface
MAIN_WORK_SURFACE: ChatGPT transcript remains primary page
```

## Future Metric Ideas

```text
last_action_receipt: latest accepted/rejected/queued action id and receipt path
gateway_surface: action gateway health, MCP preview health, and tunnel reachable flags
project_context: active project/context package selected in top sync panel
attachment_lane: current files/images/zips staged for queue send
dom_confidence: attach target, drop zone, send button, composer, and source-chip confidence
autoplay_mode: queue paused/running/manual-only and mid-output permission
chat_pressure: loaded transcript trend since last refresh, not just current total
```

## Safety Boundary

This only changes local browser-extension visibility:

```text
no browser automation authority change
no production authority
no live execution authority
no silent browser send
no secrets access
counts are loaded DOM observations, not accepted ION state
```

## Validation

```text
node --check ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
node ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js
unzip -t ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_bottom_monitor_metrics_20260511.zip
zipgrep 'Msgs A' ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_bottom_monitor_metrics_20260511.zip
```

Visual browser reload was not run in this lane; the package is ready for operator extension reload.

## Touched Paths

```text
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_BOTTOM_MONITOR_METRICS_001.md
ION/05_context/current/helixion_joc_rebuild/B04_CHATOPS_BOTTOM_MONITOR_METRICS_001_RECEIPT.json
ION/09_integrations/browser_extension/ion_chatops_bridge/src/approval_ui.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/dist/content.js
ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_bottom_monitor_metrics_20260511.zip
```

## Package Artifact

```text
zip_path: ION/06_artifacts/packages/browser_extension/ion_chatops_bridge_B04_bottom_monitor_metrics_20260511.zip
zip_sha256: 995552cbac4281413ab0ea9e3b839bc47b623333b8b7a1c944911429a498b9a6
zip_entries: 23
```
