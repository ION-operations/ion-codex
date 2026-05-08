from __future__ import annotations

import pytest

from kernel.ion_mcp_hosted_storage_receipt_ledger_alpha import (
    ALLOWED_EVENT_KINDS,
    FORBIDDEN_EVENT_KINDS,
    IonHostedStorageReceiptLedgerAlpha,
    build_storage_alpha_fixture_report,
    verify_event_chain,
)

def test_storage_alpha_fixture_report_passes_and_preserves_boundary():
    report = build_storage_alpha_fixture_report()
    assert report.passed is True
    assert report.hosted_cloud_certified is False
    assert report.public_endpoint_certified is False
    assert report.kubernetes_certified is False
    assert report.production_object_storage_certified is False
    assert report.live_execution_authorized_seen is False
    assert report.kernel_truth_mutation_seen is False
    assert report.forbidden_resolution_seen is False
    assert report.forbidden_event_seen is False
    assert report.event_chain_verified is True
    assert report.content_addressed_state_root_verified is True
    assert report.append_only_ledger_verified is True
    assert report.bundle_preview_verified is True


def test_append_only_receipt_chain_verifies():
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    ledger.append_receipt_event(
        event_kind="MOUNT_RECEIPT",
        execution_resolution="READ_ONLY",
        tool_name="ion.mount",
        payload={"mount": True},
    )
    ledger.append_receipt_event(
        event_kind="DRY_RUN_PLAN",
        execution_resolution="DRY_RUN",
        tool_name="ion.job.plan",
        payload={"plan": True},
    )
    state = ledger.state()
    assert len(state.receipt_events) == 2
    assert state.receipt_events[0].previous_event_hash is None
    assert state.receipt_events[1].previous_event_hash == state.receipt_events[0].event_hash
    assert verify_event_chain(state.receipt_events) is True


def test_forbidden_event_kinds_are_refused():
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    for kind in sorted(FORBIDDEN_EVENT_KINDS):
        with pytest.raises(ValueError):
            ledger.append_receipt_event(
                event_kind=kind,
                execution_resolution="DRY_RUN",
                tool_name="ion.job.plan",
                payload={"kind": kind},
            )


def test_forbidden_live_resolution_is_refused():
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    with pytest.raises(ValueError):
        ledger.append_receipt_event(
            event_kind="DRY_RUN_PLAN",
            execution_resolution="LIVE_EXECUTED",
            tool_name="ion.job.plan",
            payload={"bad": True},
        )


def test_snapshot_and_bundle_are_preview_only():
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    snapshot = ledger.snapshot_state_root_preview(payload={"state": "preview"})
    bundle = ledger.create_bundle_export_preview()
    assert snapshot.content_addressed is True
    assert snapshot.mutable_directly_by_mcp is False
    assert snapshot.live_execution_authorized is False
    assert bundle.export_is_preview_only is True
    assert bundle.production_bundle_certified is False
    assert bundle.live_execution_authorized is False
