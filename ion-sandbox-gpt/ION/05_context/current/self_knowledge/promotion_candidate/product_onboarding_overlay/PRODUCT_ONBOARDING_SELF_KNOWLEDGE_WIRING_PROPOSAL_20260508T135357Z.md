# Product Onboarding Self-Knowledge Wiring Proposal v0.2

Generated: `2026-05-08T13:54:49+00:00`  
Status: `candidate_overlay_pending_explicit_acceptance`

## Intent

Make the GPT product/package front-door surfaces inherit ION self-knowledge mount-first behavior for ION-about-ION work.

## Current audit finding

The package already contains:

- `ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md`
- `ION/05_context/current/self_knowledge/`
- candidate domain packets, registries, route simulations, and onboarding simulations

However, the product front-door surfaces do not yet explicitly instruct a fresh GPT/product carrier to route ION-about-ION requests through the self-knowledge mount packet before answering.

## Candidate product behavior after acceptance

For ION-about-ION tasks:

```text
normal ION mount
→ active state load
→ classify ION-about-ION
→ mount ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md
→ load self-knowledge route registry
→ load required domain packets
→ answer or act with non-claims
```

## Candidate patchset

See:

`ION/05_context/current/self_knowledge/promotion_candidate/product_onboarding_overlay/PRODUCT_ONBOARDING_SELF_KNOWLEDGE_WIRING_PATCHSET_20260508T135357Z.json`

## Target surfaces proposed for future accepted patching

- `START_HERE.md`
- `README.md`
- `PRODUCT_MANIFEST.json`
- `product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md`
- `product/custom_gpt_adapter/GPT_INSTRUCTIONS.md`
- `product/custom_gpt_adapter/STARTUP_BEHAVIOR.md`
- `product/custom_gpt_adapter/knowledge_manifest.json`
- `product/package_guides/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE.md`

## Non-claims

- This proposal does not mutate product law.
- This proposal does not mutate Custom GPT instructions.
- This proposal does not mutate `PRODUCT_MANIFEST.json`.
- This proposal does not land `ION/03_registry/self_knowledge/`.
- This proposal does not claim external Codex/MCP/daemon execution.
