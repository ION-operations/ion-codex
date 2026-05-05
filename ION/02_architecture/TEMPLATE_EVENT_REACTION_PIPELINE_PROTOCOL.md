# TEMPLATE EVENT REACTION PIPELINE PROTOCOL

**Status:** Proposed restoration / operationalization protocol  
**Authority posture:** A2 production-governance candidate, not ratified crown law  
**Created:** 2026-04-24  
**Root law served:** ION is a living context graph materialized as an evented, template-instantiated file system.

## 1. Purpose

This protocol defines the pipeline by which a template-instantiated file becomes an actionable event surface without bypassing ION's lawful write discipline.

The file is not alive merely because it exists. The file becomes event-capable only when it is classified, validated, threshold-complete, authority-permitted, and routed through a bounded reaction path with receipt evidence.

## 2. Canonical sentence

A valid completed template file is an automation event surface.

The event surface does not directly mutate the system. It authorizes a bounded review/reaction pipeline. Every mutation, refusal, warning, schedule item, index update, agent activation request, or graph writeback must remain receipt-bound.

## 3. Lifecycle

1. **FILE_DISCOVERED** — a file exists at a watched path.
2. **TEMPLATE_CLASSIFIED** — the file maps to a known template class or is explicitly unknown.
3. **COMPLETION_CANDIDATE** — fields are present enough to evaluate completion.
4. **VALIDATED_COMPLETE** — template validation and completion threshold pass.
5. **EVENT_EMITTED** — a durable Template Completion Event is emitted.
6. **REACTIONS_SELECTED** — downstream reactions are selected from template law only.
7. **REACTION_EXECUTED** — one bounded reaction executes under daemon/scheduler/operator law.
8. **GRAPH_WRITTEN_BACK** — graph/source/projection state is updated with receipt evidence.
9. **BLOCKED_OR_REFUSED** — unsafe, incomplete, unauthorized, stale, or contradictory events emit refusal/question evidence instead of guessing.

## 4. Pipeline law

The pipeline is:

```text
file change or scan
  -> template classification
  -> completion validation
  -> Template Completion Event emission
  -> reaction selection from allowlisted template effects
  -> bounded reaction proposal/execution
  -> receipt emission
  -> graph writeback or refusal
  -> index/projection refresh
```

A downstream reaction may not be inferred from prose if the template does not allow it.

## 5. Safety gates

A reaction is forbidden unless all are true:

- template class is known;
- required fields are complete;
- status is in an allowed completion state;
- authority class permits the requested effect;
- downstream effect is template-allowlisted;
- graph region is known or explicitly marked unresolved;
- idempotence key is stable;
- receipt path is defined;
- blocked uncertainty escalates to question/refusal rather than mutation.

## 6. Idempotence

The same file path, template ID, event class, and content hash must derive a stable event identity. Reprocessing an unchanged event must not duplicate graph mutations.

If the file changes after prior processing, the later event must declare whether it supersedes, amends, contradicts, or reopens the prior event.

## 7. Relation to existing ION organs

- The daemon performs bounded reaction, not freeform background automation.
- The scheduler prioritizes and times graph reactions, not arbitrary tasks.
- The indexer projects graph/file coverage; it is not source truth.
- The template registry defines event grammars.
- Receipts prove reactions and refusals.
- Steward routes governance-sensitive reactions.
- Nemesis audits false completion, unsafe effects, and unreceipted mutation.

## 8. Non-loss clauses

This protocol is invalid if interpreted to mean:

- any file can trigger automation without template classification;
- completion equals authority;
- downstream effects can be invented from prose;
- graph writes can occur without receipt evidence;
- projections or indexes can impersonate source graph truth;
- background automation can exceed bounded supervised daemon law.
