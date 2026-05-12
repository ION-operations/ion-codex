# CUSTOM_GPT_CAPSULE_SYSTEM_003_COMPARISON_REPORT

Status: candidate comparison
Created: 2026-05-10

## Verified artifact

- Source path: `ION_CODEX FULL/workpackets/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`
- Inbox copy: `ION/05_context/inbox/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`
- sha256: `d3a2de8c391f84123b7d6d7a26193a7697db5775ac3c88be210fd9fad1bfd9e9`
- Hash matches reported sandbox value: true
- Package validation: `PASS`
- Role count: `12`

## Existing local custom GPT package baseline

- Root: `ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/`
- Latest candidate zip observed: `ION/06_artifacts/packages/custom_gpt/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_7_CANDIDATE_20260509T224136Z.zip`
- Existing package role: broad ION Custom GPT carrier package with hot boot, action schemas, active state indexes, and general ION carrier instructions.

## v0.4 setup-card package role

The v0.4 package is a candidate setup-card layer for capsule-first role Custom GPTs. It provides role-specific setup cards, instructions, capsules, conversation starters, knowledge manifests, action policies, validation prompts, and release checklists.

## Relationship verdict

`composes_with`, not `supersedes`.

The v2.6.7 package remains the broad ION carrier package. The v0.4 package adds a role setup-card layer that can generate narrower Custom GPTs such as dAimon Companion and DOM Cartographer.

## Practical implication

Use v2.6.7 for the broad ION carrier. Use v0.4 drafts for role-specific GPT setup, with the shared micro-core and strict non-claim/action boundaries.

## Non-claims

- No Custom GPTs were published.
- No live actions were configured.
- v0.4 is candidate local context until settled.
- Generated build drafts still require operator review and release checklist completion.
