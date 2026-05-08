---
type: protocol_stub
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-04
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION GitHub Data-Plane Protocol

## Purpose

This protocol defines the first bounded GitHub data-plane setup for ION. MCP
remains the control plane: carriers call ION tools, create work packets, submit
task returns, and receive status through the existing MCP connector. GitHub and
local git become a durable data plane for large specs, patches, branches, pull
requests, issues, artifacts, and review history.

This draft does not authorize secret handling, GitHub authentication edits,
production deployment, direct merge, or arbitrary shell. It also does not grant
default ad hoc push authority to every carrier. The target architecture is that
`git commit` and `git push` become ION runtime capabilities through a dedicated
GitHub work daemon profile, policy gates, receipts, rollback proof, and scoped
authority, not a permanent human relay step.

## Current Evidence

Earlier ChatGPT Browser MCP connector evidence reported:

```text
ion_git_status_summary.git_present: false
```

That evidence was superseded on 2026-05-04 after human-approved local setup.
The current shell root has an explicit local git repository rooted at:

```text
/home/sev/ION - Production/ION_CODEX
```

Current configured data-plane target:

```text
branch: main
remote: https://github.com/ION-operations/ion-codex.git
visibility: public collaboration repository
auth path: gh browser login with git credential helper
```

The initial public bootstrap push was completed on 2026-05-05 after explicit
operator authorization, exact path staging, validation, and secret-scan receipt
evidence. This bootstrap does not grant general `main` push authority. The next
push-capable slice must define ION runtime push authority with staged diff
proof, validation proof, secret scan proof, receipt capture, and rollback proof.
Future `main` updates should use the repository's branch and pull-request gate
unless a separate ION break-glass policy explicitly authorizes otherwise.

## Prior-Art Consolidation

Older GitHub and git-agent work exists in nearby ION-era workspaces. The current
consolidation artifact is:

```text
ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md
```

Reusable prior art:

- AIM-ION `CodexGit` agent docs define non-destructive git operations, scoped
  staging, branch hygiene, rollback notes, and required output evidence.
- AIM-ION `scripts/git/codexgit_status_report.py` provides a useful read-only
  worktree health report shape.
- AIM-ION release slicing and hygiene packets document exclude-by-default
  generated/runtime artifacts and dirty-tree triage.
- SOS `git_chronicler.py` and the Opus Git Chronicler spec provide provenance
  and commit-message ideas.
- Older `git_integration.py` stubs show commit refs as evidence records.

Rejected or constrained prior art:

- token-paste guidance from old GitHub auth docs is rejected;
- secret-scanning bypass guidance is retained only as an incident warning;
- autonomous non-volitional commit daemons are rejected for the first slice;
- old role names or sovereign language do not transfer authority into this
  repository.

## Repository Recommendation

Use one public collaboration repository under the GitHub account/org:

```text
ION-operations/ion-codex
```

Rationale:

- matches the current package root name without encoding local filesystem
  spaces;
- keeps ION code, architecture docs, registries, connector state, and receipts
  in one reviewable repository;
- allows outside users and AI collaborators to inspect, discuss, and contribute
  through public issues, branches, and pull requests;
- allows issues, branches, pull requests, and releases to carry artifact refs
  without using MCP message bodies as the durable storage layer.

Large binary artifacts should not be pasted through MCP. Store them as GitHub
release assets, Git LFS objects, or external artifact refs recorded in ION
receipts.

More perfected production builds, infrastructure configuration, deployment
state, credentials, and other sensitive operational surfaces may live in private
repositories later. Public collaboration status for this repo is not authority
to publish secrets, production credentials, private logs, or unsafe runtime
state.

## Plane Split

```text
MCP control plane:
  ion_status
  ion_tool_manifest
  ion_request_codex_work_packet
  ion_agent_invoke
  ion_codex_queue_process_once
  ion_submit_task_return
  receipts and cockpit/status tools

GitHub data plane:
  issues for durable work requests and human discussion
  branches for bounded implementation slices
  commits for file-level history
  pull requests for review and merge proposals
  releases/assets or LFS for large artifacts
  commit/PR/issue URLs recorded in ION receipts
```

## Local Git Init And Remote Plan

Human-only setup commands, from the ION shell root:

```bash
cd "/home/sev/ION - Production/ION_CODEX"
test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md
git init
git branch -M main
git status --short
```

Before the first commit, review `.gitignore` policy and decide whether runtime
logs, local tunnel state, and generated task-return receipts should be tracked
or selectively ignored. Do not add secrets, tokens, local credential files, or
private machine-specific config.

Remote creation and attachment were completed through human-supervised `gh`
browser login. Historical setup commands below are retained as setup reference,
not as proof that they still need to be run:

```bash
gh auth login --hostname github.com --git-protocol https --scopes repo
gh repo create ION-operations/ion-codex --public --description "ION Codex carrier workspace and data plane" --disable-wiki
git remote add origin https://github.com/ION-operations/ion-codex.git
git remote -v
```

Bootstrap option before runtime push authority exists:

```bash
git add pyproject.toml ION
git commit -m "Initialize ION Codex data plane"
git push -u origin main
```

If `gh` is unavailable, create the empty public repository in the GitHub UI
under `ION-operations`, then run only the `git remote add` and verification
commands above.

## Issue, Branch, And PR Workflow

1. Create a GitHub issue for each durable work stream. Include the ION work
   packet path, objective, authority boundaries, and receipt expectations.
2. Create a branch named from the issue and task class:
   `work/<issue-number>-short-slug` or `docs/<issue-number>-short-slug`.
3. Let MCP/Sev issue control-plane commands that create or process ION packets.
   Do not let GitHub comments bypass ION packet and proof gates.
4. Let Codex/local carriers make bounded local changes in the branch.
5. Record ION task returns and receipts before opening a pull request.
6. Open a PR with links to accepted ION receipts, validation commands, and any
   artifact refs.
7. Human/Steward review decides merge readiness. A PR is a merge proposal, not
   production authority.

## First Implementation Slices

Slice 0 is complete as local setup and bootstrap evidence:

- local git initialized;
- branch is `main`;
- public GitHub repository exists under `ION-operations/ion-codex`;
- `origin` points to `https://github.com/ION-operations/ion-codex.git`;
- GitHub CLI authentication was completed by browser login outside ION files.
- initial bootstrap commit `6edea5f9ad843ad8526c4272d07885fca8065217`
  was pushed to `origin/main` after gate checks.

Slice 1 should be read-only:

- add `kernel.ion_github_data_plane_audit`;
- port the safe parts of the historical CodexGit status report;
- report branch, remote, upstream, ahead/behind, staged, unstaged, untracked,
  conflict, and top path-bucket counts;
- emit `GITHUB_DATA_PLANE_NOT_CONFIGURED`, `GITHUB_AUTH_UNAVAILABLE`,
  `GIT_WORKTREE_DIRTY_OR_UNSAFE`, `CARRIER_ADAPTER_FAILURE`, or
  `ION_CORE_FAILURE` without exposing secrets.

Slice 2 adds non-authorizing commit proposal receipts through:

```text
ION/04_packages/kernel/ion_github_commit_proposal_receipt.py
ION/05_context/current/github_data_plane/commit_proposals/
```

The proposal receipt may enumerate the exact proposed path set, run a
redacting secret scan, record fixed validation evidence, and write a path
manifest. It does not stage, commit, push, mutate GitHub, or authorize the
operation by itself.

Commit proposal receipts must include:

- exact staged file set;
- validation commands and results;
- current-tree and staged-diff secret scan result;
- rollback method;
- explicit ION runtime policy authorization field.

Slice 3 should add GitHub issue dry-run import. It may read issue metadata if
local `gh` auth is available, but it must not enqueue, comment, close, label, or
push without a separate confirmation gate.

Slice 4 should add policy-gated commit/push execution:

- define an ION runtime git push authority profile;
- commit only exact staged path scopes tied to packets/receipts;
- push only to allowed remotes and branch patterns such as `work/*`, `docs/*`,
  `agent/*`, or `data-plane/*`;
- do not auto-push directly to `main`;
- update `main` only through the existing review/merge gate or a later
  explicitly mounted release authority;
- block on secret scan, validation failure, dirty unsafe state, or missing
  rollback proof;
- record commit SHA, branch, remote, receipt path, and failure class;
- keep production deployment and merge authority separate from data-plane push.

## Artifact References

Artifacts referenced from GitHub must have at least:

- stable URL or repository-relative path;
- sha256 when locally materialized;
- source carrier or human submitter;
- linked issue/PR/commit;
- ION receipt path;
- lifecycle status: draft, accepted, superseded, contained, or archived.

## Receipt Requirements

Every GitHub data-plane action that affects ION state should leave an ION
receipt or task return that records:

- action id;
- carrier id or human actor;
- issue/branch/PR/commit refs;
- files changed or artifacts referenced;
- validation commands;
- failure classification if blocked;
- next lawful move.

## Boundaries

- MCP is not replaced by GitHub.
- GitHub issues are not ION work packets until imported or referenced by an ION
  packet.
- GitHub comments are not Steward decisions.
- Pull requests are not merges until a human/Steward path approves them.
- No carrier may read, print, store, or request GitHub tokens.
- No carrier may push, merge, or alter repo settings by default. Push may become
  an ION runtime capability only through an explicit GitHub work daemon authority
  profile with receipts and policy gates. Automated push should target scoped
  work branches by default, not `main`. Merge and repo-setting mutation remain
  separate higher-authority actions.
