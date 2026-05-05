---
type: planning_artifact
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-04
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# GitHub Agent Prior-Art Consolidation

## Purpose

This artifact consolidates older GitHub and git-agent work into the current ION
GitHub data-plane plan. It does not create a new agent system, grant push
authority, authorize production deployment, or weaken the current no-secret
boundary.

Current owner surfaces remain:

- `ION/02_architecture/ION_GITHUB_DATA_PLANE_PROTOCOL.md`
- `ION/02_architecture/ION_GITHUB_WORK_DAEMON_PROTOCOL.md`
- `ION/03_registry/ion_github_data_plane_registry.yaml`
- `ION/04_packages/kernel/ion_codex_queue_runner.py`
- `ION/04_packages/kernel/ion_agent_invocation_broker.py`
- `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json`
- `ION/05_context/current/chatgpt_connector/codex_work_requests/`
- `ION/05_context/current/chatgpt_connector/task_returns/`
- `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json`

## Prior Art Found

1. AIM-ION CodexGit agent docs:
   - `/home/sev/ION - Production/AIM-ION/docs/agents/CodexGit/README.md`
   - `/home/sev/ION - Production/AIM-ION/docs/agents/CodexGit/OPERATING_RUNBOOK.md`
   - `/home/sev/ION - Production/AIM-ION/docs/agents/CodexGit/REQUEST_TEMPLATE.md`

2. AIM-ION CodexGit tooling:
   - `/home/sev/ION - Production/AIM-ION/scripts/git/codexgit_status_report.py`
   - `/home/sev/ION - Production/AIM-ION/scripts/git/quintet_pre_commit_gate.py`
   - `/home/sev/ION - Production/AIM-ION/scripts/git/install_quintet_hook.py`

3. AIM-ION git hygiene and release planning:
   - `/home/sev/ION - Production/AIM-ION/docs/CODEXGIT_RELEASE_SLICING_PLAN_2026-03-03.md`
   - `/home/sev/ION - Production/AIM-ION/docs/GIT_HYGIENE_RECOVERY_PACKET_2026-03-04.md`
   - `/home/sev/ION - Production/AIM-ION/coordination/GIT_BACKUP_PLAN.md`

4. AIM-ION GitHub setup and incident notes:
   - `/home/sev/ION - Production/AIM-ION/archive/GITHUB_SETUP_INSTRUCTIONS.md`
   - `/home/sev/ION - Production/AIM-ION/archive/GITHUB_AUTH_ISSUE.md`
   - `/home/sev/ION - Production/AIM-ION/archive/GITHUB_PUSH_BLOCKED_SOLUTION.md`
   - `/home/sev/ION - Production/AIM-ION/archive/GITHUB_PUSH_FINAL_OPTIONS.md`

5. SOS Git Chronicler prior art:
   - `/home/sev/ION - Production/SOS-OPUS/04_packages/spawner/src/git_chronicler.py`
   - `/home/sev/ION - Production/SOS-OPUS/06_intelligence/opus_git_chronicler_spec.md`
   - duplicate copies under `SOS/` and `SOS-Gemini/`

6. Older ION git evidence stubs:
   - `/home/sev/ION - Production/Project-Gemini/ion-core/ion/git_integration.py`
   - `/home/sev/ION - Production/operation-victus/victus/ion/git_integration.py`

## Adopt, Adapt, Reject

| Prior-art surface | Decision | Current ION use |
| --- | --- | --- |
| CodexGit role posture | Adapt | Treat as a bounded git operations capability inside the GitHub work daemon, not as a separate authority. |
| `codexgit_status_report.py` | Adopt after port | Reuse the read-only branch/worktree/ahead-behind report shape for `kernel.ion_github_data_plane_audit`. |
| CodexGit scoped staging workflow | Adopt | Require exact file scope, staged diff proof, validation evidence, and rollback notes before any commit proposal. |
| CodexGit request template | Adapt | Convert to an ION action template or MCP request schema after the audit slice exists. |
| Release slicing plan | Adopt | Use explicit slices and exclude-by-default generated/runtime artifacts for first repository backup. |
| Git hygiene recovery packet | Adopt | Preserve decisions around generated outputs, runtime files, gitlinks, and staged-doc policy as human gates. |
| Quintet pre-commit gate | Adapt later | Useful as a policy-gate pattern, but not portable without AIM-specific package dependencies. |
| GitHub setup docs | Supersede | Current setup uses `gh` browser login and the `ION-operations/ion-codex` private repository. |
| GitHub auth issue docs | Reject token guidance | Do not request, print, store, or paste tokens. Use `gh auth login` or human-managed GitHub auth only. |
| GitHub secret scanning incident notes | Adopt as warning | Add pre-push secret/history checks; do not use secret-scanning bypass as normal workflow. |
| SOS Git Chronicler automatic commit daemon | Adapt cautiously | Preserve provenance metadata and commit-message structure as a receipt model; reject non-volitional autonomous commits for now. |
| Older `git_integration.py` stubs | Adapt concept only | Commit refs can become ION evidence records, but placeholder commit hashes and old imports are not reusable code. |

## Consolidated Architecture

The current system should not revive a separate "GitHub agent" beside ION.
Instead:

```text
Sev or human operator
-> MCP control plane or local Codex carrier
-> ION packet / agent invocation / carrier message
-> existing Codex queue runner or bounded GitHub work daemon adapter
-> proof-gated task return
-> ION receipt
-> optional git commit, branch, issue, or PR reference
```

GitHub is the durable data plane. MCP remains the control plane. Codex CLI and
other local carriers remain execution substrates. ION records which carrier,
role, backend, packet, receipt, branch, commit, issue, or PR did what.

## Narrow First Slice

The first implementation slice should be read-only and local:

1. Add `kernel.ion_github_data_plane_audit`.
2. Port the safe parts of `codexgit_status_report.py`.
3. Emit:
   - git present;
   - root path;
   - branch;
   - upstream/remote;
   - ahead/behind if available;
   - staged/unstaged/untracked/conflict counts;
   - top path buckets;
   - ignored secret/runtime file policy status;
   - failure class.
4. Add focused tests for:
   - non-git root;
   - clean initialized repo;
   - dirty repo parsing;
   - no token or secret output.
5. Expose the audit through current status/registry first, not through push or
   GitHub mutation tools.

This creates a safe foundation for later commit, issue, branch, PR, and daemon
work without giving browser carriers arbitrary git or shell authority.

## Next Slices

1. Commit proposal receipt:
   - exact staged file set;
   - validation commands;
   - secret scan result;
   - rollback method;
   - human authorization field.

2. Pre-push guard:
   - current-tree secret scan;
   - staged diff secret scan;
   - optional history scan before first push;
   - branch policy: scoped work branches by default, no automatic direct push
     to `main`;
   - block with `GIT_SECRET_SCAN_BLOCK` if findings exist.

3. GitHub issue dry-run import:
   - read issue metadata only if `gh` auth is available;
   - map candidate issues to proposed ION work packets;
   - do not enqueue until a human or authorized carrier confirms.

4. GitHub issue import:
   - label-gated `ion:queue` issues become ION work packets;
   - all imported packet paths and issue URLs are receipted.

5. PR/comment backflow:
   - only post receipt summaries, validation status, and next action;
   - no secrets, raw logs, or unproofed worker output.

## Boundaries

- No git push, merge, force-push, tag, issue close, label edit, or repo setting
  mutation by default carrier authority.
- Runtime push authority should target scoped work branches first; `main` is
  updated through PR/merge gates or later explicit release authority.
- No GitHub token request, display, storage, or file read.
- No non-volitional commit daemon in the first slice.
- No duplicate ION work queue.
- No raw Codex output becomes state without existing proof gates.
- Secret-scanning bypasses are not a normal operating path.

## Planning Verdict

Prior GitHub-agent work exists and is useful, but it should be consolidated as a
GitHub data-plane and git-hygiene adapter under current ION owners. The next
lawful move is the read-only `ion_github_data_plane_audit` slice, followed by
commit proposal receipts and pre-push secret guards.
