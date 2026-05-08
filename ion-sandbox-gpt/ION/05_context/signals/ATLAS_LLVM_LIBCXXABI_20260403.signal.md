---
type: signal
from: Atlas
topic: LLVM libc++abi (llvm-libcxxabi) package
created: 2026-04-03
---

# ATLAS — LLVM libc++abi (`llvm-libcxxabi`)

**New package:** `ATLAS/systems/llvm-libcxxabi/` — full schema paths, `sources.yaml` (libcxxabi.llvm.org + llvm-project), ledger **lcxa-001**–**lcxa-003**.

**Taxonomy:** **`cxx-abi-runtime`** in `tag_taxonomy.yaml` + `tag_index.yaml`; `systems_index` **primary_kind** **`cxx-abi-runtime`**.

**Relations:** **`integrates_with`** **`llvm-libcxx`**, **`clang`**, **`llvm-lld`**, **`glibc`**, **`musl`** (INFERRED), **`gnu-binutils`**, **`elf`**, **`dwarf`**, **`c-language`** (INFERRED), **`gnu-gdb`** (INFERRED), **`lldb`**, **`riscv-isa`**; **`llvm-libcxx`** **`integrates_with`** **`llvm-libcxxabi`**; reciprocals on toolchain neighbors.

**Comparative:** `language_machine_and_assembly_stack.md` §5; `ai_operating_system_reference_matrices.md` §9–§10 + **Forbidden merges**; `context_systems_landscape.md`.

**Touch-up:** `llvm-libcxx/` identity, scope, relation map, **`relations.json`**, evidence ledger.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — libc++abi wave.

**Witness:** root `ION/CAPSULE.md` **ION-097**; `ION/agents/atlas/CAPSULE.md` **A-057**.
