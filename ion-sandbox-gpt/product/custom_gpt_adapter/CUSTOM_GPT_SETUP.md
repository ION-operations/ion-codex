# Custom GPT Setup

Use this file when configuring the ION Custom GPT.

## Instructions Field

Paste the full contents of:

```text
product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md
```

Current character count is below the 8,000-character Custom GPT instruction limit.

## Knowledge Files

Upload this file as the primary doctrine/reference file:

```text
product/source_inputs/ION_Continuity_Substrate_Explainer_v7.md
```

Optional additional package files:

```text
product/custom_gpt_adapter/DATA_ZIP_OPERATING_PROTOCOL.md
product/custom_gpt_adapter/STATE_UPDATE_PROTOCOL.md
product/custom_gpt_adapter/EXPORT_PROTOCOL.md
product/custom_gpt_adapter/PERSONA_INTERFACE_RULES.md
product/starter_data/
product/data_schema/
```

## Expected Behavior

The GPT should start naturally, not with an ION lecture. If no continuity package is mounted, it should ask what the user is working on and quietly organize continuity internally.

If a continuity package is uploaded, it should inspect the manifest, state, domains, context graph, open packets, decisions, artifacts, persona state, and receipt ledger before making state claims.

Any meaningful update should end with a receipt and an exported updated project memory pack.

