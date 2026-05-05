---
type: signal
from: Atlas
topic: musl libc package
created: 2026-04-03
---

# ATLAS — musl libc (`musl`)

**New package:** `ATLAS/systems/musl/` — full schema paths, `sources.yaml` (musl.libc.org + wiki), ledger **msl-001**–**msl-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: c-runtime`); `tag_index` **`c-runtime`** → **`glibc`**, **`musl`**.

**Relations:** **`competes_with`** **`glibc`** (reciprocal **`competes_with`**); **`integrates_with`** **`linux-kernel`**, **`elf`**, **`c-language`**, **`gnu-gcc`**, **`gnu-binutils`**, **`clang`**, **`gnu-gdb`**, **`lldb`** (INFERRED where noted), **`riscv-isa`**, **`docker`** (INFERRED); reciprocals on stack packages.

**Comparative:** `language_machine_and_assembly_stack.md` §5; `ai_operating_system_reference_matrices.md` §9–§10 + **Forbidden merges**; `context_systems_landscape.md`.

**Touch-up:** **`glibc`** `01_scope.md`, `12_relation_map.md`, `relations.json`; **`gnu-gcc`** `01_scope.md`.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — musl wave; **Next waves** userland row updated.

**Witness:** root `ION/CAPSULE.md` **ION-094**; `ION/agents/atlas/CAPSULE.md` **A-054**.
