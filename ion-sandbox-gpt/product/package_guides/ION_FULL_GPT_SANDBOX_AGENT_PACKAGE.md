# ION Sandbox GPT Package

## Purpose

This package contains the operational ION body needed for a fresh Custom
GPT/browser GPT sandbox to run a capable ION agent system with the GPT as the
carrier.

The primary continuity loop is:

```text
Braden uploads newest ION zip
→ GPT mounts ION inside its own sandbox
→ GPT executes ION's role-phase sequence sequentially
→ PERSONA_INTERFACE responds to the user
→ GPT exports an updated zip for continuity
```

## Distinction From The 42-Tool MCP Lane

The 42-tool MCP surface is an adapter for communicating with Braden's local or VM ION runtime and Codex CLI. It is not required for this package's base runtime.

```text
42-tool lane: Browser GPT → MCP → local/VM ION + Codex CLI
sandbox lane: uploaded package zip → GPT sandbox → updated package zip
```

## Package Contents

- `ION/` — operational ION source, doctrine, registries, templates, current state, integrations, tests.
- `product/custom_gpt_adapter/` — Custom GPT behavior and setup surfaces.
- `product/starter_data/` — seeded base domains for first-run operation.
- `product/data_schema/` — portable data/state schema surfaces.
- `product/source_inputs/` — current uploaded doctrine/witness inputs used to build this projection.
- `nonproduct_or_forensic/` / companion zip — manifests and bulky evidence classification.

## Authority Rule

Hot operational files guide runtime. Historical and forensic evidence is preserved for lineage, but does not become hot authority merely because it is included.

This package is non-production and non-live. It cannot access local secrets,
deploy systems, push git, run arbitrary shell through a browser GPT, or mutate a
separate local ION runtime unless an external connector lane is separately
mounted and authorized.

## First Run UX

```text
What are we working on?
```
