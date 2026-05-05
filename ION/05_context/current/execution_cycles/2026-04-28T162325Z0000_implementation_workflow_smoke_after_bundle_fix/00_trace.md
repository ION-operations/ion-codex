workstream: implementation
objective: workflow smoke after bundle fix
required_surfaces_ok: True

1. steward — classify the task and prepare the scoped implementation route
   - steward.boot: ION/03_registry/boots/STEWARD.boot.md
   - steward.private_mini: ION/agents/steward/MINI.md
   - steward.private_capsule: ION/agents/steward/CAPSULE.md
   - steward.inbox: ION/05_context/inbox/steward_* [optional]
   - steward.signals: ION/05_context/signals
   - steward.projection.MINI.md: ION/MINI.md [optional]
   - steward.projection.STATUS.md: ION/STATUS.md [optional]
   - steward.projection.CAPSULE.md: ION/CAPSULE.md [optional]

2. vizier — define scope, dependencies, and required review posture
   - vizier.boot: ION/03_registry/boots/VIZIER.boot.md
   - vizier.private_mini: ION/agents/vizier/MINI.md
   - vizier.private_capsule: ION/agents/vizier/CAPSULE.md
   - vizier.inbox: ION/05_context/inbox/vizier* [optional]
   - vizier.signals: ION/05_context/signals
   - vizier.projection.MINI.md: ION/MINI.md [optional]
   - vizier.projection.STATUS.md: ION/STATUS.md [optional]
   - vizier.projection.CAPSULE.md: ION/CAPSULE.md [optional]

3. mason — execute the bounded implementation slice
   - mason.boot: ION/03_registry/boots/MASON.boot.md
   - mason.private_mini: ION/agents/mason/MINI.md
   - mason.private_capsule: ION/agents/mason/CAPSULE.md
   - mason.inbox: ION/05_context/inbox/mason_* [optional]
   - mason.signals: ION/05_context/signals
   - mason.projection.MINI.md: ION/MINI.md [optional]
   - mason.projection.STATUS.md: ION/STATUS.md [optional]
   - mason.projection.CAPSULE.md: ION/CAPSULE.md [optional]

4. vice — apply risk pressure if the slice affects continuity or governance
   - vice.boot: ION/03_registry/boots/VICE.boot.md
   - vice.private_mini: ION/agents/vice/MINI.md
   - vice.private_capsule: ION/agents/vice/CAPSULE.md
   - vice.signals: ION/05_context/signals
   - vice.projection.MINI.md: ION/MINI.md [optional]
   - vice.projection.STATUS.md: ION/STATUS.md [optional]
   - vice.projection.CAPSULE.md: ION/CAPSULE.md [optional]

5. nemesis — audit or verify when the slice becomes release-sensitive
   - nemesis.boot: ION/03_registry/boots/NEMESIS.boot.md
   - nemesis.private_mini: ION/agents/nemesis/MINI.md
   - nemesis.private_capsule: ION/agents/nemesis/CAPSULE.md [optional]
   - nemesis.signals: ION/05_context/signals
   - nemesis.projection.MINI.md: ION/MINI.md [optional]
   - nemesis.projection.STATUS.md: ION/STATUS.md [optional]
   - nemesis.projection.CAPSULE.md: ION/CAPSULE.md [optional]
