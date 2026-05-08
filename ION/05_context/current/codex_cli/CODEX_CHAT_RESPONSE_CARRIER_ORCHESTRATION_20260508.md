# Codex Chat Response Carrier Orchestration

date: 2026-05-08
status: PLANNED
authority: non-production, non-live
active_root: /home/sev/ION - Production/ION_CODEX FULL

## Purpose

Build the real GPT-5.5 Codex chat response path under the current Codex Chat
Engine. This is the next functionality step after the engine contract.

The user-facing outcome is simple: when Sev sends a normal message in the
Codex Capsule chat, the app should receive a real Codex CLI generated assistant
response, not a placeholder local contract.

## Current State

Already implemented:

- Capsule is the minimum working context.
- Mini is a pasteable lookup and receipt index, not the primary prompt.
- Skill activation selects the active workflow.
- Native ION lenses are selected as support lenses.
- Model moves select GPT-5.5 / GPT-5.3-Codex / GPT-5.3-Codex-Spark with
  reasoning effort.
- Queued implementation work already uses the existing Codex queue runner.
- The cockpit is reachable locally and through `https://ion.helixion.net`,
  with cockpit login/token protection.

Missing:

- `respond_only` chat turns do not yet invoke a real Codex CLI response
  carrier.
- The assistant turn still uses the local `assistant_response` contract.
- No response-only run artifact exists for prompt, stdout, stderr, event
  capture, final message, model move, and safety status.

## Design Principle

Do not create a second ION system. Add a response carrier under the existing
Codex Chat Engine.

```text
operator message
-> record_chat_turn
-> build_codex_chat_engine_turn
-> selected skill + native lenses + model move
-> response carrier run
-> Codex CLI final message
-> assistant turn
-> trace + run artifact
-> optional Capsule settlement only when material
```

Normal chat should feel like ChatGPT/Codex chat. ION internals should remain
available in trace/drawers, not forced into every visible answer.

## Proposed Files

New:

- `ION/04_packages/kernel/ion_codex_chat_response_carrier.py`
- `ION/tests/test_kernel_ion_codex_chat_response_carrier.py`
- response run artifacts under
  `ION/05_context/current/codex_capsule_chat/response_runs/`

Modify:

- `ION/04_packages/kernel/ion_dual_codex_chat.py`
- `ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py`
- `ION/04_packages/kernel/ion_codex_chat_app_ui.py`
- `ION/tests/test_kernel_ion_dual_codex_chat.py`
- `ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py`

Possibly modify, only if needed:

- `ION/04_packages/kernel/ion_codex_model_moves.py`
- `ION/03_registry/codex_cli_model_move_policy.yaml`
- `ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md`

## Carrier Module Contract

`ion_codex_chat_response_carrier.py` should expose:

```python
build_chat_response_prompt(...)
prepare_codex_chat_response_run(...)
run_codex_chat_response_carrier(...)
build_chat_response_carrier_status(...)
```

The run result should expose:

```yaml
schema_id: ion.codex_chat_response_carrier_run.v1
ok:
status:
run_id:
run_dir:
prompt_path:
stdout_path:
stderr_path:
latest_return_path:
events_path:
selected_model:
selected_reasoning_effort:
response_text:
response_sha256:
chat_engine_turn:
skill_activation:
native_lenses:
production_authority: false
live_execution_authority: false
provider_api_dispatch_authorized: false
state_acceptance_granted: false
```

## Prompt Contract

The carrier prompt should include:

- active root and old-root warning;
- Capsule minimum context;
- Mini lookup summary;
- selected context package refs;
- current operator message;
- chat engine response mode;
- selected skill;
- selected native lenses;
- selected model move;
- visible-answer rules;
- proof and authority boundaries.

Visible-answer rules:

- answer Sev directly;
- do not force ION internals into the visible answer unless asked;
- do not expose hidden chain of thought;
- include concise file references when useful;
- do not claim files were changed unless they were changed and verified;
- do not claim state acceptance, production readiness, or live authority;
- ask one concise clarifying question only when needed.

## Execution Policy

Use Codex CLI as the carrier. Do not call provider APIs directly from Python.

Initial command shape:

```text
codex exec -m gpt-5.5 -c model_reasoning_effort=<effort> --output-last-message <latest_return_path>
```

Before implementation, check current local `codex exec --help` and select the
least permissive usable sandbox for response-only chat. Preferred order:

1. read-only sandbox, if supported;
2. workspace-write sandbox with prompt-level no-write policy and post-run dirty
   worktree inspection;
3. refuse live response carrier if neither can be bounded.

Response-only chat should not edit repo files. The only expected writes are
state/run artifacts created by the parent Python carrier and the appended chat
assistant turn.

## Integration Plan

1. Add carrier module with pure prompt/run-packet builders first.
2. Add unit tests with fake output. Do not invoke live Codex in unit tests.
3. Integrate `record_chat_turn` so `respond_only` can call the carrier.
4. Preserve fallback: if the carrier is disabled or fails, append a clear
   local fallback assistant turn and record the carrier finding.
5. Add a model/UI trace event named `codex_chat_response_carrier`.
6. Add cockpit JSON support so `/cockpit/chat/turn` returns the actual assistant
   response and carrier metadata when requested with JSON.
7. Add service smoke tests with carrier disabled and fake carrier enabled.
8. Run one live authenticated local smoke only after the offline test slice is
   green.

## Configuration

Suggested environment switches:

```text
ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED=1
ION_CODEX_CHAT_RESPONSE_CARRIER_START_MODE=foreground
ION_CODEX_CHAT_RESPONSE_CARRIER_TIMEOUT_SECONDS=240
ION_CODEX_CHAT_RESPONSE_CARRIER_CAPTURE_JSON=1
```

Default development behavior may keep the live carrier disabled until the test
slice passes. The cockpit should clearly show whether live response carrier is
enabled.

## Transparency Model

Store and expose:

- response carrier run status;
- selected model and reasoning effort;
- prompt path;
- final response path;
- stdout/stderr paths;
- JSON/event path if available;
- summarized tool/file activity when available;
- failure classification.

Do not expose:

- secrets;
- bearer tokens;
- session cookies;
- hidden chain of thought;
- unrestricted filesystem data;
- provider credentials.

## Validation Gates

Offline tests:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_chat_response_carrier.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
```

Focused system slice:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_chat_engine.py ION/tests/test_kernel_ion_skill_activation.py ION/tests/test_kernel_ion_codex_solo_context.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_codex_queue_runner.py ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py ION/tests/test_kernel_ion_local_cockpit_app.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py ION/tests/test_kernel_ion_codex_chat_response_carrier.py -q
```

Service smoke:

```text
systemctl --user restart ion-mcp-preview.service
systemctl --user is-active ion-mcp-preview.service
curl -fsS http://127.0.0.1:8765/health
curl -sS -D - -o /tmp/ion_chat_response_probe.html http://127.0.0.1:8765/cockpit/chat
```

Live authenticated smoke, after offline green:

```text
POST /cockpit/chat/turn
lane_id=codex_general
execution_mode=respond_only
message="Summarize the current Capsule status and next lawful action."
```

Acceptance criteria:

- assistant response is generated by Codex CLI final message, not local
  placeholder text;
- response uses Capsule context correctly;
- response is concise and user-facing;
- run artifact is present;
- model move is recorded as GPT-5.5 unless routing chooses otherwise;
- no production/live/secrets authority is claimed;
- no unexpected repo edits occur;
- public cockpit still requires auth.

## Rollback

Keep the current local response contract as fallback. If carrier integration is
bad, disable:

```text
ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED=0
```

and the chat should continue using the existing local response contract.

## Non-Goals

This pass should not:

- redesign the UI;
- build a second chat;
- replace the existing Codex queue runner;
- change full ION Relay/Steward authority;
- add provider API calls outside Codex CLI;
- make every Codex CLI instance inherit Capsule context globally;
- grant production, live execution, secrets, git push, deployment, or state
  acceptance authority.
