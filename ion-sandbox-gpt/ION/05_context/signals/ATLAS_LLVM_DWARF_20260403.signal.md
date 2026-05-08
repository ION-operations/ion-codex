---
type: signal
from: Atlas
topic: LLVM IR and DWARF — Systems ATLAS protocol packages
created: 2026-04-03
---

# LLVM IR / DWARF seeded

**New packages:**

- `ATLAS/systems/llvm-ir/` — LLVM **LangRef** + toolchain edges (`integrates_with` → `c-language`, `rust-language`, `dwarf`).
- `ATLAS/systems/dwarf/` — **dwarfstd.org** + GCC debug options + LLVM SourceLevelDebugging (`integrates_with` → `llvm-ir`, `c-language`).

**Updated:**

- `ATLAS/indexes/systems_index.yaml` (`primary_kind: protocol`), `ATLAS/indexes/tag_index.yaml` (`protocol` tag)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — new §5 IR/debug table; open gaps trimmed (GPU + managed runtimes note)
- `ATLAS/README.md`

**Evidence:** LangRef / committee site / compiler docs; pin LLVM release for opcode-level claims.
