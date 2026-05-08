"""Witness-only template completion event scanner for the evented template file graph.

This module implements the first safe runnable slice of the Evented Template File
Graph law. It discovers template-instantiated markdown files, classifies whether
they are completion candidates, validates only the minimum witness-only envelope,
and emits durable dry-run Template Completion Event witness JSON files.

It intentionally does not mutate source files, kernel graph state, indexes,
schedules, registries, or downstream work. Those reactions must remain separate
from Phase 1 witness generation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .contract_bound_event_runtime import gate_template_completion_by_contract
from .template_contract_registry import load_contracts_if_projection_exists


class KernelTemplateCompletionEventError(Exception):
    """Raised when witness-only template completion scanning cannot proceed."""


@dataclass(frozen=True)
class TemplateCompletionWatchRule:
    """A bounded watch rule for template-instantiated markdown files."""

    rule_id: str
    path_glob: str
    template_class: str = "markdown_front_matter"
    required_fields: tuple[str, ...] = ("type", "status")
    active_statuses: tuple[str, ...] = ("ACTIVE", "READY", "COMPLETE", "COMPLETED", "RATIFY")
    ignored_path_parts: tuple[str, ...] = (".pytest_cache", "__pycache__")


@dataclass(frozen=True)
class TemplateCompletionCandidate:
    """One discovered file and its witness-only classification state."""

    source_path: str
    rule_id: str
    template_class: str
    front_matter: dict[str, Any]
    content_sha256: str
    completion_state: str
    template_id: str = ""
    contract_bound: bool = False
    contract_status: str = ""
    missing_contract_fields: tuple[str, ...] = ()
    missing_required_fields: tuple[str, ...] = ()
    refusal_reason: str = ""


@dataclass(frozen=True)
class TemplateCompletionEventWitness:
    """A dry-run event witness emitted from a completed template file."""

    event_id: str
    event_type: str
    source_path: str
    rule_id: str
    template_class: str
    emitted_at: str
    witness_only: bool
    content_sha256: str
    front_matter: dict[str, Any]
    allowed_phase: str
    downstream_reactions_blocked: bool
    template_id: str = ""
    contract_bound: bool = False
    contract_status: str = ""
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateCompletionScanReceipt:
    """Summary receipt for one witness-only scanner pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    candidate_count: int
    completed_count: int
    refused_count: int
    witness_count: int
    witness_paths: tuple[str, ...]
    refused_candidates: tuple[TemplateCompletionCandidate, ...]


class KernelTemplateCompletionWatcher:
    """Witness-only scanner for template completion events.

    Phase 1 contract:
    - May scan files.
    - May parse front matter.
    - May emit dry-run witness JSON files.
    - Must not mutate source files or downstream graph state.
    """

    DEFAULT_RULES: tuple[TemplateCompletionWatchRule, ...] = (
        TemplateCompletionWatchRule(
            rule_id="watch.context_graph_inbox_tasks",
            path_glob="ION/05_context/inbox/**/*.md",
            required_fields=("type", "status"),
        ),
        TemplateCompletionWatchRule(
            rule_id="watch.context_templates",
            path_glob="ION/07_templates/**/*.md",
            required_fields=("template_id",),
            active_statuses=("ACTIVE", "READY", "COMPLETE", "COMPLETED", "RATIFY", "DRAFT"),
        ),
    )

    def scan(
        self,
        workspace_root: Path,
        *,
        rules: Iterable[TemplateCompletionWatchRule] | None = None,
        emitted_at: str | None = None,
        write_witnesses: bool = True,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> TemplateCompletionScanReceipt:
        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateCompletionEventError(f"workspace root does not exist: {root}")

        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        active_rules = tuple(rules or self.DEFAULT_RULES)
        runtime_contracts = template_contracts
        if runtime_contracts is None:
            runtime_contracts = load_contracts_if_projection_exists(root)
        candidates = self.discover_candidates(root, active_rules, template_contracts=runtime_contracts)
        completed = tuple(c for c in candidates if c.completion_state == "VALIDATED_COMPLETE")
        refused = tuple(c for c in candidates if c.completion_state != "VALIDATED_COMPLETE")
        witnesses: list[TemplateCompletionEventWitness] = [
            self.make_witness(candidate, emitted_at=timestamp) for candidate in completed
        ]
        witness_paths: list[str] = []
        if write_witnesses:
            for witness in witnesses:
                path = self.write_witness(root, witness)
                witness_paths.append(path.relative_to(root).as_posix())
        receipt_id = self._stable_id("template-completion-scan", root.as_posix(), timestamp)
        receipt = TemplateCompletionScanReceipt(
            receipt_id=receipt_id,
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            candidate_count=len(candidates),
            completed_count=len(completed),
            refused_count=len(refused),
            witness_count=len(witnesses),
            witness_paths=tuple(witness_paths),
            refused_candidates=refused,
        )
        if write_witnesses:
            self.write_scan_receipt(root, receipt)
        return receipt

    def discover_candidates(
        self,
        workspace_root: Path,
        rules: Iterable[TemplateCompletionWatchRule],
        *,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> tuple[TemplateCompletionCandidate, ...]:
        candidates: list[TemplateCompletionCandidate] = []
        seen: set[Path] = set()
        for rule in rules:
            for path in sorted(workspace_root.glob(rule.path_glob)):
                if path in seen or not path.is_file():
                    continue
                seen.add(path)
                if any(part in rule.ignored_path_parts for part in path.parts):
                    continue
                candidates.append(self.classify_file(workspace_root, path, rule, template_contracts=template_contracts))
        return tuple(candidates)

    def classify_file(
        self,
        workspace_root: Path,
        path: Path,
        rule: TemplateCompletionWatchRule,
        *,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> TemplateCompletionCandidate:
        text = path.read_text(encoding="utf-8")
        front_matter = _parse_markdown_front_matter(text)
        template_id = _resolve_template_id(front_matter, rule)
        missing = tuple(
            field
            for field in rule.required_fields
            if not _front_matter_has_required_field(front_matter, field)
        )
        rel = path.relative_to(workspace_root).as_posix()
        content_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if missing:
            return TemplateCompletionCandidate(
                source_path=rel,
                rule_id=rule.rule_id,
                template_class=rule.template_class,
                front_matter=front_matter,
                content_sha256=content_sha,
                completion_state="BLOCKED_OR_REFUSED",
                template_id=template_id,
                missing_required_fields=missing,
                refusal_reason="MISSING_REQUIRED_FIELDS",
            )
        status = str(front_matter.get("status", "")).upper()
        if "status" in rule.required_fields and status not in rule.active_statuses:
            return TemplateCompletionCandidate(
                source_path=rel,
                rule_id=rule.rule_id,
                template_class=rule.template_class,
                front_matter=front_matter,
                content_sha256=content_sha,
                completion_state="BLOCKED_OR_REFUSED",
                template_id=template_id,
                refusal_reason="STATUS_NOT_EVENTABLE",
            )
        if template_contracts is not None:
            gate = gate_template_completion_by_contract(template_id, template_contracts)
            if not gate.allowed:
                return TemplateCompletionCandidate(
                    source_path=rel,
                    rule_id=rule.rule_id,
                    template_class=rule.template_class,
                    front_matter=front_matter,
                    content_sha256=content_sha,
                    completion_state="BLOCKED_OR_REFUSED",
                    template_id=template_id,
                    contract_bound=True,
                    contract_status=gate.contract_status,
                    missing_contract_fields=gate.missing_fields,
                    refusal_reason=gate.blocked_reason or "TEMPLATE_METADATA_CONTRACT_BLOCKED_EVENT",
                )
            contract_bound = True
            contract_status = gate.contract_status
        else:
            contract_bound = False
            contract_status = ""
        return TemplateCompletionCandidate(
            source_path=rel,
            rule_id=rule.rule_id,
            template_class=rule.template_class,
            front_matter=front_matter,
            content_sha256=content_sha,
            completion_state="VALIDATED_COMPLETE",
            template_id=template_id,
            contract_bound=contract_bound,
            contract_status=contract_status,
        )

    def make_witness(
        self,
        candidate: TemplateCompletionCandidate,
        *,
        emitted_at: str,
    ) -> TemplateCompletionEventWitness:
        if candidate.completion_state != "VALIDATED_COMPLETE":
            raise KernelTemplateCompletionEventError(
                f"cannot emit witness for incomplete candidate: {candidate.source_path}"
            )
        event_id = self._stable_id(
            "template-completion-event",
            candidate.source_path,
            candidate.content_sha256,
            emitted_at,
        )
        notes = [
            "Witness-only event: no source graph mutation performed.",
            "Downstream reaction routing is intentionally blocked in Phase 1.",
        ]
        if candidate.contract_bound:
            notes.append("Template metadata contract gate passed before event witness emission.")
        return TemplateCompletionEventWitness(
            event_id=event_id,
            event_type="TEMPLATE_COMPLETION_EVENT",
            source_path=candidate.source_path,
            rule_id=candidate.rule_id,
            template_class=candidate.template_class,
            emitted_at=emitted_at,
            witness_only=True,
            content_sha256=candidate.content_sha256,
            front_matter=candidate.front_matter,
            allowed_phase="PHASE_1_WITNESS_ONLY",
            downstream_reactions_blocked=True,
            template_id=candidate.template_id,
            contract_bound=candidate.contract_bound,
            contract_status=candidate.contract_status,
            notes=tuple(notes),
        )

    def write_witness(self, workspace_root: Path, witness: TemplateCompletionEventWitness) -> Path:
        output_dir = (
            Path(workspace_root)
            / "ION/05_context/history/template_completion_event_witnesses"
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{witness.event_id}.template_completion_event_witness.json"
        if path.exists():
            return path
        path.write_text(
            json.dumps(_to_jsonable(witness), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path


    def write_scan_receipt(self, workspace_root: Path, receipt: TemplateCompletionScanReceipt) -> Path:
        output_dir = (
            Path(workspace_root)
            / "ION/05_context/history/template_completion_scan_receipts"
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_completion_scan_receipt.json"
        if path.exists():
            return path
        path.write_text(
            json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return path

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateCompletionWatcher = KernelTemplateCompletionWatcher
IonTemplateCompletionEventError = KernelTemplateCompletionEventError


def _resolve_template_id(front_matter: dict[str, Any], rule: TemplateCompletionWatchRule) -> str:
    for key in ("template_id", "type", "packet_type", "template_class"):
        value = front_matter.get(key)
        if value:
            return str(value)
    return rule.template_class


def _front_matter_has_required_field(front_matter: dict[str, Any], field: str) -> bool:
    if front_matter.get(field):
        return True
    if field == "type" and front_matter.get("packet_type"):
        return True
    if field == "packet_type" and front_matter.get("type"):
        return True
    return False


def _parse_markdown_front_matter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end].strip().splitlines()
    parsed: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in block:
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            existing = parsed.setdefault(current_key, [])
            if isinstance(existing, list):
                existing.append(line[4:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            parsed[key] = []
        elif value.lower() in {"true", "false"}:
            parsed[key] = value.lower() == "true"
        else:
            parsed[key] = value.strip('"\'')
    return parsed


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value
