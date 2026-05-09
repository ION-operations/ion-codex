# ION GitHub Custom GPT Actions + True IDE Workpack

**Workpack ID:** `ION-GITHUB-CUSTOM-GPT-IDE-WORKPACK-v0.1`  
**Date:** 2026-05-07  
**Carrier target:** Local Codex CLI / local ION development lane  
**Prepared for:** ION private Custom GPT + local operator-supervised runtime  
**Status:** Candidate workpack. Not accepted state until human/Steward review, local validation, and receipt.

---

## 0. Operator Intent

The operator wants ION’s private Custom GPT to access and operate against an ION GitHub repository, and to continue evolving toward a “true IDE” operating surface.

The important posture is:

- This is a private Custom GPT.
- The human operator is present, watching, approving, and able to stop actions.
- The workflow remains ION-governed: proof, receipts, bounded packets, approval gates, and clear authority.
- The system should not artificially limit itself because ordinary AI tool-access risks exist.
- The design should aim for real power, while expressing that power through ION’s careful workflow style.

The goal is not a toy GitHub integration.

The goal is an ION-controlled development environment where ChatGPT, local Codex CLI, GitHub, local files, receipts, tests, issues, PRs, and future IDE tools become one governed work loop.

---

## 1. Governing Principle

ION doctrine:

```text
AI output is not state.
ION is the law by which AI work becomes state.

No proof -> no landing.
No Steward/human acceptance -> no state.
No receipt/export -> no inheritance.
```

For GitHub and IDE integration:

```text
GitHub gives durable history.
ION gives authority.
The GPT proposes, inspects, drafts, queues, and coordinates.
The local runtime / gateway performs bounded actions.
The human / Steward accepts state.
Receipts make the result inheritable.
```

GitHub should be treated as a durable mirror and coordination plane, not the total source of truth for local ION state.

---

## 2. Source Notes

Relevant public docs checked during design:

- OpenAI Help: Configuring actions in GPTs  
  `https://help.openai.com/en/articles/9442513-configuring-actions-in-gpts`
- OpenAI Help: Creating and editing GPTs  
  `https://help.openai.com/en/articles/8554397-creating-and-editing-gpts`
- GitHub Docs: Authenticating to the REST API  
  `https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api`
- GitHub Docs: Fine-grained token permissions  
  `https://docs.github.com/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens`
- GitHub Docs: REST API endpoints for issues  
  `https://docs.github.com/rest/issues/issues`
- GitHub Docs: REST API endpoints for pull requests  
  `https://docs.github.com/en/rest/pulls/pulls`
- GitHub Docs: GitHub App installation access tokens and app permissions  
  `https://docs.github.com`

Relevant ION doctrine mount:

- `ION_Continuity_Substrate_Explainer_v7.md`

---

## 3. Primary Design Decision

Do **not** wire the Custom GPT directly to GitHub as the first-class authority surface.

Use:

```text
Custom GPT
  -> GPT Action OpenAPI schema
    -> ION Gateway API
      -> GitHub API
      -> local daemon / Codex queue when present
      -> receipt store
      -> policy / approval gate
```

This keeps power high while keeping the control point ION-shaped.

A direct GPT -> GitHub API connection is possible, but it is too flat:

```text
GPT output -> GitHub side effect
```

The better ION shape is:

```text
GPT output
-> bounded action packet
-> gateway validation
-> operator approval when required
-> GitHub/local side effect
-> proof return
-> receipt
-> next context package
```

---

## 4. Target System Shape

### 4.1 Components

```text
[Private Custom GPT]
  - user-facing reasoning and coordination
  - GPT Actions client
  - prepares bounded ION action packets
  - reads receipts and returns

[ION GitHub Gateway]
  - validates action schema
  - enforces repo allowlist
  - enforces operation policy
  - stores approval evidence
  - calls GitHub API
  - creates receipts
  - exposes status and proof

[GitHub]
  - durable mirror
  - issues
  - branches
  - PRs
  - code review trail
  - Actions / CI result surface

[Local ION Daemon / CLI Broker]
  - local filesystem truth
  - Codex CLI invocation
  - tests
  - diffs
  - package export/import
  - queue processing
  - receipts

[Codex CLI]
  - bounded local worker
  - reads context package
  - edits local files
  - runs tests
  - returns diff/proof

[Receipt Store]
  - JSON/Markdown receipts
  - decision records
  - validation results
  - next-session bootstrap
```

### 4.2 Preferred Control Flow

```text
1. User asks ION GPT to do development work.
2. GPT classifies the work into a bounded packet.
3. GPT calls gateway read/status actions if needed.
4. GPT drafts an action packet.
5. Gateway validates action packet and returns policy posture.
6. User approves if action mutates GitHub/local state.
7. Gateway performs mutation or queues Codex work.
8. Gateway returns proof.
9. GPT summarizes result and updates receipt candidate.
10. Receipt becomes inheritable only after acceptance/export.
```

---

## 5. Custom GPT Actions Reality

Custom GPT Actions are configured in the GPT editor with:

- An external API endpoint.
- Authentication configuration.
- An OpenAPI schema describing available operations.

The action should describe **ION operations**, not raw GitHub operations.

Bad shape:

```yaml
operationId: createGitHubBlob
operationId: updateReference
operationId: mergePullRequest
```

Better shape:

```yaml
operationId: ionGithubStatus
operationId: ionGithubReadFile
operationId: ionGithubDraftIssue
operationId: ionGithubCreateIssueWithApproval
operationId: ionGithubProposePatch
operationId: ionGithubOpenPullRequestWithApproval
operationId: ionRegisterReceipt
```

The GPT should be guided toward ION-level movement rather than raw side effects.

---

## 6. Authentication Strategy

### 6.1 v0: Server-Side Gateway Token

The Custom GPT authenticates to the ION Gateway using an API key or OAuth.

The gateway holds the GitHub credential server-side.

Pros:

- Simple.
- Keeps GitHub token out of GPT schema.
- Centralizes policy and logging.
- Easy to rotate.
- Easy to restrict to one repo/org.

Cons:

- Gateway is trusted infrastructure.
- Needs secure hosting and secret handling.

### 6.2 v1: GitHub App

Prefer a GitHub App once the integration matters.

Pros:

- Installation-scoped.
- Repo-scoped.
- Permission-scoped.
- Better audit posture.
- Better for org/repo evolution.

Cons:

- More setup.
- Requires app registration and installation token handling.

### 6.3 v1 Alternative: Fine-Grained PAT

A fine-grained PAT can work for an early private operator-supervised build.

Recommended scopes for initial lane:

```text
Repository metadata: read
Contents: read
Issues: write
Pull requests: write
Actions: read
Commit statuses/checks: read
```

Only add `Contents: write` when implementing branch/file mutation through the gateway.

Avoid:

```text
Administration
Secrets
Environments
Deployments write
Actions write
Main branch direct write
```

---

## 7. Authority Posture

The operator explicitly wants real power, not a neutered assistant.

So the posture is not “never mutate.”

The posture is:

```text
Mutate only through declared packets.
Mutate only on allowed surfaces.
Mutate only with proof.
Escalate or require approval at meaningful boundaries.
Record receipts.
Prefer branches/PRs over direct main changes.
Let the operator remain in the loop without burying them in friction.
```

### 7.1 Authority Classes

```text
A0_READ_ONLY
  - inspect repo/files/issues/PRs/status
  - no approval required

A1_DRAFT
  - draft issues/PRs/patches/receipts
  - no external mutation
  - no approval required

A2_COORDINATION_WRITE
  - create issues
  - comment on issues/PRs
  - label/assign if allowed
  - approval recommended or configurable

A3_BRANCH_WRITE
  - create branch
  - commit candidate file changes to branch
  - open PR
  - explicit approval required unless operator config marks as allowed

A4_LOCAL_EXECUTION
  - queue Codex
  - run tests
  - write local draft files
  - approval depends on local daemon policy

A5_HIGH_RISK
  - merge PR
  - deploy
  - delete branches
  - change secrets/settings
  - force push
  - never autonomous in v0/v1
```

### 7.2 “Private GPT + Operator Watching” Policy

Because the operator is present and this is a private GPT, the system may support a fast lane:

```text
operator_mode: supervised_private
default_read: allowed
default_draft: allowed
default_issue_create: allowed after inline approval
default_branch_create: allowed after inline approval
default_pr_open: allowed after inline approval
default_merge: blocked unless special explicit approval token
```

The gateway can require a simple approval evidence object:

```json
{
  "approved": true,
  "approved_by": "operator",
  "approval_token": "typed-human-approval-or-session-token",
  "scope": "create_issue|create_branch|open_pr|commit_branch"
}
```

---

## 8. v0 Action Surface

### 8.1 Status

```http
GET /ion/status
GET /ion/github/status
GET /ion/policy
```

Purpose:

- Verify gateway health.
- Verify GitHub connection.
- Verify repo allowlist.
- Verify current policy.
- Return non-claims and disabled capabilities.

### 8.2 Repo Read

```http
GET /ion/github/repos
GET /ion/github/{owner}/{repo}/tree
GET /ion/github/{owner}/{repo}/file?path=...
GET /ion/github/{owner}/{repo}/search?q=...
```

Purpose:

- Let GPT inspect live GitHub mirror.
- Build context without direct local package upload.
- Compare with local package if available.

### 8.3 Issues

```http
POST /ion/github/{owner}/{repo}/issues/draft
POST /ion/github/{owner}/{repo}/issues/create
POST /ion/github/{owner}/{repo}/issues/comment
```

Draft endpoint should not mutate GitHub.

Create/comment endpoints require approval evidence.

### 8.4 Pull Requests

```http
POST /ion/github/{owner}/{repo}/pulls/draft
POST /ion/github/{owner}/{repo}/pulls/create
GET  /ion/github/{owner}/{repo}/pulls/{number}
GET  /ion/github/{owner}/{repo}/pulls/{number}/checks
```

PR creation requires approval.

Merging is deliberately out of v0.

### 8.5 Branch and File Proposal

```http
POST /ion/github/{owner}/{repo}/branches/draft
POST /ion/github/{owner}/{repo}/branches/create
POST /ion/github/{owner}/{repo}/patches/propose
```

`patches/propose` should return a candidate patch payload, not apply it.

### 8.6 Receipts

```http
POST /ion/receipts/draft
POST /ion/receipts/register
GET  /ion/receipts/recent
GET  /ion/receipts/search?q=...
```

Receipts are not just logs. They should include:

```text
action_id
operator intent
context used
authority class
approval evidence
external mutation performed
GitHub URLs / SHAs / issue IDs / PR IDs
validation/proof
non-claims
next packet
```

---

## 9. v0 OpenAPI Skeleton

Codex should convert this into a real `openapi.yaml` after implementation choices are made.

```yaml
openapi: 3.1.0
info:
  title: ION GitHub Gateway
  version: 0.1.0
  description: Bounded ION gateway for Custom GPT access to GitHub and local development coordination.
servers:
  - url: https://ION_GATEWAY_HOST
security:
  - ApiKeyAuth: []

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-ION-Gateway-Key

  schemas:
    ApprovalEvidence:
      type: object
      required: [approved, approved_by, scope]
      properties:
        approved:
          type: boolean
        approved_by:
          type: string
        scope:
          type: string
        approval_token:
          type: string
        note:
          type: string

    IonReceipt:
      type: object
      properties:
        receipt_id:
          type: string
        action_id:
          type: string
        authority_class:
          type: string
        result:
          type: string
        proof:
          type: object
        non_claims:
          type: array
          items:
            type: string
        next_packet:
          type: string

paths:
  /ion/status:
    get:
      operationId: ionStatus
      summary: Read ION gateway status.
      responses:
        "200":
          description: Gateway status.

  /ion/github/status:
    get:
      operationId: ionGithubStatus
      summary: Read bounded GitHub connection status.
      responses:
        "200":
          description: GitHub status, repo allowlist, and capability posture.

  /ion/github/{owner}/{repo}/tree:
    get:
      operationId: ionGithubTree
      summary: Read repository tree for an allowlisted repo.
      parameters:
        - name: owner
          in: path
          required: true
          schema: { type: string }
        - name: repo
          in: path
          required: true
          schema: { type: string }
        - name: ref
          in: query
          required: false
          schema: { type: string }
      responses:
        "200":
          description: Repository tree.

  /ion/github/{owner}/{repo}/file:
    get:
      operationId: ionGithubReadFile
      summary: Read a file from an allowlisted repo.
      parameters:
        - name: owner
          in: path
          required: true
          schema: { type: string }
        - name: repo
          in: path
          required: true
          schema: { type: string }
        - name: path
          in: query
          required: true
          schema: { type: string }
        - name: ref
          in: query
          required: false
          schema: { type: string }
      responses:
        "200":
          description: File contents and metadata.

  /ion/github/{owner}/{repo}/issues/draft:
    post:
      operationId: ionGithubDraftIssue
      summary: Draft a GitHub issue without creating it.
      parameters:
        - name: owner
          in: path
          required: true
          schema: { type: string }
        - name: repo
          in: path
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title, body]
              properties:
                title: { type: string }
                body: { type: string }
                labels:
                  type: array
                  items: { type: string }
      responses:
        "200":
          description: Draft issue payload and receipt draft.

  /ion/github/{owner}/{repo}/issues/create:
    post:
      operationId: ionGithubCreateIssue
      summary: Create a GitHub issue with approval evidence.
      parameters:
        - name: owner
          in: path
          required: true
          schema: { type: string }
        - name: repo
          in: path
          required: true
          schema: { type: string }
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [title, body, approval]
              properties:
                title: { type: string }
                body: { type: string }
                labels:
                  type: array
                  items: { type: string }
                approval:
                  $ref: "#/components/schemas/ApprovalEvidence"
      responses:
        "200":
          description: Created issue plus ION receipt.

  /ion/receipts/register:
    post:
      operationId: ionRegisterReceipt
      summary: Register an ION receipt for an action result.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/IonReceipt"
      responses:
        "200":
          description: Registered receipt.
```

---

## 10. Gateway Implementation Sketch

### 10.1 Minimal Stack Options

Option A: Python FastAPI

```text
fastapi
uvicorn
pydantic
httpx
PyGithub or raw GitHub REST calls
python-dotenv
```

Option B: Node/TypeScript

```text
express or fastify
zod
octokit
dotenv
```

For ION, Python FastAPI is likely easiest if the local ION tooling is Python-heavy. TypeScript is attractive if the future cockpit/IDE surface is web-first.

### 10.2 Environment Variables

```bash
ION_GATEWAY_KEY=...
ION_ALLOWED_REPOS=owner/repo,owner/another-repo
GITHUB_APP_ID=...
GITHUB_APP_PRIVATE_KEY_PATH=...
GITHUB_INSTALLATION_ID=...
# or early v0:
GITHUB_TOKEN=...
ION_RECEIPT_ROOT=./ION/receipts/github_gateway
ION_POLICY_PATH=./ION/policy/github_gateway_policy.json
```

### 10.3 Policy File

```json
{
  "mode": "supervised_private",
  "allowed_repos": ["OWNER/ION_REPO"],
  "authority": {
    "read": "allow",
    "draft": "allow",
    "create_issue": "approval_required",
    "comment": "approval_required",
    "create_branch": "approval_required",
    "commit_branch": "approval_required",
    "open_pr": "approval_required",
    "merge_pr": "blocked",
    "repo_admin": "blocked",
    "secrets": "blocked",
    "deploy": "blocked"
  },
  "default_branch_protection": {
    "direct_main_write": false,
    "require_branch_for_file_writes": true,
    "require_receipt": true
  }
}
```

---

## 11. “True IDE” Vision

A true ION IDE is not just file editing.

It is a governed development cockpit where the GPT can perceive, reason, edit, test, route, queue, review, and receipt work across local and remote surfaces.

### 11.1 IDE Capability Domains

```text
1. Workspace perception
2. File read/write/edit
3. Semantic search
4. Symbol navigation
5. Diff management
6. Test execution
7. Terminal command execution
8. Git operations
9. GitHub operations
10. Task/packet queue
11. Agent/Codex invocation
12. Receipt and proof capture
13. Context package creation
14. Dependency/build management
15. Debugging support
16. Logs/runtime observation
17. UI preview/browser control
18. Documentation generation
19. Project ingestion/cartography
20. Release/deployment gating
```

### 11.2 Why This Is Different From Normal IDE AI

Normal AI IDE:

```text
read files
suggest edits
apply patch
run command
chat about it
```

ION IDE:

```text
mount context
classify domain
select template
perform bounded edit
run proof
register receipt
route next packet
preserve continuity
```

The “IDE” is not merely a coding UI. It is a state-transition environment for AI-mediated software work.

---

## 12. Tool Inventory For a True ION IDE

### 12.1 Workspace Mount Tools

Required:

```text
workspace_status()
tree_list(root, max_depth, filters)
file_read(path)
file_write_draft(path, content)
file_patch(path, diff)
file_metadata(path)
checksum(path)
```

ION-specific:

```text
mount_contract_read()
repo_authority_read()
active_packet_read()
continuity_bundle_read()
context_package_compile(packet_id)
```

### 12.2 Search and Context Tools

Required:

```text
file_search(query, roots, filters)
symbol_search(name)
references_search(symbol)
grep(pattern)
semantic_search(query)
```

ION-specific:

```text
context_node_search(query)
domain_map_read()
template_read(template_id)
receipt_search(query)
receipt_hydrate(receipt_id)
```

### 12.3 Edit and Diff Tools

Required:

```text
diff_current()
diff_file(path)
apply_patch(diff)
revert_patch(patch_id)
format_file(path)
```

ION-specific:

```text
candidate_delta_create(packet_id)
candidate_delta_validate(delta_id)
state_landing_request(delta_id)
receipt_create_for_delta(delta_id)
```

### 12.4 Execution Tools

Required:

```text
terminal_run(command, cwd, timeout)
test_run(selector)
lint_run()
typecheck_run()
build_run()
```

ION-specific:

```text
proof_gate_run(packet_id)
validation_bundle_create(packet_id)
execution_receipt_create(run_id)
```

### 12.5 Git Tools

Required:

```text
git_status()
git_diff()
git_branch_create(name)
git_checkout(ref)
git_commit(message)
git_log()
git_show(ref)
```

ION-specific:

```text
git_candidate_branch_create(packet_id)
git_commit_with_receipt(packet_id, receipt_id)
git_state_compare(local_ref, remote_ref)
```

### 12.6 GitHub Tools

Required:

```text
github_repo_status()
github_issue_create()
github_issue_comment()
github_pr_create()
github_pr_read()
github_pr_checks()
github_pr_comment()
```

ION-specific:

```text
github_action_validate()
github_pr_receipt_register()
github_issue_from_packet()
github_pr_from_candidate_delta()
```

### 12.7 Codex / Agent Tools

Required:

```text
codex_queue_status()
codex_work_packet_create()
codex_invoke(packet_id)
codex_result_read(invocation_id)
codex_cancel(invocation_id)
```

ION-specific:

```text
agent_spawn_plan(packet_id)
agent_result_settle(parent_packet_id)
fanout_branch_create(parent_packet_id)
settlement_receipt_create(parent_packet_id)
```

### 12.8 Runtime Observation Tools

Required:

```text
process_list()
service_status()
log_tail(service, lines)
http_probe(url)
browser_preview_status()
```

ION-specific:

```text
daemon_status()
gateway_status()
extension_status()
mcp_status()
carrier_status()
```

### 12.9 Project Ingestion Tools

Required:

```text
ingest_archive(path)
quarantine_tree_list()
root_integrity_check()
language_inventory()
dependency_inventory()
test_inventory()
entrypoint_inventory()
```

ION-specific:

```text
context_graph_genesis()
domain_partition_propose()
risk_classification()
starter_context_packages_create()
project_ingestion_receipt_create()
```

---

## 13. IDE Phases

### Phase 0: GitHub Read/Draft Gateway

Deliver:

```text
- Gateway service skeleton.
- OpenAPI schema.
- Status endpoint.
- GitHub repo read endpoint.
- File read endpoint.
- Issue draft endpoint.
- Receipt draft endpoint.
```

Validation:

```text
- Gateway starts locally.
- OpenAPI validates.
- GPT action imports schema.
- Status call works from GPT preview.
- GitHub file read works on allowlisted repo.
- No mutation endpoints enabled by default.
```

### Phase 1: GitHub Issue Creation With Approval

Deliver:

```text
- Issue create endpoint.
- ApprovalEvidence schema.
- Receipt registration.
- Policy enforcement.
```

Validation:

```text
- Rejected without approval evidence.
- Creates issue with approval evidence.
- Receipt records issue URL/ID.
```

### Phase 2: Branch + PR Candidate Flow

Deliver:

```text
- Branch create endpoint.
- Candidate patch representation.
- Optional commit-to-branch endpoint.
- PR draft/create endpoint.
```

Validation:

```text
- No direct main write.
- Branch name includes packet/action id.
- Commit message includes receipt id.
- PR body includes context/proof/non-claims.
```

### Phase 3: Local Codex Queue Integration

Deliver:

```text
- Gateway can create local Codex work packets.
- Codex queue status endpoint.
- Codex result read endpoint.
- Local receipt creation.
```

Validation:

```text
- Work packet created.
- Codex run is bounded.
- Diff and tests captured.
- Return is proposal, not accepted state.
```

### Phase 4: IDE Workbench Surface

Deliver:

```text
- Web cockpit or extension view.
- Current packet.
- Repo status.
- Diff viewer.
- Test results.
- Receipts.
- Approval controls.
- GitHub issue/PR links.
```

Validation:

```text
- Operator can see before approving.
- Approvals are attached to receipts.
- State-changing actions are visible and interruptible.
```

### Phase 5: True IDE Loop

Deliver:

```text
- File tree.
- Editor/diff view.
- Terminal/test runner.
- Git/GitHub control rail.
- Context package viewer.
- Agent/Codex queue.
- Receipt ledger.
- Packet scheduler.
```

Validation:

```text
- One packet can flow from intent -> context -> edit -> test -> PR -> receipt.
- Another session can resume from receipts and continuity bundle.
```

---

## 14. First Codex Implementation Packets

### Packet 1: Gateway Skeleton

```yaml
packet_id: ION-GITHUB-GATEWAY-001
objective: Create a minimal local ION GitHub Gateway service.
authority_class: A0_READ_ONLY + A1_DRAFT
target_paths:
  - tools/ion_github_gateway/
  - tools/ion_github_gateway/openapi.yaml
  - tools/ion_github_gateway/README.md
deliverables:
  - FastAPI or Node service
  - /ion/status
  - /ion/github/status
  - policy loader
  - repo allowlist config
  - no GitHub mutation
validation:
  - service starts
  - tests pass
  - openapi validates
  - README explains setup
non_claims:
  - no production deployment
  - no GitHub mutation
  - no Custom GPT installation yet
```

### Packet 2: GitHub Read Endpoints

```yaml
packet_id: ION-GITHUB-GATEWAY-002
objective: Add allowlisted GitHub repo tree and file read endpoints.
authority_class: A0_READ_ONLY
depends_on:
  - ION-GITHUB-GATEWAY-001
deliverables:
  - repo tree endpoint
  - file read endpoint
  - path traversal protection
  - GitHub token/App config docs
validation:
  - can read allowlisted repo
  - rejects non-allowlisted repo
  - rejects invalid paths
  - records read receipt draft or access log
```

### Packet 3: Issue Draft/Create

```yaml
packet_id: ION-GITHUB-GATEWAY-003
objective: Add issue draft and approval-gated issue create flow.
authority_class: A1_DRAFT + A2_COORDINATION_WRITE
depends_on:
  - ION-GITHUB-GATEWAY-001
  - ION-GITHUB-GATEWAY-002
deliverables:
  - issue draft endpoint
  - issue create endpoint
  - ApprovalEvidence schema
  - receipt output
validation:
  - draft endpoint does not mutate GitHub
  - create endpoint rejects missing approval
  - create endpoint creates issue when approved
  - receipt includes issue URL and ID
```

### Packet 4: Custom GPT Action Import

```yaml
packet_id: ION-GPT-ACTIONS-004
objective: Prepare the OpenAPI schema and GPT instructions for Custom GPT Actions.
authority_class: A1_DRAFT
depends_on:
  - ION-GITHUB-GATEWAY-001
deliverables:
  - openapi.yaml compatible with GPT Actions
  - GPT instruction patch for GitHub gateway use
  - action operation descriptions in ION terms
validation:
  - schema imports in GPT editor
  - status endpoint test passes in Preview
  - docs identify authentication method
```

### Packet 5: Branch/PR Candidate Flow

```yaml
packet_id: ION-GITHUB-GATEWAY-005
objective: Add branch creation, candidate patch, and PR draft/create flow.
authority_class: A3_BRANCH_WRITE
depends_on:
  - ION-GITHUB-GATEWAY-003
deliverables:
  - branch create endpoint
  - PR draft endpoint
  - PR create endpoint
  - commit-to-branch design, if implemented
validation:
  - cannot write to main
  - requires approval evidence
  - branch names are packet-linked
  - PR body includes proof and receipt link
```

---

## 15. Suggested Repo Layout

If this lives inside the ION repo:

```text
ION/
  integrations/
    github_gateway/
      README.md
      openapi.yaml
      policy.example.json
      receipts/
      src/
      tests/
      .env.example
  packets/
    active/
      ION-GITHUB-GATEWAY-001.md
      ION-GITHUB-GATEWAY-002.md
  receipts/
    github_gateway/
  docs/
    integrations/
      custom_gpt_github_actions.md
```

If this is a separate repo:

```text
ion-github-gateway/
  README.md
  openapi.yaml
  policy.example.json
  src/
  tests/
  receipts/
  packets/
  docs/
```

Recommendation:

Start separate if we want clean gateway development.

Move into main ION repo later if it becomes a first-class organ.

---

## 16. Prompt / Instruction Patch For ION Custom GPT

Candidate addition to the Custom GPT instructions after gateway exists:

```text
When GitHub actions are available, treat them as a bounded ION GitHub Gateway, not as direct authority.

Before mutating GitHub:
1. State the exact intended action.
2. Identify authority class.
3. Use draft/validate endpoints when available.
4. Require operator approval evidence for write actions.
5. Prefer issues, branches, and PRs over direct main mutation.
6. Register or request a receipt for every meaningful state-affecting action.
7. Never claim GitHub state changed unless the gateway returns proof.
8. Never claim ION state accepted unless a Steward/human acceptance receipt exists.

Read and draft actions may proceed when useful.
Write actions require explicit approval unless the active gateway policy says otherwise.
```

---

## 17. Receipt Template

```markdown
# ION GitHub Gateway Receipt

**receipt_id:**  
**action_id:**  
**packet_id:**  
**timestamp:**  
**carrier:** Private Custom GPT via ION GitHub Gateway  
**operator:**  
**authority_class:**  
**repo:**  
**branch/ref:**  

## Intent

## Context Used

## Action Requested

## Approval Evidence

## Gateway Validation

## External Mutation

- issue:
- PR:
- branch:
- commit SHA:
- check run:
- URL:

## Proof Returned

## Result

## Non-Claims

## Next Packet
```

---

## 18. Safety Without Self-Neutering

This workpack should not over-index on generic AI fear.

The operator is correct that the desired system should be powerful. File access, GitHub access, terminal execution, and local editing are not inherently wrong. They are the point of a serious development carrier.

ION’s answer is not:

```text
Do not give the AI tools.
```

ION’s answer is:

```text
Give the AI tools inside a governed environment where actions are bounded, visible, reversible where possible, proof-bearing, and receipted.
```

The key distinction:

```text
Unsafe: model output silently becomes state.
Powerful and governed: model output becomes a candidate action packet, then proof-gated state movement.
```

So the path forward is to expand capability aggressively, but in ION-shaped layers.

---

## 19. Acceptance Criteria For This Workpack

This workpack is complete when local Codex can:

```text
1. Read this document.
2. Identify the first implementation packet.
3. Create a gateway skeleton or report blockers.
4. Return files changed, tests run, and proof.
5. Produce a candidate receipt.
```

The workpack is **not** asking Codex to:

```text
- connect to production GitHub without credentials
- mutate an actual repository without operator approval
- merge PRs
- deploy the gateway
- claim Custom GPT integration is active before it is configured
```

---

## 20. Immediate Next Packet

Recommended next action:

```yaml
packet_id: ION-GITHUB-GATEWAY-001
name: Build minimal ION GitHub Gateway skeleton
executor: local Codex CLI
mode: bounded implementation
authority_class: A0_READ_ONLY + A1_DRAFT
objective: Create a local gateway service with status/policy/OpenAPI surfaces and no external mutation.
success_proof:
  - service starts
  - openapi.yaml exists
  - policy.example.json exists
  - README setup path exists
  - tests or smoke check pass
```

Suggested Codex prompt:

```text
You are operating as a local Codex CLI carrier under ION governance.

Read `ION_GitHub_Custom_GPT_IDE_Workpack_v0_1.md`.

Execute Packet `ION-GITHUB-GATEWAY-001` only.

Do not connect to live GitHub unless credentials and explicit operator approval are present.
Do not implement mutation endpoints yet.
Create the gateway skeleton, OpenAPI file, policy example, README, and smoke test.
Return:
- files changed
- commands run
- validation results
- blockers
- candidate receipt
- next packet recommendation
```

---

## 21. Strong Formulation

```text
The private Custom GPT should become an ION-aware IDE carrier.

It should not be limited to chat.
It should not be trusted as magic.
It should not mutate state by vibes.

It should read, inspect, draft, route, patch, test, queue, PR, and receipt work through governed action surfaces.

The local operator remains sovereign.
The gateway is the tool boundary.
GitHub is the durable mirror.
Codex is the local worker.
ION is the law.
```
