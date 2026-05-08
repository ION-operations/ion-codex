# GRAPH REACTION REGISTRY PROTOCOL

**Status:** Proposed restoration / operationalization protocol  
**Authority posture:** A2 production-governance candidate  
**Created:** 2026-04-24

## 1. Purpose

The Graph Reaction Registry defines which reactions a Template Completion Event may request, who may execute them, what they are allowed to mutate, what they are forbidden to mutate, and what receipt proves the result.

Without this registry, evented files become unsafe: automation would infer behavior from prose or convention. With this registry, file completion becomes lawful and bounded.

## 2. Reaction record shape

Every reaction type must declare:

```yaml
reaction_id:
  class:
  source_event_types:
  allowed_template_classes:
  executor_family:
  required_authority:
  allowed_effects:
  forbidden_effects:
  required_inputs:
  outputs:
  receipt_type:
  idempotence_key:
  escalation_target:
  audit_owner:
```

## 3. Seed reaction families

- `index_update`
- `graph_node_create`
- `graph_edge_update`
- `summary_refresh`
- `dependency_warning`
- `schedule_followup`
- `agent_activation_request`
- `question_emit`
- `contradiction_mark`
- `registry_update_proposal`
- `receipt_emit`
- `settlement_request`

## 4. Authority boundary

A reaction registry entry does not itself authorize execution. It defines the lawful shape of possible reaction. The daemon, scheduler, operator policy, activation authority, and governed write path still decide whether execution may occur.

## 5. Anti-inference law

If no registry entry exists for an effect, ION must not execute the effect. It may emit a question or proposal asking whether the effect should be registered.

## 6. Relation to subagents

Reaction entries may name a manager family or sub-specialist family as the expected executor, but this is a routing hint, not live activation by itself. Specialist activation remains governed by the agent/subspecialist fan-out protocols.
