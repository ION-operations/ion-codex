---
title: Template Reaction Selection Witness Phase Protocol
status: PROPOSED_IMPLEMENTED_PHASE_2_WITNESS_ONLY
authority_class: A2_PRODUCTION_GOVERNANCE_CANDIDATE
created: 2026-04-24
root_law: ION is a living context graph materialized as an evented, template-instantiated file system.
---

# Template Reaction Selection Witness Phase Protocol

## Purpose

This protocol defines Phase 2 of the Evented Template File Graph implementation. Phase 1 proves that completed template-instantiated files can emit dry-run Template Completion Event witnesses. Phase 2 proves that those event witnesses can be routed against an allowed reaction registry without mutating the source graph.

## Law

A Template Completion Event may be inspected for declared downstream effects only after Phase 1 validation has emitted a durable event witness. Phase 2 may select reaction families, but the selections remain dry-run witnesses. They are not graph writes, schedule writes, registry writes, or agent activations.

## Allowed in Phase 2

- read Template Completion Event witness JSON files;
- extract declared downstream effects from the witnessed front matter;
- map those effects to known reaction families;
- refuse unknown or unsupported effects;
- emit Template Reaction Selection witness JSON files;
- emit scan receipts.

## Forbidden in Phase 2

- mutating source files;
- creating or updating source graph nodes or edges;
- mutating registries;
- scheduling work units;
- activating agents or subagents;
- treating selected reactions as completed work.

## Safety Boundary

Dry-run selection is a routing proof, not a mutation authority. A selected reaction must pass later governed write, scheduler gate, registry review, or activation review before it may affect live state.
