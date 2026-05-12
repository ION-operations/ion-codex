# CUSTOM_GPT_FACTORY_002_GENERATE_FIRST_ROLE_PACKS

Status: recommended next packet
Created: 2026-05-10
Depends on: `CUSTOM_GPT_FACTORY_001_DOMAIN_AND_AGENT_DESIGN`

## Purpose

Generate the first role-pack family using the Custom GPT Factory domain design.

## Scope

Generate candidate role packages for:

- ION Core Carrier
- dAimon Companion / Integration Agent
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

## Required inputs

- `ION/06_intelligence/orchestration/custom_gpt/factory/docs/custom_gpt_factory_domain.md`
- `ION/06_intelligence/orchestration/custom_gpt/factory/registry/custom_gpt_role_registry.json`
- verified v0.4 setup-card package staged at `ION/05_context/current/custom_gpt_capsule_system/ION_CUSTOM_GPT_CAPSULE_SYSTEM_20260510_v0_4/`
- existing v2.6.7 custom GPT carrier package root for broad-carrier compatibility checks

## Required outputs

For each role:

- `custom_gpt_instructions.md`
- `custom_gpt_knowledge_manifest.json`
- `custom_gpt_action_policy.md`
- `custom_gpt_conversation_starters.md`
- `codex_cli_capsule.md`
- `role_output_contract.md`
- `non_claims_and_authority.md`
- `role_build_manifest.json`

For the family:

- `gpt_build_manifest.json`
- `gpt_release_receipt.schema.json`
- validation matrix
- changelog
- factory receipt

## Validation

- instruction lint
- secret-request lint
- overclaim lint
- action policy lint
- retrieval and knowledge bloat check
- starter prompt smoke tests
- role-boundary contradiction checks
- capsule/version sync check with Codex CLI capsules

## Boundaries

- No GPT publishing.
- No production deployment.
- No secrets.
- No git push.
- No full ION package dump into role GPTs.
- No live actions unless separately authorized.
- Candidate role packs only until reviewed and receipted.
