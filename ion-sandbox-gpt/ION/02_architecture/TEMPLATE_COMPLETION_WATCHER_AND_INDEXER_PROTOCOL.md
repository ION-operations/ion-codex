# TEMPLATE COMPLETION WATCHER AND INDEXER PROTOCOL

**Status:** Proposed restoration / operationalization protocol  
**Authority posture:** A2 production-governance candidate  
**Created:** 2026-04-24

## 1. Purpose

This protocol defines the watcher/indexer surface that detects candidate template files and converts them into classification, completion, stale-state, and event-readiness records.

## 2. Watcher law

The watcher observes. It does not govern. It may discover, classify, and nominate. It may not silently mutate source graph truth.

Allowed watcher outputs:

- file discovered record;
- template classification record;
- completion candidate record;
- stale/incomplete marker;
- duplicate/idempotence marker;
- event nomination for validation.

Forbidden watcher outputs:

- direct graph mutation;
- direct registry mutation;
- direct agent activation;
- direct schedule execution;
- authority promotion.

## 3. Indexer law

The indexer maintains projections over the evented file graph:

- which template-instantiated files exist;
- which are complete;
- which are stale;
- which have emitted events;
- which reactions have receipts;
- which files lack template class;
- which graph regions have unprocessed event pressure.

Indexes are validation projections. They do not replace source graph truth.

## 4. Scan vs. event mode

ION may operate in:

- **scan mode:** bounded sweep across watched directories;
- **watch mode:** file-system event detection;
- **manual nomination mode:** operator or agent marks a file for classification;
- **receipt replay mode:** derive index posture from receipts.

All modes must converge on the same event-readiness classification.

## 5. Required fields for watch registration

A watched path must declare:

```yaml
watch_id:
path:
file_glob:
expected_template_classes:
owner_family:
classification_policy:
completion_policy:
event_policy:
index_projection:
receipt_directory:
```

## 6. Failure posture

Unknown files, incomplete files, conflicting classifications, stale templates, missing authority class, and absent receipt paths all produce blocked/refusal/question records, not guessed actions.
