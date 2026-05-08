---
type: v75_demo_spawn_packet
role: VESTIGE
mission: provenance_root_source_audit
authority: READ_ONLY
---

# V75 demo — VESTIGE spawn packet (provenance / root / source audit)

Lawful **named ION role** mount on a **Cursor Task** carrier slot. **No live execution.** **No production authority.**

```yaml
spawn_packet_id: V75-VESTIGE-PROV-20260427

parent_mount:
  carrier: cursor_parent_chat
  mounted_role: STEWARD
  relay_packet_id: RELAY-V75-20260427-VESTIGE
  authority_level: TASK_SCOPED_LOCAL_ORCHESTRATION

child_mount:
  carrier: cursor_subagent
  agent_name: VESTIGE
  role_boot: ION/03_registry/boots/VESTIGE.boot.md
  mounted_identity: VESTIGE
  mounted_by: local_STEWARD_carrier
  authority_level: READ_ONLY
  production_authority: false
  live_execution_authority: false

mission_packet:
  objective: Read-only provenance audit of REPO_AUTHORITY, boots index, and consolidation receipts for V75 spawn surfaces.
  workstream: archaeology
  context_package: |
    Context package binds VESTIGE boot + archaeology lane continuity paths +
    explicit deny of sibling-root authority claims in findings.
  required_reads:
    - ION/REPO_AUTHORITY.md
    - ION/03_registry/boots/VESTIGE.boot.md
    - ION/docs/consolidation/TEMPLATE_RESTORATION_PROVENANCE_MANIFEST.md
  active_template: ION/07_templates/bindings/VESTIGE__EVIDENCE.md
  allowed_paths:
    - ION/REPO_AUTHORITY.md
    - ION/03_registry/**
    - ION/docs/consolidation/**
    - ION/05_context/signals/v75_*
  forbidden_paths:
    - "**/.ssh/**"
    - "**/secrets/**"
    - "**/.git/objects/**"
  blocked_actions:
    - filesystem_write_outside_allowed
    - external_model_call
  validation_commands:
    - PYTHONPATH=ION/04_packages python3 -c "from pathlib import Path; from kernel.cursor_subagent_ion_role_registry import validate_cursor_subagent_role_packet; print(validate_cursor_subagent_role_packet(root=Path('.'), agent_name='VESTIGE'))"
  return_contract:
    - evidence_table
    - ambiguities
    - no_writes_assertion
  receipt_requirement: ION/05_context/signals/v75_steward_spawn_integration_receipt_20260427.txt

integration:
  proposal_status: PENDING_STEWARD_REVIEW
  steward_integration_required: true
  relay_report_required: true
  persona_visible_update_required: false
```
