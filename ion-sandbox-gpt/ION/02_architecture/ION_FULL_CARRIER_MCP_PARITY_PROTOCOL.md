---
type: planning_artifact
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-04
source_packet: chatgpt_browser_mcp_attempted_work_packet
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION Full-Carrier MCP Parity Protocol

## Purpose

This artifact starts the corrected full-carrier MCP architecture plan. It does
not grant production authority, live execution authority, arbitrary shell
authority, credential access, direct deletion, or git push. It defines the
target architecture that future carrier adapters should converge toward.

The current ChatGPT browser connector MVP remains useful implementation
scaffolding, but its bounded-management-lane restrictions are not a permanent
ION core law. They are temporary safety residue from the first hosted/browser
MCP bring-up.

## Core Invariant

ION has one core engine. Carriers mount that engine through different adapter
surfaces.

```text
ION core engine = packets + roles + templates + proof gates + receipts + state
Cursor carrier = IDE adapter over the same engine
Codex CLI carrier = CLI/local worker adapter over the same engine
ChatGPT browser carrier = MCP/browser adapter target over the same engine
Future carriers = adapter-specific mounts over the same engine
```

No carrier is ION identity. No carrier is STEWARD, RELAY, PERSONA, or final
authority by itself. Roles are mounted through packets and templates. Carrier
capability differences are adapter facts, not alternate ION ontologies.

## Corrected Interpretation Of V120 Limits

`ION_CHATGPT_BROWSER_MCP_CONNECTOR_PROTOCOL.md` and the V120 setup guide define
the current safe MVP connector. Their restrictions are valid for the current
implementation state:

- read/status visibility;
- bounded queue packets;
- proof-gated task returns;
- decision and containment receipts;
- no arbitrary shell/file/delete/git/credential/provider/browser control.

Those restrictions must be treated as current adapter guardrails, not the final
architecture ceiling for ChatGPT browser as a carrier. The corrected target is
IDE-level parity through explicit capability classes, staged proofs, and
receipts.

## Carrier Adapter Failure Is Not ION Core Failure

An adapter failure means the carrier surface did not expose, route, or prove a
capability correctly. It does not mean ION core lacks the capability.

Examples:

- If ChatGPT browser cannot create a Codex work packet, inspect the MCP tool
  call, schema, confirmation gate, tunnel, and connector adapter first.
- If a local preview exits after a documented command, inspect the preview
  adapter entry point before declaring the ION connector architecture invalid.
- If an IDE carrier can edit files but a browser carrier cannot, classify that
  as an adapter capability gap until the core packet/receipt law is shown to be
  missing.

Every failure report should classify:

```text
ION_CORE_FAILURE
CARRIER_ADAPTER_FAILURE
TRANSPORT_FAILURE
AUTH_OR_CONFIRMATION_FAILURE
CAPABILITY_NOT_YET_IMPLEMENTED
POLICY_BLOCK_WORKING_AS_DESIGNED
```

## Full MCP / IDE-Equivalent Capability Classes

Full-carrier parity does not mean unsafe direct host control. It means every
carrier can lawfully request the same ION work classes through the same core
engine, with adapter-appropriate proofs.

Target capability classes:

1. Mount and context
   - root proof;
   - carrier profile resolution;
   - current operating packet read;
   - active packet and role context package read;
   - compiled context bundle delivery.

2. Status and state visibility
   - ION status;
   - cockpit view;
   - artifact manifest;
   - receipt search;
   - git status summary;
   - carrier work queue visibility.

3. Work packet creation
   - operator message queueing;
   - Codex/local worker packet request;
   - role-cycle packet request;
   - context package materialization request.

4. File mutation through ION gates
   - bounded patch proposal;
   - bounded write execution only after confirmation and allowed-path proof;
   - diff receipt;
   - no-silent-loss preservation receipt;
   - lifecycle transition receipt for archive/containment/supersession.

5. Build, test, and command execution
   - test command request through declared validation commands;
   - bounded shell command execution only through approved carrier profile and
     explicit receipt;
   - process start/stop receipts for local previews and tunnels;
   - no arbitrary shell bridge exposed as a raw browser tool.

6. Task return and integration
   - `### CONTEXT PROOF`;
   - `### TEMPLATE ACTION PROOF`;
   - files changed;
   - tests or validations run;
   - remaining blockers;
   - Steward integration or rejection before truth promotion.

7. Decision and authority receipts
   - human gate requests;
   - operator decisions;
   - production ratification requests;
   - live execution authority requests;
   - explicit denial/deferral receipts.

8. Parity-specific diagnostics
   - carrier adapter self-test;
   - transport health check;
   - tool policy diff;
   - core capability registry diff;
   - adapter capability registry diff.

## ChatGPT Browser As Full Carrier Target

ChatGPT browser should be treated as a full ION carrier target, not merely a
bounded management panel, once its adapter proves the relevant capability
classes.

The intended target state:

```text
ChatGPT browser -> MCP adapter -> ION core engine -> bounded carriers/workers
```

In that state, ChatGPT browser may lawfully initiate the same classes of work an
IDE carrier can initiate, but only through ION packets, templates, confirmations,
proof gates, receipts, and human gates where required.

This still does not make ChatGPT browser sovereign authority. It becomes a
carrier with IDE-level parity over ION's core workflow, not a direct host shell
or production deployer.

## No-Silent-Loss And Receipt Principles

Full-carrier parity must preserve:

- no silent deletion;
- no silent loss;
- lifecycle-aware containment instead of direct removal;
- hash/path evidence for moved or superseded artifacts;
- task returns that remain proposals until integrated;
- explicit distinction between current truth, draft proposal, and forensic
  evidence.

Any adapter that cannot preserve these principles is not ready for the matching
capability class.

## File And Artifact Transfer From ChatGPT Browser

ChatGPT browser must be able to move artifacts it creates into ION custody
without relying on pasted transcript text as the artifact of record. The first
implementation surface is intentionally staged, non-production, and bounded to
ION-owned custody roots:

```text
ION/05_context/current/chatgpt_connector/artifacts/
ION/05_context/inbox/
ION/05_context/signals/
```

This is not a final restriction on full-carrier parity. It is the first adapter
proof stage for file/artifact ingress. Broader target-path classes must be added
through registry proof, mount proof, action receipts, and no-silent-loss gates.

First MCP tool surface:

```text
ion_file_put_text
ion_artifact_upload_init
ion_artifact_upload_chunk
ion_artifact_upload_commit
```

`ion_file_put_text` handles small UTF-8 text artifacts. The chunked upload tools
handle larger text or binary artifacts by opening an upload session, receiving
base64 chunks, assembling chunks in order, verifying `sha256`, and writing the
artifact only when the target path is allowed and does not already exist.

## Practical Length-Limit Risks

Full-carrier MCP must account for limits at multiple layers:

- ChatGPT message length can truncate pasted artifact text before a tool call is
  made.
- MCP JSON arguments can exceed client, connector, or model-tool limits.
- HTTP request bodies can exceed local preview, tunnel, proxy, or hosted
  deployment limits.
- Active queue JSON files can become large enough to slow reads, diffs, and
  proof gates.
- Context-proof and template-action gates reject malformed returns, missing
  headings, missing path evidence, or unapproved template identifiers.
- Codex return formatting can fail intake if `### CONTEXT PROOF` is not the
  first durable section.
- Base64 transfer expands binary payloads, so chunk sizes must be smaller than
  apparent raw artifact size.

Current staging limits are registry values, not final law:

```text
max_text_put_bytes: 524288
max_upload_chunk_bytes: 524288
max_upload_bytes: 4194304
```

## Target Path, Overwrite, Rollback, And Containment

Target paths for browser-origin artifact transfer must be repo-relative, must not
escape the shell root, must not enter `.git`, credential, secret, vault, or
environment-file paths, and must match a registered transfer root.

The first implementation blocks existing targets instead of overwriting them.
When a target exists, the connector emits or returns a no-silent-loss finding
and requires a lifecycle receipt before any later mutation. Future overwrite
support must record:

- target preimage path and sha256;
- overwrite request authority;
- containment or rollback path;
- action receipt;
- validation result after write.

No direct delete is introduced by full-carrier parity.

## Carrier-To-Carrier Communications

Carrier-to-carrier communication must reuse ION-managed queue ownership instead
of creating an out-of-band chat system. The active queue owner is:

```text
ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
```

The first MCP tool surface is:

```text
ion_carrier_message_send
ion_carrier_message_poll
ion_carrier_message_ack
```

These messages are distinct from other ION records:

```text
operator_message = human/operator instruction or continuation signal
carrier_message = carrier-to-carrier coordination note with sender/recipient evidence
steward_decision = integration or route authority record
task_return = proof-bearing work output proposed for intake
receipt = custody, validation, decision, or lifecycle evidence
```

Carrier messages may coordinate work, cite context, and point to receipts. They
do not promote truth and do not replace Steward integration.

## Next Implementation Artifacts

Current first-step artifacts:

1. `ION/03_registry/carrier_capability_registry.yaml`
   - common capability vocabulary;
   - per-carrier support state;
   - proof required for each capability class.

2. `ION/03_registry/mcp_full_carrier_tool_registry.yaml`
   - first full-carrier MCP tool surface;
   - payload limits;
   - artifact transfer policy;
   - carrier-message queue ownership.

3. `ION/07_templates/carriers/FULL_CARRIER_MOUNT_PROOF.md`
   - root proof;
   - carrier profile proof;
   - capability class proof;
   - transport proof;
   - receipt proof.

4. `ION/07_templates/actions/FULL_CARRIER_ACTION_RECEIPT.md`
   - action request;
   - carrier adapter used;
   - ION core surface used;
   - confirmations;
   - files changed;
   - validations run;
   - lifecycle proof.

5. `ION/04_packages/kernel/ion_full_carrier_capability_audit.py`
   - compares ION core capability classes to adapter-exposed tools;
   - separates core failure from adapter failure;
   - emits machine-readable gaps.

6. `ION/tests/test_kernel_ion_full_carrier_capability_audit.py`
   - verifies adapter/core gap classification;
   - verifies V120 limits are recorded as MVP guardrails, not permanent core
     ceilings.

7. `ION/02_architecture/ION_CARRIER_TO_CARRIER_COMMUNICATION_PROTOCOL.md`
   - carrier-message semantics;
   - distinction from operator messages, Steward decisions, and task returns;
   - active queue ownership.

8. Bounded project visibility MCP slice:
   - `ion_file_read`, `ion_file_search`, and `ion_tree_list` expose
     repo-relative project visibility without secret, `.git`, cache, or
     dependency-directory traversal;
   - `ion_registry_read` and `ion_template_read` expose current ION registry and
     template owners directly;
   - `ion_context_compile` returns a bounded full-carrier MCP context projection
     with path and sha256 proof;
   - `ion_receipt_hydrate` reuses the receipt hydration mapper;
   - `ion_tool_manifest` exposes the current connector contract to the carrier.

9. Codex Queue Automation MCP slice:
   - `ion_daemon_status` and `ion_codex_queue_autorun_status` expose bounded
     local queue-runner state;
   - `ion_codex_queue_process_once` can prepare or start processing one existing
     `QUEUED_FOR_CODEX_CARRIER` packet;
   - the owner remains `ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` plus
     `chatgpt_connector/codex_work_requests/` and
     `chatgpt_connector/task_returns/`;
   - run receipts live under
     `ION/05_context/current/chatgpt_connector/codex_queue_runs/`;
   - the command policy is fixed Codex CLI carrier execution only, not arbitrary
     browser-controlled shell.

10. Agent Invocation Broker MCP slice:
   - `ion_agent_list`, `ion_agent_status`, `ion_agent_queue`,
     `ion_agent_result`, `ion_agent_spawn_plan`, and `ion_swarm_status` expose
     role/backend readiness without mutating state;
   - `ion_agent_invoke` compiles a Sev/ChatGPT Browser role request into an
     invocation receipt plus a bounded Codex work request under the existing
     `codex_work_requests/` owner;
   - `ion_swarm_step_once` prepares or starts one queued agent work request by
     calling the existing Codex queue runner, not by opening arbitrary shell;
   - `ion_agent_cancel` may cancel only prepared or queued invocations and does
     not kill active backend processes;
   - role/context owners are `agent_roster_registry.yaml`,
     `agent_context_system_registry.yaml`, the role context cards, Codex CLI
     carrier profile, and `CODEX_CLI_EXECUTION_PACKET.md`;
   - no raw Codex output becomes ION state without the existing task-return
     context proof and template action proof gates;
   - failures are classified as `AGENT_INVOCATION_FAILURE`,
     `BACKEND_CODEX_FAILURE`, `CARRIER_ADAPTER_FAILURE`, `DAEMON_FAILURE`, or
     `ION_CORE_FAILURE`.

This slice improves carrier perception and planning authority. It does not grant
arbitrary shell, arbitrary filesystem mutation, direct patch application,
process control, credential access, git push, or production deployment.

The Codex Queue Automation MCP slice reduces manual operator relay for queued
work. It does not grant arbitrary command execution, production authority, git
push, credential access, direct delete, or direct acceptance of unproofed worker
output. Queue-runner failures must be classified as `CARRIER_ADAPTER_FAILURE`,
`CODEX_CLI_FAILURE`, `DAEMON_FAILURE`, or `ION_CORE_FAILURE`.

Future follow-up artifacts:

1. `ION/03_registry/chatgpt_browser_full_carrier_profile.yaml`
   - ChatGPT browser target profile beyond MVP;
   - non-production default;
   - capability proofs and forbidden direct actions.

2. `ION/docs/setup/CHATGPT_BROWSER_FULL_CARRIER_MCP_PARITY_SETUP.md`
   - staged non-production bring-up path;
   - tunnel/hosted transport requirements;
   - confirmation and receipt workflow;
   - ChatGPT trial procedure.

## Open Questions

- Which capability class should be promoted first after status/read and work
  packet creation: bounded file patch proposal, validation command execution, or
  task-return integration?
- Should ChatGPT browser parity reuse the current `chatgpt_browser` profile or
  introduce a new `chatgpt_browser_full_carrier` profile with an explicit
  migration path?
- Which receipts should be mandatory for every write-class MCP tool versus only
  for lifecycle or shell-adjacent actions?
- How should hosted auth/scopes map to ION carrier profiles without storing
  secrets in the repo?

## Next Lawful Moves

1. Add a carrier capability registry with V120 MVP values and target parity
   values.
2. Add a full-carrier mount proof template.
3. Add an action receipt template for MCP-origin carrier actions.
4. Add a kernel audit that reports `ION_CORE_FAILURE` separately from
   `CARRIER_ADAPTER_FAILURE`.
5. Patch the ChatGPT browser connector policy only after the registry and audit
   prove the next capability class.
