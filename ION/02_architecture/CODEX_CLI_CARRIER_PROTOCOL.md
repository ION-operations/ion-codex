# Codex CLI Carrier Protocol V125

## Purpose

Codex CLI is the preferred local worker carrier for the current ION build lane.
It is distinct from the older Codex IDE/extension carrier surface even when both
share the same underlying OpenAI Codex product family.

The intended operating relationship is:

```text
ChatGPT browser / GPT-5.5 Pro = coordinator, long-horizon reasoning, decision receipts, connector-visible state
Codex CLI = local bounded filesystem/build/test worker carrier
ION = governing runtime, packets, templates, proof gates, receipts, state surfaces, and cockpit projection
```

Codex CLI is not ION identity, STEWARD, RELAY, PERSONA, or final authority. It
is a high-capability local carrier for executing bounded work packets and
returning proof-bearing results.

## Mount Law

A Codex CLI session is lawful only after it proves:

- shell root contains `pyproject.toml` and `ION/REPO_AUTHORITY.md`;
- carrier profile is `CODEX_CLI_CARRIER`;
- the active objective or explicit work packet is known;
- the session is bound to allowed paths and forbidden paths;
- all changes are reported through `### CONTEXT PROOF`, `### TEMPLATE ACTION PROOF`, and `### RESULT`;
- tests and command results are included as evidence;
- live/production authority remain false unless separately ratified.

## Recommended Local Use

Use Codex CLI from the ION shell root. For exploratory or review work, prefer
interactive/suggest operation. For bounded implementation packets, use
non-interactive execution with captured output so ION can ingest the final
message as a task return.

The safest default automation shape is:

```bash
codex exec --sandbox workspace-write --output-last-message ION/05_context/current/codex_cli/latest_return.md < ION/05_context/current/codex_cli/latest_prompt.md
```

A stricter one-shot lane can add JSONL event capture:

```bash
codex exec --json --sandbox workspace-write --output-last-message ION/05_context/current/codex_cli/latest_return.md < ION/05_context/current/codex_cli/latest_prompt.md > ION/05_context/current/codex_cli/latest_events.jsonl
```

ION does not require Codex CLI to be able to self-authorize. It requires Codex
CLI to return bounded evidence that ION can validate.

## Required Return Sections

Codex CLI returns intended for ION intake must include:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

The return must list root proof, active packet used, files read, files changed,
tests run, receipts/view models emitted, boundaries not crossed, and remaining
blockers.

## ChatGPT Browser Connector Relationship

The ChatGPT browser connector may request Codex work packets through the bounded
`ion_request_codex_work_packet` tool. Those packets are not direct shell
commands. They are queueable objectives for the local Codex CLI carrier lane.

Codex CLI results must return through either:

- the connector `ion_submit_task_return` flow, when the ChatGPT connector is
  live; or
- the local `kernel.ion_carrier_task_return`/proof-gate flow, when operating
  without a live browser connector.

## Forbidden Claims

Codex CLI must not claim:

- ION identity;
- STEWARD authority;
- RELAY authority;
- PERSONA authority;
- production authority;
- live execution authority beyond the bounded packet;
- approval to delete, push, expose credentials, or deploy unless a separate
  human gate explicitly grants that action.

## Current V125 Ceiling

This protocol certifies Codex CLI as a preferred local worker carrier surface at
`L1_TOOL_ASSISTED` by default and `L2_BOUNDED_EXECUTION` when a bounded prompt,
allowed paths, captured output, and proof-gated return are present.

It does not certify unattended production deployment, unbounded filesystem
access, git push, credential access, provider API calls, or host-level destructive
operations.
