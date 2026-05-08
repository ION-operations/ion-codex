"""Audit the V81 ION Agent Context Systems installation.

This module is intentionally conservative. It verifies that every live role has
been promoted from loose MINI/CAPSULE onboarding into an explicit context-system
card, registry row, and template floor.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

REQUIRED_ROLES = [
    "STEWARD",
    "VIZIER",
    "MASON",
    "NEMESIS",
    "VICE",
    "RELAY",
    "VESTIGE",
    "THOTH",
    "SCRIBE",
    "PERSONA_INTERFACE",
    "ATLAS",
    "IONOLOGIST",
    "CONTEXT_CARTOGRAPHER",
    "RUNTIME_CARTOGRAPHER",
    "CANON_LIBRARIAN",
    "TEMPLATE_CURATOR",
]

REQUIRED_FILES = [
    "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md",
    "ION/03_registry/agent_context_system_registry.yaml",
    "ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md",
    "ION/07_templates/context/AGENT_CONTEXT_SYSTEM_CARD.md",
    "ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md",
    "ION/07_templates/context/AGENT_CONTEXT_PACKAGE_INDEX.md",
]

REQUIRED_PHRASES = [
    "MINI/CAPSULE are witness inputs, not primary context authority",
    "active package is the operative context",
    "one-file-per-step",
    "Agent Context System",
]


@dataclass(frozen=True)
class AgentContextSystemAudit:
    audit_id: str
    accepted: bool
    missing_required_files: list[str]
    missing_role_cards: list[str]
    registry_missing_roles: list[str]
    missing_required_phrases: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def audit_agent_context_systems(root: str | Path) -> AgentContextSystemAudit:
    root = Path(root)
    if root.name == "ION":
        root = root.parent

    missing_required_files = [rel for rel in REQUIRED_FILES if not (root / rel).exists()]
    registry_text = _read(root / "ION/03_registry/agent_context_system_registry.yaml")
    index_text = _read(root / "ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md")
    protocol_text = _read(root / "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md")
    combined = "\n".join([registry_text, index_text, protocol_text])

    missing_role_cards = []
    registry_missing_roles = []
    for role in REQUIRED_ROLES:
        card = root / "ION/05_context/current/agent_context_systems" / f"{role}.context_system.md"
        if not card.exists():
            missing_role_cards.append(role)
        if role not in registry_text and role.lower() not in registry_text:
            registry_missing_roles.append(role)

    missing_required_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in combined]

    accepted = not any([
        missing_required_files,
        missing_role_cards,
        registry_missing_roles,
        missing_required_phrases,
    ])
    return AgentContextSystemAudit(
        audit_id="v81_agent_context_systems",
        accepted=accepted,
        missing_required_files=missing_required_files,
        missing_role_cards=missing_role_cards,
        registry_missing_roles=registry_missing_roles,
        missing_required_phrases=missing_required_phrases,
    )
