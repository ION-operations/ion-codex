# BUILDER WORKFLOW

## Recommended first build posture

- Build a custom GPT on the web builder
- Enable Code Interpreter / Data Analysis
- Stay in file-only mode first
- Do not add Actions yet unless a real external continuity service is required

## Steps

1. Create a new GPT.
2. Paste the contents of `01_BUILDER_READY_INSTRUCTIONS.md` into the Instructions field.
3. Add the conversation starters from `02_CONVERSATION_STARTERS.md`.
4. Upload the files in `knowledge_pack/` into GPT Knowledge.
5. Enable Data Analysis.
6. Test with one known-good working continuity bundle.
7. Verify:
   - resume posture is stated clearly
   - continuity warnings are surfaced honestly
   - export naming is deterministic
   - updated bundle generation increments correctly
   - summaries preserve live obligations and unresolved questions

## First validation scenario

Use a small working continuity bundle and test:
- clean resume
- conservative resume from a slightly stale bundle
- export after a small state change
- compaction of cold history without loss of active state

## Included example bundles

Use the example working bundle in `ION/07_templates/custom_gpt/examples/generated/working_bundle_example.zip` for the first serious validation loop.
The vault example in `ION/07_templates/custom_gpt/examples/generated/vault_bundle_example.zip` is illustrative and should stay local/non-GPT-facing.
