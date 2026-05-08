---
type: research
authority: A3_OPERATIONAL
from: Thoth
created: 2026-04-12T13:05:00-04:00
status: COMPLETE
ratification: NOT_RATIFIED
topic: Active-branch evidence for canonical packet floor vs governed bridge packets and validator coverage
connections:
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/packet_validation.py
  - ION/tests/test_kernel_packet_validation.py
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
  - ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/03_mason_role_chassis_mount.md
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/03_disagreement_escalation.md
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_browser_external_return_drill/04_external_return.md
  - ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/03_thoth_role_chassis_mount.md
---

# Thoth Evidence: Bridge Packet Status On The Active Branch

## Why this exists

Answer the handoff question with **file-anchored facts** on this branch: whether canonical
packet law and the kernel validator already imply **widening** of the canonical packet
family, or whether **governed bridge packets** sit **outside** the narrow canonical floor
until an explicit law decision.

## Sources or surfaces considered

Surfaces assigned in `ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/05_thoth_cursor_handoff.md` plus the Phase 1 proof packets
referenced in `ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md`.

## Findings

### 1. Canonical packet taxonomy on this branch is still exactly five families

`PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md` lists the governed human/executor markdown
families as `task`, `role_session`, `handoff`, `cursor_handoff`, and
`manual_automation_fallback` only:

```40:55:ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
## Canonical packet taxonomy

### 1. `task`
Use for one bounded work assignment.

### 2. `role_session`
Use for one bounded executor/role pass inside a larger run.

### 3. `handoff`
Use for one bounded transfer from one executor/role to another.

### 4. `cursor_handoff`
Use for one IDE/chat-targeted handoff with explicit load order and boundaries.

### 5. `manual_automation_fallback`
Use when the lawful workflow step must be carried manually because an automation carrier is blocked, disabled, unavailable, or intentionally paused.
```

The same protocol warns against silent widening:

```242:243:ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
## Risks / warnings
Do not widen packet taxonomy beyond the canonical families without explicit need.
```

**Observation:** No `role_chassis_mount`, `disagreement_escalation`, or `external_return`
entry appears in this canonical taxonomy block.

### 2. The validator implements only those five types; any other `type` is unsupported

`_RULES` keys in `packet_validation.py` match the five canonical families and nothing else:

```78:114:ION/04_packages/kernel/packet_validation.py
_RULES = {
    "task": WorkflowPacketRule(
        packet_type="task",
        template_name="TASK",
        title_prefix="Mission:",
        required_frontmatter=("type", "agent", "template", "priority", "created", "from", "target"),
        required_sections=("Goal", "Source / Context", "Requirements", "Deliverables", "Constraints", "Completion Signal"),
    ),
    "role_session": WorkflowPacketRule(
        packet_type="role_session",
        template_name="ROLE_SESSION",
        title_prefix="Role Session:",
        required_frontmatter=("type", "template", "created", "status", "role", "objective"),
        required_sections=("Role", "Purpose", "Source Task / Objective", "Required Reads", "Expected Output", "Next Target", "Notes"),
    ),
    "handoff": WorkflowPacketRule(
        packet_type="handoff",
        template_name="HANDOFF",
        title_prefix="Handoff:",
        required_frontmatter=("type", "template", "created", "status", "from", "to", "objective"),
        required_sections=("From", "To", "What was completed", "What remains", "Exact artifacts to read", "Risks / warnings", "Requested next action"),
    ),
    "cursor_handoff": WorkflowPacketRule(
        packet_type="cursor_handoff",
        template_name="CURSOR_HANDOFF",
        title_prefix="Cursor Handoff:",
        required_frontmatter=("type", "template", "created", "status", "target_surface", "objective"),
        required_sections=("Role / chassis target", "Load order", "Exact files to read first", "Task to perform", "Boundaries", "Expected output artifact"),
    ),
    "manual_automation_fallback": WorkflowPacketRule(
        packet_type="manual_automation_fallback",
        template_name="MANUAL_AUTOMATION_FALLBACK",
        title_prefix="Manual Automation Fallback:",
        required_frontmatter=("type", "template", "created", "status", "automation_surface", "reason"),
        required_sections=("Carrier blocked or disabled", "Lawful bounded inputs", "Manual fallback step", "Outputs emitted"),
    ),
}
```

Unknown types fail validation with `UNSUPPORTED_TYPE`:

```387:401:ION/04_packages/kernel/packet_validation.py
    rule = _RULES.get(packet_type)
    if rule is None:
        errors.append(PacketValidationMessage("ERROR", "UNSUPPORTED_TYPE", f"Unsupported packet type: {packet_type!r}."))
        return PacketValidationResult(
            path=(None if path is None else str(path)),
            packet_type=packet_type,
            expected_type=expected_type,
            title=title,
            frontmatter_present=frontmatter_present,
            valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
            frontmatter=frontmatter,
            sections_present=tuple(sections),
        )
```

**Observation:** Bridge packet frontmatter values such as `role_chassis_mount`,
`disagreement_escalation`, and `external_return` are not keys in `_RULES`, so normalized
validation through `validate_packet_text(...)` would classify them as unsupported unless
the law and code are widened later.

### 3. Tests exercise only the five canonical families (plus legacy tolerance)

`ION/tests/test_kernel_packet_validation.py` contains positive-path fixtures for
`role_session`, `handoff`, `cursor_handoff`, and `manual_automation_fallback`, and an
explicit `task` takeover-insufficiency case. There is **no** test case asserting valid
structure for `role_chassis_mount`, `disagreement_escalation`, or `external_return`.

Example bounded `task` fixture text even states **no widening** in constraints:

```294:297:ION/tests/test_kernel_packet_validation.py
## Constraints

- no widening
```

**Observation:** Validator test coverage on this branch aligns with the five-family
floor; it does not encode bridge packet families.

### 4. Live Phase 1 proof packets use bridge `type` values that sit outside the canonical taxonomy

**`ROLE_CHASSIS_MOUNT`** — real filesystem packet from the mount proof feed:

```1:9:ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/03_mason_role_chassis_mount.md
---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
target_role: Mason
chassis: Composer 2 in Cursor IDE
mount_posture: MOUNTED_NOMINAL
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/01_task.md
---
```

**`DISAGREEMENT_ESCALATION`** — drill control packet:

```1:9:ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/03_disagreement_escalation.md
---
type: disagreement_escalation
template: DISAGREEMENT_ESCALATION
created: 2026-04-12T11:44:01-04:00
status: RECONCILED
initiated_by: Codex
disagreement_class: ROLE_MOUNT
subject: Browser ChatGPT direct-role mount versus external-unmounted default for Phase 1
primary_artifact: ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/05_browser_external_unmounted_role_chassis_mount.md
---
```

**`EXTERNAL_RETURN`** — zip-return drill packet:

```1:11:ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_browser_external_return_drill/04_external_return.md
---
type: external_return
template: EXTERNAL_RETURN
created: 2026-04-12T11:49:46-04:00
status: RETURNED
from: browser-class external carrier
source_chassis: browser_class_simulated
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_browser_external_return_drill/03_browser_external_handoff.md
workspace_snapshot: ION/05_context/history/external_returns/2026-04-12_phase1_browser_mount_boundary_readonly_snapshot.zip
target_owner: Codex
targets:
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/README.md
---
```

Current onboarding also records Thoth’s mount with the same bridge `type`:

```1:9:ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/03_thoth_role_chassis_mount.md
---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T12:55:19-04:00
status: COMPLETE
target_role: Thoth
chassis: Composer 2 in Cursor IDE
mount_posture: MOUNTED_DEGRADED
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/01_task.md
---
```

### 5. Bridge protocols are explicitly provisional relative to final canon

`ROLE_CHASSIS_MOUNT_PROTOCOL.md`, `DISAGREEMENT_ESCALATION_PROTOCOL.md`, and
`EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md` each declare `bridge_status: PROVISIONAL_BRIDGE`
and `canon_status: NOT_FINAL_CANON` in frontmatter (for example lines 8–9 of each file as
read in this session). They **prescribe** use of `ROLE_CHASSIS_MOUNT`,
`DISAGREEMENT_ESCALATION`, and `EXTERNAL_RETURN` as control or return surfaces without
redefining the five-family canonical taxonomy in `PACKET_AND_HANDOFF...`.

**Observation:** Operational law on this branch treats these packets as **current-phase
bridge** mechanisms layered on top of the older canonical floor, not as entries already
merged into that floor.

### 6. Codex’s internal next-workload research states the gap plainly (synthesis, not new ground)

`2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md` already
summarizes the same structural gap; Thoth’s file reads **confirm** its claims against
primary protocol, code, tests, and proof packets (see sections 1–5 above). It frames the
branch choice as widen canonical law/validator **or** keep bridge packets outside the
floor with explicit support surfaces — not as already decided widening:

```103:106:ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md
3. Mason should only implement after the branch decides one of two truthful paths:
   - widen canonical packet law and validator support to include the bridge packets, or
   - explicitly keep the bridge packets outside the canonical validator floor while
     adding the minimum truthful support surface for them.
```

## Implications

- **Fact on this branch:** Canonical taxonomy and `_RULES` remain five-family; bridge
  packets exist as separate `type` values in comms and onboarding **without** being listed
  in `PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md` §Canonical packet taxonomy.
- **Validator coverage:** Matches the five canonical families; bridge families would hit
  `UNSUPPORTED_TYPE` under normalized validation (see Finding 2).
- **Mismatch locus:** Not a silent contradiction inside the validator; it is an **explicit
  layering** of provisional bridge protocols and proof packets on top of an unchanged K2
  canonical floor, until the branch chooses a path (per Codex plan Finding 6).

## Recommended next moves

Recommendations restate `2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md`
§Recommended next moves: bounded archaeology if needed, then one Codex **proposal**
selecting widen vs non-widen, then Mason only after that decision. Thoth adds no new
branch policy beyond that evidence chain.

---

## Direct answer (handoff question)

**Does the active branch already imply packet-family widening, or only a governed bridge
set outside the canonical floor?**

**Only the latter is implied by the primary surfaces on this branch.** The canonical
protocol and validator still define **five** families; bridge packets
(`role_chassis_mount`, `disagreement_escalation`, `external_return`) are **used in comms
and prescribed by provisional bridge protocols** but are **not** incorporated into the
canonical taxonomy block or `_RULES`. **Widening** would be a **future explicit decision**
and implementation, not something already merged into canonical packet law or validator
coverage.
