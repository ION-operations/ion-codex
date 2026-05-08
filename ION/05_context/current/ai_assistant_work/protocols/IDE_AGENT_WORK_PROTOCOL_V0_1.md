# IDE Agent Work Protocol v0.1

## Status

Candidate current-context protocol. Not accepted canon.

## Purpose

Define IDE-agent work as workspace-governed action, not generic coding.

## IDE work surfaces

An IDE assistant may interact with or reason over:

- file tree,
- open buffers,
- editor selections,
- diagnostics,
- terminal state,
- test output,
- git branch/diff/status,
- package manager state,
- extension/tool state,
- local project rules,
- user chat,
- cloud/background task returns.

## Required sequence

```text
workspace mount
→ task classification
→ relevant surface inventory
→ domain route
→ context package
→ allowed action boundary
→ patch/tool/doc/UI/test branch
→ validation
→ review/security where needed
→ settlement
→ receipt/export
```

## Anti-drift rule

Do not begin from “write code.” Begin from “what IDE work state am I inside?”
