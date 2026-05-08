from pathlib import Path

from kernel.ion_cursor_autopilot_packet import build_autopilot_packet, write_packet
from kernel.ion_cursor_autopilot_audit import audit_cursor_autopilot


def test_autopilot_packet_classifies_empty_as_continue(tmp_path: Path):
    packet = build_autopilot_packet(tmp_path, "")
    assert packet["schema_id"] == "ion.cursor_autopilot_packet.v1"
    assert packet["operator_message_classification"] == "continuation_signal"
    assert packet["cursor_parent_identity"] == "CURSOR_CARRIER_CONTROL_SURFACE"


def test_autopilot_packet_writes_state(tmp_path: Path):
    packet = build_autopilot_packet(tmp_path, "/ion build the cockpit")
    write_packet(tmp_path, packet)
    assert (tmp_path / "ION/05_context/current/ACTIVE_CURSOR_AUTOPILOT_PACKET.json").exists()
    assert (tmp_path / "ION/05_context/current/ACTIVE_CURSOR_AUTOPILOT_STATE.json").exists()


def test_autopilot_audit_current_tree():
    root = Path.cwd()
    result = audit_cursor_autopilot(root)
    assert result["schema_id"] == "ion.cursor_autopilot_audit.v1"
    assert result["status"] in {"ION_CURSOR_AUTOPILOT_READY", "ION_CURSOR_AUTOPILOT_NOT_READY"}
