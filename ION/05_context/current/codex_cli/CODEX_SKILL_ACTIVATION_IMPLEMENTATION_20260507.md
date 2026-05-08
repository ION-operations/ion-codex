# Codex Skill Activation Implementation

date: 2026-05-07
status: IMPLEMENTED
authority: non-production, non-live

## Decision

ION skills are now modeled as controlled workflow activation. Templates remain
the proof contracts. A skill may select context, model posture, template refs,
and UI projection, but it cannot grant state acceptance.

## Implemented Surfaces

- `ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md`
- `ION/03_registry/ion_skill_registry.yaml`
- `ION/04_packages/kernel/ion_skill_activation.py`
- `ION/04_packages/kernel/ion_dual_codex_chat.py`
- `ION/04_packages/kernel/ion_codex_chat_app_ui.py`
- `ION/04_packages/kernel/ion_codex_solo_context.py`
- `ION/tests/test_kernel_ion_skill_activation.py`
- `ION/tests/test_kernel_ion_dual_codex_chat.py`
- `ION/tests/test_kernel_ion_codex_solo_context.py`

## Behavior

The Codex Chat model now exposes a `skills` surface and current activation.
Normal chat selects `codex-chat-answer`. Run-task queueing selects
`codex-solo-work`. Recovery language selects `codex-recovery`. The ION lane
selects `ion-full-workflow-handoff`. Template/skill governance language selects
`template-curation`.

Each user turn can carry a skill activation record. The turn trace now shows a
`skill_activation` event. The right inspector includes a Skills drawer with the
current skill, active template gates, registered skills, and the explicit
`state_acceptance_granted: false` boundary.

Queued Codex work packets now include a skill activation section before the
context policy. This makes the queued worker see which skill activated the work
without treating that skill as proof.

## Validation

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_skill_activation.py ION/tests/test_kernel_ion_codex_solo_context.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_local_cockpit_app.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
42 passed
```

## Non-Claims

This does not grant production authority, live execution authority, secrets
authority, git push authority, or state acceptance. It is an activation and UI
projection layer under existing template proof gates.
