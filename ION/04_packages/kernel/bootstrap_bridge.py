"""Bootstrap bridge from visible inbox packets into canonical daemon signals.

This module does not widen daemon law. It provides the smallest truthful bridge the
current stack can support today: discover one validated bootstrap task packet,
render one canonical daemon signal from it, archive the bootstrap packet, and
leave the existing daemon signal-follow-up path unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .authority_lineage import KernelAuthorityLineageManager
from .model import KernelRecord, WorkPriority
from .packet_validation import ParsedWorkflowPacket, parse_workflow_packet_path
from .receipts import CanonicalSignalType, EmittedSignal, SignalLifecycleStatus


BOOTSTRAP_INBOX_RELATIVE = Path("ION/05_context/inbox/bootstrap")
BOOTSTRAP_ARCHIVE_RELATIVE = Path("ION/05_context/inbox/bootstrap/archive")
BOOTSTRAP_RECEIPTS_RELATIVE = Path("ION/05_context/history/bootstrap_bridge_receipts")
DEFAULT_SIGNALS_DIR = Path("ION/05_context/signals")

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_SAFE_FILE_RE = re.compile(r"[^A-Z0-9]+")


class KernelBootstrapBridgeError(Exception):
    """Raised when one bootstrap bridge operation cannot complete lawfully."""


@dataclass(frozen=True)
class BootstrapBridgeReceipt(KernelRecord):
    receipt_id: str
    created_at: str
    packet_path: str
    packet_archived_path: str
    signal_id: str
    signal_type: str
    signal_path: str
    source_agent: str
    source_work_unit: str
    target: str


@dataclass(frozen=True)
class BootstrapBridgePreparation:
    packet_path: Path
    packet_archived_path: Path
    signal: EmittedSignal
    signal_path: Path
    receipt: BootstrapBridgeReceipt
    receipt_path: Path


@dataclass(frozen=True)
class BootstrapBridgeResult:
    preparation: BootstrapBridgePreparation


class KernelBootstrapSignalBridge:
    """Bridge validated bootstrap task packets into canonical daemon signals."""

    def discover_bootstrap_packets(
        self,
        workspace_root: str | Path,
        *,
        bootstrap_dir: str | Path = BOOTSTRAP_INBOX_RELATIVE,
    ) -> tuple[Path, ...]:
        resolved_dir = _resolve_relative_dir(workspace_root, Path(bootstrap_dir))
        if not resolved_dir.exists():
            return ()
        return tuple(
            path
            for path in sorted(resolved_dir.glob("*.task.md"))
            if path.is_file()
        )

    def prepare_bridge(
        self,
        workspace_root: str | Path,
        *,
        packet_path: str | Path | None = None,
        bootstrap_dir: str | Path = BOOTSTRAP_INBOX_RELATIVE,
        archive_dir: str | Path = BOOTSTRAP_ARCHIVE_RELATIVE,
        signals_dir: str | Path = DEFAULT_SIGNALS_DIR,
        receipts_dir: str | Path = BOOTSTRAP_RECEIPTS_RELATIVE,
        emitted_at: str | None = None,
    ) -> BootstrapBridgePreparation:
        root = Path(workspace_root).resolve()
        packet = self._select_packet(root, packet_path=packet_path, bootstrap_dir=Path(bootstrap_dir))
        parsed = parse_workflow_packet_path(packet, expected_type="task")
        created_at = emitted_at or parsed.frontmatter.get("created") or _iso_now()
        relative_packet_path = _relative_to_root(packet, root)
        packet_name = packet.name
        archived_relative = Path(archive_dir) / packet_name
        packet_archived_path = _resolve_relative_file(root, archived_relative)

        signal = _signal_from_packet(
            parsed,
            workspace_root=root,
            relative_packet_path=relative_packet_path,
            emitted_at=created_at,
        )
        signal_relative = Path(signals_dir) / _signal_filename(signal, packet.stem)
        signal_path = _resolve_relative_file(root, signal_relative)

        receipt = BootstrapBridgeReceipt(
            receipt_id=f"bootstrap-bridge-{_safe_id(_relative_to_root(packet, root).replace('/', '-'))}",
            created_at=created_at,
            packet_path=relative_packet_path,
            packet_archived_path=str(archived_relative),
            signal_id=signal.signal_id,
            signal_type=signal.signal_type.value,
            signal_path=str(signal_relative),
            source_agent=signal.source_agent,
            source_work_unit=signal.source_work_unit,
            target=signal.target,
        )
        receipt_relative = Path(receipts_dir) / f"{receipt.receipt_id}.bootstrap_bridge_receipt.json"
        receipt_path = _resolve_relative_file(root, receipt_relative)
        return BootstrapBridgePreparation(
            packet_path=packet,
            packet_archived_path=packet_archived_path,
            signal=signal,
            signal_path=signal_path,
            receipt=receipt,
            receipt_path=receipt_path,
        )

    def bridge(
        self,
        workspace_root: str | Path,
        *,
        packet_path: str | Path | None = None,
        bootstrap_dir: str | Path = BOOTSTRAP_INBOX_RELATIVE,
        archive_dir: str | Path = BOOTSTRAP_ARCHIVE_RELATIVE,
        signals_dir: str | Path = DEFAULT_SIGNALS_DIR,
        receipts_dir: str | Path = BOOTSTRAP_RECEIPTS_RELATIVE,
        emitted_at: str | None = None,
    ) -> BootstrapBridgeResult:
        preparation = self.prepare_bridge(
            workspace_root,
            packet_path=packet_path,
            bootstrap_dir=bootstrap_dir,
            archive_dir=archive_dir,
            signals_dir=signals_dir,
            receipts_dir=receipts_dir,
            emitted_at=emitted_at,
        )
        preparation.signal_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.packet_archived_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.receipt_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.signal_path.write_text(
            json.dumps(preparation.signal.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        preparation.receipt_path.write_text(
            json.dumps(preparation.receipt.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        packet_text = preparation.packet_path.read_text(encoding="utf-8")
        preparation.packet_archived_path.write_text(packet_text, encoding="utf-8")
        preparation.packet_path.unlink()
        return BootstrapBridgeResult(preparation=preparation)

    def _select_packet(
        self,
        workspace_root: Path,
        *,
        packet_path: str | Path | None,
        bootstrap_dir: Path,
    ) -> Path:
        if packet_path is not None:
            resolved = _resolve_relative_file(workspace_root, Path(packet_path))
            if not resolved.exists():
                raise KernelBootstrapBridgeError(f"Bootstrap packet does not exist: {resolved}")
            return resolved
        discovered = self.discover_bootstrap_packets(workspace_root, bootstrap_dir=bootstrap_dir)
        if not discovered:
            raise KernelBootstrapBridgeError("No bootstrap task packets available.")
        return discovered[0]


IonBootstrapSignalBridge = KernelBootstrapSignalBridge


def _signal_from_packet(
    parsed: ParsedWorkflowPacket,
    *,
    workspace_root: str | Path,
    relative_packet_path: str,
    emitted_at: str,
) -> EmittedSignal:
    frontmatter = parsed.frontmatter
    stem = Path(parsed.path or "bootstrap.task.md").stem
    source_agent = (frontmatter.get("agent") or "BOOTSTRAP").strip() or "BOOTSTRAP"
    source_work_unit = frontmatter.get("bootstrap_work_unit_id") or f"wu-bootstrap-{_safe_id(stem)}"
    delta_id = frontmatter.get("bootstrap_delta_id") or f"delta-bootstrap-{_safe_id(stem)}"
    signal_type_text = (frontmatter.get("bootstrap_signal_type") or CanonicalSignalType.BLOCKED.value).strip().upper()
    try:
        signal_type = CanonicalSignalType(signal_type_text)
    except ValueError as exc:
        raise KernelBootstrapBridgeError(f"Unsupported bootstrap_signal_type: {signal_type_text}") from exc

    summary = _packet_summary(parsed)
    resolver = KernelAuthorityLineageManager()
    resolved_source_role = resolver.resolve_authority(workspace_root, "bootstrap_packet_agent", frontmatter.get("agent"))
    blocked_needed_from = resolver.resolve_authority(
        workspace_root,
        "bootstrap_blocked_escalation",
        frontmatter.get("bootstrap_needed_from"),
    )
    payload: dict[str, object] = {
        "work_unit_id": source_work_unit,
        "delta_id": delta_id,
        "receipt_path": relative_packet_path,
        "bootstrap_packet_path": relative_packet_path,
        "task_target": frontmatter.get("target"),
        "task_from": frontmatter.get("from"),
        "summary": summary,
    }
    if signal_type is CanonicalSignalType.BLOCKED:
        payload["blocker"] = frontmatter.get("bootstrap_blocker") or summary or "BOOTSTRAP_PACKET_READY"
        payload["needed_from"] = blocked_needed_from.resolved_name
        if blocked_needed_from.requested_name is not None:
            payload["requested_needed_from"] = blocked_needed_from.requested_name
        if blocked_needed_from.status != "CURRENT_AUTHORITY":
            payload["needed_from_resolution_status"] = blocked_needed_from.status
    elif signal_type is CanonicalSignalType.TASK_FAILED:
        payload["error"] = frontmatter.get("bootstrap_error") or summary or "BOOTSTRAP_PACKET_READY"
        payload["recoverable"] = _parse_bool(frontmatter.get("bootstrap_recoverable"), default=True)
    else:
        payload["output_path"] = relative_packet_path
        payload["confidence"] = float(frontmatter.get("bootstrap_confidence") or 1.0)

    return EmittedSignal(
        signal_id=f"sig-bootstrap-{_safe_id(stem)}-{_stamp_id(emitted_at)}",
        created_at=emitted_at,
        source_agent=source_agent,
        source_work_unit=source_work_unit,
        source_role=resolved_source_role.resolved_name,
        target="DAEMON",
        signal_type=signal_type,
        payload=payload,
        priority=_parse_priority(frontmatter.get("priority")),
        status=SignalLifecycleStatus.ACTIVE,
        related_artifacts=(relative_packet_path,),
    )


def _packet_summary(parsed: ParsedWorkflowPacket) -> str:
    goal = parsed.sections.get("Goal", "")
    collapsed = " ".join(line.strip() for line in goal.splitlines() if line.strip())
    if collapsed:
        return collapsed
    title = parsed.title or "Bootstrap packet ready for daemon routing."
    return _strip_title_prefix(title)


def _strip_title_prefix(title: str) -> str:
    lowered = title.lower()
    if lowered.startswith("mission:"):
        return title.split(":", 1)[1].strip()
    return title.strip()


def _parse_priority(value: str | None) -> WorkPriority:
    if value is None:
        return WorkPriority.P1_HIGH
    try:
        return WorkPriority(value)
    except ValueError as exc:
        raise KernelBootstrapBridgeError(f"Unsupported bootstrap priority: {value}") from exc


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y"}:
        return True
    if lowered in {"0", "false", "no", "n"}:
        return False
    raise KernelBootstrapBridgeError(f"Unsupported boolean text: {value}")


def _signal_filename(signal: EmittedSignal, stem: str) -> str:
    short = _SAFE_FILE_RE.sub("_", stem.upper()).strip("_") or "BOOTSTRAP"
    stamp = re.sub(r"[^0-9]", "", signal.created_at)[:14]
    return f"BOOTSTRAP_{signal.signal_type.value}_{short}_{stamp}.signal.json"


def _safe_id(text: str) -> str:
    safe = _SAFE_ID_RE.sub("-", text.lower()).strip("-")
    return safe or "bootstrap"


def _stamp_id(value: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", value.lower())


def _resolve_relative_dir(root: str | Path, relative_dir: Path) -> Path:
    return _resolve_relative_file(Path(root).resolve(), relative_dir)


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelBootstrapBridgeError(f"Absolute paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelBootstrapBridgeError(f"Path escapes workspace root: {relative_path}") from exc
    return resolved


def _relative_to_root(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root))


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
