# ION Browser GPT Queue Workflow Authoring Package

Package id: `ion_browser_gpt_queue_workflow_authoring_package_20260511`

Purpose: give the browser GPT / Custom GPT a governed internal ION package for
authoring advanced prompt-chain workflows that the ION ChatOps Bridge can import
as queued workflows.

This package is not an execution authority source. It creates prompt material
for the browser queue only. The queue may help an operator run multi-step ION
protocol orchestration, but every mutating, cloud, production, account, paid,
deployment, destructive, or secrets-touching step must remain approval-gated in
the prompt text and by the relevant connector or local bridge.

## Mount Order

1. `000_READ_FIRST.md`
2. `001_BROWSER_GPT_SYSTEM_INSTRUCTIONS.md`
3. `010_PROTOCOL/ION_QUEUE_WORKFLOW_AUTHORING_PROTOCOL.md`
4. `020_SCHEMAS/ion_extension_queue_pack.schema.json`
5. `030_TEMPLATES/`
6. `050_VALIDATION/QUEUE_WORKFLOW_VALIDATION_CHECKLIST.md`

## What This Enables

- Browser GPT can draft an ION queue workflow from a user goal.
- Browser GPT can organize work into workflows, chains, steps, gates, and
  receipts.
- User can save the generated pack as `.json` or `.zip`.
- User can load it through the ION bridge Queue tab with `Import Pack`.
- The extension turns each step into one queued ChatGPT message.

## Importable Seed

The example under `040_EXAMPLES/advanced_orchestration_queue_pack/` is a
ready-to-zip seed workflow. Its `ion_queue_pack.json` references prompt files
under `prompts/`.

The generated artifact ZIP is expected at:

`ION/06_artifacts/packages/custom_gpt/ION_ADVANCED_ORCHESTRATION_QUEUE_PACK_SEED_20260511.zip`

## Authority Boundary

The generated queue workflows are planning and prompt orchestration artifacts.
They do not grant:

- production authority
- live execution authority
- secrets authority
- direct local file authority
- direct Google Cloud, MongoDB, GitHub, or GitLab authority
- silent browser send authority
- permission to bypass user approval

