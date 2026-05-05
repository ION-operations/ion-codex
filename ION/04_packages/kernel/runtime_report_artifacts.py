"""Bounded runtime-report artifact emission helpers for the active ION kernel stack.

This module sits one layer above runtime-state rendering. It does not create a new
kernel state family. It writes selected operator-facing runtime packets into an
explicit generated-state path under a supplied workspace root, using the same
bounded output discipline as receipts and dispatch packets.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re

from .index import KernelIndex
from .model import AuthorityClass, KernelRecord, OpenQuestion, PlannerManifest, StrEnum
from .runtime_reporting import KernelRuntimeStateReporter
from .runtime_report_anchors import anchor_tag, artifact_anchor
from .runtime_state_views import KernelRuntimeStateView


class KernelRuntimeReportArtifactError(Exception):
    """Raised when one runtime-report artifact cannot be emitted lawfully."""


class RuntimeReportArtifactKind(StrEnum):
    SCOPE_STATUS = "SCOPE_STATUS"
    PLANNER_MANIFEST = "PLANNER_MANIFEST"
    REVIEW = "REVIEW"


@dataclass(frozen=True)
class RuntimeReportArtifact(KernelRecord):
    artifact_id: str
    artifact_kind: RuntimeReportArtifactKind
    generated_at: str
    authority_class: AuthorityClass
    source_ref: str
    relative_output_path: str
    runtime_refs: tuple[str, ...] = ()
    rendered_report: str = ""
    anchor_id: str = ""


@dataclass(frozen=True)
class RuntimeReportArtifactPreparation:
    artifact: RuntimeReportArtifact
    output_path: Path


@dataclass(frozen=True)
class RuntimeReportArtifactResult:
    preparation: RuntimeReportArtifactPreparation


class KernelRuntimeReportArtifactEmitter:
    """Emit bounded runtime-state packets as explicit GENERATED_STATE artifacts."""

    def __init__(self, *, runtime_reporter: KernelRuntimeStateReporter | None = None) -> None:
        self._runtime_reporter = runtime_reporter or KernelRuntimeStateReporter()
        self._runtime_state_view = KernelRuntimeStateView()

    def prepare_scope_status_artifact(
        self,
        index: KernelIndex,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/status",
        generated_at: str | None = None,
        **render_kwargs,
    ) -> RuntimeReportArtifactPreparation:
        bundle = self._runtime_reporter.render_scope_status_report(
            index,
            scope_type,
            scope_ref,
            created_at=generated_at,
            **render_kwargs,
        )
        source_ref = f"{scope_type}:{scope_ref}"
        return self._prepare_artifact(
            workspace_root=workspace_root,
            output_path=output_path,
            default_relative=Path(reports_dir) / _timestamped_filename(
                prefix=f"scope-{scope_type.lower()}-{_safe_name(scope_ref)}",
                suffix="runtime_status",
                generated_at=generated_at,
            ),
            artifact_kind=RuntimeReportArtifactKind.SCOPE_STATUS,
            artifact_id=f"scope-status-{_safe_name(scope_type)}-{_safe_name(scope_ref)}",
            generated_at=generated_at,
            source_ref=source_ref,
            runtime_refs=bundle.scope_view.state_refs,
            rendered_report=bundle.rendered_report,
        )

    def emit_scope_status_artifact(
        self,
        index: KernelIndex,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/status",
        generated_at: str | None = None,
        **render_kwargs,
    ) -> RuntimeReportArtifactResult:
        preparation = self.prepare_scope_status_artifact(
            index,
            scope_type,
            scope_ref,
            workspace_root,
            output_path=output_path,
            reports_dir=reports_dir,
            generated_at=generated_at,
            **render_kwargs,
        )
        return self._emit(preparation)

    def prepare_planner_manifest_artifact(
        self,
        index: KernelIndex,
        manifest_id: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/planner_manifests",
        generated_at: str | None = None,
    ) -> RuntimeReportArtifactPreparation:
        rendered = self._runtime_reporter.render_planner_manifest_packet(index, manifest_id)
        return self._prepare_artifact(
            workspace_root=workspace_root,
            output_path=output_path,
            default_relative=Path(reports_dir) / _timestamped_filename(
                prefix=f"manifest-{_safe_name(manifest_id)}",
                suffix="planner_packet",
                generated_at=generated_at,
            ),
            artifact_kind=RuntimeReportArtifactKind.PLANNER_MANIFEST,
            artifact_id=f"planner-manifest-{_safe_name(manifest_id)}",
            generated_at=generated_at,
            source_ref=f"MANIFEST:{manifest_id}",
            runtime_refs=self._runtime_refs_for_manifest(index, manifest_id),
            rendered_report=rendered,
        )

    def emit_planner_manifest_artifact(
        self,
        index: KernelIndex,
        manifest_id: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/planner_manifests",
        generated_at: str | None = None,
    ) -> RuntimeReportArtifactResult:
        preparation = self.prepare_planner_manifest_artifact(
            index,
            manifest_id,
            workspace_root,
            output_path=output_path,
            reports_dir=reports_dir,
            generated_at=generated_at,
        )
        return self._emit(preparation)

    def prepare_review_packet_artifact(
        self,
        index: KernelIndex,
        question_id: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/reviews",
        generated_at: str | None = None,
    ) -> RuntimeReportArtifactPreparation:
        rendered = self._runtime_reporter.render_review_packet(index, question_id)
        return self._prepare_artifact(
            workspace_root=workspace_root,
            output_path=output_path,
            default_relative=Path(reports_dir) / _timestamped_filename(
                prefix=f"review-{_safe_name(question_id)}",
                suffix="review_packet",
                generated_at=generated_at,
            ),
            artifact_kind=RuntimeReportArtifactKind.REVIEW,
            artifact_id=f"review-packet-{_safe_name(question_id)}",
            generated_at=generated_at,
            source_ref=f"QUESTION:{question_id}",
            runtime_refs=self._runtime_refs_for_review(index, question_id),
            rendered_report=rendered,
        )

    def emit_review_packet_artifact(
        self,
        index: KernelIndex,
        question_id: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        reports_dir: str = "ION/05_context/runtime_reports/reviews",
        generated_at: str | None = None,
    ) -> RuntimeReportArtifactResult:
        preparation = self.prepare_review_packet_artifact(
            index,
            question_id,
            workspace_root,
            output_path=output_path,
            reports_dir=reports_dir,
            generated_at=generated_at,
        )
        return self._emit(preparation)

    def _prepare_artifact(
        self,
        *,
        workspace_root: str | Path,
        output_path: str | Path | None,
        default_relative: Path,
        artifact_kind: RuntimeReportArtifactKind,
        artifact_id: str,
        generated_at: str | None,
        source_ref: str,
        runtime_refs: tuple[str, ...],
        rendered_report: str,
    ) -> RuntimeReportArtifactPreparation:
        root = Path(workspace_root).resolve()
        root.mkdir(parents=True, exist_ok=True)
        relative = Path(output_path) if output_path is not None else default_relative
        resolved = _resolve_relative_file(root, relative)
        generated = generated_at or _iso_now()
        artifact = RuntimeReportArtifact(
            artifact_id=artifact_id,
            artifact_kind=artifact_kind,
            generated_at=generated,
            authority_class=AuthorityClass.GENERATED_STATE,
            source_ref=source_ref,
            relative_output_path=str(relative),
            runtime_refs=runtime_refs,
            rendered_report=rendered_report,
            anchor_id=artifact_anchor(artifact_kind.value, source_ref),
        )
        return RuntimeReportArtifactPreparation(artifact=artifact, output_path=resolved)

    def _emit(self, preparation: RuntimeReportArtifactPreparation) -> RuntimeReportArtifactResult:
        preparation.output_path.parent.mkdir(parents=True, exist_ok=True)
        preparation.output_path.write_text(
            _render_artifact(preparation.artifact),
            encoding="utf-8",
        )
        return RuntimeReportArtifactResult(preparation=preparation)


    def _runtime_refs_for_manifest(self, index: KernelIndex, manifest_id: str) -> tuple[str, ...]:
        manifest = index.get("planner_manifest", manifest_id)
        if isinstance(manifest, PlannerManifest):
            scope_view = self._runtime_state_view.scope_view(index, "WORK_UNIT", manifest.parent_work_unit_id)
            return scope_view.state_refs
        return ()

    def _runtime_refs_for_review(self, index: KernelIndex, question_id: str) -> tuple[str, ...]:
        question = index.get("open_question", question_id)
        if isinstance(question, OpenQuestion):
            scope_view = self._runtime_state_view.scope_view(index, "WORK_UNIT", question.origin_work_unit)
            return scope_view.state_refs
        return ()


IonRuntimeReportArtifactEmitter = KernelRuntimeReportArtifactEmitter


def _render_artifact(artifact: RuntimeReportArtifact) -> str:
    lines = [
        "---",
        f"artifact_kind: {artifact.artifact_kind.value}",
        f"authority_class: {artifact.authority_class.value}",
        f"generated_at: {artifact.generated_at}",
        f"source_ref: {artifact.source_ref}",
        f"relative_output_path: {artifact.relative_output_path}",
    ]
    if artifact.runtime_refs:
        lines.append("runtime_refs:")
        lines.extend(f"  - {ref}" for ref in artifact.runtime_refs)
    lines.extend(["---", "", anchor_tag(artifact.anchor_id), "", artifact.rendered_report.rstrip(), ""])
    return "\n".join(lines)


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportArtifactError(f"Absolute output paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportArtifactError(f"Output path escapes workspace root: {relative_path}") from exc
    return resolved


def _safe_name(value: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-._")
    return safe or "runtime"


def _timestamped_filename(*, prefix: str, suffix: str, generated_at: str | None) -> str:
    stamp = re.sub(r"[^0-9]", "", generated_at or _iso_now())[:14]
    return f"{prefix}__{stamp}.{suffix}.md"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
