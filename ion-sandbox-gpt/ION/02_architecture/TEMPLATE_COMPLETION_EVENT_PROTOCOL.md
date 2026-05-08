---
title: Template Completion Event Protocol
status: PROPOSED_ROOTLAW_EXTENSION_NOT_YET_RATIFIED
authority_class: A2_PRODUCTION_GOVERNANCE_CANDIDATE
created: 2026-04-24
extends:
  - EVENTED_TEMPLATE_FILE_GRAPH_PROTOCOL.md
  - TEMPLATE_BINDING_PROTOCOL.md
  - PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
---

# Template Completion Event Protocol

## 1. Definition

A Template Completion Event is a validated transition in which a template-instantiated file becomes actionable by ION automation.

It is the event that lets ION treat a completed packet, handoff, contradiction note, summary, dependency change, template proposal, or registry proposal as a graph event rather than inert text.

## 2. Completion Threshold

A completion threshold is template-specific. At minimum it must evaluate:

- required field presence;
- status validity;
- authority class;
- actor/agent identity;
- graph node type;
- graph region;
- downstream effects;
- receipt requirement;
- unresolved contradiction markers;
- stale/draft/provisional markers.

A template may be complete for archival purposes but incomplete for automation. Completion class must be explicit.

## 3. Completion Classes

- `DRAFT_COMPLETE`: enough to preserve as draft evidence; not automation-capable.
- `WITNESS_COMPLETE`: enough to index as witness/projection; not source mutation authority.
- `ACTIONABLE_COMPLETE`: enough to route bounded reactions.
- `RATIFICATION_READY`: enough to request governance review.
- `EXECUTION_READY`: enough to request bounded execution under scheduler/daemon law.
- `BLOCKED_INCOMPLETE`: recognizable but missing required authority/context fields.

## 4. Event Envelope

A completion event should emit or derive an envelope:

```yaml
event_id:
event_type: TEMPLATE_COMPLETION
template_id:
file_path:
file_hash:
completion_class:
authority_class:
actor:
graph_node_type:
graph_region:
allowed_reactions:
blocked_reactions:
validation_result:
receipt_required: true
created_at:
```

## 5. Reaction Selection

Reaction selection must be data-driven by template law. The automation system may not infer large reactions from prose. If a downstream effect is not declared and allowed, it must be escalated or ignored with receipt.

## 6. Refusal Is a Valid Reaction

If a file is incomplete, stale, unauthorized, contradictory, or unsupported, the system should emit a refusal/hold receipt. This keeps failed automation visible and prevents silent dead surfaces.

## 7. Dependency Warning Rule

If a completed file affects nodes with dependents, ION should mark or warn those dependents rather than assuming they remain valid. This is one of the primary reasons template completion events matter.

## 8. Specialist Activation Rule

Specialist or subagent activation may be requested by a template completion event only when:

1. the template declares an activation hook;
2. the graph region is known;
3. the specialist jurisdiction permits the work;
4. the scheduler/Steward route permits the activation;
5. the activation itself emits a packet/receipt.

## 9. No Hidden Completion

Completion detection must be reproducible from file contents, template registry, validation rules, and receipts. Hidden oral context is not completion evidence.
