---
type: signal
from: Atlas
topic: LLVM libc++ (llvm-libcxx) package
created: 2026-04-03
---

# ATLAS — LLVM libc++ (`llvm-libcxx`)

**New package:** `ATLAS/systems/llvm-libcxx/` — full schema paths, `sources.yaml` (libcxx.llvm.org + llvm-project), ledger **lcxx-001**–**lcxx-003**.

**Taxonomy:** **`cxx-runtime`** (`tag_index.yaml` lists **`gnu-libstdcxx`** + **`llvm-libcxx`**); `systems_index` **primary_kind** **`cxx-runtime`**.

**Relations:** **`integrates_with`** **`clang`**, **`llvm-lld`**, **`glibc`**, **`musl`** (INFERRED), **`gnu-binutils`**, **`elf`**, **`dwarf`**, **`c-language`** (INFERRED), **`gnu-gdb`** (INFERRED), **`lldb`**, **`riscv-isa`**; **`competes_with`** **`gnu-libstdcxx`** (reciprocal); reciprocals on those packages.

**Comparative:** `language_machine_and_assembly_stack.md` §5; `ai_operating_system_reference_matrices.md` §9–§10 + **Forbidden merges**; `context_systems_landscape.md`.

**Touch-up:** `gnu-libstdcxx/00_identity.md` — **LLVM** **libc++** → **`llvm-libcxx`**.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — libc++ wave; **Next waves** userland row (**`libc++abi`** still optional).

**Witness:** root `ION/CAPSULE.md` **ION-096**; `ION/agents/atlas/CAPSULE.md` **A-056**.
