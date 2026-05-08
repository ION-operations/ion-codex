# ION Self-Knowledge Onboarding Wiring Proposal v0.3

Generated: `2026-05-08T04:57:21+00:00`  
Status: `candidate_validated_pending_acceptance`

## Intent

Wire ION-about-ION tasks through the self-knowledge mount packet and route registry before a carrier explains, modifies, or continues ION itself.

This is still an activation of existing ION organs, not a new architecture.

## Candidate evidence now available

- Candidate mount packet exists.
- Candidate route registry covers ION identity, authority, full local/API runtime, GPT sandbox adaptation, context/template/receipt, self-knowledge implementation, and recovery/anti-regression.
- Route-usage simulation exercised every candidate route.
- Onboarding-wiring simulation exercises GPT sandbox and Codex CLI carrier surfaces and checks that ION-about-ION cases mount self-knowledge before answer drafting.
- Non-ION tasks bypass self-knowledge routing and continue normal active-packet workflow.

## Candidate route intercept

```yaml
route_id: route.self_knowledge_mount_first_for_ion_about_ion
action_order:
  - normal_mount_contract
  - carrier_profile
  - active_onboarding_packet
  - task_classification
  - active_self_knowledge_mount_packet
  - self_knowledge_route_registry
  - required_domain_packets
  - bounded_answer_or_action
```

## Proposed future target surfaces after acceptance

- `ION/02_architecture/ION_SELF_KNOWLEDGE_ONBOARDING_WIRING_PROTOCOL.md`
- `ION/03_registry/self_knowledge/*`
- carrier onboarding/onboard tools, if a future implementation packet authorizes mutation
- Custom GPT product onboarding instructions, if the product lane accepts the update

## Non-claims

This proposal does not mutate onboarding, registry, or product instructions. It is a candidate wiring proposal backed by sandbox-local simulation evidence.
