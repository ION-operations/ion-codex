"""Validation helpers for the canonical markdown workflow packet families.

These helpers normalize the human/executor packet surfaces used for takeover,
manual fallback, and bounded work tracking. They are intentionally narrow: they
check packet structure, not packet truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


class KernelPacketValidationError(Exception):
    """Raised when a packet cannot be parsed for bounded validation."""


@dataclass(frozen=True)
class PacketValidationMessage:
    severity: str
    code: str
    message: str


@dataclass(frozen=True)
class WorkflowPacketRule:
    packet_type: str
    template_name: str
    title_prefix: str
    required_frontmatter: tuple[str, ...]
    required_sections: tuple[str, ...]


@dataclass(frozen=True)
class PacketValidationResult:
    path: str | None
    packet_type: str | None
    expected_type: str | None
    title: str | None
    frontmatter_present: bool
    valid: bool
    errors: tuple[PacketValidationMessage, ...]
    warnings: tuple[PacketValidationMessage, ...]
    frontmatter: dict[str, str]
    sections_present: tuple[str, ...]


@dataclass(frozen=True)
class ParsedWorkflowPacket:
    path: str | None
    packet_type: str
    expected_type: str | None
    title: str | None
    frontmatter_present: bool
    frontmatter: dict[str, str]
    section_order: tuple[str, ...]
    sections: dict[str, str]


@dataclass(frozen=True)
class PacketTakeoverAssessment:
    path: str | None
    packet_type: str
    title: str | None
    created_at: str | None
    status: str | None
    objective: str
    scope_binding: str | None
    target_executor: str | None
    required_reads: tuple[str, ...]
    next_action: str | None
    expected_output: tuple[str, ...]
    warnings: tuple[str, ...]
    valid: bool


_RULES = {
    "task": WorkflowPacketRule(
        packet_type="task",
        template_name="TASK",
        title_prefix="Mission:",
        required_frontmatter=("type", "agent", "template", "priority", "created", "from", "target"),
        required_sections=("Goal", "Source / Context", "Requirements", "Deliverables", "Constraints", "Completion Signal"),
    ),
    "role_session": WorkflowPacketRule(
        packet_type="role_session",
        template_name="ROLE_SESSION",
        title_prefix="Role Session:",
        required_frontmatter=("type", "template", "created", "status", "role", "objective"),
        required_sections=("Role", "Purpose", "Source Task / Objective", "Required Reads", "Expected Output", "Next Target", "Notes"),
    ),
    "handoff": WorkflowPacketRule(
        packet_type="handoff",
        template_name="HANDOFF",
        title_prefix="Handoff:",
        required_frontmatter=("type", "template", "created", "status", "from", "to", "objective"),
        required_sections=("From", "To", "What was completed", "What remains", "Exact artifacts to read", "Risks / warnings", "Requested next action"),
    ),
    "cursor_handoff": WorkflowPacketRule(
        packet_type="cursor_handoff",
        template_name="CURSOR_HANDOFF",
        title_prefix="Cursor Handoff:",
        required_frontmatter=("type", "template", "created", "status", "target_surface", "objective"),
        required_sections=("Role / chassis target", "Load order", "Exact files to read first", "Task to perform", "Boundaries", "Expected output artifact"),
    ),
    "manual_automation_fallback": WorkflowPacketRule(
        packet_type="manual_automation_fallback",
        template_name="MANUAL_AUTOMATION_FALLBACK",
        title_prefix="Manual Automation Fallback:",
        required_frontmatter=("type", "template", "created", "status", "automation_surface", "reason"),
        required_sections=("Carrier blocked or disabled", "Lawful bounded inputs", "Manual fallback step", "Outputs emitted"),
    ),
}

_TITLE_PATTERNS = tuple((rule.packet_type, rule.title_prefix.lower()) for rule in _RULES.values())


def workflow_packet_types() -> tuple[str, ...]:
    return tuple(_RULES)


def validate_packet_path(
    path: str | Path,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
) -> PacketValidationResult:
    packet_path = Path(path)
    return validate_packet_text(
        packet_path.read_text(encoding="utf-8"),
        expected_type=expected_type,
        allow_legacy=allow_legacy,
        path=packet_path,
    )


def parse_workflow_packet_path(
    path: str | Path,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
) -> ParsedWorkflowPacket:
    packet_path = Path(path)
    return parse_workflow_packet_text(
        packet_path.read_text(encoding="utf-8"),
        expected_type=expected_type,
        allow_legacy=allow_legacy,
        path=packet_path,
    )


def parse_workflow_packet_text(
    text: str,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
    path: str | Path | None = None,
) -> ParsedWorkflowPacket:
    result = validate_packet_text(
        text,
        expected_type=expected_type,
        allow_legacy=allow_legacy,
        path=path,
    )
    if not result.valid:
        codes = ", ".join(message.code for message in result.errors) or "unknown"
        raise KernelPacketValidationError(f"Packet must validate before it can be parsed for takeover: {codes}")

    frontmatter: dict[str, str] = {}
    body = text
    if result.frontmatter_present:
        frontmatter, body = _parse_frontmatter(text)
    title, section_order, sections = _extract_sections(body)
    if result.packet_type is None:
        raise KernelPacketValidationError("Validated packet is missing a packet_type.")
    return ParsedWorkflowPacket(
        path=(None if path is None else str(path)),
        packet_type=result.packet_type,
        expected_type=result.expected_type,
        title=title,
        frontmatter_present=result.frontmatter_present,
        frontmatter=frontmatter,
        section_order=section_order,
        sections=sections,
    )


def assess_packet_takeover_path(
    path: str | Path,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
) -> PacketTakeoverAssessment:
    packet_path = Path(path)
    return assess_packet_takeover_text(
        packet_path.read_text(encoding="utf-8"),
        expected_type=expected_type,
        allow_legacy=allow_legacy,
        path=packet_path,
    )


def assess_packet_takeover_text(
    text: str,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
    path: str | Path | None = None,
) -> PacketTakeoverAssessment:
    parsed = parse_workflow_packet_text(
        text,
        expected_type=expected_type,
        allow_legacy=allow_legacy,
        path=path,
    )
    objective = (parsed.frontmatter.get("objective") or _strip_title_prefix(parsed.packet_type, parsed.title)).strip()
    target_executor = _target_executor_for_takeover(parsed)
    required_reads = _required_reads_for_takeover(parsed)
    next_action = _next_action_for_takeover(parsed)
    expected_output = _expected_output_for_takeover(parsed)
    scope_binding = _scope_binding_for_takeover(parsed)

    warnings: list[str] = []
    if not scope_binding:
        warnings.append("Packet does not carry an explicit scope binding for takeover.")
    if not required_reads:
        warnings.append("Packet does not carry explicit required reads for takeover.")
    if not next_action:
        warnings.append("Packet does not carry an explicit next-action statement for takeover.")
    if not objective:
        warnings.append("Packet does not carry an explicit objective for takeover.")

    return PacketTakeoverAssessment(
        path=parsed.path,
        packet_type=parsed.packet_type,
        title=parsed.title,
        created_at=parsed.frontmatter.get("created"),
        status=parsed.frontmatter.get("status"),
        objective=objective,
        scope_binding=scope_binding,
        target_executor=target_executor,
        required_reads=required_reads,
        next_action=next_action,
        expected_output=expected_output,
        warnings=tuple(warnings),
        valid=not warnings,
    )


def render_takeover_role_session(
    assessment: PacketTakeoverAssessment,
    *,
    role: str,
    created_at: str,
    status: str = "ACTIVE",
) -> str:
    if not assessment.valid:
        problems = "; ".join(assessment.warnings) or "unknown takeover insufficiency"
        raise KernelPacketValidationError(f"Cannot render takeover role session from insufficient packet context: {problems}")
    if not assessment.scope_binding or not assessment.next_action:
        raise KernelPacketValidationError("Takeover role session requires scope_binding and next_action.")

    lines = [
        "---",
        "type: role_session",
        "template: ROLE_SESSION",
        f"created: {created_at}",
        f"status: {status}",
        f"role: {role}",
        f"objective: {assessment.objective}",
        "---",
        "",
        f"# Role Session: {role}",
        "",
        "## Role",
        "",
        role,
        "",
        "## Purpose",
        "",
        assessment.next_action,
        "",
        "## Source Task / Objective",
        "",
            f"- scope: {assessment.scope_binding}",
            f"- source_packet_type: {assessment.packet_type}",
        ]
    if assessment.path:
        lines.append(f"- source_packet_path: {assessment.path}")
    if assessment.created_at:
        lines.append(f"- source_packet_created_at: {assessment.created_at}")
    if assessment.status:
        lines.append(f"- source_packet_status: {assessment.status}")
    lines.extend(
        [
            f"- objective: {assessment.objective}",
            "",
            "## Required Reads",
            "",
        ]
    )
    lines.extend(_render_packet_bullets(assessment.required_reads, empty_text="- no explicit required reads"))
    lines.extend(
        [
            "",
            "## Expected Output",
            "",
        ]
    )
    lines.extend(_render_packet_bullets(assessment.expected_output or (assessment.next_action,), empty_text="- one bounded continuation artifact"))
    lines.extend(
        [
            "",
            "## Next Target",
            "",
            "- next_role: operator or explicit follow-up executor",
            "",
            "## Notes",
            "",
            "- Derived from a bounded canonical packet only.",
            "- Preserve the same packet law and explicit handoff discipline.",
        ]
    )
    return "\n".join(lines) + "\n"


def validate_packet_text(
    text: str,
    *,
    expected_type: str | None = None,
    allow_legacy: bool = False,
    path: str | Path | None = None,
) -> PacketValidationResult:
    errors: list[PacketValidationMessage] = []
    warnings: list[PacketValidationMessage] = []
    frontmatter_present = text.startswith("---\n")
    frontmatter: dict[str, str] = {}
    body = text

    if frontmatter_present:
        frontmatter, body = _parse_frontmatter(text)
    else:
        message = PacketValidationMessage(
            severity="WARNING" if allow_legacy else "ERROR",
            code="MISSING_FRONTMATTER",
            message="Packet is missing normalized frontmatter.",
        )
        (warnings if allow_legacy else errors).append(message)

    title, sections = _extract_headings(body)
    inferred_type = None
    if frontmatter.get("type"):
        inferred_type = frontmatter["type"].strip()
    elif title:
        lowered = title.lower()
        for packet_type, prefix in _TITLE_PATTERNS:
            if lowered.startswith(prefix):
                inferred_type = packet_type
                break

    packet_type = expected_type or inferred_type
    if expected_type and inferred_type and inferred_type != expected_type:
        errors.append(
            PacketValidationMessage(
                "ERROR",
                "TYPE_MISMATCH",
                f"Packet type {inferred_type!r} does not match expected type {expected_type!r}.",
            )
        )

    if packet_type is None:
        errors.append(PacketValidationMessage("ERROR", "UNKNOWN_TYPE", "Could not infer packet type."))
        return PacketValidationResult(
            path=(None if path is None else str(path)),
            packet_type=None,
            expected_type=expected_type,
            title=title,
            frontmatter_present=frontmatter_present,
            valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
            frontmatter=frontmatter,
            sections_present=tuple(sections),
        )

    rule = _RULES.get(packet_type)
    if rule is None:
        errors.append(PacketValidationMessage("ERROR", "UNSUPPORTED_TYPE", f"Unsupported packet type: {packet_type!r}."))
        return PacketValidationResult(
            path=(None if path is None else str(path)),
            packet_type=packet_type,
            expected_type=expected_type,
            title=title,
            frontmatter_present=frontmatter_present,
            valid=False,
            errors=tuple(errors),
            warnings=tuple(warnings),
            frontmatter=frontmatter,
            sections_present=tuple(sections),
        )

    if title is None:
        errors.append(PacketValidationMessage("ERROR", "MISSING_TITLE", "Packet is missing a top-level heading."))
    elif not title.startswith(rule.title_prefix):
        message = PacketValidationMessage(
            severity="WARNING" if allow_legacy else "ERROR",
            code="TITLE_PREFIX",
            message=f"Packet title should begin with {rule.title_prefix!r}.",
        )
        (warnings if allow_legacy else errors).append(message)

    if frontmatter_present:
        for field in rule.required_frontmatter:
            if not frontmatter.get(field):
                errors.append(
                    PacketValidationMessage(
                        "ERROR",
                        f"MISSING_FRONTMATTER_{field.upper()}",
                        f"Missing required frontmatter field: {field}.",
                    )
                )

    if frontmatter.get("type") and frontmatter["type"] != rule.packet_type:
        errors.append(
            PacketValidationMessage(
                "ERROR",
                "TYPE_FIELD_MISMATCH",
                f"Frontmatter type {frontmatter['type']!r} does not match packet family {rule.packet_type!r}.",
            )
        )

    template_value = frontmatter.get("template")
    if template_value and template_value != rule.template_name:
        if rule.packet_type != "task":
            errors.append(
                PacketValidationMessage(
                    "ERROR",
                    "TEMPLATE_MISMATCH",
                    f"Template {template_value!r} does not match expected template {rule.template_name!r}.",
                )
            )

    normalized_sections = {_normalize(section): section for section in sections}
    for section in rule.required_sections:
        normalized = _normalize(section)
        if normalized not in normalized_sections:
            code_suffix = normalized.replace(" ", "_").upper()
            errors.append(
                PacketValidationMessage(
                    "ERROR",
                    f"MISSING_SECTION_{code_suffix}",
                    f"Missing required section: {section}.",
                )
            )

    return PacketValidationResult(
        path=(None if path is None else str(path)),
        packet_type=rule.packet_type,
        expected_type=expected_type,
        title=title,
        frontmatter_present=frontmatter_present,
        valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        frontmatter=frontmatter,
        sections_present=tuple(sections),
    )


def render_packet_validation(result: PacketValidationResult) -> str:
    lines = [
        "ION Packet Validation",
        f"path: {result.path or '<memory>'}",
        f"packet_type: {result.packet_type or 'UNKNOWN'}",
        f"expected_type: {result.expected_type or 'AUTO'}",
        f"frontmatter_present: {'yes' if result.frontmatter_present else 'no'}",
        f"valid: {'yes' if result.valid else 'no'}",
    ]
    if result.title:
        lines.append(f"title: {result.title}")
    lines.append("sections_present:")
    if result.sections_present:
        lines.extend(f"  - {section}" for section in result.sections_present)
    else:
        lines.append("  - NONE")
    lines.append("errors:")
    if result.errors:
        lines.extend(f"  - {message.code}: {message.message}" for message in result.errors)
    else:
        lines.append("  - NONE")
    lines.append("warnings:")
    if result.warnings:
        lines.extend(f"  - {message.code}: {message.message}" for message in result.warnings)
    else:
        lines.append("  - NONE")
    return "\n".join(lines)


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise KernelPacketValidationError("Expected leading frontmatter block.")
    boundary = text.find("\n---\n", 4)
    if boundary == -1:
        raise KernelPacketValidationError("Could not find closing frontmatter delimiter.")
    frontmatter_text = text[4:boundary]
    body = text[boundary + 5 :]
    payload: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in raw_line:
            raise KernelPacketValidationError(f"Invalid frontmatter line: {raw_line!r}")
        key, value = raw_line.split(":", 1)
        payload[key.strip()] = value.strip()
    return payload, body


def _extract_headings(body: str) -> tuple[str | None, tuple[str, ...]]:
    title = None
    sections: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            sections.append(line[3:].strip())
    return title, tuple(sections)


def _extract_sections(body: str) -> tuple[str | None, tuple[str, ...], dict[str, str]]:
    title = None
    current_section = None
    section_order: list[str] = []
    sections: dict[str, list[str]] = {}

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            section_order.append(current_section)
            sections.setdefault(current_section, [])
            continue
        if current_section is not None:
            sections[current_section].append(raw_line)

    return (
        title,
        tuple(section_order),
        {section: "\n".join(lines).strip() for section, lines in sections.items()},
    )


def _required_reads_for_takeover(packet: ParsedWorkflowPacket) -> tuple[str, ...]:
    section_name = {
        "handoff": "Exact artifacts to read",
        "cursor_handoff": "Exact files to read first",
        "role_session": "Required Reads",
        "manual_automation_fallback": "Lawful bounded inputs",
    }.get(packet.packet_type)
    if section_name is None:
        return ()

    section = packet.sections.get(section_name, "")
    entries = _extract_list_entries(section)
    if packet.packet_type == "manual_automation_fallback":
        refs = _extract_prefixed_values(section, "Governing task / manifest / packet refs")
        if refs:
            return refs
    return tuple(entries)


def _target_executor_for_takeover(packet: ParsedWorkflowPacket) -> str | None:
    if packet.packet_type == "handoff":
        return packet.frontmatter.get("to") or _primary_section_text(packet.sections.get("To", ""))
    if packet.packet_type == "cursor_handoff":
        return packet.frontmatter.get("target_surface") or _primary_section_text(packet.sections.get("Role / chassis target", ""))
    if packet.packet_type == "role_session":
        return packet.frontmatter.get("role") or _primary_section_text(packet.sections.get("Role", ""))
    if packet.packet_type == "manual_automation_fallback":
        section = packet.sections.get("Manual fallback step", "")
        return _extract_prefixed_value(section, "Proposed follow-up / handoff target")
    return None


def _next_action_for_takeover(packet: ParsedWorkflowPacket) -> str | None:
    section_name = {
        "handoff": "Requested next action",
        "cursor_handoff": "Task to perform",
        "role_session": "Purpose",
        "manual_automation_fallback": "Manual fallback step",
    }.get(packet.packet_type)
    if section_name is None:
        return None
    section = packet.sections.get(section_name, "")
    preferred_prefix = {
        "cursor_handoff": "bounded step",
        "manual_automation_fallback": "Exact single step being carried manually",
    }.get(packet.packet_type)
    if preferred_prefix:
        preferred = _extract_prefixed_value(section, preferred_prefix)
        if preferred:
            return preferred
    return _primary_section_text(section)


def _expected_output_for_takeover(packet: ParsedWorkflowPacket) -> tuple[str, ...]:
    section_name = {
        "cursor_handoff": "Expected output artifact",
        "role_session": "Expected Output",
        "manual_automation_fallback": "Outputs emitted",
    }.get(packet.packet_type)
    if section_name is None:
        return ()
    return tuple(_extract_list_entries(packet.sections.get(section_name, "")))


def _scope_binding_for_takeover(packet: ParsedWorkflowPacket) -> str | None:
    candidate_sections = (
        "What was completed",
        "What remains",
        "Task to perform",
        "Boundaries",
        "Source Task / Objective",
        "Lawful bounded inputs",
    )
    for section_name in candidate_sections:
        section = packet.sections.get(section_name, "")
        if not section:
            continue
        for prefix in ("scope", "Current scope / work id"):
            value = _extract_prefixed_value(section, prefix)
            if value:
                return value
        fallback = _extract_scope_pattern(section)
        if fallback:
            return fallback
    return None


def _extract_list_entries(section_text: str) -> list[str]:
    entries: list[str] = []
    for raw_line in section_text.splitlines():
        item = _strip_list_marker(raw_line.strip())
        if item:
            entries.append(item)
    return entries


def _primary_section_text(section_text: str) -> str | None:
    entries = _extract_list_entries(section_text)
    if entries:
        return entries[0]
    collapsed = " ".join(line.strip() for line in section_text.splitlines() if line.strip())
    return collapsed or None


def _extract_prefixed_value(section_text: str, prefix: str) -> str | None:
    normalized_prefix = _normalize(prefix)
    for entry in _extract_list_entries(section_text):
        key, sep, value = entry.partition(":")
        if sep and _normalize(key) == normalized_prefix and value.strip():
            return value.strip()
    return None


def _extract_prefixed_values(section_text: str, prefix: str) -> tuple[str, ...]:
    value = _extract_prefixed_value(section_text, prefix)
    if value is None:
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip() and item.strip().lower() != "none recorded")


def _extract_scope_pattern(text: str) -> str | None:
    inline = re.search(r"`([A-Z_]+:[^`]+)`", text)
    if inline:
        return inline.group(1).strip()
    plain = re.search(r"\b([A-Z_]+:[A-Za-z0-9_./-]+)\b", text)
    if plain:
        return plain.group(1).strip()
    return None


def _strip_list_marker(text: str) -> str | None:
    if not text:
        return None
    if text.startswith("- "):
        return text[2:].strip()
    numbered = re.match(r"^\d+\.\s+(.*)$", text)
    if numbered:
        return numbered.group(1).strip()
    return None


def _strip_title_prefix(packet_type: str, title: str | None) -> str:
    if not title:
        return ""
    rule = _RULES.get(packet_type)
    if rule is None:
        return title.strip()
    if title.startswith(rule.title_prefix):
        return title[len(rule.title_prefix) :].strip()
    return title.strip()


def _render_packet_bullets(items: tuple[str, ...] | list[str], *, empty_text: str) -> list[str]:
    values = [item.strip() for item in items if item and item.strip()]
    if not values:
        return [empty_text]
    return [f"- {item}" for item in values]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
