---
type: task
agent: Codex
template: PROPOSAL
priority: P1
created: 2026-04-03T19:20:46-04:00
from: Sovereign
target: ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
depends_on: ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md
status: COMPLETE
updated: 2026-04-03T19:23:30-04:00
completed_by: Codex
---

# Mission: Establish the first lawful template-bindings layer

## Goal

Create the smallest viable template-binding layer above the shared core templates so ION
can preserve a common machine language while making role-specific obligations more
explicit.

## Source / Context

- `ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md`
- `ION/07_templates/README.md`
- `ION/07_templates/_MASTER.md`
- `ION/07_templates/reports/RESEARCH.md`
- `ION/07_templates/reports/AUDIT.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/actions/HANDOFF.md`
- `ION/03_registry/boots/CODEX.boot.md`
- `ION/03_registry/boots/NEMESIS.boot.md`
- `ION/03_registry/boots/MASON.boot.md`
- `ION/03_registry/boots/THOTH.boot.md`
- `ION/03_registry/boots/RELAY.boot.md`

## Requirements

1. Write one protocol defining how template bindings differ from both core templates and boots.
2. Add a visible bindings directory and index under `ION/07_templates/`.
3. Add a small set of first-pass binding files for roles whose distinct discipline is already clear.
4. Keep the layer provisional and avoid duplicating the shared template tree.

## Deliverables

- `ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md`
- `ION/07_templates/bindings/README.md`
- first-pass binding files
- updated template indexes / key references
- one Codex signal pointing to the new layer

## Constraints

1. Do not silently ratify the bindings layer as final constitutional law.
2. Do not duplicate entire templates per agent.
3. Do not move role law out of boots; bindings should refine artifact use, not replace boots.

## Completion Signal

Emit one Codex signal pointing to the first-pass bindings layer.

## Completion Record — 2026-04-03T19:23:30-04:00

- status: COMPLETE
- operator: Codex
- summary: Established the first-pass template-bindings layer with one protocol, one bindings index, and five initial role-template bindings above the shared core templates.
- artifacts:
  - ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
  - ION/07_templates/bindings/README.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/07_templates/bindings/MASON__CODE.md
  - ION/07_templates/bindings/THOTH__RESEARCH.md
  - ION/07_templates/bindings/NEMESIS__AUDIT.md
  - ION/07_templates/bindings/RELAY__HANDOFF.md
  - ION/05_context/signals/CODEX_TEMPLATE_BINDINGS_FIRST_PASS_20260403T1923.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_template_bindings_first_pass/00_trace.md
- next_action: Use at least one of the new bindings inside the next live support-agent cycle so the layer is tested in practice rather than only documented.
- note: This creates a bindings layer without duplicating the shared template tree and without displacing boots as the source of role identity and authority law.
