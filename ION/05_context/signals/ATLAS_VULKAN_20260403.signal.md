---
type: signal
from: Atlas
topic: Vulkan — Systems ATLAS Khronos package
created: 2026-04-03
---

# Vulkan seeded

**New package:**

- `ATLAS/systems/vulkan/` — **Khronos** **Vulkan** ([vulkan.org](https://www.vulkan.org/), [registry](https://registry.khronos.org/vulkan/)); **`depends_on`** → **`spir-v`** (shader modules); **`integrates_with`** → **`linux-kernel`**, **`windows-nt`**, **`opencl`** (INFERRED where noted in package).

**Updated:**

- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`vulkan`**; ledger **`sp-005`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **Vulkan** paragraph + **SPIR-V** row
- `ATLAS/README.md`

**Evidence:** Khronos registry + vulkan.org; **pin** **Vulkan** **version** **/** **extensions** **for** **API** **claims**.
