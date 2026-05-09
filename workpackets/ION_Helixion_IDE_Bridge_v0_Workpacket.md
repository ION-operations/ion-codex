# ION Helixion IDE Bridge v0 — Workpacket

**Packet ID:** `ION-HELIXION-IDE-BRIDGE-V0`  
**Date:** 2026-05-08  
**Prepared for:** Local Codex CLI / Local Steward Runtime  
**Carrier:** ChatGPT Custom GPT / ION browser carrier  
**Target lane:** Local ION + Helixion gateway + Codex CLI orchestration  
**Status:** Candidate workpacket awaiting local Steward/operator acceptance

---

## 0. Executive Summary

Build the first working version of the **ION Helixion IDE Bridge**: a local gateway and control surface that lets a Custom GPT act as the conversational cockpit for a real local AI-native IDE workflow.

The Browser Custom GPT is **not** the whole IDE and does not pretend to be the machine. It is the front-facing carrier: conversation, intent compilation, packet drafting, routing, approval brokering, and result explanation.

The local system provides the hard execution layer:

```text
Browser Custom GPT
→ ION / Helixion Gateway
→ Local Steward Runtime
→ Codex CLI Workers
→ Local Project Files / Tests / Dev Server
→ Helixion Live Preview URL
→ Receipts / Proof / GitHub Mirror
```

Strong formulation:

```text
The Browser GPT is the face.
Helixion is the cockpit glass.
The local Steward is the nervous system.
Codex is the hands.
The preview URL is the eyes.
GitHub is the memory mirror.
ION is the law.
```

---

## 1. Objective

Create a local **Helixion IDE Bridge v0** that supports:

1. Mounting a local project.
2. Reporting current project status.
3. Queuing bounded Codex CLI work from an ION packet.
4. Tracking Codex run status and result artifacts.
5. Starting/stopping/restarting a live project preview server.
6. Returning a live preview URL to the Browser GPT/user.
7. Registering proof-bearing receipts for work attempts.
8. Preserving enough state for continuation across chat turns.

The v0 does **not** need to be a full IDE. It needs to prove the spine:

```text
chat intent
→ ION packet
→ local execution
→ preview feedback
→ proof return
→ operator settlement
→ receipt
```

---

## 2. Architecture Model

### 2.1 Layered Roles

```text
Browser Custom GPT
= persona, cockpit, operator conversation, routing intelligence

ION Gateway / Helixion API
= action bridge, packet validator, queue surface, preview/control plane

Local Steward Runtime
= authority gate, project mount manager, receipt ledger, settlement layer

Local Codex CLI Workers
= bounded executors for code, tests, file edits, analysis

Project Preview / Dev Server
= live visual feedback loop

GitHub
= durable mirror: branches, PRs, issues, history

ION
= governance law: packets, templates, proofs, approvals, receipts
```

### 2.2 Soft Steward vs Hard Steward

The Browser GPT may behave as a **Soft Steward**:

```text
- understands user intent
- drafts packets
- explains risk
- routes work
- asks for approval
- interprets results
- proposes next steps
```

The local runtime acts as the **Hard Steward**:

```text
- validates packet shape
- checks mounted project authority
- controls filesystem mutation
- runs tests/builds
- starts/stops preview servers
- writes receipts
- blocks invalid or unsafe actions
- preserves local state truth
```

The Browser GPT may recommend. The local Steward enforces.

---

## 3. Design Principles

### 3.1 Do Not Cripple Capability

This system is allowed to be powerful. The goal is not to avoid file access, command execution, or live project mutation forever. The goal is to make those operations **typed, visible, reversible, proof-bearing, and operator-governed**.

Power is acceptable when shaped like:

```text
intent
→ packet
→ context
→ authority check
→ execution
→ proof
→ preview
→ approval
→ receipt
→ durable mirror
```

Power is not acceptable when shaped like:

```text
chat suggestion
→ silent mutation
→ no proof
→ no receipt
```

### 3.2 GPT Is Not State

The Browser GPT can reason and route, but it is not durable state. Local files, receipts, queues, manifests, Git branches, and exported continuity bundles carry inheritable state.

### 3.3 GitHub Is Durable Mirror, Not Ultimate Authority

GitHub is useful for branches, issues, PRs, review trails, rollback points, and collaboration. It does not replace ION authority. Local truth, receipts, and operator acceptance remain primary.

### 3.4 Preview Is Perception

The live Helixion URL is not decorative. It is the perception layer of the IDE. The user should be able to open a URL and see the project state that Codex is changing.

---

## 4. v0 System Components

Recommended local tree:

```text
helixion_ide_bridge/
  README.md
  pyproject.toml or package.json
  .env.example

  helixion_gateway/
    server.py or server.ts
    api/
      health.py
      ion_status.py
      projects.py
      codex.py
      preview.py
      receipts.py
    models/
      packets.py
      projects.py
      runs.py
      receipts.py
    services/
      project_registry.py
      codex_adapter.py
      preview_manager.py
      receipt_store.py
      command_runner.py
      git_adapter.py
    storage/
      projects_manifest.json
      preview_registry.json
      queue/
      runs/
      receipts/
      logs/

  schemas/
    ion_packet.schema.json
    codex_run.schema.json
    receipt.schema.json
    project_manifest.schema.json
    openapi.yaml

  scripts/
    dev_server.sh
    run_gateway.sh
    smoke_test.sh

  docs/
    CUSTOM_GPT_ACTION_SETUP.md
    LOCAL_STEWARD_MODEL.md
    PREVIEW_MANAGER.md
```

Implementation language can be Python/FastAPI or Node/Express/Fastify. Prefer the fastest path already consistent with the existing local ION stack.

---

## 5. Minimum API Surface

### 5.1 Health and Status

```http
GET /health
GET /ion/status
```

Expected:

```json
{
  "ok": true,
  "service": "helixion_ide_bridge",
  "version": "0.0.1",
  "mode": "local",
  "mounted_project": null,
  "queue_depth": 0
}
```

### 5.2 Project Mount and Status

```http
GET  /projects
POST /projects/mount
GET  /projects/{project_id}/status
GET  /projects/{project_id}/tree
GET  /projects/{project_id}/git/status
```

Mount request:

```json
{
  "project_id": "ion",
  "path": "/absolute/path/to/project",
  "label": "ION local repo",
  "authority": {
    "allow_read": true,
    "allow_write_drafts": true,
    "allow_apply_patches": false,
    "allow_run_commands": true,
    "allow_preview": true,
    "allow_git": false
  }
}
```

### 5.3 Codex Queue

```http
POST /codex/queue
GET  /codex/queue
GET  /codex/runs/{run_id}
POST /codex/runs/{run_id}/cancel
```

Queue request:

```json
{
  "packet_id": "ION-PACKET-001",
  "project_id": "ion",
  "objective": "Inspect the project and report the dev preview command.",
  "mode": "inspect_only",
  "context_refs": [],
  "authority": {
    "allow_file_read": true,
    "allow_file_write": false,
    "allow_command_run": false,
    "requires_operator_approval": false
  },
  "expected_return": {
    "summary": true,
    "files_touched": true,
    "commands_run": true,
    "proof": true,
    "receipt_draft": true
  }
}
```

### 5.4 Preview Manager

```http
POST /preview/start
POST /preview/stop
POST /preview/restart
GET  /preview/status
GET  /preview/url
GET  /preview/logs
```

Preview start request:

```json
{
  "project_id": "ion-web",
  "command": "npm run dev",
  "cwd": "/absolute/path/to/project",
  "port": 5173,
  "public_label": "ION Web Preview"
}
```

Preview status response:

```json
{
  "project_id": "ion-web",
  "running": true,
  "local_url": "http://127.0.0.1:5173",
  "helixion_url": "https://helixion.example.com/preview/ion-web",
  "pid": 12345,
  "started_at": "2026-05-07T00:00:00Z",
  "last_log_excerpt": "Vite ready in 450ms"
}
```

### 5.5 Receipts

```http
POST /receipts/register
GET  /receipts
GET  /receipts/{receipt_id}
```

Receipt request:

```json
{
  "receipt_id": "receipt_20260507_helixion_v0_001",
  "packet_id": "ION-PACKET-001",
  "project_id": "ion",
  "actor": "local_codex_cli",
  "template": "bounded_local_work",
  "objective": "Inspect preview startup path.",
  "authority": {
    "read": true,
    "write": false,
    "commands": false
  },
  "result": "completed",
  "files_touched": [],
  "commands_run": [],
  "proof": [
    "project tree inspected",
    "package scripts found"
  ],
  "non_claims": [
    "No files were modified.",
    "No preview server was started.",
    "No GitHub mutation occurred."
  ],
  "next_packet": "Start preview server after operator approval."
}
```

---

## 6. Custom GPT Action Surface

The Custom GPT should call the Helixion Gateway using OpenAPI Actions.

Initial operations:

```text
ionGatewayHealth
ionGatewayStatus
ionProjectList
ionProjectMount
ionProjectStatus
ionCodexQueue
ionCodexRunStatus
ionPreviewStart
ionPreviewStatus
ionPreviewUrl
ionReceiptRegister
```

The GPT should not need raw shell access. It sends structured packets and receives structured returns.

---

## 7. Work Modes

### 7.1 Inspect Only

Allowed:

```text
- list files
- read manifest files
- read package metadata
- read git status
- detect build/dev commands
- summarize architecture
```

Blocked:

```text
- writes
- command execution unless separately allowed
- Git mutation
```

### 7.2 Draft Only

Allowed:

```text
- generate patch files
- generate diffs
- write into staging/drafts area
- create proposed file contents
```

Blocked:

```text
- applying patches to project source
- committing
- pushing
```

### 7.3 Local Apply

Allowed:

```text
- apply patch to working tree
- run tests
- start preview
- collect proof
```

Requires:

```text
- mounted project
- packet authority
- operator approval or preconfigured project policy
```

### 7.4 Git Mirror

Allowed:

```text
- create branch
- commit
- push branch
- open PR
```

Requires:

```text
- explicit operator approval
- clean receipt
- no unresolved blocker
```

### 7.5 Deployment / External Mutation

Out of scope for v0 unless an explicit deployment gateway and approval path already exist.

---

## 8. First Implementation Packets

### Packet 1 — Scaffold Gateway

**Objective:** Create the local Helixion Gateway skeleton with health/status routes and persistent storage directories.

**Authority:** Local file creation inside `helixion_ide_bridge/` only.

**Tasks:**

```text
1. Create project scaffold.
2. Implement GET /health.
3. Implement GET /ion/status.
4. Create storage directories for queue, runs, receipts, logs.
5. Add README startup instructions.
6. Add smoke test.
```

**Validation:**

```text
- gateway starts locally
- GET /health returns ok
- GET /ion/status returns version/mode/queue_depth
- smoke test passes
```

**Receipt required:** `receipt_gateway_scaffold_v0`

---

### Packet 2 — Project Mount Registry

**Objective:** Implement project registry and mount/status endpoints.

**Authority:** Read-only access to mounted project path.

**Tasks:**

```text
1. Add projects_manifest.json storage.
2. Implement GET /projects.
3. Implement POST /projects/mount.
4. Implement GET /projects/{project_id}/status.
5. Implement basic path validation.
6. Report package markers: git, package.json, pyproject.toml, README.
```

**Validation:**

```text
- can mount a local test project
- invalid paths rejected
- status returns root markers
- no project files modified
```

**Receipt required:** `receipt_project_mount_registry_v0`

---

### Packet 3 — Codex Queue Adapter

**Objective:** Add a queue interface for bounded Codex CLI work packets.

**Authority:** Queue files only; no Codex execution yet unless local operator approves.

**Tasks:**

```text
1. Define ion_packet.schema.json.
2. Implement POST /codex/queue.
3. Persist queued packets under storage/queue.
4. Implement GET /codex/queue.
5. Implement run record model under storage/runs.
6. Add validation for project_id, objective, mode, authority.
```

**Validation:**

```text
- valid packet accepted
- invalid packet rejected
- queue listing stable
- run ids deterministic or traceable
```

**Receipt required:** `receipt_codex_queue_adapter_v0`

---

### Packet 4 — Preview Manager v0

**Objective:** Start and track a local dev server preview for a mounted project.

**Authority:** Run configured dev command only inside mounted project.

**Tasks:**

```text
1. Implement POST /preview/start.
2. Implement POST /preview/stop.
3. Implement GET /preview/status.
4. Implement GET /preview/url.
5. Capture process pid and logs.
6. Store preview_registry.json.
```

**Validation:**

```text
- preview starts with explicit command
- preview URL is returned
- logs are captured
- preview stop terminates process
- status reflects running/stopped state
```

**Receipt required:** `receipt_preview_manager_v0`

---

### Packet 5 — Receipt Store

**Objective:** Make work attempts inheritable.

**Authority:** Write receipt JSON files only.

**Tasks:**

```text
1. Define receipt.schema.json.
2. Implement POST /receipts/register.
3. Implement GET /receipts.
4. Implement GET /receipts/{receipt_id}.
5. Attach receipts to packet_id and project_id.
```

**Validation:**

```text
- valid receipt accepted
- invalid receipt rejected
- receipt query works
- receipt records non-claims
```

**Receipt required:** `receipt_store_v0`

---

## 9. OpenAPI Skeleton

```yaml
openapi: 3.1.0
info:
  title: ION Helixion IDE Bridge
  version: 0.0.1
servers:
  - url: http://127.0.0.1:8787
paths:
  /health:
    get:
      operationId: ionGatewayHealth
      summary: Read gateway health
      responses:
        "200":
          description: Gateway health

  /ion/status:
    get:
      operationId: ionGatewayStatus
      summary: Read ION bridge status
      responses:
        "200":
          description: ION bridge status

  /projects:
    get:
      operationId: ionProjectList
      summary: List mounted projects
      responses:
        "200":
          description: Mounted project list

  /projects/mount:
    post:
      operationId: ionProjectMount
      summary: Mount a local project
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [project_id, path]
              properties:
                project_id:
                  type: string
                path:
                  type: string
                label:
                  type: string
                authority:
                  type: object
      responses:
        "200":
          description: Project mount result

  /projects/{project_id}/status:
    get:
      operationId: ionProjectStatus
      summary: Read mounted project status
      parameters:
        - name: project_id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Project status

  /codex/queue:
    post:
      operationId: ionCodexQueue
      summary: Queue a bounded Codex work packet
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [packet_id, project_id, objective, mode]
              properties:
                packet_id:
                  type: string
                project_id:
                  type: string
                objective:
                  type: string
                mode:
                  type: string
                context_refs:
                  type: array
                  items:
                    type: string
                authority:
                  type: object
                expected_return:
                  type: object
      responses:
        "200":
          description: Queued packet

    get:
      operationId: ionCodexQueueList
      summary: List Codex queue
      responses:
        "200":
          description: Codex queue

  /codex/runs/{run_id}:
    get:
      operationId: ionCodexRunStatus
      summary: Read Codex run status
      parameters:
        - name: run_id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Codex run status

  /preview/start:
    post:
      operationId: ionPreviewStart
      summary: Start live project preview
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [project_id, command]
              properties:
                project_id:
                  type: string
                command:
                  type: string
                cwd:
                  type: string
                port:
                  type: integer
                public_label:
                  type: string
      responses:
        "200":
          description: Preview start result

  /preview/status:
    get:
      operationId: ionPreviewStatus
      summary: Read preview status
      responses:
        "200":
          description: Preview status

  /preview/url:
    get:
      operationId: ionPreviewUrl
      summary: Read current preview URL
      responses:
        "200":
          description: Preview URL

  /receipts/register:
    post:
      operationId: ionReceiptRegister
      summary: Register an ION work receipt
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        "200":
          description: Receipt registration result
```

---

## 10. Validation Gates

v0 is complete only when:

```text
1. Gateway starts locally.
2. Health/status endpoints respond.
3. Project can be mounted.
4. Project status can be read.
5. Codex packet can be queued.
6. Queue can be listed.
7. Preview can be started/stopped for a simple project.
8. Preview URL is returned.
9. Receipt can be registered and read.
10. Smoke test script proves the flow.
```

Smoke test target:

```text
./scripts/smoke_test.sh
```

Expected smoke test flow:

```text
GET /health
POST /projects/mount
GET /projects/{id}/status
POST /codex/queue
GET /codex/queue
POST /preview/start
GET /preview/status
GET /preview/url
POST /receipts/register
GET /receipts
```

---

## 11. Non-Claims

This v0 workpacket does **not** claim:

```text
- direct GitHub integration is complete
- Custom GPT Action has already been installed
- Codex CLI execution is already wired
- preview tunneling to a public Helixion URL is already solved
- deployment authority exists
- GPT has direct filesystem authority
- ION state has landed without operator/local Steward acceptance
```

---

## 12. Future Work

After v0:

```text
v0.1 — Custom GPT Action import/test
v0.2 — Codex CLI process invocation
v0.3 — diff capture and patch application
v0.4 — preview screenshot/status capture
v0.5 — GitHub branch/PR mirror
v0.6 — operator approval UI in Helixion
v0.7 — multi-project workspace
v0.8 — receipt hydration and continuation bundles
v0.9 — domain-aware context package compiler
v1.0 — full local AI-native IDE loop
```

---

## 13. Local Codex CLI Prompt

Use this prompt to begin implementation:

```text
You are operating as a local Codex CLI worker under ION governance.

Workpacket: ION Helixion IDE Bridge v0

Objective:
Build the first local gateway/control surface that lets a Browser Custom GPT queue bounded local work, mount a project, start a live preview server, and register proof-bearing receipts.

Authority:
You may create a new local project directory named helixion_ide_bridge unless an existing target path is provided by the operator. Do not modify unrelated repositories. Do not push to GitHub. Do not deploy. Prefer scaffold + smoke-test proof over broad implementation.

First task:
Implement Packet 1 — Scaffold Gateway.

Return:
1. Files created/modified.
2. Commands run.
3. Validation output.
4. Any blockers.
5. Receipt draft: receipt_gateway_scaffold_v0.
6. Recommended next packet.
```

---

## 14. Receipt Draft for This Workpacket

```json
{
  "receipt_id": "receipt_ion_helixion_ide_bridge_workpacket_v0",
  "packet_id": "ION-HELIXION-IDE-BRIDGE-V0",
  "type": "workpacket_creation",
  "status": "candidate",
  "created_by": "Browser Custom GPT / ION carrier",
  "objective": "Define the next local Codex CLI workpacket for Helixion IDE Bridge v0.",
  "result": "standalone markdown workpacket created",
  "authority": {
    "state_landing": false,
    "local_execution": false,
    "github_mutation": false
  },
  "non_claims": [
    "No local Codex execution occurred in this chat turn.",
    "No gateway files were created locally except this markdown artifact.",
    "No GitHub mutation occurred.",
    "No ION state has landed until accepted by the operator/local Steward."
  ],
  "next_packet": "Packet 1 — Scaffold Gateway"
}
```
