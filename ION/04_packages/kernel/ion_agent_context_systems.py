"""Runtime helpers for ION Agent Context Systems.

V81 installed the registry and per-role system cards. V82 makes that state usable
by runtime package builders without adding a YAML dependency: this module parses
the deliberately small registry shape used by ION and returns the context-system
surfaces that must be prepended to a role's active package.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

REGISTRY_RELATIVE_PATH = Path("ION/03_registry/agent_context_system_registry.yaml")
PROTOCOL_RELATIVE_PATH = Path("ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md")
INDEX_RELATIVE_PATH = Path("ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md")
BUILD_STEP_TEMPLATE_RELATIVE_PATH = Path("ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md")
PACKAGE_INDEX_TEMPLATE_RELATIVE_PATH = Path("ION/07_templates/context/AGENT_CONTEXT_PACKAGE_INDEX.md")

LEGACY_POLICY_PHRASE = (
    "MINI/CAPSULE are witness inputs, not primary context authority. "
    "The active package is the operative context for this run."
)


@dataclass(frozen=True)
class AgentContextSystem:
    role_id: str
    display_name: str
    context_system_card: str
    package_strategy: str = ""
    default_active_package_class: str = "MISSION_ACTIVE_CONTEXT_PACKAGE"
    base_sources: tuple[str, ...] = ()
    primary_templates: tuple[str, ...] = ()
    source_section: str = "agents"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _shell_root(root: str | Path) -> Path:
    candidate = Path(root).expanduser().resolve()
    if candidate.name == "ION":
        return candidate.parent
    return candidate


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_registry_records(text: str, section_name: str) -> list[AgentContextSystem]:
    records: list[dict[str, Any]] = []
    active = False
    current: dict[str, Any] | None = None
    list_key: str | None = None

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw.startswith(" ") and stripped.endswith(":"):
            if active and current:
                records.append(current)
            active = stripped[:-1] == section_name
            current = None
            list_key = None
            continue
        if not active:
            continue
        if line.startswith("  - role_id:"):
            if current:
                records.append(current)
            current = {"role_id": _strip_quotes(line.split(":", 1)[1]), "source_section": section_name}
            list_key = None
            continue
        if current is None:
            continue
        if line.startswith("    ") and not line.startswith("      ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            value = _strip_quotes(value)
            if value == "":
                current[key] = []
                list_key = key
            else:
                current[key] = value
                list_key = None
            continue
        if line.startswith("      - ") and list_key:
            current.setdefault(list_key, []).append(_strip_quotes(stripped[2:].strip()))
    if active and current:
        records.append(current)

    systems: list[AgentContextSystem] = []
    for record in records:
        role_id = str(record.get("role_id", "")).strip()
        card = str(record.get("context_system_card") or "").strip()
        if not role_id or not card:
            continue
        display = str(record.get("display_name") or role_id.split(".")[-1]).upper()
        systems.append(
            AgentContextSystem(
                role_id=role_id,
                display_name=display,
                context_system_card=card,
                package_strategy=str(record.get("package_strategy", "")),
                default_active_package_class=str(record.get("default_active_package_class", "MISSION_ACTIVE_CONTEXT_PACKAGE")),
                base_sources=tuple(str(item) for item in record.get("base_sources", ()) if str(item).strip()),
                primary_templates=tuple(str(item) for item in record.get("primary_templates", ()) if str(item).strip()),
                source_section=str(record.get("source_section", section_name)),
            )
        )
    return systems


def load_agent_context_system_registry(root: str | Path) -> dict[str, AgentContextSystem]:
    root_path = _shell_root(root)
    registry_path = root_path / REGISTRY_RELATIVE_PATH
    if not registry_path.exists():
        return {}
    text = registry_path.read_text(encoding="utf-8", errors="replace")
    systems = _parse_registry_records(text, "agents") + _parse_registry_records(text, "context_specialists")
    by_key: dict[str, AgentContextSystem] = {}
    for system in systems:
        suffix = system.role_id.split(".")[-1].lower()
        by_key[suffix] = system
        by_key[system.display_name.lower()] = system
        by_key[system.role_id.lower()] = system
    return by_key


def get_agent_context_system(root: str | Path, role: str) -> AgentContextSystem | None:
    registry = load_agent_context_system_registry(root)
    key = role.lower().strip()
    return registry.get(key) or registry.get(f"role.{key}")


def agent_context_system_paths(root: str | Path, role: str) -> tuple[str, ...]:
    system = get_agent_context_system(root, role)
    if system is None:
        return ()
    candidates = [
        str(PROTOCOL_RELATIVE_PATH),
        str(REGISTRY_RELATIVE_PATH),
        str(INDEX_RELATIVE_PATH),
        system.context_system_card,
        str(BUILD_STEP_TEMPLATE_RELATIVE_PATH),
        str(PACKAGE_INDEX_TEMPLATE_RELATIVE_PATH),
        *system.primary_templates,
    ]
    seen: set[str] = set()
    ordered: list[str] = []
    for rel in candidates:
        rel = rel.strip().rstrip("/")
        if rel and rel not in seen:
            seen.add(rel)
            ordered.append(rel)
    return tuple(ordered)


def runtime_context_system_summary(root: str | Path, role: str) -> dict[str, Any]:
    system = get_agent_context_system(root, role)
    if system is None:
        return {
            "status": "missing_registry_or_role",
            "role": role,
            "context_system_card": None,
            "policy": LEGACY_POLICY_PHRASE,
            "paths_ordered": [],
        }
    return {
        "status": "active",
        "role": role,
        "role_id": system.role_id,
        "display_name": system.display_name,
        "context_system_card": system.context_system_card,
        "package_strategy": system.package_strategy,
        "default_active_package_class": system.default_active_package_class,
        "policy": LEGACY_POLICY_PHRASE,
        "paths_ordered": list(agent_context_system_paths(root, role)),
    }
