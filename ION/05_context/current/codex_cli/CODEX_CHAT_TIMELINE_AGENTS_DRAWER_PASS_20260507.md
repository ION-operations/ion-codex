---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: IMPLEMENTED
production_authority: false
live_execution_authority: false
---

# Codex Chat Timeline And Agents Drawer Pass

## Purpose

Improve the Codex Chat support drawers so they explain ION/Codex activity
without turning the main chat into a control wall.

## Timeline Drawer

The Timeline drawer now renders from the existing turn trace model:

- trace count;
- runner active flag;
- queued request count;
- event type counts;
- recent trace cards with ordered event flow;
- event labels, status/proof status, tool names, and bounded detail previews.

The drawer still follows the transparency boundary: context, tool, queue, file,
and proof events are visible; raw hidden reasoning is not exposed.

## Agents Drawer

The Agents drawer now renders from the existing ION agent invocation broker:

- broker owner path;
- explicit "no separate agent system" statement;
- available agent count;
- invocation count;
- available agent roster rows with invocable/missing-context status;
- recent invocation cards linked to Codex work request paths.

This remains a projection of the current broker. It does not create a second
queue, a second agent system, or new authority.

## Acceptance

- focused tests pass;
- rendered HTML contains `Trace Event Flow`, `Available Agents`, and
  `No separate agent system`;
- rendered HTML keeps the corrected Codex Chat language;
- old confusing primary-control strings remain absent;
- service can restart and serve the updated app shell.
