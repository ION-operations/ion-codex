# ION Product Package Specification

Status: `FIRST_SCAFFOLD_NON_RELEASE`

## Objective

Create a productized ION projection for Custom GPT and browser-sandbox
operation without creating a second ION source of truth.

## Engine / Data / Adapter Separation

```text
engine != data
adapter != engine
runtime != state
receipt != source truth
```

`ION_ENGINE/` contains law and method. `ION_STARTER_DATA/` contains
portable state. `ION_CUSTOM_GPT_ADAPTER/` teaches a browser AI carrier
how to operate the package. `ION_DATA_SCHEMA/` defines compatibility.

## Lifecycle

1. No data zip is mounted.
2. Adapter quietly initializes seeded starter continuity and asks what
   the user is working on.
3. Data package is initialized from `ION_STARTER_DATA/`.
4. Meaningful work appends a receipt and updates current state.
5. Adapter exports a new continuity data zip.
6. The user carries the data zip forward.

## Acceptance Boundary

AI output is proposal until it has context, proof, approval, and
receipt. A Custom GPT may draft state updates, but the data package is
the carried continuity body.

## Non-Release Boundary

This first scaffold is not a polished release. It establishes folder
law, provenance, starter state, draft schemas, and validation tooling.

## Product Package Invariants

- The package must name its live source commit.
- The engine layer must not contain user state.
- The data layer must not rewrite engine law.
- The adapter must treat model output as proposal.
- A state update must append a receipt.
- An exported data zip must preserve the manifest, state, graph,
  packets, receipt ledger, decisions, and artifacts custody.
- Migration between schema versions requires a migration receipt.
- First-run UX should expose continuity benefits, not ION internals.
- User-facing language should say `project memory pack` where possible.
