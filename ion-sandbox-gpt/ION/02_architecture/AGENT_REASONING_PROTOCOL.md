---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-05T09:30:00-04:00
status: ACTIVE
connections:
  - ION/03_registry/boots/STEWARD.boot.md
  - ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
  - ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md
  - ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md
  - ION/07_templates/reports/REASONING_JOURNAL.md
  - ION/07_templates/bindings/CODEX__REASONING_JOURNAL.md
---

# AGENT REASONING PROTOCOL

ION agents do not merely receive files and improvise.
They must reason through a governed chamber that binds:

- role identity and authority,
- the current ContextPackage (or IDE/manual equivalent),
- the active template and template binding,
- the protocol surfaces governing the step,
- recent witnessed timeline state,
- candidate route manifests,
- and explicit confidence / drift / issue reporting.

The goal of this protocol is not "more thinking" in the abstract.
The goal is a bounded, inspectable reasoning window that reduces drift, detects scope mismatch early, and prevents generated continuity from silently self-authorizing the next runtime family.

## 1. Core rule

Every agent step must pass through the same sequence:

1. identity and authority read,
2. ContextPackage / manual-equivalent interpretation,
3. template + binding interpretation,
4. protocol + law constraint check,
5. bounded preflight reasoning,
6. confidence / drift / novelty journal,
7. issue emission when needed,
8. execution,
9. post-action audit,
10. next-step proposal (proposal only, never silent authorization).

## 2. Reasoning chamber inputs

The reasoning chamber may use only the following classes of input for the active step:

### A. Active law-state

- boot document,
- doctrine excerpts,
- role lane authority ceilings,
- governing task / directive,
- active protocol excerpts,
- active template binding.

### B. Active work-state

- ContextPackage or IDE/manual equivalent,
- target files,
- mission / task payload,
- relevant dependencies,
- recent receipts / traces / prior findings explicitly routed into scope.

### C. Timeline witness

Agents may look backward into recent witnessed timeline state, but only through:

- recent receipts,
- recent traces,
- recent continuity deltas,
- unresolved issues,
- recent route decisions already on disk.

Timeline witness exists to reduce drift and detect contradiction.
It does not authorize broad reopening of stale branches without a governing task.

### D. Candidate future routes

Agents may inspect candidate future routes only as hypothetical manifests.
They are not future truth.
They may inform preflight comparison, escalation choices, or stop conditions, but they do not become active continuity until a lawful transition adopts them.

## 3. Required preflight questions

Before execution, the agent must be able to answer:

- Who am I in this step?
- What authority do I have here?
- What artifact class am I inside?
- What am I forbidden to silently decide?
- What is the bounded objective?
- What files or artifacts are actually in scope?
- What evidence or doctrine is load-bearing?
- What template obligations shape the work?
- What protocol constraints or routing ceilings apply?
- What issues, contradictions, or drift risks are already visible?
- Is the next proposed step grounded in doctrine / architecture / prior lineage, or only in generated continuity?

If the agent cannot answer these questions cleanly, the correct next act is issue emission or escalation, not continued expansion.

## 4. Reasoning journal

The governed artifact for this chamber is the `REASONING_JOURNAL` template.
A journal entry may be preflight-only or combined preflight/postflight depending on the step.

Minimum journal fields:

- objective continuity confidence,
- semantic novelty,
- recursion risk,
- grounding sources,
- whether a new abstraction family is being introduced,
- whether a new runtime family is being introduced,
- whether an independent runtime consumer exists,
- issue flags,
- stop / continue / escalate recommendation.

## 5. Required journal triggers

A `REASONING_JOURNAL` is required whenever any of the following are true:

- the step is multi-stage or likely to span multiple "proceed" turns,
- the step introduces or proposes a new runtime family,
- the step deepens witness / retention / policy / maintenance state,
- confidence is degraded,
- recursion risk is medium or high,
- semantic novelty is low,
- the agent sees contradiction between doctrine, protocol, template, or continuity,
- the agent is about to propose the next frontier mainly from generated continuity,
- the agent sees an issue in another agent or subsystem that should be recorded.

## 6. Confidence / drift semantics

The active current phase should use bounded qualitative bands rather than fake precision.
Suggested values:

- confidence: HIGH / MEDIUM / LOW
- semantic novelty: HIGH / MEDIUM / LOW
- recursion risk: LOW / MEDIUM / HIGH
- grounding sufficiency: STRONG / MIXED / WEAK

These fields are not cosmetic.
They are decision inputs for continue / stop / escalate behavior.

## 7. Issue emission classes

The journal does not replace signals.
When the agent detects a material problem, it should emit a short issue signal plus the fuller journal.
Suggested signal classes include:

- `SELF_DRIFT_WARNING`
- `CONTEXT_MISMATCH_WARNING`
- `TEMPLATE_MISMATCH_WARNING`
- `PROTOCOL_MISMATCH_WARNING`
- `AUTOMATION_STATE_WARNING`
- `PEER_LANE_WARNING`
- `RECURSION_RISK_WARNING`

Signals remain short witness surfaces.
The journal is the reasoning artifact.

## 8. Manual IDE mode mapping

Until daemon-owned reasoning windows exist programmatically, the manual equivalent is:

- boot document = identity injection,
- MINI route = scoped context references,
- governing task = mission binding,
- template + binding = artifact law,
- recent trace / receipt artifacts = timeline witness,
- candidate next route listed in continuity = hypothetical route manifest,
- `REASONING_JOURNAL` = explicit reasoning chamber artifact.

## 9. Anti-drift stop rules

The agent must stop and emit a journal instead of extending the lane when any of the following is true:

- repeated naming stems are recursively stacking,
- the proposed next step is a witness-of-witness expansion without a new consumer,
- generated continuity is the main source of authorization,
- the agent can no longer explain why the current axis is still the right axis,
- the step mostly transforms the residue of prior receipts rather than serving a fresh runtime need.

## 10. Current phase rollout

For the active IDE-native build:

- the reasoning chamber is active immediately as operational protocol,
- `REASONING_JOURNAL` is the first explicit artifact surface for it,
- Steward should treat this protocol as mandatory whenever the step is multi-turn, automation-adjacent, or drift-sensitive,
- later daemon work may compile the reasoning chamber programmatically as a first-class runtime bundle.
