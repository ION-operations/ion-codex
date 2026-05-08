"""Stable read-only anchor and pointer helpers for downstream runtime-report surfaces.

These helpers normalize section ids and JSON-pointer fragments across generated
runtime-report artifacts, summaries, rollups, dashboards, navigation packets,
and crosslink/browser surfaces. They remain explicitly downstream from kernel
truth and only shape read-only traversal over witness material.
"""

from __future__ import annotations

import re


def artifact_anchor(artifact_kind: str, source_ref: str) -> str:
    return f"artifact-{_safe_fragment(artifact_kind)}-{_safe_fragment(source_ref)}"


def dashboard_entry_anchor(trigger_event: str, source_ref: str, entry_index: int) -> str:
    return f"dashboard-entry-{entry_index}-{_safe_fragment(trigger_event)}-{_safe_fragment(source_ref)}"


def governance_summary_anchor(artifact_kind: str, source_ref: str, entry_index: int) -> str:
    return f"governance-summary-receipt-{entry_index}-{_safe_fragment(artifact_kind)}-{_safe_fragment(source_ref)}"


def operator_rollup_anchor(trigger_event: str, source_ref: str, entry_index: int) -> str:
    return f"governance-rollup-receipt-{entry_index}-{_safe_fragment(trigger_event)}-{_safe_fragment(source_ref)}"


def packet_index_pointer(entry_index: int) -> str:
    normalized = max(0, entry_index - 1)
    return f"#/entries/{normalized}"


def ledger_row_pointer(entry_index: int) -> str:
    normalized = max(0, entry_index - 1)
    return f"#/{normalized}"


def anchor_tag(anchor_id: str) -> str:
    return f'<a id="{anchor_id}"></a>'


def join_relative_target(relative_path: str, fragment: str | None = None) -> str:
    if not fragment:
        return relative_path
    if fragment.startswith('#'):
        return f"{relative_path}{fragment}"
    return f"{relative_path}#{fragment}"


def _safe_fragment(value: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-._")
    return safe or "runtime"
