"""Bootstrap-init writer for fresh extracted ION roots.

This module adds the smallest lawful earlier surface before the existing bootstrap
bridge: write one canonical bootstrap task packet into the visible inbox lane and
persist a receipt, without widening daemon law or bypassing packet validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re

from .authority_lineage import KernelAuthorityLineageManager
from .bootstrap_bridge import BOOTSTRAP_INBOX_RELATIVE, KernelBootstrapBridgeError
from .model import KernelRecord, WorkPriority
from .packet_validation import validate_packet_text

BOOTSTRAP_INIT_RECEIPTS_RELATIVE = Path("ION/05_context/history/bootstrap_init_receipts")
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")

DEFAULT_BOOTSTRAP_TITLE = "Bootstrap first lawful daemon pressure from this root"
DEFAULT_BOOTSTRAP_GOAL = (
    "Mint the first lawful bootstrap packet so the visible packet lane, canonical "
    "signal lane, and supervised daemon can activate without hidden runtime state."
)
DEFAULT_BOOTSTRAP_TARGET = "ION/05_context/signals"
DEFAULT_BOOTSTRAP_AGENT = "Steward"
DEFAULT_BOOTSTRAP_NEEDED_FROM = "Steward"
DEFAULT_BOOTSTRAP_SOURCE_CONTEXT = (
    "ION/README.md",
    "ION/01_doctrine/CANONICAL_WORKFLOW.md",
    "ION/06_intelligence/orchestration/2026-04-10_bootstrap_init_protocol_next_packet.md",
)
DEFAULT_BOOTSTRAP_REQUIREMENTS = (
    "Keep packet law explicit and validated before any bridge emission.",
    "Preserve the current bootstrap layering: init writes packet, bridge writes signal, daemon consumes signal.",
)
DEFAULT_BOOTSTRAP_DELIVERABLES = (
    "one bootstrap task packet under ION/05_context/inbox/bootstrap/",
    "one canonical signal after bridge emission",
)
DEFAULT_BOOTSTRAP_CONSTRAINTS = (
    "Do not widen daemon law while minting the bootstrap packet.",
    "Do not invent hidden runtime state or skip the packet lane.",
)
DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL = "Emit one daemon-consumable canonical signal through the bootstrap bridge."


class KernelBootstrapInitError(Exception):
    """Raised when one bootstrap-init operation cannot complete lawfully."""


@dataclass(frozen=True)
class BootstrapInitReceipt(KernelRecord):
    receipt_id: str
    created_at: str
    packet_path: str
    source: str
    agent: str
    template: str
    priority: str
    target: str
    signal_type: str
    requested_agent: str | None
    agent_resolution_status: str
    agent_lineage_receipt_path: str | None
    needed_from: str | None
    requested_needed_from: str | None
    needed_from_resolution_status: str | None
    needed_from_lineage_receipt_path: str | None


@dataclass(frozen=True)
class BootstrapInitPreparation:
    packet_path: Path
    packet_text: str
    receipt: BootstrapInitReceipt
    receipt_path: Path


@dataclass(frozen=True)
class BootstrapInitResult:
    preparation: BootstrapInitPreparation


class KernelBootstrapInitWriter:
    """Write one canonical bootstrap task packet into the visible inbox lane."""

    def prepare_init(
        self,
        workspace_root: str | Path,
        *,
        title: str = DEFAULT_BOOTSTRAP_TITLE,
        goal: str = DEFAULT_BOOTSTRAP_GOAL,
        target: str = DEFAULT_BOOTSTRAP_TARGET,
        agent: str = DEFAULT_BOOTSTRAP_AGENT,
        template: str = "RESEARCH",
        priority: str = WorkPriority.P1_HIGH.value,
        from_actor: str = "Operator",
        bootstrap_signal_type: str = "BLOCKED",
        bootstrap_needed_from: str = DEFAULT_BOOTSTRAP_NEEDED_FROM,
        bootstrap_blocker: str | None = None,
        bootstrap_error: str | None = None,
        bootstrap_recoverable: bool | None = None,
        source_context: tuple[str, ...] = DEFAULT_BOOTSTRAP_SOURCE_CONTEXT,
        requirements: tuple[str, ...] = DEFAULT_BOOTSTRAP_REQUIREMENTS,
        deliverables: tuple[str, ...] = DEFAULT_BOOTSTRAP_DELIVERABLES,
        constraints: tuple[str, ...] = DEFAULT_BOOTSTRAP_CONSTRAINTS,
        completion_signal: str = DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL,
        packet_path: str | Path | None = None,
        bootstrap_dir: str | Path = BOOTSTRAP_INBOX_RELATIVE,
        receipts_dir: str | Path = BOOTSTRAP_INIT_RECEIPTS_RELATIVE,
        created_at: str | None = None,
    ) -> BootstrapInitPreparation:
        root = Path(workspace_root).resolve()
        timestamp = created_at or _iso_now()
        priority_value = _parse_priority(priority)
        signal_type = bootstrap_signal_type.strip().upper()
        if signal_type not in {"BLOCKED", "TASK_FAILED", "TASK_COMPLETE"}:
            raise KernelBootstrapInitError(f"Unsupported bootstrap_signal_type: {signal_type}")

        resolver = KernelAuthorityLineageManager()
        agent_resolution = resolver.resolve_authority(root, "bootstrap_packet_agent", agent)
        needed_from_resolution = resolver.resolve_authority(root, "bootstrap_blocked_escalation", bootstrap_needed_from)
        agent_lineage_receipt = resolver.record_resolution(root, agent_resolution, created_at=timestamp)
        needed_from_lineage_receipt = None
        if signal_type == "BLOCKED":
            needed_from_lineage_receipt = resolver.record_resolution(
                root,
                needed_from_resolution,
                created_at=timestamp,
            )

        packet_relative = Path(packet_path) if packet_path is not None else Path(bootstrap_dir) / _default_filename(title, timestamp)
        packet_abs = _resolve_relative_file(root, packet_relative)
        receipt_id = f"bootstrap-init-{_safe_id(packet_abs.stem)}"
        receipt_relative = Path(receipts_dir) / f"{receipt_id}.bootstrap_init_receipt.json"
        receipt_abs = _resolve_relative_file(root, receipt_relative)

        text = render_bootstrap_task_packet(
            title=title,
            goal=goal,
            target=target,
            agent=agent_resolution.resolved_name,
            template=template,
            priority=priority_value.value,
            from_actor=from_actor,
            created_at=timestamp,
            bootstrap_signal_type=signal_type,
            bootstrap_needed_from=needed_from_resolution.resolved_name,
            requested_agent=agent_resolution.requested_name,
            agent_resolution_status=agent_resolution.status,
            requested_needed_from=needed_from_resolution.requested_name,
            needed_from_resolution_status=needed_from_resolution.status,
            bootstrap_blocker=bootstrap_blocker,
            bootstrap_error=bootstrap_error,
            bootstrap_recoverable=bootstrap_recoverable,
            source_context=source_context,
            requirements=requirements,
            deliverables=deliverables,
            constraints=constraints,
            completion_signal=completion_signal,
        )
        validation = validate_packet_text(text, expected_type="task")
        if not validation.valid:
            codes = ", ".join(message.code for message in validation.errors) or "unknown"
            raise KernelBootstrapInitError(f"Generated bootstrap task packet failed validation: {codes}")

        receipt = BootstrapInitReceipt(
            receipt_id=receipt_id,
            created_at=timestamp,
            packet_path=str(packet_relative),
            source="bootstrap.init",
            agent=agent_resolution.resolved_name,
            requested_agent=agent_resolution.requested_name,
            agent_resolution_status=agent_resolution.status,
            agent_lineage_receipt_path=(None if agent_lineage_receipt is None else agent_lineage_receipt.receipt_path),
            template=template,
            priority=priority_value.value,
            target=target,
            signal_type=signal_type,
            needed_from=(needed_from_resolution.resolved_name if signal_type == "BLOCKED" else None),
            requested_needed_from=(needed_from_resolution.requested_name if signal_type == "BLOCKED" else None),
            needed_from_resolution_status=(needed_from_resolution.status if signal_type == "BLOCKED" else None),
            needed_from_lineage_receipt_path=(
                None
                if signal_type != "BLOCKED" or needed_from_lineage_receipt is None
                else needed_from_lineage_receipt.receipt_path
            ),
        )
        return BootstrapInitPreparation(
            packet_path=packet_abs,
            packet_text=text,
            receipt=receipt,
            receipt_path=receipt_abs,
        )

    def write_init(self, workspace_root: str | Path, **kwargs: object) -> BootstrapInitResult:
        preparation = self.prepare_init(workspace_root, **kwargs)
        if preparation.packet_path.exists():
            raise KernelBootstrapInitError(f"Bootstrap packet already exists: {preparation.packet_path}")
        preparation.packet_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.receipt_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.packet_path.write_text(preparation.packet_text, encoding="utf-8")
        preparation.receipt_path.write_text(
            json.dumps(preparation.receipt.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return BootstrapInitResult(preparation=preparation)


IonBootstrapInitWriter = KernelBootstrapInitWriter


def render_bootstrap_task_packet(
    *,
    title: str,
    goal: str,
    target: str,
    agent: str,
    template: str,
    priority: str,
    from_actor: str,
    created_at: str,
    bootstrap_signal_type: str,
    bootstrap_needed_from: str,
    requested_agent: str | None,
    agent_resolution_status: str,
    requested_needed_from: str | None,
    needed_from_resolution_status: str | None,
    bootstrap_blocker: str | None,
    bootstrap_error: str | None,
    bootstrap_recoverable: bool | None,
    source_context: tuple[str, ...],
    requirements: tuple[str, ...],
    deliverables: tuple[str, ...],
    constraints: tuple[str, ...],
    completion_signal: str,
) -> str:
    frontmatter_lines = [
        "---",
        "type: task",
        f"agent: {agent}",
        f"template: {template}",
        f"priority: {priority}",
        f"created: {created_at}",
        f"from: {from_actor}",
        f"target: {target}",
        f"bootstrap_signal_type: {bootstrap_signal_type}",
        "status: ACTIVE",
        f"updated: {created_at}",
    ]
    if requested_agent is not None:
        frontmatter_lines.append(f"requested_agent: {requested_agent}")
    if agent_resolution_status != "CURRENT_AUTHORITY":
        frontmatter_lines.append(f"agent_resolution_status: {agent_resolution_status}")
    if bootstrap_signal_type == "BLOCKED":
        frontmatter_lines.append(f"bootstrap_needed_from: {bootstrap_needed_from}")
        if requested_needed_from is not None:
            frontmatter_lines.append(f"bootstrap_requested_needed_from: {requested_needed_from}")
        if needed_from_resolution_status is not None and needed_from_resolution_status != "CURRENT_AUTHORITY":
            frontmatter_lines.append(f"bootstrap_needed_from_resolution_status: {needed_from_resolution_status}")
        if bootstrap_blocker:
            frontmatter_lines.append(f"bootstrap_blocker: {bootstrap_blocker}")
    elif bootstrap_signal_type == "TASK_FAILED":
        if bootstrap_error:
            frontmatter_lines.append(f"bootstrap_error: {bootstrap_error}")
        if bootstrap_recoverable is not None:
            frontmatter_lines.append(f"bootstrap_recoverable: {str(bootstrap_recoverable).lower()}")
    frontmatter_lines.append("---")

    packet = "\n".join(
        [
            *frontmatter_lines,
            "",
            f"# Mission: {title}",
            "",
            "## Goal",
            "",
            goal,
            "",
            "## Source / Context",
            "",
            *_render_bullets(source_context),
            "",
            "## Requirements",
            "",
            *_render_numbered(requirements),
            "",
            "## Deliverables",
            "",
            *_render_bullets(deliverables),
            "",
            "## Constraints",
            "",
            *_render_numbered(constraints),
            "",
            "## Completion Signal",
            "",
            completion_signal,
            "",
        ]
    )
    return packet


def _render_bullets(items: tuple[str, ...]) -> list[str]:
    values = [item.strip() for item in items if item and item.strip()]
    return [f"- {item}" for item in values] or ["- none declared"]


def _render_numbered(items: tuple[str, ...]) -> list[str]:
    values = [item.strip() for item in items if item and item.strip()]
    if not values:
        return ["1. none declared"]
    return [f"{index}. {item}" for index, item in enumerate(values, start=1)]


def _parse_priority(value: str) -> WorkPriority:
    try:
        return WorkPriority(value)
    except ValueError as exc:
        raise KernelBootstrapInitError(f"Unsupported bootstrap priority: {value}") from exc


def _default_filename(title: str, created_at: str) -> str:
    stem = _safe_id(title).replace("-", "_")
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    return f"{stem}_{stamp}.task.md"


def _safe_id(text: str) -> str:
    safe = _SAFE_ID_RE.sub("-", text.lower()).strip("-")
    return safe or "bootstrap"


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelBootstrapInitError(f"Absolute paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelBootstrapInitError(f"Path escapes workspace root: {relative_path}") from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
