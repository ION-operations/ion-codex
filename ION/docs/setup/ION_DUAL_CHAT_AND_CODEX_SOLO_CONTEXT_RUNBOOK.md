---
type: runbook
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# ION Codex Capsule Chat And Solo Context Runbook

## Purpose

Expose one primary operator chat:

- Codex Capsule Chat: standalone Codex engineering chat backed by Capsule as the minimum working context and Mini as a lookup/receipt index.

The existing full ION Relay / Steward / Vizier / Mason-Codex / Vice / Nemesis /
Relay return / Persona path remains the full workflow system. The Capsule chat
does not replace it and does not create a second ION queue or agent system. It
communicates with full ION through existing comms, queue, and receipt owners.

The Capsule chat is intentionally simpler than the full ION workflow. It uses
the old SOS-style single-agent pattern with current ION guardrails. In the
evolved form, the AI should always carry the active Capsule at minimum. Mini is
also posted into chat when it materially changes so the operator can see the
capsule brief directly; Mini remains a receipt/summary lookup surface, not repo
law.

## Local URLs

```text
Cockpit:
http://127.0.0.1:8788/cockpit

Codex Capsule chat:
http://127.0.0.1:8788/chat

Codex Capsule chat model:
http://127.0.0.1:8788/chat/model.json
```

## Public URL

When the PC is on, the MCP preview service and Cloudflare tunnel are running:

```text
https://ion.helixion.net/cockpit/login
https://ion.helixion.net/cockpit/chat
```

The public route is guarded by signed cockpit sessions. A session can be created by permission token or, when configured, Google login.

Required baseline env:

```text
ION_COCKPIT_PUBLIC_TOKEN=<bootstrap permission token>
ION_COCKPIT_SESSION_SECRET=<long random signing secret>
```

Optional invite and Google env:

```text
ION_COCKPIT_INVITE_TOKENS=friend=<long random token>,other=<long random token>
ION_GOOGLE_OAUTH_CLIENT_ID=<google oauth client id>
ION_GOOGLE_OAUTH_CLIENT_SECRET=<google oauth client secret>
ION_GOOGLE_OAUTH_REDIRECT_URI=https://ion.helixion.net/cockpit/auth/google/callback
ION_COCKPIT_ALLOWED_GOOGLE_EMAILS=sev@example.com,other@example.com
```

## Codex Solo Context Files

```text
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/ROUTE.json
ION/05_context/current/codex_solo/STATUS.json
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/LONG_HORIZON.json
ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
ION/05_context/current/codex_solo/history/
```

Rules:

- `CAPSULE.md` is the minimum working context for the General Codex lane.
- `MINI.md` stays at 30 lines or less and acts as lookup/receipt index only.
- `CAPSULE.md` stays append-only and terse.
- `LONG_HORIZON.json` groups older capsule rows into compressed epochs.
- `CONTEXT_PACKAGES.json` declares which package types are available: capsule, Mini index, long horizon, active authority, mission, route-depth, evidence/receipt, and recovery.
- `ROUTE.json` is machine-readable and must validate before queueing Codex work.
- `HOT_CONTEXT.md` is generated with Capsule first, then Mini lookup index, then long-horizon index, package selector, and explicit route files.
- Mini/Capsule is witness continuity, not repo law.

## Codex CLI Project Setup

Project-scoped Codex setup lives under:

```text
.codex/config.toml
.codex/hooks/ion_session_start_context.py
```

This is a Codex adapter convenience only. It does not revive root `AGENTS.md` as ION authority. Active ION authority remains `ION/REPO_AUTHORITY.md`, the mount contract, carrier profiles, carrier templates, active packets, and receipts.

On Codex session start, the project hook emits bounded developer context compiled from `ION/05_context/current/codex_solo/HOT_CONTEXT.md`. The hook is read-only and fails soft if Codex is not running inside `/home/sev/ION - Production/ION_CODEX FULL`.

Useful commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_solo_context --ion-root . status --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_solo_context --ion-root . boot-context --max-bytes 24000
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_solo_context --ion-root . post --summary "<work summary>" --evidence "ION/path" --status IMPLEMENTED --confirmation ION_BOUNDED_WRITE_CONFIRMED --json
```

The `post` command is for material work receipts, not every conversational turn.

## Rolling Windows

The current solo lane keeps a small active window and routes deeper by index:

```text
Capsule active working window: 80 lines
Mini lookup window: 5 recent capsule rows
Long-horizon epoch size: 10 capsule rows
Hot-context long-horizon window: 6 recent epochs
Route excerpt window: 1600 chars per routed file
```

The full capsule remains durable on disk. Older continuity should be reached through `LONG_HORIZON.json` and named evidence paths, not by loading the entire capsule into every prompt.

## Queue Behavior

When the Codex Capsule Chat routes bounded Codex work, the queue packet is prefixed with:

- the Codex solo witness policy,
- the active `CAPSULE.md` as minimum context,
- the `LONG_HORIZON.json` epoch index,
- the `CONTEXT_PACKAGES.json` package selector,
- the active-root boundary,
- the generated `HOT_CONTEXT.md`,
- required route references,
- the selected Codex CLI model move,
- the operator objective.

If required route files are missing, the queue action is blocked before the connector is called.

## Codex CLI Model Moves

Model-move policy lives in:

```text
ION/03_registry/codex_cli_model_move_policy.yaml
ION/04_packages/kernel/ion_codex_model_moves.py
```

Default posture is `conserve_main_bank`:

- Spark (`gpt-5.3-codex-spark`) handles low-risk intake, status, smoke, and classification work.
- Codex (`gpt-5.3-codex`) handles normal implementation and code review.
- GPT-5.5 handles Steward/Vizier/Vice authority, architecture, high-risk review, and user-facing synthesis.

Usage pool labels are advisory and operator-observed until verified in the account/provider surface. Every queued work link and Codex queue run records `selected_model`, `selected_reasoning_effort`, `usage_pool_id`, `work_class`, and `ion_stage_id`.

Useful command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_model_moves --ion-root . --lane-id codex_general --objective "Implement focused fix" --json
```

## Mini Auto-Post

`MINI.md` is hashed whenever the Codex Capsule chat model is refreshed with write enabled. If the hash changes, the chat app appends an `ion_context` turn of kind `mini_auto_post` to the primary Codex chat. This makes the Mini brief visible to the user without promoting it to authority or accepting any state by itself.

## ION Comms Adapter

The UI may expose an ION comms drawer for bounded notes into the existing full
ION workflow. This drawer is secondary. It must not become the main user
experience, and it must not create a second ION chat infrastructure. Full ION
communication remains owned by the existing Relay/Steward/workflow queues and
receipts.

## Chat Execution Bridge

The primary chat endpoint is still:

```text
POST /chat/turn
```

The same endpoint accepts `execution_mode`:

```text
respond_only
queue_for_codex
queue_and_start
```

Default is `respond_only`, controlled by:

```text
ION_CODEX_CAPSULE_CHAT_DEFAULT_EXECUTION_MODE=respond_only
```

`queue_for_codex` routes the chat message into the existing
`ion_request_codex_work_packet` owner and appends an execution-status turn back
into the same chat.

`queue_and_start` is disabled unless this env var is set:

```text
ION_CODEX_CAPSULE_CHAT_ALLOW_RUNNER_START=1
```

Without that env, the app may queue the packet but must refuse runner start and
show the refusal as chat status. This keeps a normal chat UX while preserving
the existing Codex queue/proof gates.

## Chat Response Carrier

Normal `respond_only` chat turns can use the Codex CLI response carrier when
explicitly enabled:

```text
ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED=1
ION_CODEX_CHAT_RESPONSE_CARRIER_TIMEOUT_SECONDS=240
ION_CODEX_CHAT_RESPONSE_CARRIER_CAPTURE_JSON=1
ION_CODEX_CHAT_RESPONSE_CARRIER_SANDBOX=workspace-write
```

The response carrier stores run artifacts under:

```text
ION/05_context/current/codex_capsule_chat/response_runs/
```

The carrier is response-only. Implementation work still belongs in
`queue_for_codex` / the existing proof-gated Codex work queue. The response
carrier uses Codex CLI, not direct Python provider API calls, and records prompt,
stdout, stderr, event, final-message, model-move, skill, native-lens, and drift
status artifacts.

This local Codex CLI build could not initialize a nested session under
`--sandbox read-only`, so the configured fallback is `workspace-write` plus a
no-write prompt contract and before/after `git status --short` drift detection.

## Isolation Rule

Capsule context is opt-in for the Codex Capsule chat/profile. Do not globally
inject Capsule into every Codex CLI instance. ION worker packets and full ION
agents must keep their own context contracts unless they explicitly route
through the Capsule profile.

## Service Notes

Local cockpit service:

```text
ion-cockpit-app.service
```

Public MCP/cockpit service:

```text
ion-mcp-preview.service
```

To enable public cockpit access, add a user-service override for the MCP preview service:

```ini
[Service]
Environment=ION_COCKPIT_PUBLIC_TOKEN=<long-random-token>
Environment=ION_COCKPIT_SESSION_SECRET=<different-long-random-secret>
```

Then restart:

```text
systemctl --user restart ion-mcp-preview.service
```

Do not put the token in Git, docs, screenshots, or chat transcripts.
