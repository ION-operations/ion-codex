# ION Self-Knowledge Onboarding Wiring Proposal v0.2

Generated: `2026-05-08T04:05:23+00:00`  
Status: `candidate_pending_acceptance`

## Intent

Wire ION-about-ION tasks through the self-knowledge mount packet and route registry before a carrier explains or modifies ION.

This implements the canvas Phase 4 behavior:

```text
if task is about ION itself:
  mount ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET
  route through self_knowledge route registry
else:
  proceed with normal packet/domain workflow
```

## Proposed future target surfaces

After acceptance, a bounded implementation packet should update only the appropriate carrier/onboarding surfaces. Candidate target classes:

- `ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json`
- `ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.codex_cli.json`
- `ION/03_registry/boots/*` where self-knowledge boot routing is appropriate
- Custom GPT package setup docs/instructions, if the product package lane accepts the update

## Candidate routing rule

```yaml
route_id: route.self_knowledge_mount_first
trigger:
  any_of:
    - task_mentions_ION_identity
    - task_mentions_ION_architecture
    - task_mentions_ION_runtime
    - task_mentions_ION_package
    - task_mentions_ION_workpacket
    - task_mentions_ION_state_or_receipt
    - task_mentions_ION_agent_or_role
action:
  - mount: ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md
  - load_route_registry: ION/03_registry/self_knowledge/route_registry.yaml
  - classify_query
  - load_required_domain_packets
guardrails:
  - do_not_free_answer_from_memory
  - preserve_candidate_vs_accepted_boundary
  - cite_or_name evidence surfaces
  - do_not_reduce_full_ION_to_single_carrier_sandbox_mode
  - do_not_call_GPT_package_reduced_ION
  - do_not_promote_witness_or_donor_material_to_law
```

## Non-claims

This file does not mutate onboarding. It is a candidate wiring proposal for a future accepted implementation packet.
