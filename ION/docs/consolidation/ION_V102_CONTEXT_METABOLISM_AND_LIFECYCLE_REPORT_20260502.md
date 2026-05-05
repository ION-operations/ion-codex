# ION V102 Context Metabolism and Lifecycle Report

```yaml
report_id: ion-v102-context-metabolism-and-lifecycle-report-20260502
version_line: V102_CONTEXT_METABOLISM_AND_LIFECYCLE
production_authority: false
mutation_authority: proposal_only
```

## Finding

A separate branch reported a very large `ION/05_context/current` tree caused by temporary multi-root session material, repeated template graph writeback proposal snapshots, and many execution cycles. This V102 pass verified the current V101 branch directly and did **not** find that exact 581MB condition here.

That does not make the report irrelevant. It identifies a real ION growth mode: the system can produce receipts faster than it metabolizes them into compact current truth.

## Root cause classification

The issue is not that ION writes evidence. Writing evidence is correct. The issue is missing lifecycle ontology across generated evidence:

```text
current truth vs hot state vs warm evidence vs cold history vs quarantine
```

Without that distinction, carrier packages can become bloated and agents can mistake proof-of-work for active operational truth.

## V102 repair

V102 adds a proposal-only context lifecycle module that scans the context tree, classifies artifacts, records soft-limit findings, and writes a report without mutating evidence.

## Boundary

No deletion, movement, compression, or archival mutation is authorized by this pass.
