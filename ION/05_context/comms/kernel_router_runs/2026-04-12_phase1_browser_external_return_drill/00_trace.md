---
type: trace
template: PATCH_PACKAGE
created: 2026-04-12T11:49:46-04:00
status: COMPLETE
packet: phase1_browser_external_return_drill
owner: Codex
---

# Trace: Phase 1 Browser-Class External Return Drill

## Goal

Materialize one real browser-class external return over a bounded readonly snapshot, then
land the returned delta through the live branch owner instead of treating the external
carrier as direct truth.

## Outputs

- one bounded governing task for the external-return drill
- one bounded Codex role session carrying the drill
- one browser-class `HANDOFF` packet
- one real exported readonly snapshot zip
- one real `EXTERNAL_RETURN` packet
- one real `PATCH_PACKAGE`
- one bounded live-branch landing of the returned delta
- one handoff pointing to the next post-Phase-1 move
