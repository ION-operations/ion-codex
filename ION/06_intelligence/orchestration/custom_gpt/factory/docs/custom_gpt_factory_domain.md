# CUSTOM_GPT_FACTORY_001_DOMAIN_AND_AGENT_DESIGN

Status: proposal
Created: 2026-05-10
Work request: `codex_req_2026-05-10T184613Z0000_custom_gpt_factory_001_domain_and_agent_design_goal_design_the_ion_daimon_custom`
Carrier authorization: `carmsg_2026-05-10T192948Z0000_chatgpt_browser_carrier_to_codex_cli_carrier`

## Purpose

Design the ION/dAimon Custom GPT Factory domain: a governed domain and specialist agent system for building, packaging, validating, updating, and publishing role-specific Custom GPTs using capsule-first packages aligned with Codex CLI capsules.

The factory compiles role capsules into Custom GPT configuration packages and aligned Codex CLI capsule packages. It must prevent full ION engine dumps into every role GPT.

## Product taxonomy

ION is the engine, continuity substrate, context graph, state-transition law, packets, proof gates, receipts, and settlement layer.

dAimon is the agent/product layer users meet. It helps users and enterprises connect APIs, systems, pages, workflows, databases, and tools into ION safely.

WisdomNET is the global federation hub for evolved states, domain packs, templates, connectors, workflows, receipts, and carrier evolutions.

Custom GPTs are role carriers. They use capsules, not full engine dumps.

## Domain: custom_gpt_factory

The `custom_gpt_factory` domain owns the governed lifecycle for role-specific GPT builds:

- role roster and boundary design
- shared micro-core curation
- role capsule compilation
- Custom GPT instruction and knowledge packaging
- action schema policy and least-privilege tool layout
- validation and smoke prompts
- release receipts and version history
- optional WisdomNET contribution packages
- alignment with Codex CLI capsule families

## Authority boundary

This domain produces candidate artifacts until reviewed and receipted.

It does not publish GPTs, configure live actions, deploy production systems, collect secrets, mutate accepted engine law, or claim any role GPT is the whole ION organism.

## Specialist roles

### GPT_FACTORY_ARCHITECT

Owns GPT roster, role boundaries, package layout, composition rules, and release topology.

Outputs:

- factory domain map
- role family map
- build packet structure
- package layout decisions

### CAPSULE_COMPILER

Compiles shared micro-core, product taxonomy, role capsule, non-claims, and output contract into GPT-ready instructions and knowledge files.

Outputs:

- `custom_gpt_instructions.md`
- `custom_gpt_knowledge_manifest.json`
- `codex_cli_capsule.md`
- `role_output_contract.md`

### ACTION_SCHEMA_CURATOR

Manages actions, OpenAPI schemas, auth modes, allowed domains, tool policies, and least-privilege configuration.

Outputs:

- `custom_gpt_action_policy.md`
- action schema manifest
- auth mode notes
- forbidden tool list

### GPT_NEMESIS

Audits overclaiming, privacy, secret handling, instruction conflicts, retrieval bloat, and marketplace/workspace risk.

Outputs:

- overclaim lint report
- secret-request lint report
- instruction conflict report
- release risk decision

### GPT_QA_CARTOGRAPHER

Tests GPT behavior, conversation starters, output contracts, retrieval behavior, refusal posture, and role-boundary routing.

Outputs:

- starter prompt smoke report
- retrieval behavior report
- role-boundary contradiction report
- validation matrix

### GPT_RELEASE_SCRIBE

Creates manifests, changelogs, version notes, setup instructions, and release receipts.

Outputs:

- `gpt_build_manifest.json`
- changelog
- setup instructions
- `gpt_release_receipt.json`

### GPT_WISDOMNET_PACKAGER

Prepares trusted role, capsule, connector, workflow, and receipt packs for WisdomNET contribution.

Outputs:

- WisdomNET candidate contribution bundle
- trust/provenance manifest
- compatibility notes

## Standard artifact structure

Factory outputs should use this package shape:

- `shared_micro_core.md`
- `product_taxonomy.md`
- `role_capsule_template.md`
- `roles/<role_id>/custom_gpt_instructions.md`
- `roles/<role_id>/custom_gpt_knowledge_manifest.json`
- `roles/<role_id>/custom_gpt_action_policy.md`
- `roles/<role_id>/custom_gpt_conversation_starters.md`
- `roles/<role_id>/codex_cli_capsule.md`
- `roles/<role_id>/role_output_contract.md`
- `roles/<role_id>/non_claims_and_authority.md`
- `gpt_build_manifest.json`
- `gpt_release_receipt.schema.json`

The same role family should be mountable by ChatGPT Custom GPT and Codex CLI as different carriers of the same bounded role.

## First role GPT packages

Initial role package family:

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

## Validation gates

Each role GPT package requires:

- instruction lint
- secret-request lint
- overclaim lint
- action policy lint
- retrieval and knowledge bloat check
- starter prompt smoke tests
- role-boundary contradiction checks
- capsule/version sync check with Codex CLI capsules
- release receipt completeness check

## Build workflow

1. Select accepted engine/context source.
2. Define or update capsule delta.
3. Compile shared micro-core, role capsule, output contract, non-claims, and action policy.
4. Generate GPT package and aligned Codex CLI capsule package.
5. Validate instruction, secret, overclaim, action, retrieval, and role-boundary gates.
6. Preview and test with starter prompts.
7. Create release receipt.
8. Publish or configure only after explicit operator authorization.
9. Optionally package for WisdomNET contribution.

## Relationship to current artifacts

The existing v2.6.7 custom GPT carrier package remains the broad ION carrier package.

The verified v0.4 Custom GPT Capsule System package is a candidate role setup-card layer.

This factory design composes with both:

- v2.6.7 provides broad carrier law, action surfaces, and live connector posture.
- v0.4 provides role setup cards, shared micro-core, role capsules, and first role build drafts.
- Custom GPT Factory provides the governed repeatable build, validation, release, and update process.

## Non-claims

- No GPTs were published by this packet.
- No live actions were configured by this packet.
- No production deployment occurred.
- No secrets were requested or handled.
- No full ION package dump is authorized for role GPTs.
- GPT configs remain candidate artifacts until reviewed and receipted.
