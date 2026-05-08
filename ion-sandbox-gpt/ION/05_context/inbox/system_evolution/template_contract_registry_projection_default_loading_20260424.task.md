# Template Contract Registry Projection and Default Loading

```yaml
packet_id: template_contract_registry_projection_default_loading_20260424
status: COMPLETE_PROPOSAL
agent: Mason
depth_class: D3
authority_posture: A3_OPERATIONAL_PROPOSAL
objective: Add dependency-free JSON contract projection/loader and make Phase 1/Phase 2 auto-load it when present.
created_surfaces:
  - ION/02_architecture/TEMPLATE_CONTRACT_REGISTRY_PROJECTION_PROTOCOL.md
  - ION/03_registry/template_metadata_contract_registry.projection.json
  - ION/04_packages/kernel/template_contract_registry.py
  - ION/07_templates/templates/TEMPLATE_CONTRACT_REGISTRY_PROJECTION.md
  - ION/tests/test_kernel_template_contract_registry_projection.py
modified_surfaces:
  - ION/04_packages/kernel/template_completion_events.py
  - ION/04_packages/kernel/template_reaction_selection.py
required_reviewers:
  - Steward
  - Nemesis
next_lawful_move: Expand contracts for all automation-capable templates and decide when to require projection presence for production roots.
receipt_required: true
```

## Summary

This packet gives kernel-safe runtime code a dependency-free contract registry projection and makes contract-bound eventing automatic when that projection exists.
