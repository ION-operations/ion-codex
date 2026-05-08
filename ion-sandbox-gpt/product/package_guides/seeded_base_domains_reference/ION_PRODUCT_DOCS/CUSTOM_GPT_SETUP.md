# Custom GPT Setup

Use `ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md` as the instruction
base. Upload adapter docs and selected engine docs from
`ION_CUSTOM_GPT_ADAPTER/knowledge_manifest.json`.

Do not upload user data zips as permanent knowledge. User data zips are
mounted per session and exported after updates.

Include `FIRST_RUN_BEHAVIOR.md` and `PERSONA_INTERFACE_RULES.md` so the
GPT does not expose protocol machinery as its default user experience.
