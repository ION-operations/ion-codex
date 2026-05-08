---
protocol_id: ion.context_authority_team.protocol.v1
status: ACTIVE_OPERATIONAL_LAW
rank: A2_CONTEXT_AUTHORITY
created: 2026-04-28
supersedes:
  - stale-mini-capsule-primary-context-onboarding
  - boot-file-path-list-as-context
owned_by:
  - role.ionologist
  - role.context_cartographer
  - role.runtime_cartographer
  - role.canon_librarian
  - role.template_curator
---

# ION Context Authority Team Protocol

## 1. Problem statement

ION cannot be correctly operated by handing an agent a boot file, a small context note, or a legacy `MINI.md` / `CAPSULE.md` and expecting the host model to recursively discover the living system. That pattern is the exact failure mode seen in Cursor carrier work: a worker reads the file that names the context but does not actually load the context.

ION context is not a pointer list. ION context is a governed, role-specific, evolving context package compiled from the living context graph, role law, current branch state, templates, receipts, and task objective.

## 2. Governing invariant

Every ION agent receives a unique, high-detail, role-evolving context package compiled for its mission and authority ceiling. The package must contain enough actual loaded material for the agent to operate without pretending that path awareness equals comprehension.

A context package is nonconformant when it only says “read these files,” “use the boot,” “see the mini,” or “continue from capsule.” Paths may be included as provenance and proof anchors, but the working package must also contain the role-relevant distilled content, scope constraints, current deltas, stale-surface warnings, and return contract.

## 3. Supersession of stale context surfaces

The following surfaces are not primary context authority:

- root `ION/MINI.md`
- root `ION/CAPSULE.md`
- root `ION/STATUS.md`
- private `ION/agents/{role}/MINI.md`
- private `ION/agents/{role}/CAPSULE.md`
- release-candidate capsule prose
- boot files used as link lists

Those surfaces may remain as historical witnesses, UI/operator projections, receipt artifacts, or donor-material references. They may not be treated as the agent's living context source unless promoted into a current High-Detail Agent Context Package with a receipt.

## 4. ION Context Authority Team

The ION Context Authority Team is a standing specialist set responsible for ION’s own self-context: what ION is, how it runs, what is current, what is historical, which terms are stale, and how agent-specific context packages evolve.

### 4.1 IONOLOGIST

The IONOLOGIST owns reconstructive understanding of ION itself. It maintains the current “what ION is and how ION runs” corpus, true-name/semantic corrections, anti-drift definitions, and the difference between metaphor, historical lineage, and live authority.

The IONOLOGIST answers: **What is ION, exactly, in the current branch?**

### 4.2 CONTEXT_CARTOGRAPHER

The CONTEXT_CARTOGRAPHER owns the context graph-to-package operation. It compiles High-Detail Agent Context Packages, context-load receipts, context deltas, role package lineage, and proof requirements.

The CONTEXT_CARTOGRAPHER answers: **What context does this exact agent need, and what loaded material proves it received it?**

### 4.3 RUNTIME_CARTOGRAPHER

The RUNTIME_CARTOGRAPHER owns the live run map: shell root, carrier limits, kernel/scheduler route, role phase sequence, spawn semantics, context-proof gates, validation commands, and host-specific execution constraints.

The RUNTIME_CARTOGRAPHER answers: **How does ION actually run here, on this carrier, with these limits?**

### 4.4 CANON_LIBRARIAN

The CANON_LIBRARIAN owns branch lineage and authority classification. It distinguishes current, donor, archived, projection, receipt, deprecated, and false-primary surfaces; it prevents older branches or legacy concepts from silently re-crowning themselves.

The CANON_LIBRARIAN answers: **Which source is live authority, which is donor evidence, and which is stale?**

### 4.5 TEMPLATE_CURATOR

The TEMPLATE_CURATOR owns the template layer that makes context evolution operational. It maintains `ION/07_templates/` surfaces for agent context packages, context deltas, load proofs, specialist returns, and package evolution receipts.

The TEMPLATE_CURATOR answers: **What template makes this context action lawful, repeatable, and checkable?**

## 5. Required routing trigger

Route through this team whenever work concerns any of these topics:

- what ION is;
- how ION runs;
- carrier mount, Cursor mount, MCP mount, scheduler, kernel, or spawn law;
- branch consolidation, donor comparison, authority lineage, stale branch detection;
- context package generation, context graph evolution, agent onboarding, role boots;
- mini/capsule retirement, projection demotion, stale-name collapse;
- template restoration, template binding, context package schema;
- any change that would alter what future agents receive as context.

## 6. High-Detail Agent Context Package contract

A High-Detail Agent Context Package must include:

1. `package_id`, `role_id`, `mission_id`, `package_class`, and `authority_ceiling`.
2. The current role identity and exact operating boundary.
3. The live ION definition relevant to the role.
4. The relevant kernel/scheduler/carrier run map.
5. The actual compressed/quoted content the agent must know; not just paths.
6. Required source paths with checksums and authority posture.
7. Stale-surface warnings, especially old `MINI/CAPSULE` and old branch names.
8. Allowed write scope and forbidden write scope.
9. The expected return contract.
10. A context-load proof requirement beginning with `### CONTEXT PROOF`.
11. A context-delta/evolution section showing what changed since the prior package.
12. A receipt path under `ION/05_context/signals/` or `ION/05_context/current/context_packages/`.

## 7. Context package classes

- `ROLE_BASE_CONTEXT_PACKAGE`: durable role identity, law, permissions, and core ION knowledge.
- `MISSION_CONTEXT_PACKAGE`: task-specific context for one bounded objective.
- `DELTA_CONTEXT_PACKAGE`: update package created when ION evolves.
- `RECOVERY_CONTEXT_PACKAGE`: branch/donor/historical reconstruction package.
- `CARRIER_CONTEXT_PACKAGE`: host-specific package for Cursor, ChatGPT, Codex, Claude, Gemini, MCP, shell, or other carrier limits.

## 8. Context evolution loop

When ION evolves, the team performs this loop:

1. IONOLOGIST identifies semantic impact.
2. CANON_LIBRARIAN classifies affected sources and retires stale authority claims.
3. TEMPLATE_CURATOR updates templates/bindings when the context action shape changes.
4. CONTEXT_CARTOGRAPHER updates affected High-Detail Agent Context Packages and writes package lineage.
5. RUNTIME_CARTOGRAPHER validates that carrier/kernel/scheduler routes can deliver the new packages.
6. STEWARD integrates or rejects the update.
7. RELAY reports the accepted delta to the operator.

## 9. Carrier enforcement

A carrier must not spawn a role from a boot file alone. It must spawn from a context package. If a host can only paste a prompt, the prompt must contain the actual package body. If a host can attach files, the attached files must still be checked by context-load proof.

A worker response that only says “I have context” is rejected. A worker response that begins with `### CONTEXT PROOF`, names the required files, provides excerpts or section summaries, and passes the relevant proof gate may be accepted as loaded state.

## 10. Acceptance condition

This protocol is operating only when all of the following are true:

- `ION/03_registry/ion_context_authority_team_registry.yaml` exists.
- `ION/07_templates/context/AGENT_CONTEXT_PACKAGE.md` exists.
- `ION/07_templates/context/ION_CONTEXT_DELTA_RECEIPT.md` exists.
- `ION/04_packages/kernel/ion_context_authority_team_audit.py` accepts the root.
- Future role spawns refer to High-Detail Agent Context Packages rather than stale mini/capsule surfaces.
