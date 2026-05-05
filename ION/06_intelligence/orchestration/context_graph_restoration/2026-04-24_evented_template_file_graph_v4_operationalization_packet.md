# Evented Template File Graph — V4 Operationalization Packet

**Status:** Proposed implementation-path packet  
**Date:** 2026-04-24  
**Authority posture:** Restoration/evolution proposal, not live ratified law  
**Depends on:** Context Graph Root-Law V2 and Evented Template File Graph V3

## 1. Why this packet exists

V3 recovered the mechanical doctrine that ION files are template-instantiated graph objects whose valid completion can trigger lawful automation. V4 defines the first operational path needed to make that doctrine runnable.

The key risk after V3 is false aliveness: declaring files to be event surfaces without defining the pipeline that prevents unsafe automation. V4 closes that gap.

## 2. V4 claim

The evented template file graph becomes operational only when completion detection, validation, reaction routing, bounded execution, receipt emission, and graph writeback are all explicit.

## 3. New required surfaces

V4 adds four protocols:

- `TEMPLATE_EVENT_REACTION_PIPELINE_PROTOCOL.md`
- `GRAPH_REACTION_REGISTRY_PROTOCOL.md`
- `TEMPLATE_COMPLETION_WATCHER_AND_INDEXER_PROTOCOL.md`
- `GRAPH_WRITEBACK_AND_RECEIPT_PROTOCOL.md`

It adds two registries:

- `graph_reaction_registry.yaml`
- `template_completion_watch_registry.yaml`

It adds three templates:

- `GRAPH_REACTION_RULE.md`
- `TEMPLATE_COMPLETION_WATCH_REGISTRATION.md`
- `GRAPH_WRITEBACK_RECEIPT.md`

## 4. Operational sequence

```text
template file appears or changes
  -> watcher classifies it
  -> validator checks completion threshold
  -> Template Completion Event is emitted
  -> reaction registry selects allowed reactions
  -> daemon/scheduler executes one bounded reaction or refuses
  -> receipt is emitted
  -> graph/source/projection state is written back
  -> indexes and membrane update
```

## 5. First implementation milestone

The first code milestone should not attempt full graph mutation. It should implement a safe witness pipeline:

1. scan configured watched paths;
2. classify known template files;
3. detect completion candidates;
4. emit dry-run `TemplateCompletionEvent` witnesses;
5. refuse unknown or incomplete files with evidence;
6. update a projection index;
7. add tests proving no mutation occurs without a known template and allowed reaction.

Only after this milestone passes should source graph mutation be implemented.

## 6. Candidate kernel modules

```text
kernel/template_completion_events.py
kernel/template_file_watcher.py
kernel/graph_reaction_registry.py
kernel/graph_writeback.py
kernel/evented_file_index.py
```

## 7. Required tests

```text
test_kernel_template_completion_events.py
test_kernel_template_file_watcher.py
test_kernel_graph_reaction_registry.py
test_kernel_graph_writeback.py
test_kernel_evented_file_index.py
```

## 8. Ratification question

Should ION MASTER CURRENT 3 accept the V4 operationalization surfaces as the next lawful implementation path for the restored context graph substrate?

Recommended answer: yes, as `PROPOSED_IMPLEMENTATION_PATH_NOT_YET_RATIFIED`, then assign Mason/Nemesis/Scribe review before code mutation.
