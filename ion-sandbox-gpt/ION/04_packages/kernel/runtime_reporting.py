"""Operational runtime-state reporting helpers for the active ION kernel stack.

This module does not create a new runtime family. It composes the already-landed
manifest/route-state and automation-state surfaces into operator-facing packets so
planner, review, and status reporting can expose live posture without pretending a
larger autonomous reporting daemon already exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .automation_state import KernelAutomationStateManager
from .authority_lineage import KernelAuthorityLineageManager, lineage_warning
from .index import KernelIndex
from .manifest_state import KernelManifestRouteStateManager
from .model import CommitDelta, OpenQuestion, PlannerManifest, WorkUnit
from .runtime_state_views import KernelRuntimeStateView, RuntimeDispatchPosture, RuntimeReviewPressure, RuntimeStateScopeView


class KernelRuntimeReportingError(Exception):
    """Raised when one bounded runtime reporting operation cannot be completed."""


@dataclass(frozen=True)
class RuntimeScopeStatusBundle:
    """Small operator-facing status bundle for one runtime scope."""

    scope_view: RuntimeStateScopeView
    dispatch_posture: RuntimeDispatchPosture
    review_pressure: RuntimeReviewPressure | None
    rendered_report: str


class KernelRuntimeStateReporter:
    """Render bounded operator-facing runtime posture for current kernel records."""

    def __init__(
        self,
        *,
        runtime_state_view: KernelRuntimeStateView | None = None,
        manifest_manager: KernelManifestRouteStateManager | None = None,
        automation_manager: KernelAutomationStateManager | None = None,
    ) -> None:
        self._runtime_state_view = runtime_state_view or KernelRuntimeStateView()
        self._manifest_manager = manifest_manager or KernelManifestRouteStateManager()
        self._automation_manager = automation_manager or KernelAutomationStateManager()

    def render_scope_status_report(
        self,
        index: KernelIndex,
        scope_type: str,
        scope_ref: str,
        *,
        report_from: str = "Steward",
        created_at: str | None = None,
        responding_to: str = "runtime-state status request",
        completed: tuple[str, ...] = (),
        current_objectives: tuple[str, ...] = (),
        planned_next_actions: tuple[str, ...] = (),
        cross_accountability: tuple[str, ...] = (),
        title: str | None = None,
    ) -> RuntimeScopeStatusBundle:
        scope_view = self._runtime_state_view.scope_view(index, scope_type, scope_ref)
        dispatch_posture = self._runtime_state_view.dispatch_posture_for_work_unit(index, scope_ref) if scope_view.scope_type == "WORK_UNIT" else RuntimeDispatchPosture(scope_view=scope_view, dispatch_permitted=True, reason="NON_WORK_SCOPE", blockers=(), source_created_at=scope_view.latest_timestamp)
        resolved_report_from, lineage_notes = self.resolve_report_from(report_from)
        review_pressure = None
        if scope_view.scope_type == "WORK_UNIT":
            review_pressure = self._review_pressure_for_scope(index, scope_view)
        rendered = self._render_status_report(
            scope_view=scope_view,
            dispatch_posture=dispatch_posture,
            review_pressure=review_pressure,
            report_from=resolved_report_from,
            created_at=created_at,
            responding_to=responding_to,
            completed=completed,
            current_objectives=current_objectives,
            planned_next_actions=planned_next_actions,
            cross_accountability=(tuple(cross_accountability) + lineage_notes),
            title=title,
        )
        return RuntimeScopeStatusBundle(
            scope_view=scope_view,
            dispatch_posture=dispatch_posture,
            review_pressure=review_pressure,
            rendered_report=rendered,
        )

    def resolve_report_from(
        self,
        report_from: str,
        *,
        workspace_root: str | Path | None = None,
    ) -> tuple[str, tuple[str, ...]]:
        requested = (report_from or "").strip() or "Steward"
        if requested == "FreshExecutor":
            return requested, ()
        resolution = KernelAuthorityLineageManager().resolve_authority(
            workspace_root or Path(__file__).resolve().parents[3],
            "runtime_status_report_from",
            requested,
        )
        warning = lineage_warning(resolution)
        return resolution.resolved_name, (() if warning is None else (warning,))

    def render_planner_manifest_packet(self, index: KernelIndex, manifest_id: str) -> str:
        manifest = index.get("planner_manifest", manifest_id)
        if not isinstance(manifest, PlannerManifest):
            raise KernelRuntimeReportingError(f"Unknown planner manifest: {manifest_id}")
        parent = index.get("work_unit", manifest.parent_work_unit_id)
        if not isinstance(parent, WorkUnit):
            raise KernelRuntimeReportingError(
                f"Missing parent work unit for planner manifest {manifest.manifest_id}: {manifest.parent_work_unit_id}"
            )
        delta = index.get("commit_delta", manifest.planner_delta_id)
        if not isinstance(delta, CommitDelta):
            raise KernelRuntimeReportingError(
                f"Missing planner delta for planner manifest {manifest.manifest_id}: {manifest.planner_delta_id}"
            )
        question = index.get("open_question", manifest.source_question_id)
        if not isinstance(question, OpenQuestion):
            raise KernelRuntimeReportingError(
                f"Missing source question for planner manifest {manifest.manifest_id}: {manifest.source_question_id}"
            )

        scope_view = self._runtime_state_view.work_unit_view(index, parent.work_unit_id)
        dispatch_posture = self._runtime_state_view.dispatch_posture_for_work_unit(index, parent.work_unit_id)
        lines = [
            f"# Planner Manifest Packet — {manifest.manifest_id}",
            "",
            "## Manifest Status",
            "",
            f"- Status: {manifest.status}",
            f"- Parent Work Unit: {parent.work_unit_id}",
            f"- Source Question: {question.question_id}",
            f"- Planner Delta: {delta.delta_id}",
            f"- Child Spec Count: {manifest.child_spec_count}",
            f"- Created By: {manifest.created_by}",
        ]
        if manifest.status_reason:
            lines.append(f"- Status Reason: {manifest.status_reason}")
        if manifest.expires_at:
            lines.append(f"- Expires At: {manifest.expires_at}")
        if manifest.notes:
            lines.extend(["", "## Manifest Notes", "", manifest.notes])

        lines.extend([
            "",
            "## Runtime Posture",
            "",
            f"- Scope: {scope_view.scope_type}:{scope_view.scope_ref}",
            f"- Dispatch Permitted: {'YES' if dispatch_posture.dispatch_permitted else 'NO'}",
            f"- Dispatch Reason: {dispatch_posture.reason}",
        ])
        if dispatch_posture.blockers:
            lines.extend(["", "### Runtime Blockers", ""])
            lines.extend(f"- {item}" for item in dispatch_posture.blockers)
        if scope_view.manifest is not None:
            lines.extend(["", "### Route Surface", "", self._compact_manifest_summary(scope_view.manifest)])
        if scope_view.automation is not None:
            lines.extend(["", "### Automation Surface", "", self._compact_automation_summary(scope_view.automation)])

        lines.extend([
            "",
            "## Source Question",
            "",
            f"- Domain: {question.domain}",
            f"- Needed From: {question.needed_from}",
            f"- Question: {question.question_text}",
        ])
        if question.resolution:
            lines.append(f"- Resolution: {question.resolution}")
        if question.resolution_evidence:
            lines.extend(["", "### Resolution Evidence", ""])
            lines.extend(f"- {item}" for item in question.resolution_evidence)

        lines.extend(["", "## Proposed Child Work", ""])
        for child in delta.proposed_child_work_units:
            lines.append(
                f"- {child.suggested_agent or 'UNSPECIFIED'} :: {child.suggested_template} :: {child.scope_ref}"
            )
            lines.append(f"  - Rationale: {child.rationale}")
        if delta.review_reasons:
            lines.extend(["", "## Review Pressure", ""])
            lines.extend(f"- {item}" for item in delta.review_reasons)
        return "\n".join(lines) + "\n"

    def render_review_packet(self, index: KernelIndex, question_id: str) -> str:
        question = index.get("open_question", question_id)
        if not isinstance(question, OpenQuestion):
            raise KernelRuntimeReportingError(f"Unknown open question: {question_id}")
        if question.domain != "validation_review":
            raise KernelRuntimeReportingError(
                f"Question is not a review-domain escalation: {question.question_id} ({question.domain})"
            )
        work_unit = index.get("work_unit", question.origin_work_unit)
        if not isinstance(work_unit, WorkUnit):
            raise KernelRuntimeReportingError(
                f"Missing review work unit for question {question.question_id}: {question.origin_work_unit}"
            )
        delta = self._review_delta(index, question)
        pressure = self._runtime_state_view.review_pressure_for_delta(index, delta) if delta is not None else None
        scope_view = self._runtime_state_view.work_unit_view(index, work_unit.work_unit_id)
        dispatch_posture = self._runtime_state_view.dispatch_posture_for_work_unit(index, work_unit.work_unit_id)

        lines = [
            f"# Review Packet — {question.question_id}",
            "",
            "## Review Request",
            "",
            f"- Work Unit: {work_unit.work_unit_id}",
            f"- Needed From: {question.needed_from}",
            f"- Priority: {question.priority}",
            f"- Question: {question.question_text}",
        ]
        if delta is not None:
            lines.append(f"- Held Delta: {delta.delta_id}")
            lines.append(f"- Delta Status: {delta.status}")
        lines.extend([
            "",
            "## Runtime Posture",
            "",
            f"- Dispatch Permitted: {'YES' if dispatch_posture.dispatch_permitted else 'NO'}",
            f"- Dispatch Reason: {dispatch_posture.reason}",
        ])
        if pressure is not None:
            lines.append(f"- Review Pressure: {pressure.reason}")
        if scope_view.manifest is not None:
            lines.extend(["", "### Route Surface", "", self._compact_manifest_summary(scope_view.manifest)])
        if scope_view.automation is not None:
            lines.extend(["", "### Automation Surface", "", self._compact_automation_summary(scope_view.automation)])
        if question.context:
            lines.extend(["", "## Review Context", "", question.context])
        if question.linked_artifacts:
            lines.extend(["", "## Linked Artifacts", ""])
            lines.extend(f"- {item}" for item in question.linked_artifacts)
        if delta is not None and delta.review_reasons:
            lines.extend(["", "## Review Reasons", ""])
            lines.extend(f"- {item}" for item in delta.review_reasons)
        return "\n".join(lines) + "\n"

    def write_report(self, content: str, output_path: str | Path) -> Path:
        resolved = Path(output_path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
        return resolved

    def _render_status_report(
        self,
        *,
        scope_view: RuntimeStateScopeView,
        dispatch_posture: RuntimeDispatchPosture,
        review_pressure: RuntimeReviewPressure | None,
        report_from: str,
        created_at: str | None,
        responding_to: str,
        completed: tuple[str, ...],
        current_objectives: tuple[str, ...],
        planned_next_actions: tuple[str, ...],
        cross_accountability: tuple[str, ...],
        title: str | None,
    ) -> str:
        timestamp = created_at or _iso_now()
        title_value = title or f"{scope_view.scope_type}:{scope_view.scope_ref}"
        lines = [
            "---",
            "type: status_report",
            f"from: {report_from}",
            f"created: {timestamp}",
            f"responding_to: {responding_to}",
            "---",
            "",
            f"# Runtime Status Report — {title_value}",
            "",
            "## What I completed",
            "",
        ]
        lines.extend(self._render_list_or_default(completed, default="- Runtime posture assessed against live manifest and automation state."))
        lines.extend(["", "## Current objectives", ""])
        lines.extend(self._render_list_or_default(current_objectives, default="- Maintain lawful bounded progression for the current scope."))
        lines.extend(["", "## Planned next actions", ""])
        lines.extend(self._render_list_or_default(planned_next_actions, default="- Continue only through dispatch-permitted or review-cleared paths."))
        lines.extend(["", "## System state assessment", ""])
        lines.append(f"- Scope: {scope_view.scope_type}:{scope_view.scope_ref}")
        if scope_view.manifest is not None:
            lines.append(f"- Route Action: {scope_view.manifest.routing_assessment.recommended_action}")
            lines.append(f"- Loop Position: {scope_view.manifest.route_frame.loop_position}")
        else:
            lines.append("- Route Action: NO_MANIFEST_ROUTE_STATE")
        if scope_view.automation is not None:
            lines.append(f"- Automation Stage: {scope_view.automation.current_stage}")
        else:
            lines.append("- Automation Stage: NO_AUTOMATION_STATE")
        lines.append(f"- Dispatch Posture: {'PERMITTED' if dispatch_posture.dispatch_permitted else 'BLOCKED'}")
        lines.append(f"- Dispatch Reason: {dispatch_posture.reason}")
        if review_pressure is not None:
            lines.append(f"- Review Pressure: {review_pressure.reason}")
        if scope_view.state_refs:
            lines.append(f"- Runtime Refs: {', '.join(scope_view.state_refs)}")
        if dispatch_posture.blockers:
            lines.extend(["", "### Blockers", ""])
            lines.extend(f"- {item}" for item in dispatch_posture.blockers)
        lines.extend(["", "## Cross-accountability", ""])
        default_cross = tuple(_cross_accountability_lines(scope_view, dispatch_posture, review_pressure))
        lines.extend(self._render_list_or_default(cross_accountability or default_cross, default="- Runtime state currently has no additional cross-accountability note."))
        return "\n".join(lines) + "\n"

    def _review_pressure_for_scope(
        self,
        index: KernelIndex,
        scope_view: RuntimeStateScopeView,
    ) -> RuntimeReviewPressure | None:
        for record in index.records_for_work_unit(scope_view.scope_ref):
            if isinstance(record, CommitDelta):
                pressure = self._runtime_state_view.review_pressure_for_delta(index, record)
                if pressure.requires_review:
                    return pressure
        return None

    def _review_delta(self, index: KernelIndex, question: OpenQuestion) -> CommitDelta | None:
        for blocking_ref in question.blocking:
            record = index.get("commit_delta", blocking_ref)
            if isinstance(record, CommitDelta):
                return record
        for record in index.records_for_work_unit(question.origin_work_unit):
            if isinstance(record, CommitDelta) and question.context and record.delta_id in question.context:
                return record
        return None

    @staticmethod
    def _render_list_or_default(items: tuple[str, ...], *, default: str) -> list[str]:
        if items:
            return [f"- {item}" for item in items]
        return [default]

    def _compact_manifest_summary(self, record) -> str:
        rendered = self._manifest_manager.render_report(record).strip().splitlines()
        return "\n".join(rendered[: min(len(rendered), 12)])

    def _compact_automation_summary(self, record) -> str:
        rendered = self._automation_manager.render_report(record).strip().splitlines()
        return "\n".join(rendered[: min(len(rendered), 16)])


IonRuntimeStateReporter = KernelRuntimeStateReporter


def _cross_accountability_lines(
    scope_view: RuntimeStateScopeView,
    dispatch_posture: RuntimeDispatchPosture,
    review_pressure: RuntimeReviewPressure | None,
) -> tuple[str, ...]:
    lines: list[str] = []
    if scope_view.manifest is not None:
        lines.append(
            f"Route state {scope_view.manifest.manifest_id} currently steers {scope_view.manifest.routing_assessment.recommended_action}."
        )
    if scope_view.automation is not None:
        lines.append(
            f"Automation state {scope_view.automation.automation_state_id} is staged at {scope_view.automation.current_stage}."
        )
    if not dispatch_posture.dispatch_permitted:
        lines.append(f"Dispatch remains blocked by {dispatch_posture.reason}.")
    if review_pressure is not None:
        lines.append(f"Review pressure source: {review_pressure.reason}.")
    return tuple(lines)


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
