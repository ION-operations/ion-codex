# ACTIONS_DECISION_TREE_FOR_ION

## Purpose

This document determines when the ION custom GPT should remain file-only and when custom Actions become justified.

## Default answer

**Stay file-only first.**

## Why file-only first

Use file-only mode if the product only needs:
- upload working continuity bundle
- read/update current state
- export updated bundle
- rely on local archive/vault outside ChatGPT

This is the smallest serious product loop and should be the first release posture.

## When Actions become justified

Actions become justified only if one or more of the following are true:

### 1. Remote continuity registry required
You need a server-side continuity manifest or project registry.

### 2. Remote validation service required
You need centralized validation, normalization, or continuity linting beyond local bundle logic.

### 3. Shared environment coordination required
You need the same continuity state discoverable across multiple shells/environments without manual bundle selection.

### 4. Remote lineage or checkpoint lookup required
You need a remote service to find prior checkpoints or continuity chains.

### 5. Richer product orchestration is impossible with files alone
Only after the file-only loop proves insufficient.

## When Actions are still premature

Actions are still premature if:
- the product can be validated through manual bundle upload/download
- archive and encryption remain local
- remote state adds more complexity than value
- the core continuity loop is not yet proven stable

## Recommended sequencing

1. file-only shell
2. local vault/helper
3. test continuity discipline and compaction
4. only then evaluate Actions

## Present conclusion

For ION, Actions should be a **second-phase optimization**, not the foundation of the first custom-GPT product.
