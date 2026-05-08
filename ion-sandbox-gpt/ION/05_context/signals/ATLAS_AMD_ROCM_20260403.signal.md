---
type: signal
from: Atlas
topic: AMD ROCm — Systems ATLAS GPU compute stack package
created: 2026-04-03
---

# AMD ROCm seeded

**New package:**

- `ATLAS/systems/amd-rocm/` — **AMD ROCm** ([documentation](https://rocm.docs.amd.com/), [product](https://www.amd.com/en/products/software/rocm.html), Wikipedia); **`integrates_with`** → **`linux-kernel`**, **`llvm-ir`**; **`competes_with`** → **`nvidia-ptx`** (INFERRED). **`primary_kind`:** `gpu-compute-stack`; **`tags`:** `distributed-system`.

**Updated:**

- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`distributed-system`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — GPU **vendor** **stack** table + §8 (machine ISA gap clarified)
- `ATLAS/README.md`

**Evidence:** AMD docs; **not** a substitute for **RDNA/CDNA** **machine** **ISA** **primaries** (still out of scope).
