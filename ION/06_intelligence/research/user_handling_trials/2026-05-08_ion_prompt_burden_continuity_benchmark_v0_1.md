# ION Prompt-Burden and Governed-Continuity Benchmark

**Draft:** v0.1  
**Date:** 2026-05-08  
**Purpose:** Convert the first custom-GPT user-handling case study into a repeatable benchmark.

## Scope

This benchmark evaluates interaction handling, not truth of a domain theory.

It tests whether an AI system can receive raw or nonlinear user ideation and produce governed continuity with low user prompt-management burden.

## Comparison Conditions

Use the same or equivalent user input across:

1. Baseline assistant: ordinary ChatGPT-style conversation with no ION governance.
2. Custom GPT without ION state discipline, if available.
3. ION custom GPT with Actions/MCP and governed continuity surfaces.
4. ION cold-start package reentry in a fresh chat.

## Required Input Set

Each trial should include:

- Raw ideation prompt with unclear structure.
- Continuation-only prompts such as "continue" or "proceed".
- At least one analogy-heavy claim that could be overpromoted.
- One fresh-chat reentry using only a work package.
- One explicit correction or user concern, if naturally occurring.

## Metrics

### 1. Prompt Burden Index

```text
Prompt Burden Index = explicit organizational commands / total user prompts
```

Organizational commands include: remember this, make a plan, classify claims, write next steps, create a receipt, update state, do not overclaim, make a queue, recover context.

Lower is better when output quality remains high.

### 2. Continuity Recovery Score

```text
Continuity Recovery Score = recovered state fields / expected state fields
```

Expected state fields:

- current project/state version
- latest executed packet
- latest result
- active non-claims
- next queued work
- artifact lineage
- accepted vs candidate boundary
- validation status
- evidence file list

### 3. Claim Hygiene Score

```text
Claim Hygiene Score = correctly bounded claims / required claim boundaries
```

Required boundaries:

- analogy vs derivation
- benchmark vs proof
- candidate scaffold vs accepted state
- validation result vs domain truth
- user intuition vs system assertion

### 4. Artifact Completeness Score

```text
Artifact Completeness Score = expected artifacts produced / expected artifacts
```

Expected artifacts:

- report or synthesis
- packet
- receipt or receipt draft
- state file
- queue or next action file
- validation file or explicit validation-blocker note
- non-claim ledger
- lineage or manifest entry

### 5. Next-Step Precision Score

Scored manually from 0 to 5.

Question:

```text
Does the queued next action address the weakest unresolved gate rather than merely continuing prose?
```

Scoring:

- 0: no next step
- 1: vague next step
- 2: related but not weakest gate
- 3: concrete next step
- 4: concrete next step aimed at real blocker
- 5: concrete packet targeting the decisive unresolved claim boundary

### 6. User Friction Score

```text
User Friction Score = correction/restatement turns required to preserve structure
```

Lower is better. Corrections about preference or direction may be excluded if the system preserved governance correctly.

## Trial Record Template

```yaml
trial_id:
date:
system_condition:
domain:
input_count:
explicit_organizational_command_count:
prompt_burden_index:
continuity_expected_fields:
continuity_recovered_fields:
continuity_recovery_score:
claim_boundaries_required:
claim_boundaries_correct:
claim_hygiene_score:
expected_artifacts:
artifacts_produced:
artifact_completeness_score:
next_step_precision_score:
user_friction_turn_count:
non_claims:
evidence_refs:
limitations:
```

## First Trial Baseline Row

```yaml
trial_id: ION_CUSTOM_GPT_FIRST_USER_HANDLING_20260508
system_condition: ION custom GPT with governed memory pack output
domain: Field of Time / Temporal Density research
evidence_index: ION/06_intelligence/evidence/user_handling_trials/2026-05-08_ion_first_custom_gpt_user_handling_evidence_index.json
pack_name: ION_Field_of_Time_Project_Memory_Pack_v2_4_candidate.zip
pack_sha256: a964973b647edba00fb15c49620ba3bb45cf857771cadbdfdfd77be9f19c5985
file_count: 298
latest_packet: PCKT-20260508-013A - Temporal Scale Kernel Seed
next_packet: PCKT-20260508-013B - Temporal Scale Weight Derivation Attempt
status: qualitative_first_use_candidate
```

## Non-Claims

This benchmark does not measure model intelligence in isolation. It measures interaction governance, continuity, claim discipline, and artifact generation under messy user input.

It does not validate the domain theory used as input.

