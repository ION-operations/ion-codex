---
type: signal
from: Atlas
topic: WebGPU — Systems ATLAS W3C package
created: 2026-04-03
---

# WebGPU seeded

**New package:**

- `ATLAS/systems/webgpu/` — **W3C** **WebGPU** **+** **WGSL** ([WebGPU](https://www.w3.org/TR/webgpu/), [WGSL](https://www.w3.org/TR/WGSL/)); **`integrates_with`** → **`webassembly`**, **`vulkan`**, **`metal`**, **`direct3d`**, **`spir-v`** (INFERRED).

**Updated:**

- `ATLAS/systems/webassembly/relations.json` — **`integrates_with`** → **`webgpu`**
- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`webgpu`**; ledger **`sp-009`**
- `ATLAS/systems/vulkan/relations.json` — **`integrates_with`** → **`webgpu`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §6 **Web** **platform** **GPU** (**WebGPU**) paragraph
- `ATLAS/README.md`

**Evidence:** W3C TR snapshots; **pin** **dated** **revisions** **for** **normative** **claims.**
