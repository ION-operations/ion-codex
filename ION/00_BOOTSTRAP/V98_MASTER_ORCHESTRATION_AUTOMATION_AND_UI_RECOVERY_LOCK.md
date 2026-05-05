# V98 Master Orchestration, Automation, and UI Recovery Lock

**Date:** 2026-05-01  
**Lock:** `V98_MASTER_ORCHESTRATION_AUTOMATION_AND_UI_RECOVERY_PLAN`  
**Authority posture:** non-production recovery lock.

This lock records the recovery direction after the V97 lead-dev survival audit.

V98 establishes that the next ION phase must bind four survival obligations:

```text
1. autonomous loop proof;
2. template-action gate enforcement;
3. Steward integration as executable state transition;
4. cockpit/UI visibility as required proof surface.
```

No future branch may treat the UI as optional. The JOC/cockpit is required because the operator must be able to see ION working, see why it stopped, and see whether work was accepted/rejected by proof gates.

No future branch may treat Cursor Auto mode as the primary carrier. Cursor may remain an editor, extension host, MCP client, or optional carrier slot after the local autonomous loop exists.

The next implementation target remains:

```text
ION/04_packages/kernel/ion_autonomous_loop.py
ION/04_packages/kernel/ion_template_action_gate.py
ION/04_packages/kernel/ion_steward_integrate.py
```

The core survival proof remains:

```text
one command → one goal → template-bound loop → proof gates → Steward integration → receipt → visible cockpit state
```
