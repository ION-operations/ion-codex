---
type: signal
from: Atlas
topic: OpenGL ES — Systems ATLAS Khronos package
created: 2026-04-03
---

# OpenGL ES seeded

**New package:**

- `ATLAS/systems/opengl-es/` — **Khronos** **OpenGL** **ES** ([opengles](https://www.khronos.org/opengles/), [ES 3.2 registry](https://registry.khronos.org/OpenGL/specs/es/3.2/)); **`integrates_with`** → **`opengl`**, **`webgl`**, **`linux-kernel`** (INFERRED); **`competes_with`** → **`vulkan`** (INFERRED).

**Updated:**

- `ATLAS/systems/opengl/relations.json` — **`integrates_with`** → **`opengl-es`**
- `ATLAS/systems/webgl/relations.json` — **`integrates_with`** → **`opengl-es`**
- `ATLAS/systems/vulkan/relations.json` — **`competes_with`** → **`opengl-es`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **OpenGL** **ES** paragraph
- `ATLAS/README.md`

**Evidence:** Khronos registry; **pin** **ES** **version** **(2.0** **vs** **3.x)** **for** **claims.**
