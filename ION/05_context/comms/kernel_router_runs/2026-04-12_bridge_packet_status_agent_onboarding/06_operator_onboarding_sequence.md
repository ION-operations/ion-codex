# Operator Onboarding Sequence: Bridge Packet Status Workload

## When to involve the other agents

Involve the support field **now** for the post-Phase-1 workload.

This is the right time because:

- Phase 1 is explicitly closed out
- the next workload begins with archaeology and evidence, not implementation
- that means the first support activations should be read-heavy and contradiction-safe

## Who to involve now

Start now:

1. `Vestige` on Composer 2 chat A
2. `Thoth` on Composer 2 chat B

Hold for later:

3. `Mason` on Composer 2 only after Codex decides whether packet-law widening is
   actually required
4. browser ChatGPT only after there is a bounded compare, witness, or external-return
   pass worth routing outward

## Exact onboarding order

### 1. Vestige

Open Composer 2 chat A and have it read, in this order:

1. `ION/03_registry/boots/VESTIGE.boot.md`
2. `ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/04_vestige_cursor_handoff.md`

Expected output path:

- `ION/06_intelligence/archaeology/vestige/reports/2026-04-12_bridge_packet_family_archaeology.md`

Vestige’s job is archaeology only:

- older-estate precedent
- contradictions
- prior packet or validator patterns

### 2. Thoth

Open Composer 2 chat B and have it read, in this order:

1. `ION/03_registry/boots/THOTH.boot.md`
2. `ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/03_thoth_role_chassis_mount.md`
3. `ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/05_thoth_cursor_handoff.md`

Expected output path:

- `ION/06_intelligence/research/2026-04-12_thoth_bridge_packet_status_evidence.md`

Thoth’s job is active-branch evidence only:

- current packet law
- current validator code
- current tests
- exact mismatch extraction

### 3. Mason

Do **not** start Mason yet.

Wait until Codex has:

- the Vestige archaeology report
- the Thoth evidence report
- one Codex proposal deciding whether bridge packets should widen canonical packet law

If widening is approved, then Mason should be onboarded with a bounded code/test packet
for:

- `ION/04_packages/kernel/packet_validation.py`
- `ION/tests/test_kernel_packet_validation.py`

### 4. browser ChatGPT

Do **not** start browser ChatGPT yet for this workload.

Browser should come in only if one of these becomes true:

- Codex wants a bounded external comparison witness on the law decision
- there is a concrete external-return drill or compare pass worth routing out
- the branch wants one independent external reading of the final proposal before Mason
  implements

If browser is activated later, keep it `EXTERNAL_UNMOUNTED` and onboard it through:

- `EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- one bounded `HANDOFF`
- one bounded snapshot or zip
- one `EXTERNAL_RETURN` plus optional `PATCH_PACKAGE`

## What I need back before the next turn

Ideally:

- Vestige report path
- Thoth report path

At that point Codex can consolidate locally and tell you whether Mason should start.
