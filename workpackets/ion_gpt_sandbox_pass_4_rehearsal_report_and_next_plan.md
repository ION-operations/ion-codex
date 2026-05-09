# ION GPT Sandbox Pass 4 Rehearsal Report and Next Plan

## Purpose of this canvas

The sandbox file download links failed, so this document records the full substance of the last output in plain text: what was tested, what was generated, what passed, what was not claimed, and what the next work should be.

This document should be treated as a **report / handoff**, not as accepted ION state. It is meant to preserve the result of the Pass 4 Custom GPT rehearsal so it can be copied, reviewed, or manually transferred into the project.

---

# 1. Current workstream

We corrected the package strategy.

The work is **not** to invent a new tiny pretend ION package.

The work is:

```text
Start from the existing real ION GPT sandbox/custom-GPT package.
Remove development-folder bloat and inherited dogfood state.
Preserve the real ION engine, templates, workflow, runtime law, receipts, context system, and package behavior.
Validate that it still operates as a sandbox Custom GPT version.
```

The meaning of “minimum” is now correctly understood:

```text
Minimum = sandbox-limited execution environment.
Minimum does not mean reduced ION engine.
```

The Custom GPT sandbox version should not rely on unavailable local tools as baseline:

```text
No local IDE baseline.
No Codex CLI baseline.
No MCP baseline.
No gateway baseline.
No browser extension baseline.
No production or live execution authority.
```

But it should still carry enough real ION self-knowledge and operating substrate to act as:

```text
ION’s sandbox lead developer
ION explainer
ION package auditor
ION workflow carrier
ION user/company data ingester
ION receipt/package/diff/friction writer
ION integration guide
```

---

# 2. Package state before Pass 4

The source for Pass 4 was the Pass 3 candidate:

```text
ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_PRUNE_PASS_3_STARTER_STATE_CANDIDATE_20260507.zip
```

That candidate came from the existing real GPT sandbox package, after three subtractive passes.

## Pass 1 summary

Pass 1 removed obvious dogfood run evidence and connector history while preserving operating organs.

Examples removed:

```text
ION/05_context/current/execution_cycles/
ION/05_context/current/chatgpt_connector/
ION/05_context/current/chatops_bridge/
ION/05_context/current/backups/
temporary kernel/tool trace files
```

Pass 1 preserved:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/
ION/03_registry/
ION/04_agents/
ION/04_packages/
ION/07_templates/
ION/tests/
product/custom_gpt_adapter/
product/data_schema/
product/starter_data/
product/package_guides/
```

## Pass 2 summary

Pass 2 removed high-confidence sandbox-irrelevant development surfaces while preserving engine/templates/workflow.

Examples removed:

```text
.cursor/
.vscode/
.github/
product/source_inputs/
product/previous_projection/
old projection/package reports
local-only browser/cursor/local-daemon integration source
selected local-only MCP implementation files
```

Important boundary:

```text
Removing local-only implementation source from the sandbox Custom GPT baseline does not mean those systems are not part of full ION or future local integration packages.
```

## Pass 3 summary

Pass 3 reset inherited dogfood current-state into clean starter state.

It did not remove engine, templates, or workflow.

Examples removed:

```text
ION/05_context/current/task_returns/
ION/05_context/current/startup_test_reports/
ION/05_context/current/github_data_plane/
ION/05_context/current/codex_cli/
ION/05_context/current/single_carrier_sequences/
dogfood audit/connector snapshots
```

Examples reset instead of deleted:

```text
ACTIVE_OPERATOR_MESSAGE_QUEUE.json
ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
ACTIVE_HUMAN_GATE_QUEUE.json
ACTIVE_CARRIER_MESSAGE_QUEUE.json
ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
ACTIVE_STEWARD_INTEGRATION_QUEUE.json
ACTIVE_CURSOR_HOOK_STATE.json
ACTIVE_ROLE_SPAWN_PLAN.json
ACTIVE_CARRIER_TURN_PACKET.json
ACTIVE_WORK_PACKET.json
ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json
ACTIVE_CARRIER_ONBOARDING_PACKET*.json
```

Pass 3 added a starter-state receipt/note so the reset was documented.

---

# 3. Pass 4 objective

Pass 4 was not another pruning pass.

Pass 4 was a **Custom GPT rehearsal**.

The target architecture tested was:

```text
ION self-package inside GPT sandbox
→ first external user/company data simulation
→ source classification
→ user continuity package creation
→ fresh-chat resume from that package
```

The goal was to prove that the pruned sandbox package can support the core demo loop:

```text
ION knows itself
→ user gives company/project data
→ ION builds a user continuity package
→ package can be re-mounted in a fresh chat
```

---

# 4. Template action proof

```yaml
template_id: ion.template.gpt_sandbox_rehearsal.v1
action_id: gpt_sandbox_pass_4_first_user_package_rehearsal_20260507
result: rehearsal_passed
```

This was a sandbox rehearsal, not production execution.

---

# 5. What was simulated

A fictional first external user/company dataset was created for:

```text
Acme Demo Co
```

The demo project was:

```text
Acme Demo Co Intake Studio
```

The purpose of this fictional company dataset was to test whether ION could:

1. Receive new user/company material.
2. Classify source authority.
3. Build a first user-specific continuity package.
4. Record initial state and receipt surfaces.
5. Produce a fresh-chat handoff.
6. Resume from that handoff/package.

---

# 6. Sample company input files

The simulated uploaded user/company materials were:

```text
company_overview.md
current_product_notes.md
customer_call_notes.md
old_roadmap_2024.md
```

The intended classification result was:

```text
company_overview.md       → CURRENT_REFERENCE
current_product_notes.md  → CURRENT_REFERENCE
customer_call_notes.md    → CURRENT_REFERENCE
old_roadmap_2024.md       → HISTORICAL_CONTEXT
```

The important behavior tested here was that old/historical material should not be treated as current authority without user confirmation.

The fresh-chat resume report retained this warning:

```text
old_roadmap_2024.md is historical unless confirmed current.
```

---

# 7. User/company continuity package created in rehearsal

The rehearsal created a demo user/company continuity package.

Because the download link failed, the important structure is recorded here.

The package represented the user/company state, not ION’s self-package.

It included surfaces equivalent to:

```text
MANIFEST / package identity
PROJECT_BRIEF / project identity
CURRENT_STATE / accepted current state
SOURCE_MAP / classified uploaded sources
DECISION_LEDGER / initial decisions found or accepted
OPEN_QUESTIONS / unresolved questions
NEXT_ACTIONS / next recommended packet/action
ARTIFACT_MANIFEST / generated artifact list
CONTEXT_GRAPH_UPDATES / context additions from ingestion
RECEIPTS / initial ingestion receipt
HANDOFF_FOR_NEW_CHAT / fresh-chat continuation instructions
```

The point is the two-layer product model:

```text
1. ION self-package inside the Custom GPT
   The GPT already knows ION and how to operate.

2. User/company continuity package
   The user uploads data, ION creates a package for that user, and future chats resume from it.
```

---

# 8. Fresh-chat resume behavior

The rehearsal then simulated a fresh ION GPT chat re-uploading the user/company continuity package.

The resume mount result was:

```text
Project: Acme Demo Co Intake Studio
Latest receipt: receipt_pass4_initial_ingestion_demo
Next packet: Draft an engagement brief workflow for consultant client intake.
Warning: old_roadmap_2024.md is historical unless confirmed current.
```

This proves the intended user experience:

```text
User opens a fresh ION GPT chat.
User uploads their latest ION user/company package.
ION mounts the package.
ION reports current state, latest receipt, open questions, next action, and warnings.
ION continues from there.
```

---

# 9. Validation performed

The Pass 4 rehearsal validation covered the following checks:

```text
self-package required surface check
ion_status
ion_carrier_continue
user data package zip integrity
required data-package file presence
JSON validity across package
fresh-chat resume mount read
```

The final validation result was:

```text
ION_GPT_SANDBOX_PASS_4_REHEARSAL_READY
```

This means the current pruned GPT sandbox candidate was able to support the rehearsal loop in sandbox.

---

# 10. What Pass 4 did not claim

Pass 4 did **not** claim:

```text
final release readiness
accepted state
production readiness
live execution authority
local file mutation
Codex execution
MCP execution
Gateway execution
browser extension execution
complete package audit
all bloat removed
perfect Custom GPT upload behavior
```

Pass 4 only claimed:

```text
The current pruned GPT sandbox candidate can support the core first-user demo loop in a sandbox rehearsal:
ION self-package → user data ingestion → user continuity package → fresh-chat resume.
```

---

# 11. What artifacts were intended but failed to download

The previous response attempted to provide these downloadable artifacts:

```text
ION_GPT_SANDBOX_PRUNE_PASS_4_CUSTOM_GPT_REHEARSAL_RETURN_20260507.md
ION_PASS4_DEMO_USER_COMPANY_PACKAGE_ACME_20260507.zip
ION_PASS4_FRESH_CHAT_RESUME_MOUNT_REPORT_20260507.md
ION_GPT_SANDBOX_PASS_4_REHEARSAL_VALIDATION_20260507.json
ION_PASS4_SAMPLE_COMPANY_INPUTS_20260507.zip
```

Because sandbox downloads failed, this canvas preserves the substantive contents and conclusions.

---

# 12. Current state of the package process

The process is now on the right track:

```text
Start from existing real GPT sandbox ION package.
Prune only proven bloat.
Preserve ION engine/templates/workflow.
Reset dogfood state into starter state.
Validate sandbox mount/continue.
Rehearse first-user package creation and resume.
```

The current candidate is approximately:

```text
ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_PRUNE_PASS_3_STARTER_STATE_CANDIDATE_20260507.zip
```

with Pass 4 rehearsal evidence showing the core demo flow works in principle.

---

# 13. Next planned work

## Pass 5 — Custom GPT upload/readiness audit

Goal:

```text
Verify the package is ready to be uploaded/configured as a Custom GPT knowledge package.
```

Checks:

```text
Is GPT Builder instruction surface clear?
Are knowledge files too numerous or too large?
Which files should be uploaded as GPT Knowledge?
Which files should remain inside downloadable package only?
Does the package contain a clear START HERE for the GPT carrier?
Does it instruct the GPT to operate in sandbox mode only?
Does it prohibit claims of local/Codex/MCP execution as baseline?
```

Output should be:

```text
CUSTOM_GPT_UPLOAD_PLAN.md
KNOWLEDGE_FILE_SELECTION_MANIFEST.json
CUSTOM_GPT_CONFIGURATION_CHECKLIST.md
```

## Pass 6 — Final bloat review / uncertain file queue

Goal:

```text
Review remaining files that may still be removable, but do not delete anything uncertain.
```

Classifications:

```text
KEEP_ENGINE
KEEP_TEMPLATE
KEEP_WORKFLOW
KEEP_SANDBOX_RUNTIME
KEEP_PACKAGE_SCHEMA
KEEP_STARTER_DATA
KEEP_TEST_OR_AUDIT
KEEP_GUIDE
REVIEW_UNCERTAIN
REMOVE_PROVEN_BLOAT
```

Output should be:

```text
REMAINING_FILE_CLASSIFICATION_MANIFEST.json
UNCERTAIN_FILE_REVIEW_QUEUE.csv
PASS_5_OR_6_REMOVAL_MANIFEST.json if removals occur
```

## Pass 7 — Real Custom GPT rehearsal with actual package upload

Goal:

```text
Use the candidate package in the actual Custom GPT setup if possible, or emulate as closely as possible.
```

Test user flow:

```text
fresh project start
upload user/company data
classify data
create user package
record receipt
fresh chat resume from package
```

Expected result:

```text
ION_SANDBOX_CUSTOM_GPT_RELEASE_CANDIDATE_READY
```

Only after this should a final candidate be named.

---

# 14. Correct package philosophy going forward

Do not invent a new package.

Do not write a tiny pretend ION.

Do not remove engine/templates/workflow.

Do not call a spec an engine.

Correct rule:

```text
Minimum GPT demo = full ION sandbox operating substrate + minimal sandbox execution assumptions + clean starter state.
```

What gets minimized:

```text
external tool assumptions
dev-folder sediment
dogfood state
old package residue
local-only runtime expectation
```

What does not get minimized:

```text
ION engine
ION templates
ION workflow
ION mount law
ION context system
ION receipts/proof gates
ION package behavior
```

---

# 15. Short handoff summary

```text
Pass 4 tested the current pruned GPT sandbox ION package as a Custom GPT-style self-package.
A fictional company dataset was ingested.
ION classified sources, created a user/company continuity package, recorded initial state, and simulated fresh-chat resume.
The resume report successfully mounted project name, latest receipt, next packet, and stale-source warning.
Validation result: ION_GPT_SANDBOX_PASS_4_REHEARSAL_READY.
Next work: Custom GPT upload/readiness audit and remaining file classification, not speculative rebuilding.
```

---

# 16. Non-claims for this canvas

This canvas is not accepted state.

It does not prove final release readiness.

It does not include the actual zip contents because file download failed.

It preserves the Pass 4 report and next plan in text form so the work is not lost.

