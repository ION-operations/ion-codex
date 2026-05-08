---
type: signal
from: Atlas
topic: OpenCL — Systems ATLAS Khronos package
created: 2026-04-03
---

# OpenCL seeded

**New package:**

- `ATLAS/systems/opencl/` — **Khronos** **OpenCL** ([opencl](https://www.khronos.org/opencl/), [registry](https://registry.khronos.org/OpenCL/)); **`integrates_with`** → **`spir-v`**, **`amd-rocm`**; **`competes_with`** → **`nvidia-cuda`** (INFERRED); **`linux-kernel`** (INFERRED).

**Updated:**

- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`opencl`**; ledger `sp-004`
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **OpenCL** paragraph
- `ATLAS/README.md`

**Evidence:** Khronos registry + spec pages; **pin** **OpenCL** **version** **for** **API** **claims**.
