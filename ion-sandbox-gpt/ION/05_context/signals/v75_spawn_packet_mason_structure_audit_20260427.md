---
type: v75_demo_spawn_packet
role: MASON
mission: structure_template_surface_audit
authority: READ_ONLY
---

# V75 demo — MASON spawn packet (structure / template / surface audit)

Lawful **named ION role** mount on a **Cursor Task** carrier slot. **No live execution.** **No production authority.**

```yaml
spawn_packet_id: V75-MASON-STRUCT-20260427

parent_mount:
  carrier: cursor_parent_chat
  mounted_role: STEWARD
  relay_packet_id: RELAY-V75-20260427-MASON
  authority_level: TASK_SCOPED_LOCAL_ORCHESTRATION

child_mount:
  carrier: cursor_subagent
  agent_name: MASON
  role_boot: ION/03_registry/boots/MASON.boot.md
  mounted_identity: MASON
  mounted_by: local_STEWARD_carrier
  authority_level: READ_ONLY
  production_authority: false
  live_execution_authority: false

mission_packet:
  objective: Audit ION/07_templates and ION/02_architecture carrier surfaces for structural consistency.
  workstream: implementation
  context_package: |
    Compile boot excerpt + STEWARD routing + template bindings for a read-only
    structure audit bounded to ION/07_templates and ION/docs/cursor spawn docs.
  required_reads:
    - ION/03_registry/boots/MASON.boot.md
    - ION/docs/cursor/ION_SUBAGENT_SPAWN_PACKET_TEMPLATE.md
  active_template: ION/07_templates/actions/CODE.md
  allowed_paths:
    - ION/07_templates/**
    - ION/docs/cursor/**
    - ION/02_architecture/**
  forbidden_paths:
    - "**/.env"
    - "**/credentials/**"
    - "**/node_modules/**"
  blocked_actions:
    - external_api_call
    - live_mcp_tool_execution
  validation_commands:
    - PYTHONPATH=ION/04_packages python3 -m pytest ION/tests/test_kernel_v75_cursor_subagent_spawn_readiness_audit.py -q
  return_contract:
    - findings_markdown
    - risks
    - template_surface_notes
  receipt_requirement: ION/05_context/signals/v75_steward_spawn_integration_receipt_20260427.txt

integration:
  proposal_status: PENDING_STEWARD_REVIEW
  steward_integration_required: true
  relay_report_required: true
  persona_visible_update_required: false
```
