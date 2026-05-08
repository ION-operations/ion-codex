---
protocol_id: ion.skill_activation_protocol.v1
status: ACTIVE_PROVISIONAL
rank: A3_OPERATIONAL
created: 2026-05-07
scope: codex_cli_capsule_and_full_ion_skill_activation
production_authority: false
live_execution_authority: false
---

# ION Skill Activation Protocol

## Purpose

Skills are the controlled activation layer for ION workflows. A skill may mount
context, choose a model move, choose a reasoning posture, select templates, and
route work through the correct carrier surface. A skill does not make output
lawful by itself.

Templates remain the proof contract. A completed action becomes admissible only
when the relevant template proof, validation evidence, and receipt/acceptance
gate are present.

```text
operator intent
-> skill selection
-> context mount
-> authority check
-> model/thinking route
-> template activation
-> bounded work or response
-> template action proof
-> validation
-> receipt / Capsule update
-> UI projection
```

## Definitions

**Skill**: user/Codex-facing reusable workflow activator. It answers when and
how a workflow should run.

**Template**: governed artifact/proof contract. It defines required sections,
authority boundaries, evidence expectations, validation, and receipt shape.

**Binding**: role-specific discipline for using a shared template. A binding
refines a template for a role; it does not replace the template.

**Capsule**: minimum working context for Codex solo work.

**Mini**: pasteable lookup and receipt index. Mini is not the primary prompt
source and is not authority.

## Authority Rule

A skill may never grant:

- production authority;
- live execution authority;
- secrets authority;
- arbitrary shell authority;
- git push authority;
- approval to work outside the active ION root;
- state acceptance without template proof and receipt.

The registry must carry these booleans explicitly as false for current Codex
and Custom GPT lanes.

## Selection Rule

Skill selection is deterministic by default:

- normal Codex chat selects `codex-chat-answer`;
- queued Codex work selects `codex-solo-work`;
- wrong-root, drift, or failed-product confusion selects `codex-recovery`;
- full ION path projection selects `ion-full-workflow-handoff`;
- template or skill surface changes select `template-curation`;
- context load and receipt posting may be invoked as internal supporting
  skills.

The selected skill must be visible in the Codex Chat trace and inspector. The
operator should not have to manually choose internal templates for normal chat.

## Activation Record

Every material skill activation should be representable as:

```yaml
skill_id:
display_name:
selection_reason:
context_mount:
  required_packages:
  route_deeper_packages:
authority:
  production_authority: false
  live_execution_authority: false
  secrets_authority: false
model_route:
  preferred_model:
  reasoning_effort:
activates_templates:
template_bindings:
proof_contract:
  context_proof_required:
  template_action_proof_required:
  receipt_required:
ui_projection:
  user_visible_label:
  drawer_visible:
```

This activation record is witness/projection only. It is not state acceptance.

## Template Gate

Correct flow:

```text
skill selected
-> template contract selected
-> context loaded
-> work performed or response produced
-> TEMPLATE ACTION PROOF validated
-> receipt written
-> Capsule/Mini refreshed if material
```

Incorrect flow:

```text
skill selected
-> prose says success
-> UI treats prose as accepted state
```

## UI Rule

The main app remains normal chat. Skills, templates, model moves, queue state,
agents, traces, and receipts belong in support drawers and timelines. They may
be inspected and audited, but they must not become required manual chores for
ordinary use.

## Relation To Full ION

Capsule ION uses skills as a compact local operating layer. Full ION may use the
same skill registry as a front-door routing surface, but Relay, Steward,
role-context packages, proof gates, and receipts remain the governing pipeline.
