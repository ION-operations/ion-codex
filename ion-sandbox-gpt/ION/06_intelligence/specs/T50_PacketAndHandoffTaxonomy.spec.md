---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-08T23:58:00-04:00
status: ACTIVE
implements:
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
implemented_by:
  - ION/07_templates/actions/TASK.md
  - ION/07_templates/actions/ROLE_SESSION.md
  - ION/07_templates/actions/HANDOFF.md
  - ION/07_templates/actions/CURSOR_HANDOFF.md
  - ION/07_templates/actions/MANUAL_AUTOMATION_FALLBACK.md
---

# T50 — Packet and Handoff Taxonomy

## Goal

Normalize the markdown packet families used for human/executor continuity so takeover, fallback, and bounded work remain legible.

## Canonical families

- `task`
- `role_session`
- `handoff`
- `cursor_handoff`
- `manual_automation_fallback`

## Required properties

1. Each family has a distinct purpose.
2. Each family has required frontmatter and required body sections.
3. Legacy packets may exist, but new canonical packets should satisfy the normalized form.
4. Machine-generated JSON runtime packets remain separate from these markdown continuity packets.

## Acceptance

This spec is satisfied when the packet families have one clear protocol, normalized templates, and canonical example surfaces that a fresh executor can recognize quickly.
