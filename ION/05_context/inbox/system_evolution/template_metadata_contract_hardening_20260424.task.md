# Template Metadata Contract Hardening

```yaml
packet_id: template_metadata_contract_hardening_20260424
status: COMPLETE_PROPOSAL
agent: Steward
depth_class: D3
authority_posture: A3_OPERATIONAL_PROPOSAL
objective: Install machine-readable template metadata contract law, registry seed, template, validator, and tests.
created_surfaces:
  - ION/02_architecture/TEMPLATE_METADATA_CONTRACT_PROTOCOL.md
  - ION/03_registry/template_metadata_contract_registry.yaml
  - ION/07_templates/templates/TEMPLATE_METADATA_CONTRACT.md
  - ION/04_packages/kernel/template_metadata_contracts.py
  - ION/tests/test_kernel_template_metadata_contracts.py
required_reviewers:
  - Mason
  - Nemesis
next_lawful_move: Bind V10 evented graph phases to contract lookup instead of permissive inference.
receipt_required: true
```

## Summary

This packet hardens the template layer. It does not yet rewrite the V10 event pipeline to require contract lookup for every event; it creates the law, registry seed, validator, and tests needed for that next step.
