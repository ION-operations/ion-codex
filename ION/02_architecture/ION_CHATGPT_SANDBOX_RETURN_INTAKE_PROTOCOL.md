---
type: protocol
authority: A3_IMPLEMENTATION
status: DRAFT_NON_PRODUCTION
created: 2026-05-05
production_authority: false
live_execution_authority: false
---

# ION ChatGPT Sandbox Return Intake Protocol

This protocol defines how Sev/ChatGPT Browser may return sandbox-produced work
to local ION for review.

It is not ION law, not production authority, and not direct patch authority.
It is a bounded implementation lane under the existing ION proof and receipt
model.

## Core Rule

```text
ChatGPT sandbox output is inbox evidence, not accepted state.
```

A sandbox return may contain a summary, manifest, patch, validation notes, and
optional full-file overlays. It must land under:

```text
ION/05_context/inbox/chatgpt_sandbox_returns/<return_id>/
```

No sandbox endpoint may patch live source, delete files, push git, access
credentials, deploy production, or accept worker output directly into state.

## Return Identity

Return IDs use:

```text
sev-YYYYMMDD-HHMMSS-<short-slug>
```

Example:

```text
sev-20260505-041500-chatops-ui-return
```

Each return ID is immutable after registration. Duplicate IDs are blocked.

## Required Files

Every committed return must contain:

```text
SANDBOX_RETURN_MANIFEST.json
SUMMARY.md
```

Preferred code-change evidence:

```text
PATCH.diff
```

Optional overlay material may appear under:

```text
files/<repo-relative-path>
```

Overlay files are review material only and never apply themselves.

## Manifest Commitments

The manifest schema is:

```text
ion.chatgpt_sandbox_return.v1
```

It must record:

- `return_id`
- authoring carrier `Sev` / `chatgpt_browser` / `sandbox: true`
- human sovereign `Braden`
- source snapshot package path and sha256 when known
- expected archive root markers `pyproject.toml` and `ION/REPO_AUTHORITY.md`
- changed paths
- sandbox validation claims
- requested receipts
- `production_authority: false`
- `live_execution_authority: false`
- `direct_apply_authority: false`
- `git_push_authority: false`

## Active Queue

The active projection lives at:

```text
ION/05_context/current/ACTIVE_CHATGPT_SANDBOX_RETURN_QUEUE.json
```

Queue statuses:

```text
RETURN_DRAFT_WRITTEN
RETURN_COMMITTED_FOR_REVIEW
DIFF_PREVIEW_READY
CODEX_REVIEW_QUEUED
CODEX_REVIEW_RUNNING
RETURN_REVIEW_ACCEPTED
RETURN_REVIEW_BLOCKED
SUPERSEDED_BY_NEW_BASE
```

## Kernel Owner

The implementation owner is:

```text
ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py
```

The owner provides:

```text
register_sandbox_return
write_sandbox_return_file
commit_sandbox_return
build_sandbox_return_diff_preview
queue_sandbox_return_codex_review
build_sandbox_return_queue_projection
```

## ChatOps Daemon Surface

The local daemon may expose bounded endpoints:

```text
GET  /sandbox/returns
GET  /sandbox/returns/{return_id}
POST /sandbox/returns/register
POST /sandbox/returns/file
POST /sandbox/returns/commit
POST /sandbox/returns/diff-preview
POST /sandbox/returns/queue-review
```

All mutating endpoints require Braden approval through the daemon operation
approval gate.

## Review Path

Diff preview may run read-only commands such as:

```bash
git apply --check ION/05_context/inbox/chatgpt_sandbox_returns/<return_id>/PATCH.diff
git apply --stat ION/05_context/inbox/chatgpt_sandbox_returns/<return_id>/PATCH.diff
```

If a patch must be tested, apply it only in a temporary review root. Live source
patching remains outside this protocol.

## Failure Classes

Use existing ChatOps/ION failure classes where possible:

```text
CHATOPS_SCHEMA_FAILURE
USER_APPROVAL_REJECTED
LOCAL_DAEMON_FAILURE
ION_PACKET_WRITE_FAILURE
CODEX_BACKEND_FAILURE
CARRIER_ADAPTER_FAILURE
ION_CORE_FAILURE
POLICY_BLOCK_WORKING_AS_DESIGNED
```

Missing or malformed sandbox return material is normally
`POLICY_BLOCK_WORKING_AS_DESIGNED`, not `ION_CORE_FAILURE`.
