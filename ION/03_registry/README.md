# ION Registry

This directory contains structured registries, schemas, and policy files used
by carriers, tools, templates, audits, integrations, and runtime projections.

## Common Registry Types

```text
*_registry.yaml/json      named surfaces, owners, roles, or capabilities
*.schema.json/yaml        data shapes and validation contracts
*_policy.yaml             bounded behavior and guardrail policy
*_profile.yaml            carrier or runtime profiles
```

## Key Current Surfaces

- `codex_cli_carrier_profile.yaml`
- `chatgpt_browser_carrier_profile.yaml`
- `gpt_sandbox_carrier_profile.yaml`
- `carrier_capability_registry.yaml`
- `mcp_full_carrier_tool_registry.yaml`
- `ion_github_data_plane_registry.yaml`
- `ion_chatops_action.schema.yaml`
- `ion_chatops_extension_policy.yaml`
- `ion_chatops_local_daemon_policy.yaml`
- `ion_chatgpt_browser_mcp_tool_policy.yaml`

## Subdirectories

```text
boots/                 role boot packets
capabilities/          capability registry material
domains/               domain maps and domain-specific registries
reintegration/         reintegration and recovery mappings
semantic_identities/   semantic identity surfaces
```

## Rule

Registry changes should be small and traceable. When changing runtime behavior,
update the relevant protocol, tests, and receipt path where practical.
