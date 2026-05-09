# v2.6 Package Validation Report

status: candidate_builder_ready
validated_at: 2026-05-08T21:57:36Z

## Checks

- Package tree created under active root.
- Old v1.4 package preserved.
- Root mount anchors preserved.
- Hot boot spine added.
- Sign-in, sign-up, guest mode, Actions/MCP, extension/YAML bridge, dynamic
  domains, Persona envelope, export, and failure recovery docs added.
- Active-root dynamic route compiler and Persona envelope surfaces overlaid.
- `.pytest_cache`, `__pycache__`, and `*.pyc` excluded from the candidate tree.
- JSON manifests parse successfully.
- v2.6.1 guest-mode starter/tool gate added after live Custom GPT trial showed
  `/guest-mode` could over-trigger MCP status checks.
- v2.6.2 sandbox-first action gate added after live Custom GPT trial showed
  file/instruction/sandbox requests could still over-trigger MCP.

## Expected ZIP Artifact

`ION/06_artifacts/packages/custom_gpt/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508T215736Z.zip`

Updated revision artifact:

`ION/06_artifacts/packages/custom_gpt/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_1_CANDIDATE_20260508T222000Z.zip`

Updated sandbox-first revision artifact:

`ION/06_artifacts/packages/custom_gpt/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_2_CANDIDATE_20260508T224500Z.zip`

## Non-Claims

This validation does not prove live Custom GPT upload behavior, live Action auth,
Cloudflare tunnel health, local hub health, or production readiness.
