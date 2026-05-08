---
type: signal
from: Atlas
topic: OpenGL — Systems ATLAS Khronos package
created: 2026-04-03
---

# OpenGL seeded

**New package:**

- `ATLAS/systems/opengl/` — **Khronos** **OpenGL** ([khronos.org/opengl](https://www.khronos.org/opengl/), [registry](https://registry.khronos.org/OpenGL/)); **`integrates_with`** → **`spir-v`** (4.6-era SPIR-V ingest); **`competes_with`** → **`vulkan`** (INFERRED); **`linux-kernel`** / **`windows-nt`** (INFERRED).

**Updated:**

- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`opengl`**; ledger **`sp-006`**
- `ATLAS/systems/vulkan/relations.json` — **`competes_with`** → **`opengl`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **OpenGL** paragraph + **SPIR-V** row
- `ATLAS/README.md`

**Evidence:** Khronos registry; **pin** **GL** **/** **GLSL** **/** **extension** **names** **for** **claims.**
