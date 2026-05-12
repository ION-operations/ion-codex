# CUSTOM_GPT_CAPSULE_SYSTEM_003_SETUP_CARDS_INTAKE

Status: superseded by verified local ingest
Created: 2026-05-10
Sandbox package: `ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4`
Reported sha256: `d3a2de8c391f84123b7d6d7a26193a7697db5775ac3c88be210fd9fad1bfd9e9`

Correction: the artifact was present in the main project workpackets lane:

`/home/sev/ION - Production/ION_CODEX FULL/workpackets/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`

The prior blocked finding missed this path because it searched inside the `ION/` subtree but not the main `ION_CODEX FULL/workpackets/` lane.

Corrected local ingest:

- `ION/05_context/current/custom_gpt_capsule_system/CUSTOM_GPT_CAPSULE_SYSTEM_003_SETUP_CARDS_INGEST.json`
- `ION/05_context/current/custom_gpt_capsule_system/CUSTOM_GPT_CAPSULE_SYSTEM_003_COMPARISON_REPORT.md`
- `ION/05_context/current/custom_gpt_capsule_system/build_drafts/DAIMON_COMPANION_CUSTOM_GPT_BUILD_DRAFT.md`
- `ION/05_context/current/custom_gpt_capsule_system/build_drafts/DOM_CARTOGRAPHER_CUSTOM_GPT_BUILD_DRAFT.md`

## Purpose

Track local ION/Codex intake for the Custom GPT setup-card layer created by ChatGPT Browser in sandbox.

The package is reported to contain capsule-first setup cards for:

- ION Core Carrier
- dAimon Companion
- ATLAS Systems Cartographer
- WisdomNET Librarian
- Context Cartographer
- Runtime Cartographer
- DOM Cartographer
- Integration Architect
- Nemesis Audit
- Scribe
- Living Graph Designer
- Mason Builder

Each role is reported to include:

- `custom_gpt_setup_card.json`
- `instructions.md`
- role capsule
- conversation starters
- knowledge file manifest
- actions policy
- validation prompts
- release checklist

## Local artifact check

Local Codex checked these paths:

- `/mnt/data/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`
- `/home/sev/ION - Production/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`
- `/home/sev/ION - Production/ION_CODEX FULL/ION/05_context/inbox/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`
- `/home/sev/ION - Production/ION_CODEX FULL/ION/06_artifacts/packages/custom_gpt/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`

Original result: artifact absent locally.

Corrected result: artifact present in root-level workpackets lane and sha256 verified.

## Required local staging path

Place the zip at:

`/home/sev/ION - Production/ION_CODEX FULL/ION/05_context/inbox/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4.zip`

Then Codex can:

- verify sha256 equals `d3a2de8c391f84123b7d6d7a26193a7697db5775ac3c88be210fd9fad1bfd9e9`
- inspect zip manifest and validation report
- stage as candidate context package
- compare against existing custom GPT root
- generate the first two build drafts: dAimon Companion and DOM Cartographer

## Existing local custom GPT roots observed

- `ION/06_artifacts/packages/custom_gpt/`
- `ION/06_intelligence/orchestration/custom_gpt/`
- latest local candidate zip observed: `ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_7_CANDIDATE_20260509T224136Z.zip`
- latest local v2.6 candidate source root observed: `ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508/`

## Non-claim boundary

- The sandbox package is not accepted local ION state.
- No Custom GPTs were published.
- No live actions were configured.
- No setup card contents were fabricated from the relay summary.
- No build drafts were generated from unverified sandbox contents.

## Next gate

`CUSTOM_GPT_CAPSULE_SYSTEM_003_SETUP_CARDS_LOCAL_INGEST`

Acceptance:

- zip exists at the required local staging path
- sha256 matches reported value
- package manifest and proof files parse
- package is staged as candidate local context
- dAimon Companion and DOM Cartographer build drafts are generated from verified package contents
