# Boot Package Artifact Map

status: candidate_custom_gpt_saved_file
purpose: Map boot layers to concrete artifacts the Custom GPT can mount or ask
for.

## Artifact Families

```text
ION_BOOT_MINI
ION_BOOT_STANDARD
ION_BOOT_DEEP
ION_DOMAIN_PACK_*
ION_RECEIPT_PACK
ION_DOC_PACK
ION_EXPORT_PACK
```

## `ION_BOOT_MINI`

Use for ordinary Custom GPT sessions and fast reentry.

Should contain:

- BOOT-0 Kernel law;
- BOOT-1 carrier mount summary;
- boot posture classifier;
- auth/reentry route;
- action/MCP/extension surface map;
- anti-drift source priority.

Current v2.5 files serving this role:

- `ION_CUSTOM_GPT_INSTRUCTIONS_V2_5.md`
- `MOUNT_FIRST_OPERATING_LAW.md`
- `BOOT_LAYER_CONTEXT_MODEL.md`
- `DRIFT_PREVENTION_AND_SOURCE_PRIORITY.md`
- `AUTH_REENTRY_AND_GUEST_MODE.md`

## `ION_BOOT_STANDARD`

Use for serious connected work.

Should contain:

- all mini material;
- BOOT-2 current state;
- active packet/objective;
- recent receipts;
- open loops;
- relevant carrier status;
- selected BOOT-3 domain pack.

In Custom GPT this usually requires Action/MCP/extension proof or an uploaded
continuity bundle. Saved files alone are not enough.

## `ION_BOOT_DEEP`

Use for architecture, recovery, promotion, major app build, or ION self-analysis.

Should contain:

- all standard material;
- selected BOOT-4 architecture/doctrine;
- relevant historical decisions;
- accepted/candidate boundary;
- promotion/settlement gates;
- test and receipt map.

Deep boot should be precompiled when possible. The GPT should not reconstruct it
from scratch under pressure.

## `ION_DOMAIN_PACK_*`

Use for route-local work.

Examples:

- `ION_DOMAIN_PACK_CODEX_CLI_CARRIER`
- `ION_DOMAIN_PACK_CUSTOM_GPT_ACTIONS`
- `ION_DOMAIN_PACK_BROWSER_EXTENSION`
- `ION_DOMAIN_PACK_MCP_JSON_RPC`
- `ION_DOMAIN_PACK_UI_APP_BUILD`
- `ION_DOMAIN_PACK_SELF_KNOWLEDGE`
- `ION_DOMAIN_PACK_PUBLIC_PACKAGE`

Each domain pack should include:

- domain purpose;
- current authority;
- allowed work;
- forbidden work;
- key source paths;
- relevant templates/skills;
- proof gates;
- return contract.

## `ION_RECEIPT_PACK`

Use to inherit recent proof.

Should contain:

- recent receipts;
- validation notes;
- accepted state changes;
- non-claims;
- unresolved blockers;
- continuity generation or state-root hash.

## `ION_DOC_PACK`

Use for human explanation and product orientation.

Lower authority than live returns, manifests, receipts, active packets, and
tests. It should not override current state.

## `ION_EXPORT_PACK`

Use at closure.

Should contain:

- receipt draft;
- state delta;
- next packet;
- files changed;
- validation results;
- export/continuity instructions;
- successor boot recommendation.

## Compiler Rule

Every serious carrier should know:

```text
what is always loaded
what must be mounted from live state
what is selected by route
what is available only by retrieval
what must be produced before closure
```

That is the practical distinction between a prompt and an operating substrate.
