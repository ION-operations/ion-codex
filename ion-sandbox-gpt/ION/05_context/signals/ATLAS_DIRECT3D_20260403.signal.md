---
type: signal
from: Atlas
topic: Direct3D — Systems ATLAS Microsoft GPU API package
created: 2026-04-03
---

# Direct3D seeded

**New package:**

- `ATLAS/systems/direct3d/` — **Microsoft** **Direct3D** **12** **grain** ([learn.microsoft.com — Direct3D 12](https://learn.microsoft.com/en-us/windows/win32/direct3d12/)); **`integrates_with`** → **`windows-nt`**; **`competes_with`** → **`vulkan`**, **`opengl`**, **`metal`** (INFERRED). **HLSL** **/** **DXIL** **—** **not** **`spir-v`** **native.**

**Updated:**

- `ATLAS/systems/vulkan/relations.json` — **`competes_with`** → **`direct3d`**
- `ATLAS/systems/opengl/relations.json` — **`competes_with`** → **`direct3d`**
- `ATLAS/systems/metal/relations.json` — **`competes_with`** → **`direct3d`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **Direct3D** paragraph
- `ATLAS/README.md`

**Evidence:** Microsoft Learn; **pin** **SDK** **/** **Agility** **deployment** **for** **feature** **claims.**
