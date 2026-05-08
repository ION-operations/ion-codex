---
type: signal
from: Atlas
topic: Metal — Systems ATLAS Apple GPU API package
created: 2026-04-03
---

# Metal seeded

**New package:**

- `ATLAS/systems/metal/` — **Apple** **Metal** ([developer.apple.com/metal](https://developer.apple.com/metal/)); **`integrates_with`** → **`xnu-macos`**; **`competes_with`** → **`vulkan`**, **`opengl`** (INFERRED). **No** **`spir-v`** **edge** — **MSL** **/** **AIR** **tooling** **(not** **Khronos** **SPIR-V** **as** **native** **surface).**

**Updated:**

- `ATLAS/systems/vulkan/relations.json` — **`competes_with`** → **`metal`**
- `ATLAS/systems/opengl/relations.json` — **`competes_with`** → **`metal`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **Metal** paragraph
- `ATLAS/README.md`

**Evidence:** Apple developer documentation; **pin** **OS** **/** **Xcode** **version** **for** **feature** **claims.**
