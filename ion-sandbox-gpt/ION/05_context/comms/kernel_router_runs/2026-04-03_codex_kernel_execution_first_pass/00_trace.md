workstream: implementation
objective: Implement the first bounded kernel execution helper for returned commit-delta materialization
required_surfaces_ok: True

1. codex — classify the task and prepare the scoped implementation route
   - codex.boot: ION/03_registry/boots/CODEX.boot.md
   - codex.private_mini: ION/agents/codex/MINI.md
   - codex.private_capsule: ION/agents/codex/CAPSULE.md
   - codex.directive.1: ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
   - codex.inbox: ION/05_context/inbox/codex_* [optional]
   - codex.signals: ION/05_context/signals
   - codex.projection.MINI.md: ION/MINI.md [optional]
   - codex.projection.STATUS.md: ION/STATUS.md [optional]
   - codex.projection.CAPSULE.md: ION/CAPSULE.md [optional]
   - codex.extra.1: ION/04_packages/kernel/dispatch.py [optional]
   - codex.extra.2: ION/06_intelligence/specs/T01_TransitionSchema.spec.md [optional]
   - codex.extra.3: ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md [optional]
   - codex.extra.4: ION/06_intelligence/research/2026-04-03_codex_kernel_dispatch_first_pass.md [optional]
   - codex.extra.5: ION/07_templates/bindings/CODEX__CODE.md [optional]

2. vizier — define scope, dependencies, and required review posture
   - vizier.boot: ION/03_registry/boots/VIZIER.boot.md
   - vizier.private_mini: ION/agents/vizier/MINI.md
   - vizier.private_capsule: ION/agents/vizier/CAPSULE.md
   - vizier.directive.1: ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
   - vizier.inbox: ION/05_context/inbox/vizier* [optional]
   - vizier.signals: ION/05_context/signals
   - vizier.projection.MINI.md: ION/MINI.md [optional]
   - vizier.projection.STATUS.md: ION/STATUS.md [optional]
   - vizier.projection.CAPSULE.md: ION/CAPSULE.md [optional]
   - vizier.extra.1: ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md [optional]

3. mason — execute the bounded implementation slice
   - mason.boot: ION/03_registry/boots/MASON.boot.md
   - mason.private_mini: ION/agents/mason/MINI.md
   - mason.private_capsule: ION/agents/mason/CAPSULE.md
   - mason.directive.1: ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
   - mason.inbox: ION/05_context/inbox/mason_* [optional]
   - mason.signals: ION/05_context/signals
   - mason.projection.MINI.md: ION/MINI.md [optional]
   - mason.projection.STATUS.md: ION/STATUS.md [optional]
   - mason.projection.CAPSULE.md: ION/CAPSULE.md [optional]
   - mason.extra.1: ION/07_templates/bindings/MASON__CODE.md [optional]

4. vice — apply risk pressure if the slice affects continuity or governance
   - vice.boot: ION/03_registry/boots/VICE.boot.md
   - vice.private_mini: ION/agents/vice/MINI.md
   - vice.private_capsule: ION/agents/vice/CAPSULE.md
   - vice.directive.1: ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
   - vice.signals: ION/05_context/signals
   - vice.projection.MINI.md: ION/MINI.md [optional]
   - vice.projection.STATUS.md: ION/STATUS.md [optional]
   - vice.projection.CAPSULE.md: ION/CAPSULE.md [optional]

5. nemesis — audit or verify when the slice becomes release-sensitive
   - nemesis.boot: ION/03_registry/boots/NEMESIS.boot.md
   - nemesis.private_mini: ION/agents/nemesis/MINI.md
   - nemesis.private_capsule: ION/agents/nemesis/CAPSULE.md [optional]
   - nemesis.directive.1: ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
   - nemesis.signals: ION/05_context/signals
   - nemesis.projection.MINI.md: ION/MINI.md [optional]
   - nemesis.projection.STATUS.md: ION/STATUS.md [optional]
   - nemesis.projection.CAPSULE.md: ION/CAPSULE.md [optional]
   - nemesis.extra.1: ION/07_templates/bindings/NEMESIS__AUDIT.md [optional]
