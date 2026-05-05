---
type: task
agent: Codex
template: RESEARCH
priority: P1
created: 2026-04-03T19:09:57-04:00
from: Sovereign
target: ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md
depends_on: ION/07_templates/_MASTER.md
status: COMPLETE
updated: 2026-04-03T19:10:56-04:00
completed_by: Codex
---

# Mission: Determine whether ION templates should be shared, agent-specific, or layered

## Goal

Evaluate whether the active ION build should move toward agent-unique templates, remain
shared, or adopt a layered structure that separates universal artifact contracts from
role-specific obligations.

## Source / Context

- `ION/01_doctrine/SOVEREIGN_CONSTITUTION.md`
- `ION/01_doctrine/SOVEREIGN_KERNEL.md`
- `ION/07_templates/README.md`
- `ION/07_templates/_MASTER.md`
- `ION/03_registry/boots/`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/PLAN.md`

## Requirements

1. Distinguish the different jobs templates are currently being asked to do.
2. Decide whether fully agent-unique templates strengthen or weaken the system.
3. Recommend a structure that preserves machine legibility, auditability, and role law.
4. Keep the result provisional unless and until governance chooses to ratify it.

## Deliverables

- `ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md`
- one Codex signal pointing the field to the note

## Constraints

1. Do not silently alter doctrine or the template tree as if the conclusion were already ratified.
2. Do not confuse boot obligations with template obligations.
3. Preserve future portability to an extracted runtime.

## Completion Signal

Emit one Codex signal pointing to the analysis.

## Completion Record — 2026-04-03T19:10:56-04:00

- status: COMPLETE
- operator: Codex
- summary: Evaluated whether ION templates should become agent-specific and concluded that the strongest future architecture is layered: shared core templates, role bindings/profiles above them, and only rare truly role-native templates when the artifact type is genuinely distinct.
- artifacts:
  - ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md
  - ION/05_context/signals/CODEX_TEMPLATE_ARCHITECTURE_LAYERING_20260403T1910.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_template_architecture_shared_vs_agent_specific/00_trace.md
- next_action: Keep the current shared template floor intact and revisit role bindings/profiles during the next deliberate template-restoration phase rather than duplicating the template tree immediately.
- note: This is a recorded architectural judgment, not yet ratified doctrine.
