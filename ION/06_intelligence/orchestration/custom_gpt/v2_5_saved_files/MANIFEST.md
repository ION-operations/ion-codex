# ION Custom GPT Saved Files v2.5 Manifest

## Upload Order

1. `01_core_mount/ION_CUSTOM_GPT_INSTRUCTIONS_V2_5.md`
2. `01_core_mount/MOUNT_FIRST_OPERATING_LAW.md`
3. `01_core_mount/BOOT_LAYER_CONTEXT_MODEL.md`
4. `01_core_mount/BOOT_PACKAGE_ARTIFACT_MAP.md`
5. `05_drift_guards/DRIFT_PREVENTION_AND_SOURCE_PRIORITY.md`
6. `04_auth_reentry/AUTH_REENTRY_AND_GUEST_MODE.md`
7. `02_extension_yaml_bridge/README.md`
8. `02_extension_yaml_bridge/ION_ACTION_YAML_REFERENCE.md`
9. `03_actions_and_mcp/ACTION_GATEWAY_REFERENCE.md`
10. `03_actions_and_mcp/MCP_JSON_RPC_ACTION_REFERENCE.md`
11. `03_actions_and_mcp/ACTION_SELECTION_AND_PROOF_MAP.md`
12. `07_dynamic_domains/DYNAMIC_DOMAIN_AGENT_ROUTING.md`
13. `08_persona/PERSONA_VISIBLE_ENVELOPE_REFERENCE.md`
14. `06_examples/YAML_AND_ACTION_EXAMPLES.md`

## Companion Source Paths

These are source references inside the repo. They are not all required as GPT
saved files, but they anchor this pack to real implementation surfaces.

- `ION/09_integrations/browser_extension/ion_chatops_bridge/README.md`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/src/schema.ts`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/examples/SEV_CHATOPS_SMOKE.yaml`
- `ION/09_integrations/custom_gpt_action_gateway/README.md`
- `ION/09_integrations/custom_gpt_action_gateway/openapi.yaml`
- `ION/09_integrations/chatgpt_browser_mcp_action/README.md`
- `ION/09_integrations/chatgpt_browser_mcp_action/openapi.yaml`
- `ION/03_registry/chatgpt_browser_carrier_profile.yaml`
- `ION/03_registry/gpt_sandbox_carrier_profile.yaml`
- `ION/05_context/current/self_knowledge/`
- `ION/04_packages/kernel/ion_assistant_work_route_compiler.py`
- `ION/04_packages/kernel/ion_persona_response_envelope.py`
- `ION/05_context/current/ai_assistant_work/fission/AI_ASSISTANT_WORK_DOMAIN_FISSION_CANDIDATES_V0_1.yaml`
- `ION/05_context/current/ai_assistant_work/protocols/DYNAMIC_DOMAIN_AGENT_FISSION_PROTOCOL_V0_1.md`
- `ION/05_context/current/ai_assistant_work/protocols/PERSONA_VISIBLE_ENVELOPE_PROTOCOL_V0_1.md`

## Product Posture

The GPT should rely on saved files for stable operating law, live Actions/MCP
returns for current runtime proof, and exported continuity bundles or receipts
for durable state.

The GPT should treat BOOT-0 and BOOT-1 as always-on operating law, BOOT-2 as
live/current-state proof, BOOT-3 as route-selected domain context, BOOT-4 as
deep doctrine for serious design/recovery, BOOT-5 as retrieval reserve, and
BOOT-6 as closure/export context.

## Non-Claims

This manifest does not certify production readiness, does not certify external
availability, and does not accept any candidate surface as canonical law.
