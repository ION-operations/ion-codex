---
type: protocol_stub
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-04
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION GitHub Work Daemon Protocol

## Purpose

This protocol defines a future local GitHub work daemon as a thin adapter over
existing ION owners. It must not create a second agent system, second queue, or
second authority layer.

The daemon watches/syncs the GitHub data plane and translates eligible work into
existing ION queues, receipts, and proof gates:

```text
GitHub issue/branch/PR/artifact refs
-> ION work packet or carrier message
-> existing Codex queue runner / agent invocation broker
-> proof-gated task return
-> ION receipt
-> optional GitHub issue/PR comment by policy-approved adapter
```

## Existing Owners Reused

- Codex work queue:
  `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json`
- Work request packets:
  `ION/05_context/current/chatgpt_connector/codex_work_requests/`
- Queue runner:
  `ION/04_packages/kernel/ion_codex_queue_runner.py`
- Agent invocation broker:
  `ION/04_packages/kernel/ion_agent_invocation_broker.py`
- Carrier messages:
  `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json`
- Task returns:
  `ION/05_context/current/chatgpt_connector/task_returns/`
- Proof gates:
  `kernel.ion_context_proof_gate` and `kernel.ion_template_action_gate`
- Full-carrier MCP parity:
  `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md`
- GitHub data-plane prior-art consolidation:
  `ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md`

## Prior-Art Reuse

The daemon is the consolidation target for older GitHub-agent ideas. It is not a
new authority layer.

Reusable patterns:

- CodexGit read-only status reporting becomes the first audit slice.
- CodexGit scoped staging, staged diff proof, validation proof, and rollback
  notes become commit proposal receipt fields.
- Release slicing and git hygiene packets become exclude-by-default policy for
  generated outputs, runtime state, local vaults, logs, caches, and accidental
  gitlinks.
- SOS Git Chronicler provenance fields become optional receipt and commit
  metadata fields after human approval.
- Older commit-as-evidence stubs become a future ION receipt mapping for commit
  refs, not a direct code dependency.

Rejected patterns:

- no token paste, token file reads, or credential storage;
- no secret-scanning bypass as normal workflow;
- no non-volitional autonomous commits in the first daemon slice;
- no separate GitHub agent queue beside the existing ION queues.

## Daemon Posture

The GitHub work daemon is non-production and disabled by default. It may only
run after a human has initialized local git and authenticated GitHub outside
ION. It must never store tokens in ION files.

Status classes:

```text
NOT_CONFIGURED
CONFIGURED_NOT_RUNNING
DRY_RUN_READY
WATCHING_READ_ONLY
IMPORTING_TO_ION_QUEUE
BLOCKED_REQUIRES_HUMAN_AUTH
BLOCKED_POLICY
```

Failure classes:

```text
GITHUB_DATA_PLANE_NOT_CONFIGURED
GITHUB_AUTH_UNAVAILABLE
GIT_WORKTREE_DIRTY_OR_UNSAFE
GIT_SECRET_SCAN_BLOCK
CARRIER_ADAPTER_FAILURE
DAEMON_FAILURE
ION_CORE_FAILURE
```

## Minimum Read-Only Loop

The first daemon slice should only inspect and report:

1. confirm local `.git` exists at the ION shell root;
2. confirm `origin` points to `git@github.com:ION-operations/ion-codex.git`
   or `https://github.com/ION-operations/ion-codex.git`;
3. list open issues or a configured project board only if GitHub auth is
   already available to the local operator environment;
4. map issue refs to proposed ION work packets without writing them;
5. emit a dry-run receipt under the existing runtime/receipt surface.

It should be implemented as `kernel.ion_github_data_plane_audit` before any
daemon loop is started. The audit should be callable by tests and future MCP
status tools without requiring network access.

## First Write Loop

Only after the dry-run loop is accepted:

1. import a GitHub issue marked `ion:queue` into
   `codex_work_requests/` as a `QUEUED_FOR_CODEX_CARRIER` packet;
2. record issue URL, branch hint, labels, and artifact refs inside the packet;
3. let `ion_codex_queue_process_once` or `ion_swarm_step_once` process it;
4. submit the result through `ion_submit_task_return`;
5. record the task-return path and validation result in a daemon receipt.

The daemon must not merge PRs, push branches, close issues, or mutate GitHub
state until a later human-approved adapter explicitly authorizes those actions.

## Commit Proposal Mode

Commit proposal mode is separate from daemon watch mode. It may prepare evidence
for review, but it must not run `git commit` or `git push` unless the current
packet and runtime policy explicitly grant that action.

The first implementation is the non-authorizing local kernel receipt:

```text
ION/04_packages/kernel/ion_github_commit_proposal_receipt.py
```

It writes proposal and path-manifest artifacts under
`ION/05_context/current/github_data_plane/commit_proposals/` and keeps
`commit_authority: false` and `push_authority: false`.

Required fields:

- requested actor or carrier;
- packet path or issue URL;
- exact path scope;
- staged diff stat;
- validation commands;
- secret scan status;
- rollback method;
- receipt path;
- ION runtime policy authorization status.

If secret scanning finds a current-tree, staged-diff, or history issue, classify
the result as `GIT_SECRET_SCAN_BLOCK` and stop.

## Runtime Commit And Push Mode

Git push is a target data-plane runtime capability, not a permanent human relay
step. The daemon may eventually commit and push without per-push human approval
only after a dedicated ION runtime push authority profile exists.

Required controls:

- allowed remotes and branch patterns;
- default branch patterns: `work/*`, `docs/*`, `agent/*`, and `data-plane/*`;
- no automatic push directly to `main`;
- `main` updates only through PR/merge gate or a later explicit release
  authority;
- exact packet or receipt reference;
- exact staged path scope;
- no unrelated staged paths;
- validation pass evidence;
- current-tree and staged-diff secret scan pass evidence;
- rollback method, normally `git revert <commit>`;
- commit SHA and push result receipt;
- failure classification for every blocked push.

This mode is still not production deployment authority, merge authority, repo
settings authority, force-push authority, or arbitrary shell authority.

## GitHub Comment Backflow

GitHub comments generated by ION are optional and gated. If implemented, the
comment must contain only:

- receipt path;
- validation summary;
- current status;
- next human action.

It must not include secrets, full private logs, or unproofed worker output.

## Heartbeat And Receipts

Each daemon step must write a receipt with:

- daemon status;
- root path;
- git remote and branch;
- issue/PR refs considered;
- packet paths created or proposed;
- command/tool invoked;
- validation result;
- stop reason;
- failure classification.

## Non-Goals

- no autonomous production deployment;
- no raw shell bridge exposed through MCP;
- no hidden GitHub token management;
- no duplicate work queue;
- no direct acceptance of raw Codex output;
- no merge, close, label-edit, or repo-setting mutation without explicit
  higher-authority action;
- no commit or push until the ION runtime push authority profile is implemented
  and mounted.
