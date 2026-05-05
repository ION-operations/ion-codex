---
type: protocol_stub
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-05
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION Browser Carrier Runtime Protocol

## Purpose

The ION Browser Carrier Runtime is a carrier adapter for ChatGPT Browser. It
lets Sev emit strict action blocks in chat, lets a browser extension detect and
preview those blocks, and lets a localhost-only daemon write bounded ION
packets, drafts, and receipts after Braden approval.

It does not create a second ION identity, second work queue, or second authority
system. ION remains the core engine. Sev remains a browser carrier callsign.
The extension and daemon are transport adapters.

Core invariant: ION has one core engine mounted by all carriers. ChatGPT
Browser/Sev is a full ION carrier target, not an observer-only or
management-only lane. Runtime failures in this layer are carrier adapter,
transport, or capability failures unless proof shows an ION core failure.

## Architecture

```text
ChatGPT Browser / Sev text
-> browser extension parser and approval UI
-> localhost ChatOps daemon
-> ION packets, receipts, drafts, Codex queue, GitHub data-plane refs
-> Codex/local workers and existing proof gates
```

MCP remains useful for status and small live tool calls, but it is no longer the
only transport for durable work. Large content, fragile start calls, and
cross-chat continuity should flow through local files, GitHub refs, and
receipt-addressed packets.

## Owners

- Browser extension scaffold:
  `ION/09_integrations/browser_extension/ion_chatops_bridge/`
- Local daemon wrapper:
  `ION/09_integrations/local_daemon/ion_chatops_bridge/`
- Kernel implementation:
  `ION/04_packages/kernel/ion_chatops_bridge.py`
- Action schema:
  `ION/03_registry/ion_chatops_action.schema.yaml`
- Extension policy:
  `ION/03_registry/ion_chatops_extension_policy.yaml`
- Local daemon policy:
  `ION/03_registry/ion_chatops_local_daemon_policy.yaml`
- Actions:
  `ION/05_context/current/chatops_bridge/actions/`
- Receipts:
  `ION/05_context/current/chatops_bridge/receipts/`
- Runtime state:
  `ION/05_context/current/chatops_bridge/runtime/`
- Artifacts:
  `ION/05_context/current/chatops_bridge/artifacts/`

## Authority Boundaries

- Braden is the human sovereign/source authority.
- Sev is a delegated browser control-plane carrier.
- The browser extension parses, previews, and transports action packets.
- The local daemon validates, writes bounded artifacts, and emits receipts.
- The daemon does not decide authority by itself.
- Raw Codex/local output still requires existing ION proof gates and Steward
  integration before it becomes accepted project truth.

## MVP Intents

The first runtime slice supports only:

```text
register_artifact
write_file_draft
create_codex_work_packet
create_github_issue_draft
```

These are deliberately bounded. They create files, packets, drafts, and
receipts. They do not run arbitrary shell, delete files, push git, deploy
production, or access credentials.

## Local Daemon

The daemon must listen only on loopback:

```text
127.0.0.1:8767
```

Initial endpoints:

```text
GET  /health
GET  /policy
GET  /context/sev/onboarding
GET  /agent/status
GET  /agent/queue
GET  /exports/context-pack
POST /actions/validate
POST /actions/submit
POST /agent/prepare-next
POST /agent/process-one
POST /exports/lifecycle-zip
POST /exports/safe-full-zip
GET  /actions/{action_id}
GET  /receipts/{receipt_id}
```

`/actions/submit` requires extension-side approval evidence. The MVP approval
token is a local ceremony field, not a secret:

```text
ION_CHATOPS_APPROVED
```

## Agent And Export Surfaces

The browser extension may project a local cockpit for Sev and Braden, but the
cockpit must reuse existing ION owners:

- Codex-backed agent queue/status/prepare/start operations use
  `ION/04_packages/kernel/ion_codex_queue_runner.py`.
- Context-pack and ZIP export operations use existing package owners:
  `ION/04_packages/kernel/ion_lifecycle_packager.py` and
  `ION/04_packages/kernel/ion_safe_full_project_packager.py`.
- Mutating agent/export operations require Braden approval and emit
  `ion.chatops.bridge_operation_receipt.v1` receipts under
  `ION/05_context/current/chatops_bridge/receipts/`.

`/agent/prepare-next` creates a prepared Codex run packet and context receipt
without starting Codex. `/agent/process-one` may start one bounded queue-runner
worker only after approval. Neither endpoint grants broad shell authority, git
push authority, production authority, credential authority, or direct Steward
integration authority.

## Branch And Git Policy

The ChatOps runtime does not push git in the MVP. Later commit/push support must
reuse the GitHub data-plane policy:

```yaml
main_auto_push_allowed: false
scoped_branch_push_allowed: policy_gated
allowed_branch_prefixes:
  - work/
  - docs/
  - agent/
  - data-plane/
  - sev/
```

`main` updates only through a PR/merge gate or explicit release authority.

## Receipt Rule

Every accepted, rejected, completed, or failed daemon action emits a receipt.
Receipts must record actor, approval, intent, target refs, files touched,
validation, and failure classification.

## Non-Goals

- no production deployment;
- no direct shell bridge;
- no direct delete;
- no credential access;
- no push to `main`;
- no bypass of ION task-return or Steward integration gates;
- no duplicate ION identity, queue, or authority system.
