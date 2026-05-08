---
type: signal
from: Atlas
topic: SYCL — Systems ATLAS Khronos package
created: 2026-04-03
---

# SYCL seeded

**New package:**

- `ATLAS/systems/sycl/` — **Khronos** **SYCL** ([khronos.org/sycl](https://www.khronos.org/sycl/), [registry](https://registry.khronos.org/SYCL/)); **`integrates_with`** → **`opencl`**, **`llvm-ir`**, **`linux-kernel`**, **`amd-rocm`** (INFERRED); **`competes_with`** → **`nvidia-cuda`** (INFERRED).

**Updated:**

- `ATLAS/systems/opencl/relations.json` — **`integrates_with`** → **`sycl`**
- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`sycl`** (INFERRED); ledger **`sp-007`**
- `ATLAS/systems/nvidia-cuda/relations.json` — **`competes_with`** → **`sycl`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **SYCL** paragraph
- `ATLAS/README.md`

**Evidence:** Khronos registry; **pin** **SYCL** **spec** **revision** **for** **API** **claims.**
