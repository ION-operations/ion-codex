---
type: signal
from: Codex
to:
  - Sovereign
  - Vizier
  - Vestige
  - Thoth
  - Mason
signal: KERNEL_ROUTER_UPDATE
status: ACTIVE
created: 2026-04-12T14:24:48-04:00
payload:
  artifact: ION/02_architecture/BRIDGE_PACKET_STATUS_CLARIFICATION.md
  companion_artifacts:
    - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
    - ION/03_registry/current_phase_template_surface_registry.yaml
    - ION/07_templates/README.md
    - ION/07_templates/_MASTER.md
  summary: "Landed the small bridge-packet clarification: keep the canonical packet floor at five families and keep ROLE_CHASSIS_MOUNT, DISAGREEMENT_ESCALATION, and EXTERNAL_RETURN as governed current-phase bridge packets outside the validator floor."
---
Codex landed the small bridge-packet support clarification. The branch now says this
plainly at startup surfaces instead of leaving future sessions to infer it from
validator behavior or proposal archaeology.
