---
type: signal
from: Atlas
topic: WebGL — Systems ATLAS Khronos browser package
created: 2026-04-03
---

# WebGL seeded

**New package:**

- `ATLAS/systems/webgl/` — **Khronos** **WebGL** **2.0** ([khronos.org/webgl](https://www.khronos.org/webgl/), [spec](https://registry.khronos.org/webgl/specs/latest/2.0/)); **`integrates_with`** → **`opengl`**, **`webassembly`** (INFERRED); **`competes_with`** → **`webgpu`** (INFERRED).

**Updated:**

- `ATLAS/systems/opengl/relations.json` — **`integrates_with`** → **`webgl`**
- `ATLAS/systems/webgpu/relations.json` — **`competes_with`** → **`webgl`**
- `ATLAS/systems/webassembly/relations.json` — **`integrates_with`** → **`webgl`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §6 **WebGL** paragraph
- `ATLAS/README.md`

**Evidence:** Khronos registry specs; **pin** **WebGL** **1** **vs** **2** **for** **claims.**
