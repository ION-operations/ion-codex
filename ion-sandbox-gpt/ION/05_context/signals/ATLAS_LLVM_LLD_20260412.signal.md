---
type: signal
from: Atlas
topic: LLVM lld linker package
created: 2026-04-12
---

# ATLAS — LLVM lld

**New package:** `ATLAS/systems/llvm-lld/` — full `00`–`14`, `sources.yaml` (lld.llvm.org, LLVM CommandGuide), ledger **lld-001**–**lld-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: toolchain`); `tag_index.yaml` **`toolchain`** → `llvm-lld`.

**Relations:** `integrates_with` `llvm-ir`, `elf`, `c-language`, `rust-language`, `riscv-isa`; `integrates_with` / `INFERRED` `linux-kernel`; **`competes_with`** `gnu-binutils` (reciprocal). Reciprocal edges on `elf`, `llvm-ir`, `c-language`, `rust-language`, `riscv-isa`, `linux-kernel`.

**Touch-ups:** `gnu-binutils/00_identity.md` boundary; `elf/07_extension_tooling.md` pointer.

**Comparative:** `language_machine_and_assembly_stack.md` §5; `ai_operating_system_reference_matrices.md` §9 + **Forbidden merges** + evolution line; `context_systems_landscape.md` companion.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — LLVM lld wave.

**Witness:** root `ION/CAPSULE.md` **ION-082**; `ION/agents/atlas/CAPSULE.md` **A-042**.
