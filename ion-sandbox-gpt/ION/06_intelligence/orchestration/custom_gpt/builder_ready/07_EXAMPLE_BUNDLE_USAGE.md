# EXAMPLE BUNDLE USAGE

## Purpose

This note explains how to use the example continuity bundles included in the repo.

## Included examples

### Working bundle example

Path:

- `ION/07_templates/custom_gpt/examples/working_bundle_example/ION_WORKING_CONTINUITY_BUNDLE/`

Generated zip:

- `ION/07_templates/custom_gpt/examples/generated/working_bundle_example.zip`

Use this bundle to test:

- clean resume
- continuity summaries
- active temporal objects
- export-update behavior
- fresh-chat restart

### Vault bundle example

Path:

- `ION/07_templates/custom_gpt/examples/vault_bundle_example/ION_VAULT_CONTINUITY_BUNDLE/`

Generated zip:

- `ION/07_templates/custom_gpt/examples/generated/vault_bundle_example.zip`

This bundle is illustrative only. It exists to show structure and expected archival fields.
It is not intended to be decrypted by the GPT.

## Recommended test posture

1. Upload the working example zip to the custom GPT.
2. Ask for a conservative continuity resume.
3. Ask the GPT to update the bundle after a small change.
4. Start a new chat and re-upload the updated working bundle.
5. Verify that continuity survives.

## Example project in the bundle

The example bundle is intentionally aligned to the current custom-GPT development effort.

It models:

- a project preparing ION for a custom GPT shell
- active priorities around instructions, Knowledge pack, and continuity bundle design
- unresolved questions around encryption, bundle compaction, and file-only vs Actions posture
- active temporal obligations for builder validation and export/resume testing

This makes the example more realistic than a toy placeholder.
