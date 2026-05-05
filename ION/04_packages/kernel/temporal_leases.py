from __future__ import annotations

"""Conservative lease recommendation logic."""

from .temporal_model import HeatLevel, LeaseRole, LeaseState, TemporalLeaseRecommendation
from .temporal_relevance import trace


def evaluate_lease_recommendation(obj, ctx, heat, transitions):
    traces = []
    lease_required = heat.composite_relevance in {HeatLevel.MEDIUM, HeatLevel.HIGH, HeatLevel.CRITICAL}
    role = None
    state = None
    holder_type = None
    holder_ref = None

    if lease_required:
        holder_type = "SUBSYSTEM"
        holder_ref = "TEMPORAL_RUNTIME"

    if transitions.reconfirm_required:
        role = LeaseRole.REVIEWER
        state = LeaseState.REVIEW
        traces.append(trace("lease_reviewer", "lease_rules", "reconfirmation required", "lease_role", role.value))
    elif transitions.prepare_required:
        role = LeaseRole.PREPARER
        state = LeaseState.ACTIVE
        traces.append(trace("lease_preparer", "lease_rules", "preparation required", "lease_role", role.value))
    elif transitions.wake_required:
        role = LeaseRole.WATCHER
        state = LeaseState.WARM
        traces.append(trace("lease_watcher", "lease_rules", "wake required", "lease_role", role.value))
    elif transitions.dormant_eligible:
        role = LeaseRole.DORMANT_STEWARD
        state = LeaseState.LATENT
        traces.append(trace("lease_dormant", "lease_rules", "dormancy eligible", "lease_role", role.value))

    transfer_required = False
    downgrade_required = transitions.cooling_permitted
    expiration_permitted = transitions.dormant_eligible or transitions.cooling_permitted

    return TemporalLeaseRecommendation(
        lease_required=lease_required,
        holder_type=holder_type,
        holder_ref=holder_ref,
        lease_role=role,
        lease_state=state,
        transfer_required=transfer_required,
        downgrade_required=downgrade_required,
        expiration_permitted=expiration_permitted,
    ), traces
