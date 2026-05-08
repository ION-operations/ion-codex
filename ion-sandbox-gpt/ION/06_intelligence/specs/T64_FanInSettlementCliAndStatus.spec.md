---
type: spec
authority: A2_EXECUTOR
created: 2026-04-09T23:56:30-04:00
status: ACTIVE
---

# T64 — Fan-In settlement CLI and status projection

## Goal
Expose M2 settlement through the canonical operator surface.

## Required
- `allocator snapshot-settlement`
- `allocator settle-children`
- latest settlement projection in `status`
- text/json renderers for settlement outcomes

## Proof
- operator CLI tests prove settlement routing and status rediscovery.
