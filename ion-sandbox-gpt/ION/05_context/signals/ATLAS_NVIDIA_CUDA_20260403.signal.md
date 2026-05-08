---
type: signal
from: Atlas
topic: NVIDIA CUDA — Systems ATLAS GPU platform package
created: 2026-04-03
---

# NVIDIA CUDA seeded

**New package:**

- `ATLAS/systems/nvidia-cuda/` — **CUDA** **platform** ([CUDA docs](https://docs.nvidia.com/cuda/), [toolkit](https://developer.nvidia.com/cuda-toolkit)); **`integrates_with`** → **`nvidia-ptx`**, **`linux-kernel`**, **`windows-nt`**; **`competes_with`** → **`amd-rocm`** (INFERRED); **`llvm-ir`** (INFERRED). **`primary_kind`:** `gpu-compute-stack`; **`tags`:** `distributed-system`.

**Updated:**

- `ATLAS/systems/nvidia-ptx/relations.json` — **`integrates_with`** → **`nvidia-cuda`**
- `ATLAS/systems/amd-rocm/relations.json` — **`competes_with`** **target** **`nvidia-ptx`** → **`nvidia-cuda`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml`
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — GPU **vendor** **table** (PTX vs CUDA vs ROCm)
- `ATLAS/README.md`

**Evidence:** NVIDIA docs; **PTX** **vs** **CUDA** **platform** **split** **matches** **`nvidia-ptx`** **/** **`nvidia-cuda`** **packages**.
