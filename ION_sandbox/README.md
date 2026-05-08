# ION Sandbox Lane

Status: source/reference/product-sandbox lane, not active runtime authority.

This folder keeps sandbox GPT/product ION package snapshots beside the active
full build so they do not remain scattered across the machine.

Active authority remains:

```text
ION/
```

This lane is evidence and source material. It may feed candidate import,
diffing, scorecards, promotion proposals, and product-package reconciliation.
It does not automatically update accepted ION law, runtime state, services,
MCP tools, Action schemas, or registries.

## Current Snapshot

```text
ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_EXERCISES_CANDIDATE_20260508T154333Z/
```

Local inventory on 2026-05-08:

- size: about 26M
- file count: 3,756
- primary package root:
  `ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_PRUNE_PASS_3_STARTER_STATE_CANDIDATE/`

## Operating Rule

```text
ION_sandbox -> compare/import as candidate -> score/validate -> promote only by explicit receipt
```

Do not edit active code directly inside this folder. If a sandbox artifact is
needed by the full build, copy or adapt the selected surface into `ION/` through
a receipted candidate lifecycle path.

## Git Rule

Raw package snapshots under this folder are ignored by default. The README and
index files may be tracked. If a specific sandbox file should be versioned, add
it intentionally through a promotion or evidence packet rather than committing
the entire package tree accidentally.

## Non-Claims

- This folder is not accepted ION canon.
- This folder is not the active runtime root.
- This folder does not grant production, live execution, secrets, deployment,
  git push, or arbitrary shell authority.
