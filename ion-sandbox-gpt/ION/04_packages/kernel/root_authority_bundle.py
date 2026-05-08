"""Helpers for the legacy root-authority bundle retained as containment evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
from pathlib import Path
import re
from typing import Any

from .index import KernelIndex
from .model import RootAuthorityBundleExerciseReceipt, RootAuthorityBundleExternalReturnReceipt
from .store import KernelStore


BUNDLE_ROOT_RELATIVE_PATH = Path(
    "ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/root_authority_bundle_2026-04-17"
)
_MARKDOWN_FILES = (
    "START_HERE.md",
    "CURSOR_CODEX_READ_MODE.md",
    "BROWSER_CHATGPT_READ_MODE.md",
    "CLAUDE_CODE_READ_MODE.md",
)
_LOCAL_BUNDLE_FILES = (*_MARKDOWN_FILES, "BUNDLE_MANIFEST.yaml")
_BACKTICK_REF_RE = re.compile(r"`([^`]+)`")
_YAML_KEY_RE = re.compile(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$")
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_CURRENT_CARRIER_KEY = "cursor_codex"
_EXTERNAL_CARRIER_KEYS = ("browser_chatgpt", "claude_code")
_EXTERNAL_BRIEF_FILENAMES = {
    "browser_chatgpt": "BROWSER_CHATGPT_EXTERNAL_EXERCISE_BRIEF.md",
    "claude_code": "CLAUDE_CODE_EXTERNAL_EXERCISE_BRIEF.md",
}
_EXTERNAL_RETURN_STUB_FILENAMES = {
    "browser_chatgpt": "BROWSER_CHATGPT_EXTERNAL_RETURN_STUB.md",
    "claude_code": "CLAUDE_CODE_EXTERNAL_RETURN_STUB.md",
}
_CARRIER_LABELS = {
    "cursor_codex": "Cursor",
    "browser_chatgpt": "Browser ChatGPT",
    "claude_code": "Claude Code",
}
_EXTERNAL_RETURN_ALLOWED_STATUSES = {"RETURNED", "HELD", "REJECTED", "LANDED_AS_WITNESS"}
_EXTERNAL_RETURN_REQUIRED_SECTIONS = (
    "Source Carrier",
    "Governing Inputs",
    "Produced Artifacts",
    "Proposed Delta or Patch",
    "Validation Notes",
    "Unresolved Drift / Risks",
    "Requested Landing Path",
)
_EXTERNAL_RETURN_SOURCE_CHASSIS = {
    "browser_chatgpt": "browser",
    "claude_code": "local_tooling",
}
_EXTERNAL_RETURN_ARCHIVE_DIRECTORY = "root_authority_bundle_external_return_packets"


@dataclass(frozen=True)
class RootAuthorityBundleSnapshot:
    bundle_root_relative_path: str
    manifest_relative_path: str
    status: str | None
    shared_entry: str | None
    forward_path_anchor: str | None
    carrier_entries: dict[str, str]
    decision_anchors: tuple[str, ...]
    root_terms: dict[str, str]
    bundle_files: dict[str, bool]
    missing_paths: tuple[str, ...]
    valid: bool


@dataclass(frozen=True)
class RootAuthorityBundleExternalExerciseBrief:
    carrier_key: str
    carrier_label: str
    created_at: str
    output_path: str
    output_relative_path: str | None
    shared_entry: str | None
    carrier_entry_path: str | None
    forward_path_anchor: str | None
    decision_anchors: tuple[str, ...]
    valid: bool
    warnings: tuple[str, ...]
    content: str


@dataclass(frozen=True)
class RootAuthorityBundleExternalReturnStub:
    carrier_key: str
    carrier_label: str
    created_at: str
    output_path: str
    output_relative_path: str | None
    governing_packet: str
    valid: bool
    warnings: tuple[str, ...]
    content: str


@dataclass(frozen=True)
class ParsedExternalReturnPacket:
    title: str | None
    frontmatter: dict[str, Any]
    section_names: tuple[str, ...]


class KernelRootAuthorityBundleError(Exception):
    """Raised when one root-authority bundle exercise cannot complete lawfully."""


class KernelRootAuthorityBundleManager:
    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "Q004_ROOT_AUTHORITY_BUNDLE_CURRENT_CARRIER_EXERCISE_V1",
            "notes": (
                "Q004 records the current carrier's successful startup-bundle exercise as one durable kernel receipt.",
                "This receipt proves a lawful startup path for the present carrier posture only.",
                "It does not claim external-carrier parity by itself.",
            ),
        }

    def external_return_policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "Q004_ROOT_AUTHORITY_BUNDLE_EXTERNAL_RETURN_INGESTION_V1",
            "notes": (
                "Q004 may ingest a completed external carrier return only from a structured EXTERNAL_RETURN packet.",
                "This receipt records one returned external packet as evidence without claiming parity beyond the cited carrier.",
                "External return ingestion remains governed by the corresponding bundle exercise brief.",
            ),
        }

    def record_exercise(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        workspace_root: str | Path,
        carrier_key: str = "cursor_codex",
        execution_mode: str = "BRANCH_LOCAL_EDITABLE_INSTALL",
        executor_identity: str | None = "STEWARD",
        created_at: str | None = None,
    ) -> RootAuthorityBundleExerciseReceipt:
        if carrier_key != _CURRENT_CARRIER_KEY:
            raise KernelRootAuthorityBundleError(
                "Durable root-authority bundle exercise receipts are limited to cursor_codex until an external carrier completes its own exercise. "
                "Use materialize_external_exercise_brief for browser_chatgpt or claude_code."
            )
        timestamp = created_at or _iso_now()
        snapshot = build_snapshot(Path(workspace_root).resolve())
        warnings: list[str] = []
        if not snapshot.valid:
            warnings.append("BUNDLE_INVALID")
        carrier_entry_path = snapshot.carrier_entries.get(carrier_key)
        if carrier_entry_path is None:
            warnings.append("UNKNOWN_CARRIER_KEY")

        receipt = RootAuthorityBundleExerciseReceipt(
            receipt_id=root_authority_bundle_exercise_receipt_id(carrier_key, timestamp),
            created_at=timestamp,
            policy_id=str(self.policy_surface()["policy_id"]),
            carrier_key=carrier_key,
            execution_mode=execution_mode,
            bundle_root_relative_path=snapshot.bundle_root_relative_path,
            manifest_relative_path=snapshot.manifest_relative_path,
            bundle_status=snapshot.status,
            executor_identity=(None if executor_identity is None else executor_identity.strip() or None),
            shared_entry=snapshot.shared_entry,
            forward_path_anchor=snapshot.forward_path_anchor,
            carrier_entry_path=carrier_entry_path,
            decision_anchors=snapshot.decision_anchors,
            missing_paths=snapshot.missing_paths,
            valid=snapshot.valid,
            next_action=(
                "Use the recorded carrier entry as the startup surface for the retained dual-center settlement."
                if snapshot.valid
                else "Repair the root-authority bundle before relying on it as a startup surface."
            ),
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def materialize_external_exercise_brief(
        self,
        *,
        workspace_root: str | Path,
        carrier_key: str,
        created_at: str | None = None,
        output_path: str | Path | None = None,
    ) -> RootAuthorityBundleExternalExerciseBrief:
        if carrier_key not in _EXTERNAL_CARRIER_KEYS:
            raise KernelRootAuthorityBundleError(
                "External exercise briefs are only defined for browser_chatgpt and claude_code."
            )
        timestamp = created_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        snapshot = build_snapshot(workspace)
        warnings: list[str] = []
        if not snapshot.valid:
            warnings.append("BUNDLE_INVALID")
        carrier_entry_path = snapshot.carrier_entries.get(carrier_key)
        if carrier_entry_path is None:
            warnings.append("UNKNOWN_CARRIER_KEY")
        output = _resolve_external_brief_output(workspace, carrier_key, output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        content = _render_external_exercise_brief(
            carrier_key=carrier_key,
            carrier_label=_carrier_label(carrier_key),
            created_at=timestamp,
            shared_entry=snapshot.shared_entry,
            carrier_entry_path=carrier_entry_path,
            decision_anchors=snapshot.decision_anchors,
            forward_path_anchor=snapshot.forward_path_anchor,
            root_terms=snapshot.root_terms,
        )
        output.write_text(content, encoding="utf-8")
        return RootAuthorityBundleExternalExerciseBrief(
            carrier_key=carrier_key,
            carrier_label=_carrier_label(carrier_key),
            created_at=timestamp,
            output_path=str(output),
            output_relative_path=_relative_to_workspace(output, workspace),
            shared_entry=snapshot.shared_entry,
            carrier_entry_path=carrier_entry_path,
            forward_path_anchor=snapshot.forward_path_anchor,
            decision_anchors=snapshot.decision_anchors,
            valid=snapshot.valid and carrier_entry_path is not None,
            warnings=tuple(dict.fromkeys(warnings)),
            content=content,
        )

    def latest_receipt(self, index: KernelIndex) -> RootAuthorityBundleExerciseReceipt | None:
        receipts = [
            record
            for record in index.records_by_type("root_authority_bundle_exercise_receipt")
            if isinstance(record, RootAuthorityBundleExerciseReceipt)
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: RootAuthorityBundleExerciseReceipt | None) -> dict[str, Any] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "carrier_key": receipt.carrier_key,
            "execution_mode": receipt.execution_mode,
            "executor_identity": receipt.executor_identity,
            "bundle_root_relative_path": receipt.bundle_root_relative_path,
            "manifest_relative_path": receipt.manifest_relative_path,
            "bundle_status": receipt.bundle_status,
            "shared_entry": receipt.shared_entry,
            "forward_path_anchor": receipt.forward_path_anchor,
            "carrier_entry_path": receipt.carrier_entry_path,
            "decision_anchors": list(receipt.decision_anchors),
            "missing_paths": list(receipt.missing_paths),
            "valid": receipt.valid,
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }

    def render_external_brief_projection(self, brief: RootAuthorityBundleExternalExerciseBrief) -> dict[str, Any]:
        return {
            "carrier_key": brief.carrier_key,
            "carrier_label": brief.carrier_label,
            "created_at": brief.created_at,
            "output_path": brief.output_path,
            "output_relative_path": brief.output_relative_path,
            "shared_entry": brief.shared_entry,
            "carrier_entry_path": brief.carrier_entry_path,
            "forward_path_anchor": brief.forward_path_anchor,
            "decision_anchors": list(brief.decision_anchors),
            "valid": brief.valid,
            "warnings": list(brief.warnings),
            "content": brief.content,
        }

    def materialize_external_return_stub(
        self,
        *,
        workspace_root: str | Path,
        carrier_key: str,
        created_at: str | None = None,
        output_path: str | Path | None = None,
    ) -> RootAuthorityBundleExternalReturnStub:
        if carrier_key not in _EXTERNAL_CARRIER_KEYS:
            raise KernelRootAuthorityBundleError(
                "External return stubs are only defined for browser_chatgpt and claude_code."
            )
        timestamp = created_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        snapshot = build_snapshot(workspace)
        warnings: list[str] = []
        if not snapshot.valid:
            warnings.append("BUNDLE_INVALID")
        governing_packet = _expected_external_brief_relative_path(carrier_key)
        output = _resolve_external_return_stub_output(workspace, carrier_key, output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        content = _render_external_return_stub(
            created_at=timestamp,
            carrier_key=carrier_key,
            carrier_label=_carrier_label(carrier_key),
            governing_packet=governing_packet,
        )
        output.write_text(content, encoding="utf-8")
        return RootAuthorityBundleExternalReturnStub(
            carrier_key=carrier_key,
            carrier_label=_carrier_label(carrier_key),
            created_at=timestamp,
            output_path=str(output),
            output_relative_path=_relative_to_workspace(output, workspace),
            governing_packet=governing_packet,
            valid=snapshot.valid,
            warnings=tuple(dict.fromkeys(warnings)),
            content=content,
        )

    def render_external_return_stub_projection(self, stub: RootAuthorityBundleExternalReturnStub) -> dict[str, Any]:
        return {
            "carrier_key": stub.carrier_key,
            "carrier_label": stub.carrier_label,
            "created_at": stub.created_at,
            "output_path": stub.output_path,
            "output_relative_path": stub.output_relative_path,
            "governing_packet": stub.governing_packet,
            "valid": stub.valid,
            "warnings": list(stub.warnings),
            "content": stub.content,
        }

    def record_external_return(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        workspace_root: str | Path,
        carrier_key: str,
        input_path: str | Path,
        created_at: str | None = None,
    ) -> RootAuthorityBundleExternalReturnReceipt:
        if carrier_key not in _EXTERNAL_CARRIER_KEYS:
            raise KernelRootAuthorityBundleError(
                "External return ingestion is only defined for browser_chatgpt and claude_code."
            )
        timestamp = created_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        source_path = Path(input_path)
        if not source_path.is_absolute():
            source_path = (workspace / source_path).resolve()
        if not source_path.is_file():
            raise KernelRootAuthorityBundleError(f"External return packet not found: {source_path}")

        snapshot = build_snapshot(workspace)
        source_text = source_path.read_text(encoding="utf-8")
        parsed = _parse_external_return_packet(source_text)
        frontmatter = parsed.frontmatter
        warnings: list[str] = []
        errors: list[str] = []

        if not snapshot.valid:
            warnings.append("BUNDLE_INVALID")

        type_value = _as_optional_string(frontmatter.get("type"))
        if type_value != "external_return":
            errors.append("type must be external_return")

        template_value = _as_optional_string(frontmatter.get("template"))
        if template_value != "EXTERNAL_RETURN":
            errors.append("template must be EXTERNAL_RETURN")

        status_value = _as_optional_string(frontmatter.get("status"))
        if status_value not in _EXTERNAL_RETURN_ALLOWED_STATUSES:
            errors.append("status must be RETURNED, HELD, REJECTED, or LANDED_AS_WITNESS")

        reported_from = _as_optional_string(frontmatter.get("from"))
        if reported_from is None:
            errors.append("from is required")
        elif reported_from != _carrier_label(carrier_key):
            warnings.append("REPORTED_FROM_LABEL_MISMATCH")

        source_chassis = _as_optional_string(frontmatter.get("source_chassis"))
        if source_chassis is None:
            errors.append("source_chassis is required")
        elif source_chassis != _EXTERNAL_RETURN_SOURCE_CHASSIS[carrier_key]:
            warnings.append("SOURCE_CHASSIS_MISMATCH")

        expected_governing_packet = _expected_external_brief_relative_path(carrier_key)
        governing_packet = _as_optional_string(frontmatter.get("governing_packet"))
        if governing_packet is None:
            errors.append("governing_packet is required")
        governing_packet_matches_expected = governing_packet == expected_governing_packet
        if governing_packet is not None and not governing_packet_matches_expected:
            errors.append(f"governing_packet must match {expected_governing_packet}")

        workspace_snapshot = _as_optional_string(frontmatter.get("workspace_snapshot"))
        if workspace_snapshot is None:
            errors.append("workspace_snapshot is required")

        target_owner = _as_optional_string(frontmatter.get("target_owner"))
        if target_owner is None:
            errors.append("target_owner is required")

        targets = tuple(
            str(item)
            for item in frontmatter.get("targets", ())
            if isinstance(item, str) and item.strip()
        )
        if not targets:
            errors.append("targets must name at least one bounded landing path")

        missing_sections = [
            section
            for section in _EXTERNAL_RETURN_REQUIRED_SECTIONS
            if section not in parsed.section_names
        ]
        if missing_sections:
            errors.append("missing required sections: " + ", ".join(missing_sections))

        if errors:
            raise KernelRootAuthorityBundleError("; ".join(errors))

        next_action = {
            "RETURNED": "Review returned findings and decide whether to strengthen q004 for this carrier or preserve one contradiction as witness.",
            "HELD": "Fill and resubmit the held external return before treating it as completed carrier evidence.",
            "REJECTED": "Preserve the rejected return as witness and name the blocking defect explicitly before any retrial.",
            "LANDED_AS_WITNESS": "Preserve the external return as witness and keep q004 parity claims bounded to the proven carrier set.",
        }[status_value or "HELD"]
        receipt_id = root_authority_bundle_external_return_receipt_id(carrier_key, timestamp)
        archived_packet_path = _archive_external_return_packet(store, receipt_id, source_text)
        packet_checksum = _content_checksum(source_text)

        receipt = RootAuthorityBundleExternalReturnReceipt(
            receipt_id=receipt_id,
            created_at=timestamp,
            policy_id=str(self.external_return_policy_surface()["policy_id"]),
            carrier_key=carrier_key,
            external_return_status=status_value or "HELD",
            reported_from=reported_from or _carrier_label(carrier_key),
            source_chassis=source_chassis or _EXTERNAL_RETURN_SOURCE_CHASSIS[carrier_key],
            governing_packet=governing_packet or expected_governing_packet,
            governing_packet_matches_expected=governing_packet_matches_expected,
            workspace_snapshot=workspace_snapshot or "",
            target_owner=target_owner or "",
            targets=targets,
            source_path=str(source_path),
            source_relative_path=_relative_to_workspace(source_path, workspace),
            archived_packet_path=str(archived_packet_path),
            archived_packet_relative_path=_relative_to_workspace(archived_packet_path, workspace),
            packet_checksum=packet_checksum,
            title=parsed.title,
            section_names=parsed.section_names,
            valid=True,
            next_action=next_action,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_external_return_receipt(
        self,
        index: KernelIndex,
    ) -> RootAuthorityBundleExternalReturnReceipt | None:
        receipts = [
            record
            for record in index.records_by_type("root_authority_bundle_external_return_receipt")
            if isinstance(record, RootAuthorityBundleExternalReturnReceipt)
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_external_return_receipt_projection(
        self,
        receipt: RootAuthorityBundleExternalReturnReceipt | None,
    ) -> dict[str, Any] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "carrier_key": receipt.carrier_key,
            "external_return_status": receipt.external_return_status,
            "reported_from": receipt.reported_from,
            "source_chassis": receipt.source_chassis,
            "governing_packet": receipt.governing_packet,
            "governing_packet_matches_expected": receipt.governing_packet_matches_expected,
            "workspace_snapshot": receipt.workspace_snapshot,
            "target_owner": receipt.target_owner,
            "targets": list(receipt.targets),
            "source_path": receipt.source_path,
            "source_relative_path": receipt.source_relative_path,
            "archived_packet_path": receipt.archived_packet_path,
            "archived_packet_relative_path": receipt.archived_packet_relative_path,
            "packet_checksum": receipt.packet_checksum,
            "title": receipt.title,
            "section_names": list(receipt.section_names),
            "valid": receipt.valid,
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


def build_snapshot(workspace_root: Path) -> RootAuthorityBundleSnapshot:
    bundle_root = (workspace_root / BUNDLE_ROOT_RELATIVE_PATH).resolve()
    manifest_path = bundle_root / "BUNDLE_MANIFEST.yaml"
    bundle_files = {name: (bundle_root / name).is_file() for name in _LOCAL_BUNDLE_FILES}
    parsed = _parse_bundle_manifest(manifest_path) if manifest_path.is_file() else {}

    missing_paths: list[str] = []

    # Validate references carried by the manifest itself.
    refs = []
    refs.extend(
        item
        for item in (
            parsed.get("shared_entry"),
            parsed.get("forward_path_anchor"),
        )
        if isinstance(item, str) and item
    )
    refs.extend(str(item) for item in parsed.get("decision_anchors", ()) if isinstance(item, str))
    refs.extend(str(item) for item in parsed.get("supersedes_as_first_startup_surface", ()) if isinstance(item, str))
    refs.extend(str(item) for item in parsed.get("carrier_entries", {}).values() if isinstance(item, str))
    refs.extend(str(item) for item in parsed.get("root_terms", {}).values() if isinstance(item, str))

    for ref in refs:
        resolved = _resolve_reference(workspace_root, bundle_root, ref)
        if resolved is not None and not resolved.exists():
            missing_paths.append(ref)

    # Validate markdown backtick references inside bundle files.
    for filename in _MARKDOWN_FILES:
        path = bundle_root / filename
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for ref in _BACKTICK_REF_RE.findall(text):
            resolved = _resolve_reference(workspace_root, bundle_root, ref)
            if resolved is not None and not resolved.exists():
                missing_paths.append(ref)

    unique_missing = tuple(sorted(set(missing_paths)))
    bundle_root_relative = _relative_to_workspace(bundle_root, workspace_root)
    manifest_relative = _relative_to_workspace(manifest_path, workspace_root)
    status = parsed.get("status") if isinstance(parsed.get("status"), str) else None
    valid = (
        all(bundle_files.values())
        and status == "READ_TESTED_STABLE_STARTUP_EXPORT"
        and not unique_missing
    )

    return RootAuthorityBundleSnapshot(
        bundle_root_relative_path=bundle_root_relative or str(bundle_root),
        manifest_relative_path=manifest_relative or str(manifest_path),
        status=status,
        shared_entry=_as_optional_string(parsed.get("shared_entry")),
        forward_path_anchor=_as_optional_string(parsed.get("forward_path_anchor")),
        carrier_entries={
            str(key): str(value)
            for key, value in parsed.get("carrier_entries", {}).items()
            if isinstance(key, str) and isinstance(value, str)
        },
        decision_anchors=tuple(
            str(item) for item in parsed.get("decision_anchors", ()) if isinstance(item, str)
        ),
        root_terms={
            str(key): str(value)
            for key, value in parsed.get("root_terms", {}).items()
            if isinstance(key, str) and isinstance(value, str)
        },
        bundle_files=bundle_files,
        missing_paths=unique_missing,
        valid=valid,
    )


def render_snapshot(snapshot: RootAuthorityBundleSnapshot) -> dict[str, Any]:
    return {
        "bundle_root_relative_path": snapshot.bundle_root_relative_path,
        "manifest_relative_path": snapshot.manifest_relative_path,
        "status": snapshot.status,
        "shared_entry": snapshot.shared_entry,
        "forward_path_anchor": snapshot.forward_path_anchor,
        "carrier_entries": dict(snapshot.carrier_entries),
        "decision_anchors": list(snapshot.decision_anchors),
        "root_terms": dict(snapshot.root_terms),
        "bundle_files": dict(snapshot.bundle_files),
        "missing_paths": list(snapshot.missing_paths),
        "valid": snapshot.valid,
    }


def root_authority_bundle_exercise_receipt_id(carrier_key: str, created_at: str) -> str:
    return f"root-authority-bundle-exercise-{_slug(carrier_key)}-{_slug(created_at)}"


def root_authority_bundle_external_return_receipt_id(carrier_key: str, created_at: str) -> str:
    return f"root-authority-bundle-external-return-{_slug(carrier_key)}-{_slug(created_at)}"


def _content_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _as_optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _parse_bundle_manifest(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_dict_key: str | None = None
    current_list_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0:
            current_dict_key = None
            current_list_key = None
            match = _YAML_KEY_RE.match(stripped)
            if not match:
                continue
            key, value = match.groups()
            value = (value or "").strip()
            if value in {"", ">-", ">", "|", "|-"}:
                if key in {"carrier_entries", "root_terms"}:
                    data[key] = {}
                    current_dict_key = key
                elif key in {"decision_anchors", "supersedes_as_first_startup_surface"}:
                    data[key] = []
                    current_list_key = key
                else:
                    data[key] = ""
                continue
            data[key] = value
            continue

        if indent == 2 and current_dict_key is not None:
            key, sep, value = stripped.partition(":")
            if sep:
                data[current_dict_key][key.strip()] = value.strip()
            continue

        if indent == 2 and current_list_key is not None and stripped.startswith("- "):
            data[current_list_key].append(stripped[2:].strip())

    return data


def _resolve_reference(workspace_root: Path, bundle_root: Path, ref: str) -> Path | None:
    if ref.startswith("/home/sev/"):
        return Path(ref)
    if ref.startswith("ION/"):
        return (workspace_root / ref).resolve()
    if ref in _LOCAL_BUNDLE_FILES:
        return (bundle_root / ref).resolve()
    return None


def _relative_to_workspace(path: Path, workspace_root: Path) -> str | None:
    try:
        return str(path.relative_to(workspace_root))
    except ValueError:
        return None


def _resolve_external_brief_output(workspace_root: Path, carrier_key: str, output_path: str | Path | None) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace_root / out
        return out.resolve()
    return (workspace_root / BUNDLE_ROOT_RELATIVE_PATH / _EXTERNAL_BRIEF_FILENAMES[carrier_key]).resolve()


def _resolve_external_return_stub_output(workspace_root: Path, carrier_key: str, output_path: str | Path | None) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace_root / out
        return out.resolve()
    return (workspace_root / BUNDLE_ROOT_RELATIVE_PATH / _EXTERNAL_RETURN_STUB_FILENAMES[carrier_key]).resolve()


def _archive_external_return_packet(store: KernelStore, receipt_id: str, content: str) -> Path:
    archive_root = (store.root / _EXTERNAL_RETURN_ARCHIVE_DIRECTORY).resolve()
    archive_root.mkdir(parents=True, exist_ok=True)
    archive_path = (archive_root / f"{receipt_id}.md").resolve()
    archive_path.write_text(content, encoding="utf-8")
    return archive_path


def _expected_external_brief_relative_path(carrier_key: str) -> str:
    return f"{BUNDLE_ROOT_RELATIVE_PATH.as_posix()}/{_EXTERNAL_BRIEF_FILENAMES[carrier_key]}"


def _parse_external_return_packet(text: str) -> ParsedExternalReturnPacket:
    lines = text.splitlines()
    frontmatter: dict[str, Any] = {}
    body_lines = lines
    if lines and lines[0].strip() == "---":
        try:
            end_index = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
        except StopIteration as exc:
            raise KernelRootAuthorityBundleError(
                "External return packet is missing closing frontmatter delimiter."
            ) from exc
        frontmatter = _parse_frontmatter_block(lines[1:end_index])
        body_lines = lines[end_index + 1 :]

    title: str | None = None
    section_names: list[str] = []
    for line in body_lines:
        stripped = line.strip()
        if title is None and stripped.startswith("# "):
            title = stripped[2:].strip() or None
        elif stripped.startswith("## "):
            section_names.append(stripped[3:].strip())
    return ParsedExternalReturnPacket(
        title=title,
        frontmatter=frontmatter,
        section_names=tuple(section_names),
    )


def _parse_frontmatter_block(lines: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if indent == 0:
            current_list_key = None
            match = _YAML_KEY_RE.match(stripped)
            if not match:
                continue
            key, value = match.groups()
            value = (value or "").strip()
            if value == "":
                data[key] = []
                current_list_key = key
                continue
            data[key] = value
            continue
        if indent == 2 and current_list_key is not None and stripped.startswith("- "):
            data[current_list_key].append(stripped[2:].strip())
    return data


def _render_external_exercise_brief(
    *,
    carrier_key: str,
    carrier_label: str,
    created_at: str,
    shared_entry: str | None,
    carrier_entry_path: str | None,
    decision_anchors: tuple[str, ...],
    forward_path_anchor: str | None,
    root_terms: dict[str, str],
) -> str:
    shared = shared_entry or "START_HERE.md"
    carrier_entry = carrier_entry_path or "UNKNOWN_CARRIER_ENTRY"
    lines = [
        f"# {carrier_label} External Exercise Brief",
        "",
        f"Created: `{created_at}`",
        "",
        "## Purpose",
        "",
        "Exercise the retained dual-center startup bundle from this external carrier without claiming parity that has not yet been proven.",
        "",
        "## Read Order",
        "",
        f"1. `{shared}`",
        f"2. `{carrier_entry}`",
    ]
    for anchor in decision_anchors:
        lines.append(f"{len(lines) - lines.index('## Read Order') - 1}. `{anchor}`")  # placeholder, corrected below
    if forward_path_anchor:
        lines.append(f"`{forward_path_anchor}`")
    # Rebuild ordered read list cleanly after the fixed first two items.
    read_refs = [shared, carrier_entry, *decision_anchors]
    if forward_path_anchor:
        read_refs.append(forward_path_anchor)
    read_block = ["## Read Order", ""]
    for index, ref in enumerate(read_refs, start=1):
        read_block.append(f"{index}. `{ref}`")
    lines = [
        f"# {carrier_label} External Exercise Brief",
        "",
        f"Created: `{created_at}`",
        "",
        "## Purpose",
        "",
        "Exercise the retained dual-center startup bundle from this external carrier without claiming parity that has not yet been proven.",
        "",
        *read_block,
        "",
        "## Required Findings",
        "",
        f"- name the packaged runnable content root: `{root_terms.get('packaged_current_generation_root', 'UNKNOWN')}`",
        f"- name the packaged shell root used for package-aware commands: `{root_terms.get('packaged_current_generation_shell_root', 'UNKNOWN')}`",
        f"- name the retained top-level production root: `{root_terms.get('top_level_production_root', 'UNKNOWN')}`",
        f"- name the embedded residue lane: `{root_terms.get('embedded_residue_lane', 'UNKNOWN')}`",
        "- state that single-root ratification is not authorized in the current phase",
        "- state that the top-level production external transport shell remains retained support/witness-only",
        "",
        "## Return Contract",
        "",
        "- return a cited written result naming the four path classes above",
        "- state whether the bundle was sufficient for startup without hidden chat context",
        "- report any ambiguity, missing anchor, or path conflict immediately",
        "- do not claim external-carrier parity or write a durable bundle exercise receipt from this environment",
        "",
        "## Boundary",
        "",
        "This brief prepares an external-carrier exercise. It is not itself proof of browser or Claude parity.",
        "",
    ]
    return "\n".join(lines)


def _render_external_return_stub(
    *,
    created_at: str,
    carrier_key: str,
    carrier_label: str,
    governing_packet: str,
) -> str:
    source_chassis = {
        "browser_chatgpt": "browser",
        "claude_code": "local_tooling",
    }[carrier_key]
    title = f"{carrier_label} Root Authority Bundle Exercise Return"
    targets = [
        "ION/06_intelligence/decisions/2026-04-17_root_authority_carrier_export_bundle_canonicalization_decision.md",
        "ION/06_intelligence/orchestration/2026-04-17_root_authority_bundle_external_carrier_exercise_briefs.md",
        "ION/03_registry/reintegration/canonicalization_queue.yaml",
    ]
    lines = [
        "---",
        "type: external_return",
        "template: EXTERNAL_RETURN",
        f"created: {created_at}",
        "status: HELD",
        f"from: {carrier_label}",
        f"source_chassis: {source_chassis}",
        f"governing_packet: {governing_packet}",
        "workspace_snapshot: root_authority_bundle_2026_04_17",
        "target_owner: STEWARD",
        "targets:",
    ]
    lines.extend(f"  - {target}" for target in targets)
    lines.extend([
        "---",
        "",
        f"# External Return: {title}",
        "",
        "## Source Carrier",
        "",
        f"- carrier key: `{carrier_key}`",
        f"- carrier label: `{carrier_label}`",
        "",
        "## Governing Inputs",
        "",
        f"- `{governing_packet}`",
        f"- `{BUNDLE_ROOT_RELATIVE_PATH.as_posix()}/START_HERE.md`",
        "",
        "## Produced Artifacts",
        "",
        "- none yet; fill with any returned notes, transcripts, or structured findings",
        "",
        "## Proposed Delta or Patch",
        "",
        "- state whether q004 should remain unchanged, gain new anchors, or escalate one ambiguity",
        "",
        "## Validation Notes",
        "",
        "- name the packaged content root, packaged shell root, top-level production root, and embedded residue lane",
        "- state whether startup succeeded without hidden chat context",
        "- state whether any bundle anchor was insufficient or misleading",
        "",
        "## Unresolved Drift / Risks",
        "",
        "- list any ambiguity, missing anchor, or contradictory startup instruction",
        "",
        "## Requested Landing Path",
        "",
        "- if successful, update q004 proof posture without claiming external parity beyond this carrier",
        "- if ambiguous, land as witness and preserve contradiction explicitly",
        "",
    ])
    return "\n".join(lines)


def _carrier_label(carrier_key: str) -> str:
    return _CARRIER_LABELS.get(carrier_key, carrier_key)


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def _slug(value: str) -> str:
    compact = _SAFE_ID_RE.sub("-", value.lower()).strip("-")
    return compact or "value"
