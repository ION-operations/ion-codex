# ION GPT Sandbox Limitations and Fundamentals Improvement Packet

created_at: 2026-05-07T03:59:19+00:00
status: PROPOSAL_WITH_SANDBOX_PATCH_EVIDENCE
carrier: GPT_SANDBOX_CARRIER
production_authority: false
live_execution_authority: false

## Context Proof

Mounted shell root:

```text
/mnt/data/ion_sandbox_limitations_work/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_1
```

Required startup surfaces inspected:

- `ION/REPO_AUTHORITY.md`
- `ION/02_architecture/ION_MOUNT_CONTRACT.md`
- `ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md`
- `ION/03_registry/gpt_sandbox_carrier_profile.yaml`
- `ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md`
- `ION/05_context/current/ACTIVE_WORK_PACKET.json`
- `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`
- `ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md`
- `ION/02_architecture/ION_CARRIER_RUNTIME_FOUNDATION_PROTOCOL.md`
- `ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/ION_CARRIER_TASK_RETURN_INTAKE_PROTOCOL.md`
- `ION/02_architecture/ION_CHATGPT_SANDBOX_RETURN_INTAKE_PROTOCOL.md`
- `ION/tests/test_product_gpt_sandbox_package_readiness.py`

## Template Action Proof

template_id: `ion.template.patch_proposal.v1`
action_id: `gpt_sandbox_limitations_foundation_improvement_20260507T035919Z`
result: `candidate_patch_and_improvement_plan_exported`
touched_paths:

- `ION/03_registry/gpt_sandbox_carrier_profile.yaml`
- `ION/04_packages/kernel/ion_carrier_onboard.py`
- `ION/04_packages/kernel/ion_carrier_continue.py`
- `ION/tests/test_product_gpt_sandbox_package_readiness.py`
- `ION/docs/consolidation/ION_GPT_SANDBOX_LIMITATIONS_AND_FUNDAMENTALS_IMPROVEMENT_PACKET_20260507T035919Z.md`
- `ION/05_context/current/SANDBOX_LIMITATIONS_IMPROVEMENT_PATCH_20260507T035919Z.diff`
- `ION/05_context/current/SANDBOX_LIMITATIONS_IMPROVEMENT_RECEIPT_20260507T035919Z.json`

## Sandbox limitations observed

1. **No background execution.** The carrier cannot promise later work. Every useful act must complete in the current turn or be exported as an artifact/proposal.
2. **Tool execution windows are bounded.** A monolithic full pytest suite may exceed the available execution window. ION needs a declared focused-test envelope for sandbox readiness.
3. **Uploaded zips are mounted through filesystem tools, not file-search.** The package zip is not accessible through document search; it must be extracted and inspected as a filesystem root.
4. **No real external workers were spawned.** The GPT sandbox lane can execute ION role phases sequentially through one carrier. It cannot claim separate Cursor/Codex/MCP agents unless an authorized external adapter actually ran.
5. **Exports are candidate state, not landing.** An updated zip from the sandbox is review material until Steward/human acceptance.
6. **Context budget is real.** Full context bundles are useful but can be too large. Sandbox mode needs compact, role-specific, depth-tiered context packages.
7. **No hidden persistence.** Continuity exists only through uploaded package state, generated receipts, and exported artifacts.
8. **Git/GitHub/live runtime authority is absent in the self-contained package.** The package may contain GitHub or MCP protocols, but this sandbox lane has no direct push/deploy/live execution authority.
9. **Host tool noise can appear in stderr.** The focused pytest run passed, but the host emitted unrelated spreadsheet warmup stderr. Test receipts should separate command exit status from host-environment noise.

## Ambiguity or confusion captured

1. **Capability contradiction.** `gpt_sandbox_carrier_profile.yaml` said the sandbox can run Python validation and write updated package artifacts, while `ACTIVE_WORK_PACKET.json` projected `can_run_tests: false` and `can_edit_files: false`.
2. **MCP contradiction.** The generic active packet defaulted `can_use_mcp: true`, but the self-contained GPT sandbox package does not have live MCP authority.
3. **Mode-label drift.** `ion_carrier_continue` reported mode `manual-cursor` for `GPT_SANDBOX_CARRIER`, which made a GPT sandbox run look like a Cursor/manual lane.
4. **Root ambiguity.** The package has a shell root, content root `ION/`, and nested residue `ION/ION/...`; startup law explains this, but the package should surface it in a single sandbox preflight result.
5. **Tool-read proof ambiguity.** ContextPackages require file-read proof. In this host, that means Python/filesystem inspection rather than a Cursor Task tool or document-search interface.
6. **Design-discussion mutation ambiguity.** The operator classifier marked the sandbox-limitations request as `design_discussion` with `mutates_runtime: false`, but `ion_carrier_continue` still refreshed active packets and emitted a spawn plan. ION should decide whether discussion-class turns are state-refreshing or plan-only by default.
7. **Allowed-path mismatch.** The active allowed paths did not include `ION/03_registry/`, even though the capability fix necessarily touched the GPT sandbox carrier profile. This patch is therefore exported as proposal evidence, not silently accepted landing.
8. **Startup report verdict capture bug.** The prior startup report/proof recorded an initial status command verdict as `ION_TASK_RETURN_ACCEPTED_FOR_STEWARD`, while direct `kernel.ion_status` returns `ION_STATUS_READY`. Report generation should bind verdicts to each command's own JSON response.

## Candidate patch applied inside this sandbox package

The sandbox copy now includes a minimal repair so future `GPT_SANDBOX_CARRIER` runs project the correct capability/mode surface:

- `ion_carrier_onboard.py` now recognizes GPT sandbox aliases when reading registry-backed capabilities.
- `gpt_sandbox_carrier_profile.yaml` now exposes the generic capability keys used by `ACTIVE_WORK_PACKET.json`.
- `ion_carrier_continue.py` now defaults GPT sandbox carriers to mode `gpt-sandbox` instead of `manual-cursor`.
- Product readiness tests now guard the capability projection and mode label.

This is a candidate patch in the exported zip. It should be reviewed before promotion.

## Validation performed

```text
python3 -m pytest \
  ION/tests/test_product_gpt_sandbox_package_readiness.py \
  ION/tests/test_kernel_ion_carrier_continue.py \
  ION/tests/test_kernel_ion_carrier_onboarding_packet.py \
  -q
```

Result:

```text
28 passed in 0.69s
```

Additional smoke checks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_onboard --ion-root . --carrier GPT_SANDBOX_CARRIER --objective "verify GPT sandbox capability projection after patch" --force --json
```

Observed projected capabilities:

```json
{
  "can_read_files": true,
  "can_edit_files": true,
  "can_run_tests": true,
  "can_spawn_carrier_slots": false,
  "can_use_mcp": false,
  "production_authority": false,
  "live_execution_authority": false
}
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier GPT_SANDBOX_CARRIER --operator-message status --max-spawn-rows 0 --json
```

Observed mode:

```text
gpt-sandbox
```

Final status check:

```text
ION_STATUS_READY
```

## Fundamentals improvement plan

### 1. Add a machine-readable sandbox environment contract

Create a carrier-host contract that records observed host constraints separately from ION role authority:

```yaml
host_can_read_uploaded_zip: true
host_can_write_mnt_data_artifacts: true
host_can_run_python_validation: true
host_can_run_full_test_suite: bounded_or_unknown
host_can_spawn_external_agents: false
host_can_use_live_mcp: false
host_can_mutate_github: false
host_can_work_asynchronously: false
```

This should be loaded before active packet capability projection.

### 2. Add a capability reconciliation gate

Before a carrier executes role phases, compare:

```text
carrier registry profile
+ host-observed capabilities
+ active work packet capabilities
+ operator-granted authority
```

If they disagree, ION should emit `CAPABILITY_RECONCILIATION_BLOCKED` or write a review packet. It should not make the carrier infer the truth from contradictory surfaces.

### 3. Add a sandbox startup preflight command

A single command should report:

- shell/content root confirmation;
- nested residue warning;
- active carrier profile;
- projected capabilities;
- mode label;
- allowed paths;
- production/live authority false;
- focused test envelope;
- export/receipt target.

This turns startup from multi-file orientation into a compact proof surface.

### 4. Split sandbox edit capability from production authority

ION needs vocabulary that distinguishes:

```text
can_edit_sandbox_copy: true
can_export_candidate_zip: true
can_patch_live_repo: false
can_push_git: false
can_deploy: false
```

The current `can_edit_files` field is too coarse. It caused part of the ambiguity.

### 5. Add a default focused-test ladder

Sandbox validation should have tiers:

```text
L0 root/status smoke
L1 carrier onboarding + capability reconciliation
L2 context proof / template-action gate
L3 focused package readiness tests
L4 full suite only when time/tool budget permits
```

The status report should say which tier passed, instead of treating full-suite incompletion as vague uncertainty.

### 6. Make design-discussion turns plan-only unless explicitly state-bearing

If the classifier returns `design_discussion` and `mutates_runtime: false`, `ion_carrier_continue` should either avoid refreshing active state or mark the turn as `DISCUSSION_TRACE_ONLY`.

### 7. Add compact context bundles for GPT sandbox

Each role should get:

```text
compact bundle: required law + current objective + exact return contract
expanded bundle: compact + relevant protocols
deep bundle: expanded + historical witnesses
```

This reduces context pressure without weakening authority.

### 8. Repair report/proof capture

Startup report generators should parse each command's JSON independently and store:

```text
command_name
module
returncode
verdict_from_that_command
stdout_hash
stderr_classification
```

This would prevent cross-command verdict contamination.

### 9. Include registry/template paths when the work class is carrier-foundation repair

When the objective concerns carrier limitations, onboarding, or capabilities, allowed paths should include:

```text
ION/03_registry/
ION/07_templates/carriers/
ION/02_architecture/
ION/04_packages/kernel/
ION/tests/
ION/05_context/current/
```

### 10. Export clean packages by default

Generated cache paths such as `__pycache__/` and `.pytest_cache/` should be removed during sandbox export with an explicit `REMOVE_GENERATED_CACHE` receipt.


## Final active-state refresh

After the patch validation, the active carrier turn was refreshed with the user's sandbox-limitations objective and `--max-spawn-rows 0`.

Observed final state:

```text
verdict: ION_STATUS_READY
mode: gpt-sandbox
objective: consider GPT sandbox limitations, note carrier ambiguity/confusion observed during startup, and propose ION fundamentals improvements for better operation within sandbox limits
spawn_queue_count: 0
classification: design_discussion
mutates_runtime_classification: false
```

This preserves the current work as a discussion/proposal packet without requiring role-task returns.

## Steward decision needed

Recommended decision:

```text
REVIEW_PATCH_FOR_ACCEPTANCE
```

The patch is small and validated, but it touches registry and kernel carrier surfaces, so it should not be treated as automatically canon merely because it passed in the sandbox.

## Non-claims

- No production authority was exercised.
- No live external agent was spawned.
- No MCP/GitHub mutation occurred.
- This packet is not final ION law.
- The historical archive was not promoted.
- The full monolithic pytest suite was not rerun after this patch.
