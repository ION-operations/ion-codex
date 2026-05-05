"""Planner-manifest runtime helpers for the active ION kernel stack.

This module sits one layer above explicit question resolution and the existing child-work
issuer. It still does not claim a full retry compiler or broader planner runtime already
exists. It now supports five narrower truthful steps the current stack can support today:

1. discover manifest-worthy resolved review/follow-up pressure,
2. persist dedicated planner-manifest state after that pressure resolves,
3. manage manifest lifecycle through cancellation, supersession, and explicit expiry,
4. emit bounded sweep receipts when broader manifest housekeeping is applied, and
5. allow child-work issuance only through READY manifests plus a later accepted delta
   carrying bounded ChildSpec intent.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path

from .children import ChildAgentBinding, ChildWorkIssuanceResult, KernelChildWorkIssuer
from .graph import KernelGraph
from .id_compaction import compact_identifier
from .index import KernelIndex
from .model import (
    CommitDelta,
    CommitDeltaStatus,
    OpenQuestion,
    OpenQuestionStatus,
    PlannerIntentType,
    PlannerManifest,
    PlannerManifestStatus,
    PlannerManifestSweepAggregateRecord,
    PlannerManifestSweepReceipt,
    TierOneDoctrine,
    WorkUnit,
)
from .reviews import REVIEW_DOMAIN
from .signal_followups import SIGNAL_FOLLOWUP_DOMAIN
from .store import KernelStore
from .runtime_reporting import KernelRuntimeStateReporter
from .runtime_report_artifacts import KernelRuntimeReportArtifactEmitter, RuntimeReportArtifactResult
from .runtime_report_triggers import (
    KernelRuntimeReportTriggerManager,
    RuntimeReportTriggerReceipt,
    RuntimeReportTriggerRequest,
)


_SUPPORTED_DOMAINS = frozenset({REVIEW_DOMAIN, SIGNAL_FOLLOWUP_DOMAIN})
_ACCEPTED_DELTA_STATUSES = frozenset({
    CommitDeltaStatus.ACCEPTED,
    CommitDeltaStatus.ACCEPTED_AS_WITNESS,
})


class KernelPlannerGateError(Exception):
    """Raised when planner-gated child issuance cannot be completed lawfully."""


@dataclass(frozen=True)
class PlannerManifestPreparation:
    """Validated resolved pressure plus the explicit accepted child-bearing delta."""

    resolved_question: OpenQuestion
    parent_work_unit: WorkUnit
    planner_commit_delta: CommitDelta
    planner_manifest: PlannerManifest


@dataclass(frozen=True)
class PlannerManifestResult:
    """Result of persisting one dedicated planner manifest."""

    preparation: PlannerManifestPreparation
    persisted_manifest: PlannerManifest
    triggered_artifacts: tuple[RuntimeReportTriggerReceipt, ...] = ()


@dataclass(frozen=True)
class PlannerManifestCompileCandidate:
    """Resolved pressure plus the latest acceptable delta the daemon may compile."""

    resolved_question: OpenQuestion
    parent_work_unit: WorkUnit
    planner_commit_delta: CommitDelta


@dataclass(frozen=True)
class PlannerManifestMaintenanceCandidate:
    """One bounded lifecycle-maintenance action over an existing planner manifest."""

    planner_manifest: PlannerManifest
    target_status: PlannerManifestStatus
    reason: str


@dataclass(frozen=True)
class PlannerManifestSweepResult:
    """Result of maintaining a bounded batch of planner manifests plus one sweep receipt."""

    receipt: PlannerManifestSweepReceipt
    updated_manifests: tuple[PlannerManifest, ...]
    candidates: tuple[PlannerManifestMaintenanceCandidate, ...]


@dataclass(frozen=True)
class PlannerManifestSweepAggregateResult:
    """Result of aggregating a bounded retained sweep-receipt window."""

    aggregate: PlannerManifestSweepAggregateRecord
    retained_receipts: tuple[PlannerManifestSweepReceipt, ...]


@dataclass(frozen=True)
class PlannerChildIssuancePreparation:
    """Validated persisted planner manifest ready for child issuance."""

    planner_manifest: PlannerManifest
    resolved_question: OpenQuestion
    parent_work_unit: WorkUnit
    planner_commit_delta: CommitDelta


@dataclass(frozen=True)
class PlannerChildIssuanceResult:
    """Result of planner-gated child issuance through explicit child specs."""

    manifest_result: PlannerManifestResult
    preparation: PlannerChildIssuancePreparation
    child_work_result: ChildWorkIssuanceResult
    updated_manifest: PlannerManifest


class KernelPlannerChildIssuanceGate:
    """Gate child issuance behind resolved pressure and explicit accepted child intent."""

    def __init__(
        self,
        *,
        child_issuer: KernelChildWorkIssuer | None = None,
        runtime_reporter: KernelRuntimeStateReporter | None = None,
        runtime_report_emitter: KernelRuntimeReportArtifactEmitter | None = None,
        runtime_report_trigger_manager: KernelRuntimeReportTriggerManager | None = None,
    ) -> None:
        self._child_issuer = child_issuer or KernelChildWorkIssuer()
        self._runtime_reporter = runtime_reporter or KernelRuntimeStateReporter()
        self._runtime_report_emitter = runtime_report_emitter or KernelRuntimeReportArtifactEmitter(runtime_reporter=self._runtime_reporter)
        self._runtime_report_trigger_manager = runtime_report_trigger_manager or KernelRuntimeReportTriggerManager(runtime_report_emitter=self._runtime_report_emitter)

    def discover_compile_candidates(
        self,
        index: KernelIndex,
    ) -> tuple[PlannerManifestCompileCandidate, ...]:
        candidates: list[PlannerManifestCompileCandidate] = []
        for question in index.open_questions_by_status(OpenQuestionStatus.RESOLVED):
            if question.domain not in _SUPPORTED_DOMAINS:
                continue
            parent_work_unit = index.get("work_unit", question.origin_work_unit)
            if not isinstance(parent_work_unit, WorkUnit):
                continue
            if _has_issued_children(index, parent_work_unit.work_unit_id):
                continue
            if _has_executed_manifest(index, question.question_id):
                continue
            deltas = _candidate_deltas_for_question(index, question, parent_work_unit.work_unit_id)
            if not deltas:
                continue
            latest_delta = deltas[-1]
            existing = _existing_manifest(index, question.question_id, latest_delta.delta_id, parent_work_unit.work_unit_id)
            if existing is not None and existing.status is PlannerManifestStatus.READY:
                continue
            candidates.append(
                PlannerManifestCompileCandidate(
                    resolved_question=question,
                    parent_work_unit=parent_work_unit,
                    planner_commit_delta=latest_delta,
                )
            )
        candidates.sort(
            key=lambda item: (
                item.planner_commit_delta.created_at,
                item.resolved_question.question_id,
                item.planner_commit_delta.delta_id,
            )
        )
        return tuple(candidates)

    def discover_maintenance_candidates(
        self,
        index: KernelIndex,
        *,
        as_of: str,
    ) -> tuple[PlannerManifestMaintenanceCandidate, ...]:
        candidates: list[PlannerManifestMaintenanceCandidate] = []
        as_of_dt = _parse_iso(as_of)
        for manifest in index.planner_manifests_by_status(PlannerManifestStatus.READY):
            if manifest.intent is not PlannerIntentType.ISSUE_CHILD_WORK:
                continue
            if manifest.expires_at is not None and _parse_iso(manifest.expires_at) <= as_of_dt:
                candidates.append(
                    PlannerManifestMaintenanceCandidate(
                        planner_manifest=manifest,
                        target_status=PlannerManifestStatus.EXPIRED,
                        reason="EXPIRED_AT_DEADLINE",
                    )
                )
                continue
            if _has_issued_children(index, manifest.parent_work_unit_id):
                candidates.append(
                    PlannerManifestMaintenanceCandidate(
                        planner_manifest=manifest,
                        target_status=PlannerManifestStatus.CANCELLED,
                        reason="CHILD_WORK_ALREADY_ISSUED",
                    )
                )
                continue
            question = index.get("open_question", manifest.source_question_id)
            if isinstance(question, OpenQuestion) and question.status is not OpenQuestionStatus.RESOLVED:
                candidates.append(
                    PlannerManifestMaintenanceCandidate(
                        planner_manifest=manifest,
                        target_status=PlannerManifestStatus.CANCELLED,
                        reason="SOURCE_QUESTION_NO_LONGER_RESOLVED",
                    )
                )
        candidates.sort(key=lambda item: (item.planner_manifest.created_at, item.planner_manifest.manifest_id))
        return tuple(candidates)

    def maintain_manifest(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        manifest_id: str,
        *,
        as_of: str,
    ) -> PlannerManifest:
        manifest = index.get("planner_manifest", manifest_id)
        if not isinstance(manifest, PlannerManifest):
            raise KernelPlannerGateError(f"Unknown planner manifest: {manifest_id}")
        candidate = next((item for item in self.discover_maintenance_candidates(index, as_of=as_of) if item.planner_manifest.manifest_id == manifest_id), None)
        if candidate is None:
            return manifest
        updated = replace(
            manifest,
            status=candidate.target_status,
            status_changed_at=as_of,
            status_reason=candidate.reason,
        )
        store.replace(updated)
        index.record_changed(updated)
        graph.build_from_index(index)
        return updated

    def sweep_maintenance_candidates(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        as_of: str,
        generated_at: str | None = None,
        generated_by: str = "DAEMON",
    ) -> PlannerManifestSweepResult | None:
        candidates = self.discover_maintenance_candidates(index, as_of=as_of)
        if not candidates:
            return None
        updated_manifests: list[PlannerManifest] = []
        for candidate in candidates:
            updated = replace(
                candidate.planner_manifest,
                status=candidate.target_status,
                status_changed_at=as_of,
                status_reason=candidate.reason,
            )
            store.replace(updated)
            index.record_changed(updated)
            updated_manifests.append(updated)
        receipt = PlannerManifestSweepReceipt(
            receipt_id=planner_manifest_sweep_receipt_id(generated_at or as_of),
            generated_at=generated_at or as_of,
            as_of=as_of,
            maintained_manifest_ids=tuple(item.manifest_id for item in updated_manifests),
            resulting_statuses=tuple(item.status for item in updated_manifests),
            reasons=tuple(item.status_reason or "" for item in updated_manifests),
            candidate_count=len(candidates),
            maintained_count=len(updated_manifests),
            generated_by=generated_by.strip() or "DAEMON",
        )
        if index.exists("planner_manifest_sweep", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        graph.build_from_index(index)
        return PlannerManifestSweepResult(
            receipt=receipt,
            updated_manifests=tuple(updated_manifests),
            candidates=candidates,
        )

    def retained_sweep_receipts(
        self,
        index: KernelIndex,
        *,
        retention_limit: int = 16,
    ) -> tuple[PlannerManifestSweepReceipt, ...]:
        if retention_limit <= 0:
            raise KernelPlannerGateError("retention_limit must be positive.")
        return tuple(index.planner_manifest_sweep_receipts()[:retention_limit])

    def needs_sweep_aggregate(
        self,
        index: KernelIndex,
        *,
        retention_limit: int = 16,
    ) -> bool:
        retained = self.retained_sweep_receipts(index, retention_limit=retention_limit)
        if len(retained) < 2:
            return False
        aggregates = index.planner_manifest_sweep_aggregates()
        if not aggregates:
            return True
        latest = aggregates[0]
        return tuple(latest.retained_receipt_ids) != tuple(receipt.receipt_id for receipt in retained)

    def aggregate_sweep_receipts(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        generated_at: str | None = None,
        generated_by: str = "DAEMON",
        retention_limit: int = 16,
    ) -> PlannerManifestSweepAggregateResult | None:
        retained = self.retained_sweep_receipts(index, retention_limit=retention_limit)
        if len(retained) < 2:
            return None
        status_counts: dict[str, int] = {}
        reason_counts: dict[str, int] = {}
        for receipt in retained:
            for status in receipt.resulting_statuses:
                status_counts[status.value] = status_counts.get(status.value, 0) + 1
            for reason in receipt.reasons:
                if not reason:
                    continue
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
        aggregate_timestamp = generated_at or retained[0].generated_at
        aggregate = PlannerManifestSweepAggregateRecord(
            aggregate_id=planner_manifest_sweep_aggregate_id(aggregate_timestamp, retention_limit=retention_limit),
            generated_at=aggregate_timestamp,
            retained_receipt_ids=tuple(receipt.receipt_id for receipt in retained),
            retained_count=len(retained),
            total_maintained_count=sum(receipt.maintained_count for receipt in retained),
            status_counts=status_counts,
            reason_counts=reason_counts,
            earliest_as_of=min(receipt.as_of for receipt in retained),
            latest_as_of=max(receipt.as_of for receipt in retained),
            generated_by=generated_by.strip() or "DAEMON",
        )
        if index.exists("planner_manifest_sweep_aggregate", aggregate.aggregate_id):
            store.replace(aggregate)
            index.record_changed(aggregate)
        else:
            store.create(aggregate)
            index.record_added(aggregate)
        graph.build_from_index(index)
        return PlannerManifestSweepAggregateResult(aggregate=aggregate, retained_receipts=retained)

    def compile_ready_manifests(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        compiled_at: str | None = None,
        created_by: str = "DAEMON",
        notes: str | None = None,
        expires_at: str | None = None,
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> tuple[PlannerManifestResult, ...]:
        results: list[PlannerManifestResult] = []
        for candidate in self.discover_compile_candidates(index):
            results.append(
                self.create_manifest(
                    store,
                    index,
                    graph,
                    candidate.resolved_question.question_id,
                    candidate.parent_work_unit.work_unit_id,
                    candidate.planner_commit_delta.delta_id,
                    created_at=compiled_at,
                    created_by=created_by,
                    notes=notes,
                    expires_at=expires_at,
                    artifact_trigger_request=artifact_trigger_request,
                )
            )
        return tuple(results)

    def prepare_manifest(
        self,
        index: KernelIndex,
        question_id: str,
        work_unit_id: str,
        delta_id: str,
        *,
        created_at: str | None = None,
        created_by: str = "DAEMON",
        notes: str | None = None,
        expires_at: str | None = None,
    ) -> PlannerManifestPreparation:
        question = index.get("open_question", question_id)
        if not isinstance(question, OpenQuestion):
            raise KernelPlannerGateError(f"Unknown open question: {question_id}")
        if question.domain not in _SUPPORTED_DOMAINS:
            raise KernelPlannerGateError(
                "Question domain is not supported for planner-gated child issuance: "
                f"{question.question_id} ({question.domain})"
            )
        if question.status is not OpenQuestionStatus.RESOLVED:
            raise KernelPlannerGateError(
                "Question must be RESOLVED before planner-gated child issuance: "
                f"{question.question_id} ({question.status})"
            )

        parent_work_unit = index.get("work_unit", work_unit_id)
        if not isinstance(parent_work_unit, WorkUnit):
            raise KernelPlannerGateError(f"Unknown parent work unit: {work_unit_id}")
        if question.origin_work_unit != parent_work_unit.work_unit_id:
            raise KernelPlannerGateError(
                "Resolved question does not belong to the requested parent work unit: "
                f"{question.question_id} -> {question.origin_work_unit}"
            )

        planner_commit_delta = index.get("commit_delta", delta_id)
        if not isinstance(planner_commit_delta, CommitDelta):
            raise KernelPlannerGateError(f"Unknown planner commit delta: {delta_id}")
        if planner_commit_delta.status not in _ACCEPTED_DELTA_STATUSES:
            raise KernelPlannerGateError(
                "Planner commit delta is not in an accepted status: "
                f"{delta_id} ({planner_commit_delta.status})"
            )
        if planner_commit_delta.work_unit_id != parent_work_unit.work_unit_id:
            raise KernelPlannerGateError(
                "Planner commit delta does not belong to the requested parent work unit: "
                f"expected {parent_work_unit.work_unit_id}, found {planner_commit_delta.work_unit_id}"
            )
        if not planner_commit_delta.proposed_child_work_units:
            raise KernelPlannerGateError(
                f"Planner commit delta does not contain explicit child specs: {delta_id}"
            )
        if question.question_id not in planner_commit_delta.resolved_question_ids:
            raise KernelPlannerGateError(
                "Planner commit delta is not explicitly linked to the resolved question: "
                f"question={question.question_id} delta={delta_id}"
            )
        if question.resolved_at is None:
            raise KernelPlannerGateError(
                f"Resolved question is missing resolved_at: {question.question_id}"
            )
        if _parse_iso(planner_commit_delta.created_at) < _parse_iso(question.resolved_at):
            raise KernelPlannerGateError(
                "Planner commit delta predates resolved pressure: "
                f"question={question.question_id} delta={delta_id}"
            )

        existing = _existing_manifest(index, question_id, delta_id, work_unit_id)
        if existing is not None:
            planner_manifest = existing
        else:
            created_timestamp = created_at or planner_commit_delta.created_at
            planner_manifest = PlannerManifest(
                manifest_id=planner_manifest_id(question_id, delta_id),
                created_at=created_timestamp,
                parent_work_unit_id=parent_work_unit.work_unit_id,
                protocol_id=parent_work_unit.protocol_id,
                transition_id=parent_work_unit.transition_id,
                context_version=parent_work_unit.context_version,
                source_question_id=question.question_id,
                planner_delta_id=planner_commit_delta.delta_id,
                intent=PlannerIntentType.ISSUE_CHILD_WORK,
                status=PlannerManifestStatus.READY,
                created_by=created_by.strip() or "DAEMON",
                child_spec_count=len(planner_commit_delta.proposed_child_work_units),
                resolved_question_ids=planner_commit_delta.resolved_question_ids,
                notes=notes.strip() if notes is not None else None,
                expires_at=expires_at,
            )
        return PlannerManifestPreparation(
            resolved_question=question,
            parent_work_unit=parent_work_unit,
            planner_commit_delta=planner_commit_delta,
            planner_manifest=planner_manifest,
        )

    def create_manifest(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        question_id: str,
        work_unit_id: str,
        delta_id: str,
        *,
        created_at: str | None = None,
        created_by: str = "DAEMON",
        notes: str | None = None,
        expires_at: str | None = None,
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> PlannerManifestResult:
        preparation = self.prepare_manifest(
            index,
            question_id,
            work_unit_id,
            delta_id,
            created_at=created_at,
            created_by=created_by,
            notes=notes,
            expires_at=expires_at,
        )
        manifest = preparation.planner_manifest
        created_new = False
        if not index.exists("planner_manifest", manifest.manifest_id):
            for stale_manifest in _ready_manifests_for_question(index, question_id, exclude_manifest_id=manifest.manifest_id):
                updated_stale = replace(
                    stale_manifest,
                    status=PlannerManifestStatus.SUPERSEDED,
                    status_changed_at=created_at or manifest.created_at,
                    status_reason="SUPERSEDED_BY_NEWER_PLANNER_DELTA",
                    superseded_by_manifest_id=manifest.manifest_id,
                )
                store.replace(updated_stale)
                index.record_changed(updated_stale)
            store.create(manifest)
            index.record_added(manifest)
            graph.build_from_index(index)
            created_new = True
        triggered: tuple[RuntimeReportTriggerReceipt, ...] = ()
        if created_new:
            triggered = self._runtime_report_trigger_manager.emit_for_manifest_creation(
                index,
                manifest.manifest_id,
                artifact_trigger_request,
            )
        return PlannerManifestResult(
            preparation=preparation,
            persisted_manifest=manifest,
            triggered_artifacts=triggered,
        )

    def cancel_manifest(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        manifest_id: str,
        *,
        cancelled_at: str | None = None,
        reason: str = "CANCELLED_BY_OPERATOR",
    ) -> PlannerManifest:
        manifest = index.get("planner_manifest", manifest_id)
        if not isinstance(manifest, PlannerManifest):
            raise KernelPlannerGateError(f"Unknown planner manifest: {manifest_id}")
        if manifest.status is PlannerManifestStatus.EXECUTED:
            raise KernelPlannerGateError(
                f"Executed planner manifests cannot be cancelled: {manifest.manifest_id}"
            )
        if manifest.status is PlannerManifestStatus.CANCELLED:
            return manifest
        updated = replace(
            manifest,
            status=PlannerManifestStatus.CANCELLED,
            status_changed_at=cancelled_at or _iso_now(),
            status_reason=reason,
        )
        store.replace(updated)
        index.record_changed(updated)
        graph.build_from_index(index)
        return updated

    def expire_due_manifests(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        as_of: str,
    ) -> tuple[PlannerManifest, ...]:
        expired: list[PlannerManifest] = []
        for manifest in index.planner_manifests_by_status(PlannerManifestStatus.READY):
            if manifest.expires_at is None:
                continue
            if _parse_iso(manifest.expires_at) > _parse_iso(as_of):
                continue
            updated = replace(
                manifest,
                status=PlannerManifestStatus.EXPIRED,
                status_changed_at=as_of,
                status_reason="EXPIRED_AT_DEADLINE",
            )
            store.replace(updated)
            index.record_changed(updated)
            expired.append(updated)
        if expired:
            graph.build_from_index(index)
        return tuple(expired)

    def prepare_issuance(
        self,
        index: KernelIndex,
        question_id: str,
        work_unit_id: str,
        delta_id: str,
    ) -> PlannerChildIssuancePreparation:
        preparation = self.prepare_manifest(index, question_id, work_unit_id, delta_id)
        manifest = preparation.planner_manifest
        if manifest.status is not PlannerManifestStatus.READY:
            raise KernelPlannerGateError(
                "Planner manifest is not in READY status: "
                f"{manifest.manifest_id} ({manifest.status})"
            )
        return PlannerChildIssuancePreparation(
            planner_manifest=manifest,
            resolved_question=preparation.resolved_question,
            parent_work_unit=preparation.parent_work_unit,
            planner_commit_delta=preparation.planner_commit_delta,
        )

    def prepare_issuance_from_manifest(
        self,
        index: KernelIndex,
        manifest_id: str,
    ) -> PlannerChildIssuancePreparation:
        manifest = index.get("planner_manifest", manifest_id)
        if not isinstance(manifest, PlannerManifest):
            raise KernelPlannerGateError(f"Unknown planner manifest: {manifest_id}")
        if manifest.status is not PlannerManifestStatus.READY:
            raise KernelPlannerGateError(
                "Planner manifest is not in READY status: "
                f"{manifest.manifest_id} ({manifest.status})"
            )
        preparation = self.prepare_manifest(
            index,
            manifest.source_question_id,
            manifest.parent_work_unit_id,
            manifest.planner_delta_id,
            created_by=manifest.created_by,
            notes=manifest.notes,
            expires_at=manifest.expires_at,
        )
        return PlannerChildIssuancePreparation(
            planner_manifest=manifest,
            resolved_question=preparation.resolved_question,
            parent_work_unit=preparation.parent_work_unit,
            planner_commit_delta=preparation.planner_commit_delta,
        )

    def issue_child_work_from_manifest(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        manifest_id: str,
        *,
        repo_root: str | Path,
        doctrine: TierOneDoctrine,
        agent_bindings: dict[str, ChildAgentBinding] | None = None,
        created_at: str | None = None,
    ) -> PlannerChildIssuanceResult:
        preparation = self.prepare_issuance_from_manifest(index, manifest_id)
        manifest_result = PlannerManifestResult(
            preparation=PlannerManifestPreparation(
                resolved_question=preparation.resolved_question,
                parent_work_unit=preparation.parent_work_unit,
                planner_commit_delta=preparation.planner_commit_delta,
                planner_manifest=preparation.planner_manifest,
            ),
            persisted_manifest=preparation.planner_manifest,
        )
        child_work_result = self._child_issuer.issue_child_work_units(
            store,
            index,
            graph,
            preparation.parent_work_unit.work_unit_id,
            preparation.planner_commit_delta.delta_id,
            repo_root=repo_root,
            doctrine=doctrine,
            agent_bindings=agent_bindings,
            created_at=created_at,
        )
        updated_manifest = replace(
            preparation.planner_manifest,
            status=PlannerManifestStatus.EXECUTED,
            executed_child_work_unit_ids=tuple(
                work_unit.work_unit_id for work_unit in child_work_result.created_work_units
            ),
            executed_at=created_at or _iso_now(),
            status_changed_at=created_at or _iso_now(),
            status_reason="EXECUTED_CHILD_WORK_ISSUANCE",
        )
        store.replace(updated_manifest)
        index.record_changed(updated_manifest)
        graph.build_from_index(index)
        return PlannerChildIssuanceResult(
            manifest_result=manifest_result,
            preparation=preparation,
            child_work_result=child_work_result,
            updated_manifest=updated_manifest,
        )

    def render_manifest_packet(self, index: KernelIndex, manifest_id: str) -> str:
        return self._runtime_reporter.render_planner_manifest_packet(index, manifest_id)

    def write_manifest_packet(
        self,
        index: KernelIndex,
        manifest_id: str,
        workspace_root: str | Path,
        *,
        output_path: str | Path | None = None,
        generated_at: str | None = None,
    ) -> RuntimeReportArtifactResult:
        return self._runtime_report_emitter.emit_planner_manifest_artifact(
            index,
            manifest_id,
            workspace_root,
            output_path=output_path,
            generated_at=generated_at,
        )

    def issue_child_work(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        question_id: str,
        work_unit_id: str,
        delta_id: str,
        *,
        repo_root: str | Path,
        doctrine: TierOneDoctrine,
        agent_bindings: dict[str, ChildAgentBinding] | None = None,
        created_at: str | None = None,
        created_by: str = "DAEMON",
        notes: str | None = None,
        expires_at: str | None = None,
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> PlannerChildIssuanceResult:
        manifest_result = self.create_manifest(
            store,
            index,
            graph,
            question_id,
            work_unit_id,
            delta_id,
            created_at=created_at,
            created_by=created_by,
            notes=notes,
            expires_at=expires_at,
        )
        return self.issue_child_work_from_manifest(
            store,
            index,
            graph,
            manifest_result.persisted_manifest.manifest_id,
            repo_root=repo_root,
            doctrine=doctrine,
            agent_bindings=agent_bindings,
            created_at=created_at,
        )


IonPlannerChildIssuanceGate = KernelPlannerChildIssuanceGate


def planner_manifest_id(question_id: str, delta_id: str) -> str:
    question = compact_identifier(question_id, empty="question", max_length=48)
    delta = compact_identifier(delta_id, empty="delta", max_length=48)
    return f"planner-manifest-{question}-{delta}"


def planner_manifest_sweep_receipt_id(as_of: str) -> str:
    safe = compact_identifier(as_of, empty="sweep", max_length=32)
    return f"planner-sweep-{safe}"


def planner_manifest_sweep_aggregate_id(generated_at: str, *, retention_limit: int) -> str:
    safe = compact_identifier(generated_at, empty="aggregate", max_length=32)
    return f"planner-sweep-aggregate-{safe}-r{retention_limit}"


def _candidate_deltas_for_question(
    index: KernelIndex,
    question: OpenQuestion,
    work_unit_id: str,
) -> list[CommitDelta]:
    deltas: list[CommitDelta] = []
    if question.resolved_at is None:
        return deltas
    for record in index.records_for_work_unit(work_unit_id):
        if not isinstance(record, CommitDelta):
            continue
        if record.status not in _ACCEPTED_DELTA_STATUSES:
            continue
        if not record.proposed_child_work_units:
            continue
        if question.question_id not in record.resolved_question_ids:
            continue
        if _parse_iso(record.created_at) < _parse_iso(question.resolved_at):
            continue
        deltas.append(record)
    deltas.sort(key=lambda item: (item.created_at, item.delta_id))
    return deltas


def _existing_manifest(
    index: KernelIndex,
    question_id: str,
    delta_id: str,
    work_unit_id: str,
) -> PlannerManifest | None:
    manifests = [
        manifest
        for manifest in index.planner_manifests_for_question(question_id)
        if manifest.planner_delta_id == delta_id
        and manifest.parent_work_unit_id == work_unit_id
        and manifest.intent is PlannerIntentType.ISSUE_CHILD_WORK
        and manifest.status
        not in {
            PlannerManifestStatus.CANCELLED,
            PlannerManifestStatus.SUPERSEDED,
            PlannerManifestStatus.EXPIRED,
        }
    ]
    if len(manifests) > 1:
        raise KernelPlannerGateError(
            "Multiple active planner manifests exist for the same question/delta binding: "
            f"question={question_id} delta={delta_id}"
        )
    return manifests[0] if manifests else None


def _ready_manifests_for_question(
    index: KernelIndex,
    question_id: str,
    *,
    exclude_manifest_id: str | None = None,
) -> tuple[PlannerManifest, ...]:
    return tuple(
        manifest
        for manifest in index.planner_manifests_for_question(question_id)
        if manifest.status is PlannerManifestStatus.READY
        and manifest.intent is PlannerIntentType.ISSUE_CHILD_WORK
        and manifest.manifest_id != exclude_manifest_id
    )


def _has_executed_manifest(index: KernelIndex, question_id: str) -> bool:
    return any(
        manifest.status is PlannerManifestStatus.EXECUTED
        and manifest.intent is PlannerIntentType.ISSUE_CHILD_WORK
        for manifest in index.planner_manifests_for_question(question_id)
    )


def _has_issued_children(index: KernelIndex, parent_work_unit_id: str) -> bool:
    return any(
        isinstance(record, WorkUnit) and record.parent_work_unit_id == parent_work_unit_id
        for record in index.records_by_type("work_unit")
    )


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
