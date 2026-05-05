---
title: Evented Template File Graph Protocol
status: PROPOSED_ROOTLAW_EXTENSION_NOT_YET_RATIFIED
authority_class: A2_PRODUCTION_GOVERNANCE_CANDIDATE
created: 2026-04-24
extends:
  - CONTEXT_GRAPH_SUBSTRATE_PROTOCOL.md
  - CONTEXT_NODE_AND_PACKAGE_PROTOCOL.md
  - TEMPLATE_BINDING_PROTOCOL.md
  - SUPERVISED_DAEMON_SERVICE_PROTOCOL.md
root_law: "ION is a living context graph materialized as an evented, template-instantiated file system."
---

# Evented Template File Graph Protocol

## 1. Purpose

This protocol restores the mechanical half of ION's context-graph substrate: ION files are not inert documents. A lawful ION file is a template-instantiated graph object. When that file reaches a valid completion state, it can become an automation event surface.

The living graph is therefore not merely stored. It reacts.

## 2. Core Doctrine

ION is a living context graph materialized as an evented, template-instantiated file system.

Files are durable graph objects. Templates define the lawful shape and automation behavior of those files. Agents and humans fill templates using bounded context packages. When completed files pass validation, daemons, schedulers, indexers, registry updaters, dependency watchers, or specialist agents may trigger lawful graph reactions. Receipts prove every mutation, warning, scheduling action, settlement, or refusal.

## 3. Template-Instantiated Graph Object

A file may be treated as a template-instantiated graph object only when all of the following hold:

1. Its template class is known.
2. Its required fields are present.
3. Its status is declared.
4. Its authority class is declared or inferable from its governing template.
5. Its graph node type is declared or inferable.
6. Its graph region or owner jurisdiction is declared or inferable.
7. Its downstream effects are declared or forbidden by template law.
8. Its processing produces a receipt or a refusal record.

A file that does not satisfy these conditions may remain evidence, draft, witness, or raw source, but it must not silently trigger automation.

## 4. Template Completion Event

A Template Completion Event is the moment when a template-instantiated file crosses from candidate graph object into actionable graph event.

A completion event is valid only when:

- the template class is recognized;
- completion threshold is met;
- validation succeeds;
- authority posture permits the requested reaction;
- downstream reactions are allowed by the template;
- blocked or uncertain reactions escalate instead of guessing;
- the event emits a receipt.

Completion is not merely "the file exists." Completion is a validated state transition.

## 5. Reaction Cycle

The lawful reaction cycle is:

1. Template exists. ION knows what kind of file this is.
2. Agent or human fills the template. The file becomes a candidate graph object.
3. File reaches completion threshold. Required fields, status, authority, and route markers are present.
4. Watcher, daemon, indexer, scheduler, registry updater, or agent detects it.
5. Validator checks it.
6. Extractor derives graph meaning.
7. Automation routes allowed reactions.
8. Receipt records what happened.
9. Graph state updates or refusal remains visible.

## 6. Allowed Reaction Families

Allowed reaction families include, when authorized by template law:

- `index_update`: update a validation projection or graph index;
- `graph_node_create`: create or register a new graph node;
- `graph_edge_update`: add, remove, or mark an edge;
- `summary_refresh`: mark or update a summary/projection surface;
- `dependency_warning`: warn affected owners or domains;
- `schedule_followup`: create a scheduler or horizon item;
- `agent_activation_request`: request a specialist or subagent lane;
- `question_emit`: create an open question rather than guessing;
- `contradiction_mark`: mark affected claims as contested;
- `registry_update_proposal`: propose registry mutation;
- `receipt_emit`: emit evidence of action/refusal;
- `settlement_request`: route fan-in review.

No reaction family is self-authorizing. Each reaction must be permitted by the template and current authority posture.

## 7. Forbidden Reactions

The following are forbidden unless separately authorized by higher law:

- silent promotion of draft to live law;
- silent mutation of source graph truth from witness/projection files;
- auto-spawning agents from incomplete or ambiguous files;
- overwriting prior receipts or archives;
- treating a completed file as enough evidence to bypass landing/approval;
- creating graph edges without provenance;
- using template completion as an excuse for uncontrolled daemon autonomy.

## 8. Relationship to the Daemon

The daemon is not generic background automation. In this protocol, the daemon is the bounded executor that reacts to valid graph/file events and performs lawful graph reactions.

Daemon sequence:

```text
detect completed template file
  -> validate
  -> classify event
  -> select allowed reaction template
  -> execute one bounded reaction
  -> emit receipt
  -> stop, continue under cap, or escalate
```

The supervised daemon service remains supervised. Evented graph reaction does not create unattended authority.

## 9. Relationship to the Scheduler

The scheduler is the priority and timing layer for graph reactions. A completed file may request follow-up work, but the scheduler decides schedulability under lawful state. Downstream effects in a template are routing candidates, not automatic commits.

## 10. Relationship to Indexes

Indexes are validation projections over the evented file graph. They answer:

- which template-instantiated files exist;
- which are complete;
- which are stale;
- which graph regions they cover;
- which dependencies changed;
- which summaries need refresh;
- which receipts prove processing.

An index is not source truth. It is a projection whose value comes from traceable graph/file/receipt evidence.

## 11. Relationship to Templates

Templates are automation grammar. Every automation-capable template should eventually declare:

```yaml
template:
  id:
  file_class:
  graph_node_type:
  allowed_statuses:
  required_fields:
  completion_threshold:
  authority_class:
  graph_region:
  downstream_effects:
  allowed_reactions:
  forbidden_reactions:
  scheduler_hooks:
  agent_activation_hooks:
  index_update_hooks:
  receipt_required:
  settlement_behavior:
```

This prevents automation from guessing what a completed file means.

## 12. Safety Principle

A valid completed template file is an automation event surface, not an automatic permission slip.

The event may trigger validation, indexing, warnings, queueing, review, or bounded execution. It may also trigger refusal. The receipt is mandatory either way.

## 13. Anti-Drift Clause

ION must not forget that its files are alive only through template law. A file without template shape, authority posture, validation, and receipt linkage is not an automation event surface. A daemon without event validation is not ION automation. A graph without evented template objects is a static memory system, not living ION.
