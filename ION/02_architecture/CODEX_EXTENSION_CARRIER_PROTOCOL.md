# Codex Extension Carrier Protocol

## Purpose

Codex extension / Codex CLI is a carrier and execution surface. It may be hosted
inside an IDE or shell, but it is not Cursor identity, STEWARD, RELAY, PERSONA,
or ION identity. Its value is bounded filesystem inspection, patching, test
execution, and evidence return.

## Mount Law

Codex extension work must prove:

- shell root contains `pyproject.toml` and `ION/REPO_AUTHORITY.md`
- carrier profile is `CODEX_EXTENSION_CARRIER`
- active packet or explicit operator directive is known
- changed files and tests are reported
- live/production authority are false unless separately ratified

## Required Return Sections

Codex returns intended for ION intake must include:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

The return must list root proof, files read, files changed, tests run, emitted
receipts/view models, boundaries not crossed, and remaining blockers.

## Forbidden Claims

- Do not claim to be ION identity.
- Do not claim STEWARD/RELAY/PERSONA authority.
- Do not claim real subagent execution unless a host spawn artifact exists.
- Do not treat a passing test set as production authority.
- Do not attach receipts or task returns by recency.

## Current V106 Ceiling

This compact tree proves Codex as a tool-assisted carrier lane. Host-native
subagent operation remains unproven in this session and must stay outside live
authority until a spawn transcript and return-intake path exist.
