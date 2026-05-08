---
type: signal
from: Atlas
topic: Clang package + Kubernetes systemd-unit-model edges
created: 2026-04-12
---

# ATLAS — Clang + K8s ↔ systemd units

**New package:** `ATLAS/systems/clang/` — full `00`–`14`, `sources.yaml` (clang.llvm.org, Users Manual), ledger **cl-001**–**cl-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: toolchain`); `tag_index` **`toolchain`**.

**Clang relations:** `llvm-ir`, `llvm-lld`, `gnu-binutils`, `c-language`, `dwarf`, `elf`, `language-server-protocol`. Reciprocal updates on those packages (LSP already documents **clangd**).

**Kubernetes:** `relations.json` → **`integrates_with`** **`systemd-unit-model`**; **`systemd-unit-model`** → **`kubernetes`** (reciprocal).

**Comparative:** `language_machine_and_assembly_stack.md` §5; `ai_operating_system_reference_matrices.md` §8 (**systemd-unit-model** row restored, **K8s Linux node** row), §9 **Clang** row, **Forbidden merges**, evolution companion line.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — executed wave entry.

**Witness:** root `ION/CAPSULE.md` **ION-084**; `ION/agents/atlas/CAPSULE.md` **A-044**.
