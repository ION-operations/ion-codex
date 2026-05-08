---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE_PROVISIONAL
scope: codex_capsule_fallback_operating_kernel
production_authority: false
live_execution_authority: false
---

# Codex Capsule Operating Protocol

## Purpose

This protocol defines the small ION operating kernel for Codex CLI and Codex
chat carriers while the full ION Codex CLI system is still being built.

The capsule system is not a replacement for full ION. It is the fallback and
basic-ops layer that lets one capable Codex carrier stay oriented, bounded,
evidence-aware, and recoverable across long work.

## Operating Split

```text
Full ION
-> user-facing Persona chat
-> Relay / Steward / role workflow
-> Codex CLI bounded worker packets
-> proof gates
-> Steward integration
-> receipts and next context

Capsule ION
-> one Codex carrier
-> Capsule as minimum working context
-> Mini as pasteable lookup/receipt brief
-> explicit mode declaration
-> bounded plan / work / verification
-> capsule post receipt
```

The full path remains the target architecture. The capsule path preserves useful
work when full orchestration, UI, agents, actions, or services are incomplete,
blocked, or too heavy for the current step.

## Context Stack

Codex must treat these as the natural starting stack for serious ION work:

1. Active root proof: `pyproject.toml` and `ION/REPO_AUTHORITY.md`.
2. `ION/05_context/current/codex_solo/HOT_CONTEXT.md`.
3. `ION/05_context/current/codex_solo/CAPSULE.md`.
4. `ION/05_context/current/codex_solo/MINI.md`.
5. The active workpacket, protocol, test, or source files for the task.

`CAPSULE.md` is the minimum working context. `MINI.md` is the pasteable
operator-visible lookup brief and receipt index. Neither outranks current repo
authority, explicit operator instruction, test evidence, or proof receipts.

## Required Mode Declaration

Before material action, Codex should name the current mode:

```text
RESEARCH: read and map evidence only.
PLAN: produce an executable orchestration without editing.
IMPLEMENT: edit bounded files according to approved plan.
VERIFY: run focused checks and inspect proof.
SETTLE: summarize result, blockers, receipts, and next state.
RECOVER: repair drift, wrong-root risk, failed context, or confusion.
```

If the operator has forbidden coding, the mode must remain `RESEARCH`, `PLAN`,
or `RECOVER` until approval changes that boundary.

## Small ION Loop

For long multi-step work, Codex should run this loop:

1. Mount: confirm active root and read the capsule context stack.
2. Interpret: restate the real user objective and the ION boundary.
3. Plan: name files, risks, tests, and stop conditions.
4. Execute: do one bounded work slice at a time.
5. Verify: run focused tests or evidence checks proportional to risk.
6. Settle: report changed paths, validation, blockers, and next move.
7. Receipt: after material work, append one capsule post.

The operator should not have to manually drive internal queues, pins, lanes, or
workflow plumbing. UI surfaces may expose those as evidence and control panels,
but the primary product behavior is still normal user chat with a useful AI
response.

## Drift Rules

Codex must enter `RECOVER` mode when any of these occur:

- active root is unclear or points outside `/home/sev/ION - Production/ION_CODEX FULL`;
- a UI/control plan starts replacing the actual chat/product behavior;
- internal ION concepts are exposed as required user chores;
- Codex cannot explain why a file or control belongs to the requested product;
- a prior capsule row claims success that operator feedback has disproven;
- an action, MCP, Custom GPT, or worker return conflicts with local repo evidence.

Recovery means stop broad implementation, map the evidence, identify the bad
assumption, and propose a correction before continuing.

## Custom GPT Helpers

Custom GPTs and Actions may assist Codex by running read/status/proof checks,
calling ION gateway or MCP surfaces, and returning structured witness output.

Their output is evidence, not automatic state. Codex may rely on it only after
checking authority, timestamp, path/root, and whether the helper performed a
read-only, validation-only, or mutating action.

Useful helper roles:

```text
ION Custom GPT
-> read policy, context, queue, receipts, MCP status, and action validation

ION MCP JSON-RPC Action
-> read/status tools and bounded queue/receipt tools

Codex local carrier
-> source edits, tests, local verification, capsule posts
```

Both the GPT Action lane and MCP lane must route into the same ION owners. They
must not create parallel truth, a second queue, or a second agent system.

## Product Guardrail

For the ION Codex CLI app, the first acceptance criterion is not a cockpit panel.
It is:

```text
The user types a normal message into a chat.
The system returns a useful assistant response.
The response is visibly grounded in the correct lane:
  - full ION chat through Persona / Relay / Steward boundaries, or
  - Codex solo chat through Capsule / Mini / HOT_CONTEXT.
Evidence, queues, receipts, agents, and model routes are visible as support,
not forced manual workflow chores.
```

Any UI that records turns without producing assistant responses is not the target
chat product. It may be a projection or debug surface only.

## Capsule Receipt Rule

After material work, Codex should record one capsule post with:

```text
summary: one short completed-work sentence
evidence: changed files, tests, receipts, or protocols
status: IMPLEMENTED, CORRECTED, VERIFIED, BLOCKED, or RECOVERY
next_action: the next operator-relevant step
```

Do not update the capsule for every ordinary message. Update it when a work unit,
correction, proof, or important decision needs to survive context loss.

## Non-Claims

This protocol does not grant ION identity, Steward authority, Relay authority,
Persona authority, production authority, live execution authority, secrets
authority, deployment authority, git-push authority, or permission to work in a
different ION root without operator approval.
