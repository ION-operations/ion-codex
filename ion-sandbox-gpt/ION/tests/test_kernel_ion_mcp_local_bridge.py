import json
import tempfile
import unittest
from pathlib import Path

from kernel.ion_mcp_local_bridge import (
    ALLOWED_RESOLUTIONS,
    FORBIDDEN_TOOL_NAMES,
    VERSION,
    IonMcpExecutionResolution,
    IonMcpLocalBridge,
    IonMcpToolStatus,
    handle_jsonrpc_message,
)


class IonMcpLocalBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.store_dir = tempfile.TemporaryDirectory()
        self.ion_root = Path(self.tempdir.name) / "ION"
        (self.ion_root / "00_BOOTSTRAP").mkdir(parents=True)
        (self.ion_root / "02_architecture").mkdir(parents=True)
        (self.ion_root / "04_packages" / "kernel").mkdir(parents=True)
        (self.ion_root / "tests").mkdir(parents=True)
        (self.ion_root / "03_registry").mkdir(parents=True)
        (self.ion_root / "05_context").mkdir(parents=True)
        (self.ion_root / "00_BOOTSTRAP" / "V64_LOCAL_MCP_BRIDGE_LOCK.md").write_text("lock", encoding="utf-8")
        (self.ion_root / "00_BOOTSTRAP" / "V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL_LOCK.md").write_text("v63", encoding="utf-8")
        (self.ion_root / "02_architecture" / "ION_V64_LOCAL_MCP_BRIDGE_EXECUTION_HORIZON_PROTOCOL.md").write_text(
            "# Horizon\nNo live execution.\n",
            encoding="utf-8",
        )
        self.bridge = IonMcpLocalBridge(self.ion_root, self.store_dir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()
        self.store_dir.cleanup()

    def test_mount_creates_runtime_session_but_not_live_authority(self) -> None:
        result = self.bridge.mount({
            "client_name": "unit-test",
            "transport": "stdio",
            "requested_mode": "dry_run",
            "workspace_id": "workspace-test",
        })
        self.assertEqual(result.status, IonMcpToolStatus.OK)
        self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.READ_ONLY)
        self.assertFalse(result.live_execution_authorized)
        self.assertFalse(result.external_model_call_authorized)
        self.assertFalse(result.kernel_truth_mutated)
        self.assertEqual(result.payload["execution_mode"], "DRY_RUN_ONLY")
        self.assertIn("ion.job.submit_dry_run", result.payload["allowed_tools"])
        self.assertEqual(len(self.bridge.session_store.list_session_ids()), 1)

    def test_mount_refuses_live_mode(self) -> None:
        result = self.bridge.mount({
            "client_name": "unit-test",
            "transport": "stdio",
            "requested_mode": "live_candidate",
            "workspace_id": "workspace-test",
        })
        self.assertEqual(result.status, IonMcpToolStatus.BLOCKED)
        self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.REFUSED)
        self.assertFalse(result.live_execution_authorized)
        self.assertIn("forbids live execution", result.next_required_action or result.payload.get("reason", ""))

    def test_status_boot_horizon_are_read_only(self) -> None:
        self.bridge.mount({"client_name": "unit-test", "requested_mode": "dry_run"})
        for name in ("ion.status", "ion.boot_packet", "ion.horizon.current"):
            result = self.bridge.call_tool(name, {})
            self.assertEqual(result.status, IonMcpToolStatus.OK)
            self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.READ_ONLY)
            self.assertFalse(result.kernel_truth_mutated)

    def test_job_submit_dry_run_queues_without_execution(self) -> None:
        mount = self.bridge.mount({"client_name": "unit-test", "requested_mode": "dry_run"})
        session_id = mount.session_id
        result = self.bridge.job_submit_dry_run({"work_unit_id": "wu-test-1", "summary": "dry run"}, session_id)
        self.assertEqual(result.status, IonMcpToolStatus.OK)
        self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.APPROVAL_REQUIRED)
        self.assertFalse(result.kernel_truth_mutated)
        self.assertFalse(result.live_execution_authorized)
        queue = self.bridge.session_store.read_queue(session_id)
        self.assertEqual(len(queue.items), 1)
        self.assertEqual(queue.items[0].payload["mode"], "DRY_RUN_ONLY")

    def test_daemon_dry_run_step_does_not_start_loop(self) -> None:
        self.bridge.mount({"client_name": "unit-test", "requested_mode": "dry_run"})
        result = self.bridge.daemon_dry_run_step({"action": "preview"})
        self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.APPROVAL_REQUIRED)
        self.assertFalse(result.payload["daemon_loop_started"])
        self.assertFalse(result.payload["daemon_action_executed"])
        self.assertFalse(result.kernel_truth_mutated)

    def test_forbidden_live_tools_are_refused(self) -> None:
        self.bridge.mount({"client_name": "unit-test", "requested_mode": "dry_run"})
        for tool in FORBIDDEN_TOOL_NAMES:
            result = self.bridge.call_tool(tool, {})
            self.assertEqual(result.status, IonMcpToolStatus.BLOCKED)
            self.assertEqual(result.execution_resolution, IonMcpExecutionResolution.REFUSED)
            self.assertFalse(result.live_execution_authorized)
            self.assertFalse(result.kernel_truth_mutated)

    def test_every_bridge_result_uses_allowed_resolution(self) -> None:
        self.bridge.mount({"client_name": "unit-test", "requested_mode": "dry_run"})
        results = [
            self.bridge.status(),
            self.bridge.boot_packet(),
            self.bridge.horizon_current(),
            self.bridge.approvals_list(),
            self.bridge.job_plan({"summary": "plan"}),
            self.bridge.job_submit_dry_run({"summary": "submit"}),
            self.bridge.daemon_dry_run_step({"summary": "daemon"}),
            self.bridge.bundle_export_preview(),
        ]
        for result in results:
            self.assertIn(str(result.execution_resolution), ALLOWED_RESOLUTIONS)
            self.assertNotEqual(str(result.execution_resolution), "LIVE_EXECUTED")
            self.assertFalse(result.live_execution_authorized)
            self.assertFalse(result.external_model_call_authorized)
            self.assertFalse(result.browser_mutation_authorized)
            self.assertFalse(result.credential_access_authorized)
            self.assertFalse(result.canonical_write_authorized)

    def test_minimal_jsonrpc_tools_list_and_call(self) -> None:
        init = handle_jsonrpc_message(self.bridge, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(init["result"]["serverInfo"]["name"], "ion-mcp-local-bridge")
        tools = handle_jsonrpc_message(self.bridge, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        names = [tool["name"] for tool in tools["result"]["tools"]]
        self.assertIn("ion.mount", names)
        call = handle_jsonrpc_message(
            self.bridge,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "ion.mount", "arguments": {"client_name": "jsonrpc-test"}},
            },
        )
        self.assertFalse(call["result"]["isError"])
        text = call["result"]["content"][0]["text"]
        payload = json.loads(text)
        self.assertEqual(payload["tool_name"], "ion.mount")
        self.assertEqual(payload["execution_resolution"], "READ_ONLY")


if __name__ == "__main__":
    unittest.main()
