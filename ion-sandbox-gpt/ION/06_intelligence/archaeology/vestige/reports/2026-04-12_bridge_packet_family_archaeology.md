---
type: archaeology_report
from: Vestige
created: 2026-04-12
status: COMPLETE
topic: Bridge packet family — older-estate precedent vs active branch
connections:
  - ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/packet_validation.py
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
ratification: NOT_RATIFIED
---

# Bridge packet family archaeology (2026-04-12)

## Scope

Excavation asked whether older-estate surfaces already distinguished: (1) canonical vs governed bridge markdown packets, (2) validator-backed vs support packet families, or (3) widening patterns the active branch should recover.

## Active-branch anchors (cited)

1. **Canonical workflow floor (five families only)** — `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md` lists `task`, `role_session`, `handoff`, `cursor_handoff`, `manual_automation_fallback` as the canonical human/executor markdown taxonomy. It explicitly scopes out “machine-generated JSON dispatch packets, service receipts, or runtime-report artifacts” as separate families (lines 36–38 in the version read for this pass).

2. **Legacy vs canonical** — Same protocol § “Legacy compatibility”: older surfaces may lack frontmatter; they are “legacy packets” not silently redefined; validation may use a “legacy-tolerant mode” for archaeology/migration while new packets stay strict (lines 134–140).

3. **Validator encodes only the five** — `ION/04_packages/kernel/packet_validation.py` defines `_RULES` for exactly those keys; any other `type:` yields `UNSUPPORTED_TYPE` (e.g. lines 387–401).

4. **Bridge protocols self-label as provisional** — Current-phase bridge law files carry paired metadata, e.g. `bridge_status: PROVISIONAL_BRIDGE` and `canon_status: NOT_FINAL_CANON`, and still **link** to `PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`:
   - `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md` (frontmatter lines 1–20)
   - `ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md` (lines 1–20)
   - `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md` (lines 1–20)

   So the active branch already encodes a **two-layer story in prose metadata**: canonical packet law (narrow floor) vs provisional bridge protocols that extend practice without yet being folded into the validator taxonomy.

## Older-estate stratum (ION-BUILD) — cited

5. **Aether “packet” universe is schema-first, not K2 markdown families** — `ION-BUILD/canon/constitution/AETHER_INTERFACE.md` defines many packet kinds (e.g. § “10. HANDOFF PACKET”, `schema: handoff/v1`, fields such as `from_agent`, `to_agent`, `capsule_snapshot`, invariants like “no hidden-context handoff is lawful”, lines 443–483). This is a **parallel lineage**: YAML schema packets for interface/constitution, not the markdown frontmatter + heading law enforced by `packet_validation.py`.

6. **ION-BUILD HANDOFF template is not the same species** — `ION-BUILD/context/templates/actions/HANDOFF.md` is framed as `type: template` under D35, with a different output shape (“Final State Summary”, “Execution Pointer”, D35 signals) (lines 1–35). It does **not** establish `ROLE_CHASSIS_MOUNT` / `DISAGREEMENT_ESCALATION` / `EXTERNAL_RETURN` as markdown packet families for a Python validator.

## Sibling search note

Targeted searches under `ION-BUILD/`, `SOS/`, `ProjectOpus/`, and `SOS-OPUS/` for strings including `ROLE_CHASSIS_MOUNT`, `DISAGREEMENT_ESCALATION`, `EXTERNAL_RETURN`, `packet_validation`, and `PACKET_AND_HANDOFF` returned **no hits** on this disk layout (April 2026). Those bridge names and the narrow kernel validator appear **active-branch-native**; they are not recoverable as a dropped file pattern from those sibling trees in this environment.

## Contradictions preserved (do not flatten)

| Surface A | Surface B | Tension |
|-----------|-----------|---------|
| Example handoff in `PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md` warns not to widen taxonomy without explicit need | Phase 1 proof loop uses bridge packets outside the five | Operational necessity vs written caution in the same protocol doc |
| Protocol says generated/dispatch packets are separate families | Bridge protocols are markdown-adjacent governance, connected to same workflow doc | “Outside canonical validator” is coherent but easy for sessions to misread as “invalid” rather than “other family” |
| Aether `handoff/v1` schema | K2 `handoff` markdown rule set | Same word “handoff”; different contracts — high lineage collision risk for anyone merging estates mentally |

## Recommendation

The active branch is **not** simply recovering a lost single taxonomy from ION-BUILD/SOS-style estates. Those estates used **different packet ontologies** (schema packets; template-type handoffs). What the branch **is** recovering is an **explicit pattern already drafted in active law**: narrow validator floor + **explicitly labeled provisional bridge protocols** that point at the packet standardization doc but are not yet in `_RULES`.

**Actionable framing for Codex:** the lawful choice is between (a) **widening** `_RULES` + protocol taxonomy to include the three bridge packet types as first-class canonical families, or (b) **keeping** them as governed bridge packets with a **documented** non-validator path (and tooling that does not imply `UNSUPPORTED_TYPE` == “illegal”), aligned with the existing `PROVISIONAL_BRIDGE` / `NOT_FINAL_CANON` frontmatter. Either path should **name** the relationship to legacy Aether schema packets and ION-BUILD templates so “handoff” does not collapse three meanings.

## Evidence index

- Active: `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- Active: `ION/04_packages/kernel/packet_validation.py`
- Active bridges: `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`, `DISAGREEMENT_ESCALATION_PROTOCOL.md`, `EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- Older: `ION-BUILD/canon/constitution/AETHER_INTERFACE.md` (handoff packet section)
- Older: `ION-BUILD/context/templates/actions/HANDOFF.md`
- Planning context: `ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md`
