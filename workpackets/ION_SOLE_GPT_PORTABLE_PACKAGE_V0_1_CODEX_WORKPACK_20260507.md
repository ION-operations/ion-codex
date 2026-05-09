# Codex Work Packet: ION Sole GPT Portable Package v0.1

```yaml
packet_id: ion_sole_gpt_portable_package_v0_1_codex_workpack_20260507
created_at: 2026-05-07T18:00:49.563520+00:00
status: DRAFT_FOR_LOCAL_CODEX_REVIEW
authority:
  production_authority: false
  live_execution_authority: false
  git_push_authority: false
  secrets_authority: false
```

## Objective

Review and apply the portable Custom GPT product projection patch.

This adds:

```text
product/portable_gpt/
diffs/README.md
```

The new product lane turns the existing GPT sandbox/data-zip idea into a clean
solo Custom GPT demo:

```text
user uploads project/company files
→ ION Portable classifies source authority
→ ION creates a project memory pack zip
→ user keeps the latest package
→ fresh ION GPT chat resumes from the package
```

## Inspiration Sources

- existing `product/custom_gpt_adapter/`
- existing `product/starter_data/`
- Carrier Friction Ledger work packet
- ION Portable Continuity Pack demo spec

## Artifacts

Patch file:

```text
ION_SOLE_GPT_PORTABLE_PACKAGE_V0_1_PATCH_20260507.diff
```

Package zip:

```text
ION_SOLE_GPT_PORTABLE_CUSTOM_GPT_PACKAGE_v0_1_20260507.zip
```

Starter package template:

```text
ION_PORTABLE_STARTER_PACKAGE_TEMPLATE_20260507.zip
```

## Required Review

1. Confirm this is product projection, not full dev root mutation.
2. Check compatibility with existing `product/custom_gpt_adapter/` docs.
3. Decide whether `product/portable_gpt/` should stand alone or merge with `custom_gpt_adapter`.
4. Run relevant package/schema/doc tests if available.
5. If accepted, create a receipt and move the diff to `diffs/applied/`.

## Return Contract

### CONTEXT PROOF
### TEMPLATE ACTION PROOF
template_id: ion.template.product_projection_review.v1
action_id: codex_review_ion_sole_gpt_portable_package_v0_1
result: accepted | rejected | needs_revision
touched_paths:
### RESULT
### VALIDATION
### NON-CLAIMS
### ARTIFACTS
