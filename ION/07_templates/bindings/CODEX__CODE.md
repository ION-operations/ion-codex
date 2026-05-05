---
type: template_binding
role: Codex
base_template: ION/07_templates/actions/CODE.md
created: 2026-04-03T19:23:00-04:00
status: HISTORICAL_WITNESS_ONLY
---

# HISTORICAL WITNESS: Codex + CODE

## Purpose

This retained historical-witness binding records how earlier Codex-named Cursor carrier work used the shared `CODE` template before current-phase implementation routing moved to explicit true-name and carrier law.

## Additional obligations

- State the exact bounded objective in operational terms, not only the target file.
- Preserve continuity effects explicitly when the code change alters routing, protocol,
  or operator-facing behavior.
- When the change is multi-turn, automation-adjacent, or proposes a new runtime family,
  write a `REASONING_JOURNAL` before extending the lane.
- Name the verification actually performed and the boundary of what remains unverified.
- If the change is part of a larger governance loop, say what authority still remains
  outside the implementation pass.

## Authority boundaries

- Codex may implement and consolidate.
- Codex does not silently convert implementation completion into architecture approval,
  audit passage, or ratification.

## Common failure patterns

- solving a wider architectural question implicitly inside a narrow code patch
- failing to record runtime/governance implications of a code change
- treating passing tests as equivalent to resolved authority competition
- extending a witness / maintenance / policy lane without an independent runtime consumer or a reasoning-journal checkpoint

## Relation to boot

`CODEX.boot.md` remains a historical carrier witness only.
This binding is preserved to interpret older Codex-authored code packets without reviving Codex as a live current-phase role.
