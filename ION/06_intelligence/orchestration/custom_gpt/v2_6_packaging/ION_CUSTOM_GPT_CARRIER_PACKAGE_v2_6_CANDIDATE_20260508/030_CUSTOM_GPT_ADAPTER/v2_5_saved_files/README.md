# ION Custom GPT Saved Files v2.5

status: candidate_builder_ready
created: 2026-05-08
purpose: Saved-file pack for the ION Custom GPT browser carrier.

## Why This Exists

The Custom GPT must not treat ION as a passive reference library. It must mount
ION first, classify the route, obey source priority, use connection proof when
available, and only then answer or emit a tool/action proposal.

This pack gives the GPT small lookup files for the connected surfaces:

- core ION carrier law and mount-first behavior;
- ChatOps browser extension YAML bridge;
- ION Action Gateway;
- ION MCP JSON-RPC Action;
- auth, sign-in, guest, and reentry proof;
- anti-drift source priority and failure handling;
- BOOT-0 through BOOT-6 context layering;
- dynamic domain/agent proposal routing;
- persona-visible response envelopes;
- examples for lawful YAML/action use.

## Upload Rule

Upload these files into the GPT Knowledge / saved files area. Do not upload the
full ION repo or full engine package for this purpose.

## Builder Instructions

Use:

`01_core_mount/ION_CUSTOM_GPT_INSTRUCTIONS_V2_5.md`

as the instruction-field paste candidate. The other files are saved-file lookup
material.

For serious carriers, the key saved-file pair is:

- `01_core_mount/BOOT_LAYER_CONTEXT_MODEL.md`
- `01_core_mount/BOOT_PACKAGE_ARTIFACT_MAP.md`

These define the difference between always-loaded law, route-selected domain
context, retrieval reserve, and closure/export context.

## Authority Boundary

This pack is operational guidance for the Custom GPT carrier. It is not accepted
ION law by itself, does not grant production authority, does not grant live
execution authority, and does not replace connector/tool proof.
