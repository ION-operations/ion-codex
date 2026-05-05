"""V57 cost-quality routing facade.

The implementation intentionally delegates to model_router scoring. It exists as a
separate organ boundary so later branches can evolve margin-aware economics
without collapsing router, budget governor, and rate governor into one module.
"""
from __future__ import annotations

from .model_router import CallIntent, RouteDecision, build_call_intent_from_work_class, decide_route

__all__ = ["CallIntent", "RouteDecision", "build_call_intent_from_work_class", "decide_cost_quality_route"]


def decide_cost_quality_route(workspace_root, intent: CallIntent | dict) -> RouteDecision:
    return decide_route(workspace_root, intent)

