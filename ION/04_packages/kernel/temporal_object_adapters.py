from __future__ import annotations

"""Adapters from present ION-facing record shapes into TemporalObject.

These are starter adapters only. They intentionally accept mapping-like objects
so current ION records can be mapped incrementally without forced migration.
"""

from dataclasses import dataclass
from typing import Mapping, Any

from .temporal_model import (
    TemporalBudgetProfile,
    TemporalCivilProfile,
    TemporalLeaseProfile,
    TemporalObject,
    TemporalOrchestrationProfile,
)


@dataclass(frozen=True)
class ScheduledDeliverableAdapter:
    record: Mapping[str, Any]

    def to_temporal_object(self) -> TemporalObject:
        return TemporalObject(
            object_id=str(self.record["object_id"]),
            object_type=str(self.record.get("object_type", "SCHEDULED_DELIVERABLE")),
            title=str(self.record.get("title", "Untitled deliverable")),
            status=str(self.record.get("status", "ACTIVE")),
            created_at=str(self.record.get("created_at", "")),
            updated_at=str(self.record.get("updated_at", self.record.get("created_at", ""))),
            civil=TemporalCivilProfile(
                scheduled_at=self.record.get("scheduled_at"),
                deadline_at=self.record.get("deadline_at"),
                timezone=self.record.get("timezone"),
                recurrence_rule=self.record.get("recurrence_rule"),
                alarm_windows=tuple(self.record.get("alarm_windows", ())),
                calendar_visibility=self.record.get("calendar_visibility"),
                real_world_commitment_strength=self.record.get("real_world_commitment_strength"),
                user_confirmation_required=bool(self.record.get("user_confirmation_required", False)),
            ),
            orchestration=TemporalOrchestrationProfile(
                horizon_class=self.record.get("horizon_class"),
                dependency_pressure=self.record.get("dependency_pressure"),
                open_question_pressure=self.record.get("open_question_pressure"),
                reconfirmation_window=self.record.get("reconfirmation_window"),
                preparation_window=self.record.get("preparation_window"),
            ),
            budget=TemporalBudgetProfile(
                estimated_token_burn=self.record.get("estimated_token_burn"),
                estimated_slice_count=self.record.get("estimated_slice_count"),
                effort_class=self.record.get("effort_class"),
                confidence_band=self.record.get("confidence_band"),
                context_pressure=self.record.get("context_pressure"),
                throughput_requirement=self.record.get("throughput_requirement"),
                expected_tpm_band=self.record.get("expected_tpm_band"),
                project_budget_ref=self.record.get("project_budget_ref"),
                compression_potential=self.record.get("compression_potential"),
                minimum_viable_slice=self.record.get("minimum_viable_slice"),
                reserve_sensitivity=self.record.get("reserve_sensitivity"),
            ),
            lease=self._maybe_lease(),
            related_object_ids=tuple(self.record.get("related_object_ids", ())),
            dependency_ids=tuple(self.record.get("dependency_ids", ())),
            blocked_by_ids=tuple(self.record.get("blocked_by_ids", ())),
        )

    def _maybe_lease(self) -> TemporalLeaseProfile | None:
        if not self.record.get("lease_id"):
            return None
        return TemporalLeaseProfile(
            lease_id=self.record.get("lease_id"),
            holder_type=self.record.get("holder_type"),
            holder_ref=self.record.get("holder_ref"),
            fallback_holder_ref=self.record.get("fallback_holder_ref"),
        )


@dataclass(frozen=True)
class RecurringReviewAdapter(ScheduledDeliverableAdapter):
    pass


@dataclass(frozen=True)
class DormantCommitmentAdapter(ScheduledDeliverableAdapter):
    pass
