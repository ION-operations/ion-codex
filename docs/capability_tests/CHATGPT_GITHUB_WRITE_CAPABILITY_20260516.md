# ChatGPT GitHub Write Capability Test — 2026-05-16

Status: candidate scratch-branch artifact
Branch: `test/chatgpt-github-write-capability-20260516`
Repository: `ION-operations/ION`
Accepted state claim: false
Production authority claim: false
Purpose: verify whether this ChatGPT connector can create a branch, write a useful Markdown artifact, read it back, and support later PR-style review without mutating the default branch.

## Write gate

```yaml
write_gate:
  action: create scratch-branch capability document
  repository: ION-operations/ION
  branch: test/chatgpt-github-write-capability-20260516
  path: docs/capability_tests/CHATGPT_GITHUB_WRITE_CAPABILITY_20260516.md
  owners:
    - Braden Bohme
    - ION-operations repository authority
  evidence:
    - GitHub connector exposed write-capable repository permissions
    - default branch was not targeted
    - scratch branch was created first
  duplicate_risk: low
  allowed_output: candidate documentation artifact only
  forbidden_output:
    - production state claim
    - default branch mutation
    - deploy
    - secret read/write
    - destructive operation
  new_system: false
  verdict: PASS
```

## Observed connector capability under test

This test is intentionally small. It proves end-to-end mechanics, not maximum payload capacity.

Tested operations:

1. Read repository metadata.
2. Search recent commits to obtain a plausible base commit SHA.
3. Create scratch branch.
4. Create this Markdown file on the scratch branch.
5. Read the file back after writing.
6. Optionally compare branch to base and inspect commit status.

## ION/Codex native integration capture

The architecture developed in the prior discussion should be preserved as a candidate planning object. The core thesis:

> ION should compile itself into Codex-native operating surfaces rather than sit beside Codex as an external memory/control wrapper.

### ION to Codex crosswalk

| ION primitive | Codex-native surface | Candidate integration |
|---|---|---|
| ION law / standing invariants | `AGENTS.md`, config profiles, hooks | Stable law should be short, layered, and closest to the working directory. |
| Folder-local context packages | Directory `AGENTS.md` + `context/` folder | Each governed folder becomes a context region with load order, active packet, routes, receipts, and verification. |
| Templates | Skills, skill references/assets/scripts, output schemas | Every template should be routable; not every template should be a top-level skill. |
| Branch/action routing | Root router skill + branch router skills + lazy context injection | Codex should see a small root menu, then descend through branch maps. |
| Roles | `.codex/agents/*.toml` custom agents/subagents | Roles become bounded carrier slots, not free-floating identities. |
| Context proof | Hook receipts + validator scripts + explicit proof sections | No unsupported “I read it” claims. |
| Carrier gates | `UserPromptSubmit`, `PreToolUse`, `PermissionRequest` hooks | Writes and side effects require gate evidence before execution. |
| Receipts | PostToolUse/Stop hooks + receipt files + optional Supabase mirror | Receipts become the continuity spine. |
| Thread continuity | Codex local transcripts + app-server thread APIs + ION branch capsules | Native resume is useful, but accepted state still requires settlement. |
| Active context injection | app-server `thread/inject_items` | Compiled active packets can become model-visible native thread history. |
| MCP tools | Codex MCP config with allow/deny lists | Tools are exposed as capability-scoped surfaces. |
| Cockpit/JOC | UI over Codex app-server + receipts + service health | Cockpit observes dispatch, context, proof, drift, and settlement. |

### Skill routing principle

Bad shape:

```text
300 ION templates -> 300 top-level Codex skills
```

Better shape:

```text
small visible root skills
  -> branch/domain router
    -> skill family
      -> template pack/reference/script
        -> exact leaf action
```

Candidate root skill set:

```text
$ion-router
$ion-continue
$ion-audit
$ion-carrier-gate
$ion-context-compile
```

Candidate branch routers:

```text
$ion-codex-native-router
$ion-action-gateway-router
$ion-runtime-session-router
$ion-template-governance-router
$ion-ui-cockpit-router
$ion-repo-forensics-router
```

### Folder-local context package pattern

For each important folder/domain:

```text
domain/
  README.md
  AGENTS.md
  context/
    CONTEXT_INDEX.md
    DOMAIN_CARD.yaml
    DOMAIN_CONTEXT_PACKAGE.md
    DOMAIN_HISTORY.md
    DOMAIN_PROTOCOLS.md
    ACTIVE_PACKET.md
    ROUTES.yaml
    TEMPLATES_INDEX.yaml
    RECEIPTS_INDEX.md
    OPEN_QUESTIONS.md
    FAILURE_MODES.md
    VERIFY.md
```

The `AGENTS.md` file should be the Codex-native entrypoint. It should not contain every detail. It should direct Codex to load the local context package and stop if required context is missing or stale.

### Hook lifecycle spine

Candidate hook mapping:

| Hook | ION use |
|---|---|
| `SessionStart` | Load root law, current folder context, branch capsule, mount receipt. |
| `UserPromptSubmit` | Classify prompt, route to branch, block malformed writes. |
| `PreToolUse` | Gate Bash, patch, and MCP side effects before execution. |
| `PermissionRequest` | Allow/deny according to ION authority and duplicate-risk rules. |
| `PostToolUse` | Capture evidence, classify outputs, emit receipt candidates. |
| `Stop` | Verify proof/receipts/tests/handoff; force continuation if required work was skipped. |

### Non-claims

This document does not claim:

- that the architecture is accepted ION law;
- that Codex hooks provide a complete security boundary;
- that raw Codex thread-log editing is a safe normal workflow;
- that Supabase has a ready receipt schema in this repository;
- that this scratch branch should be merged.

## Capability-test conclusion placeholder

This section should be updated after the connector reads this file back and optionally compares the branch.

Expected result:

```yaml
capability_test_result:
  branch_created: true
  file_created: true
  file_read_back: pending
  default_branch_mutated: false
  suitable_for_candidate_docs: likely
  suitable_for_large_artifacts: unproven
  next_recommended_surface: draft PR or issue linked to branch
```
