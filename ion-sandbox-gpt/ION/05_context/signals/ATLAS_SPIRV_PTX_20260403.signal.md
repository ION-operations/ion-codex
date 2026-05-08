---
type: signal
from: Atlas
topic: SPIR-V and NVIDIA PTX — Systems ATLAS GPU IR packages
created: 2026-04-03
---

# SPIR-V / NVIDIA PTX seeded

**New packages:**

- `ATLAS/systems/spir-v/` — Khronos **SPIR-V** registry + LLVM **SPIRVUsage**; `integrates_with` → `llvm-ir`.
- `ATLAS/systems/nvidia-ptx/` — NVIDIA **PTX** manual + LLVM **NVPTXUsage**; `integrates_with` → `llvm-ir`.

**Updated:**

- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — GPU IR table + CPU vs GPU pipeline notes; **§7** open gaps (vendor machine ISAs, JVM/.NET)
- `ATLAS/README.md`

**Evidence:** Khronos + NVIDIA + LLVM docs; vendor **SASS** / **undisclosed** **machine** **code** remains out of scope.
