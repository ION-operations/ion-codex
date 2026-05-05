from pathlib import Path
import shutil

from kernel.ion_carrier_continue import continue_carrier
from kernel.ion_human_gate_queue import add_human_gate, unresolved_human_gates
from kernel.ion_operator_message_queue import enqueue_operator_message, load_operator_message_queue
from kernel.ion_status import build_ion_status


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


ACTIVE_RUNTIME_FILES = (
    "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
    "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
    "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
)


class preserve_active_runtime:
    def __init__(self, root: Path):
        self.root = root
        self.originals: dict[str, bytes | None] = {}
        self.cycle_root = root / "ION/05_context/current/execution_cycles"
        self.original_cycles: set[str] = set()

    def __enter__(self):
        for rel in ACTIVE_RUNTIME_FILES:
            path = self.root / rel
            self.originals[rel] = path.read_bytes() if path.exists() else None
        if self.cycle_root.exists():
            self.original_cycles = {child.name for child in self.cycle_root.iterdir()}
        return self

    def __exit__(self, exc_type, exc, tb):
        for rel, data in self.originals.items():
            path = self.root / rel
            if data is None:
                if path.exists():
                    path.unlink()
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        if self.cycle_root.exists():
            for child in self.cycle_root.iterdir():
                if child.name not in self.original_cycles:
                    if child.is_dir():
                        shutil.rmtree(child)
                    else:
                        child.unlink()


def test_operator_queue_can_be_consumed_by_carrier_continue():
    root = _repo_root()
    with preserve_active_runtime(root):
        enqueue_operator_message(root, message="test queued V88 directive", status="pending", priority=90)
        result = continue_carrier(root, carrier="cursor", operator_message="continue", consume_operator_queue=True)

        assert result["verdict"] == "ION_CARRIER_CONTINUE_READY"
        assert result["source_operator_queue_item"] is not None
        assert result["operator_message_classification"]["classification"] == "new_work_directive"
        assert result["operator_message_queue_path"].endswith("ACTIVE_OPERATOR_MESSAGE_QUEUE.json")

        queue = load_operator_message_queue(root)
        assert any(item["status"] == "carrier_packet_generated" for item in queue["items"] if item["message"] == "test queued V88 directive")


def test_human_gate_blocks_spawn_until_resolved():
    root = _repo_root()
    with preserve_active_runtime(root):
        add_human_gate(root, prompt="Synthetic test gate for V88")
        blocked = continue_carrier(root, carrier="cursor", operator_message="continue")

        assert blocked["verdict"] == "ION_CARRIER_BLOCKED_BY_HUMAN_GATE"
        assert blocked["blocked_by_human_gate"] is True
        assert blocked["spawn_queue"] == []
        assert unresolved_human_gates(root)

        resumed = continue_carrier(root, carrier="cursor", operator_message="yes")
        assert resumed["gate_resolution"] is not None
        assert resumed["verdict"] == "ION_CARRIER_CONTINUE_READY"


def test_ion_status_reports_v88_queues():
    root = _repo_root()
    with preserve_active_runtime(root):
        continue_carrier(root, carrier="cursor", operator_message="continue", objective="test V88 status", force_new_objective=True)
        status = build_ion_status(root)

        assert status["schema_id"] == "ion.status.v1"
        assert "operator_message_queue" in status["authoritative_paths"]
        assert "human_gate_queue" in status["authoritative_paths"]
        assert status["next_lawful_action"] in {
            "execute_spawn_rows_and_run_task_return_intake",
            "spawn_steward_integration_from_accepted_queue",
            "continue_or_queue_new_work",
            "resolve_human_gate",
            "run_ion_carrier_continue_with_consume_operator_queue",
            "repair_active_state_integrity",
        }
