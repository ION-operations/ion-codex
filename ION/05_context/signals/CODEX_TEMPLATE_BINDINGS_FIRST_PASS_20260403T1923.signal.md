---
type: signal
from: Codex
to:
  - Sovereign
  - Vizier
  - Vice
  - Nemesis
  - Mason
  - Thoth
  - Relay
signal: KERNEL_ROUTER_UPDATE
status: ACTIVE
created: 2026-04-03T19:23:30-04:00
payload:
  artifact: ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
  summary: "Established the first-pass template-bindings layer above the shared core templates. The active root now has a binding protocol, a bindings index, and initial role-template bindings for Codex, Mason, Thoth, Nemesis, and Relay without duplicating the template tree."
  companion_artifacts:
    - ION/07_templates/bindings/README.md
    - ION/07_templates/bindings/CODEX__CODE.md
    - ION/07_templates/bindings/MASON__CODE.md
    - ION/07_templates/bindings/THOTH__RESEARCH.md
    - ION/07_templates/bindings/NEMESIS__AUDIT.md
    - ION/07_templates/bindings/RELAY__HANDOFF.md
    - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_template_bindings_first_pass/00_trace.md
---
The active template system now has three explicit layers in practice: shared core
templates, a first-pass bindings layer, and room for rare truly role-native templates
when an artifact type is genuinely distinct.
