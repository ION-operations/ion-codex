# ION First-Time User Context Package v1

This ZIP is the small first-run continuity seed for a new ION Custom GPT user or workspace.

It is meant to be uploaded alongside the main ION Custom GPT carrier package:

```text
ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508T215736Z.zip
```

The carrier package supplies ION operating law, boot order, action/MCP routing, dynamic domain rules, persona envelope rules, and product docs. This package supplies a blank but structured first-time user context body so the GPT does not have to invent state layout during the first conversation.

## Authority

This package is not the full ION engine. It is not production authority. It is not accepted project truth by itself.

It is seeded continuity state. The carrier may inspect it, use it to organize first-run work, update it by explicit receipt/export, and ask the user where to route the next step.

Do not call Action Gateway or MCP to mount this package. This package is already
the sandbox/starter context. Use connector tools only if the user explicitly
asks for live local hub/MCP/gateway status or a connector-backed draft.

## Mount Order

1. Read this file.
2. Read `ION_DATA_MANIFEST.json`.
3. Read `STATE/current_state.json` and `STATE/current_state.md`.
4. Read `PERSONA/persona_state.json`.
5. Read `DOMAINS/domain_registry.json`.
6. Read `CONTEXT/context_graph.json`.
7. Read `PACKETS/open_packets.json`.
8. Read `DECISIONS/decision_ledger.json`.
9. Read `ARTIFACTS/artifact_manifest.json`.
10. Read `RECEIPTS/bootstrap_receipt.json` and `RECEIPTS/receipt_ledger.jsonl`.
11. Use `FIRST_TIME_CONTEXT_MOUNT_GUIDE.md` for first response behavior.
12. Use `EXPORT_INSTRUCTIONS.md` when producing an updated continuity bundle.

## First Response Rule

If this is mounted in a new chat, the GPT should not dump internal file contents. It should quietly mount the package, state that ION first-time context is ready, and ask what project, idea, codebase, document, or workflow the user wants to start or attach.

For messy user input, the carrier should preserve primitives, classify claims, form a bounded next step, and create/update continuity only as candidate state until accepted or receipted.

Expected first response:

```text
ION first-time context is ready in sandbox mode. What project, idea, codebase,
document, or workflow should we start or attach?
```

Do not report MCP/local runtime status in this first response unless the user
asked for live diagnostics.
