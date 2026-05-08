# Template Completion Event Witness Phase Protocol

**Status:** PROPOSED_IMPLEMENTATION_SLICE  
**Authority class:** A2 production-governance candidate  
**Created:** 2026-04-24  
**Depends on:** `EVENTED_TEMPLATE_FILE_GRAPH_PROTOCOL.md`, `TEMPLATE_COMPLETION_EVENT_PROTOCOL.md`, `TEMPLATE_EVENT_REACTION_PIPELINE_PROTOCOL.md`

## 1. Purpose

This protocol defines the first runnable implementation slice of the evented template file graph.

The witness phase exists because ION must be able to detect template completion events before it is allowed to mutate the source graph, schedule downstream work, update registries, or activate specialist agents from those events.

The witness phase proves the following narrow capability:

1. discover watched template-instantiated files;
2. parse their template-facing metadata;
3. classify completion candidates;
4. refuse incomplete or unsafe candidates;
5. emit dry-run `TEMPLATE_COMPLETION_EVENT` witnesses for completed candidates;
6. emit scan receipts;
7. perform no downstream graph mutation.

## 2. Root law

A valid completed template file is an automation event surface.

During Phase 1, that event surface may produce only witness artifacts. It may not directly mutate source graph state.

## 3. Allowed effects

The Phase 1 watcher may:

- read watched markdown files;
- parse YAML-like front matter;
- compute source content hashes;
- emit witness JSON under `ION/05_context/history/template_completion_event_witnesses/`;
- emit scan receipt JSON under `ION/05_context/history/template_completion_scan_receipts/`.

## 4. Forbidden effects

The Phase 1 watcher must not:

- edit the source file it observed;
- create graph node source records;
- update graph edges;
- promote registry entries;
- schedule follow-up work;
- activate agents or subagents;
- resolve open questions;
- claim ratification authority.

## 5. Completion classification

A file becomes a Phase 1 completion candidate when:

1. it is inside a watched path;
2. it is a markdown file;
3. it has front matter bounded by `---` lines;
4. required fields for the watch rule are present;
5. status is eventable for that watch rule.

The watcher supports `type` and `packet_type` as equivalent file-kind declarations for Phase 1 compatibility.

## 6. Witness semantics

A witness event proves only this:

> At a specific scan time, a watched file had a known template-facing shape, passed the Phase 1 completion envelope, and was eligible for later reaction review.

A witness event does not prove:

- that the file is ratified;
- that the file should mutate the graph;
- that downstream reactions are authorized;
- that the file is free of semantic contradiction.

## 7. Implementation surface

The Phase 1 kernel implementation is:

`ION/04_packages/kernel/template_completion_events.py`

Primary exported classes:

- `KernelTemplateCompletionWatcher`
- `IonTemplateCompletionWatcher`
- `TemplateCompletionWatchRule`
- `TemplateCompletionCandidate`
- `TemplateCompletionEventWitness`
- `TemplateCompletionScanReceipt`

## 8. Tests

The first tests are:

`ION/tests/test_kernel_template_completion_events.py`

They assert that:

- completed template files emit witness-only events;
- incomplete files are refused;
- source files are not mutated;
- missing workspace roots are rejected.

## 9. Next phase

Phase 2 may add reaction selection, but only as dry-run candidate selection. Source graph mutation remains forbidden until graph writeback and governed-write boundaries are ratified.
