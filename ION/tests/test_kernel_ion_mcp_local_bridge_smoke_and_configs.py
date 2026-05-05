import json
import tempfile
import unittest
from pathlib import Path

from kernel.ion_mcp_client_configs import build_profiles, write_profiles
from kernel.ion_mcp_local_bridge_smoke import run_stdio_smoke


class IonMcpLocalBridgeSmokeAndConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.state_dir = tempfile.TemporaryDirectory()
        self.ion_root = Path(self.tempdir.name) / "ION"
        (self.ion_root / "00_BOOTSTRAP").mkdir(parents=True)
        (self.ion_root / "02_architecture").mkdir(parents=True)
        (self.ion_root / "03_registry").mkdir(parents=True)
        (self.ion_root / "04_packages").mkdir(parents=True)
        (self.ion_root / "05_context").mkdir(parents=True)
        (self.ion_root / "tests").mkdir(parents=True)
        (self.ion_root / "00_BOOTSTRAP" / "V64_LOCAL_MCP_BRIDGE_LOCK.md").write_text("lock", encoding="utf-8")
        (self.ion_root / "00_BOOTSTRAP" / "V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL_LOCK.md").write_text("v63", encoding="utf-8")
        (self.ion_root / "02_architecture" / "ION_V64_LOCAL_MCP_BRIDGE_EXECUTION_HORIZON_PROTOCOL.md").write_text(
            "# Horizon\nNo live execution.\n",
            encoding="utf-8",
        )
        self.package_root = Path(__file__).resolve().parents[1] / "04_packages"

    def tearDown(self) -> None:
        self.tempdir.cleanup()
        self.state_dir.cleanup()

    def test_external_stdio_smoke_harness_mounts_and_refuses_live_execution(self) -> None:
        report = run_stdio_smoke(
            self.ion_root,
            self.state_dir.name,
            package_path=self.package_root,
        )
        self.assertTrue(report.passed, report.to_dict())
        self.assertFalse(report.forbidden_resolution_seen)
        self.assertFalse(report.live_execution_authorized_seen)
        self.assertFalse(report.kernel_truth_mutation_seen)
        step_names = [step.step for step in report.steps]
        self.assertIn("ion.mount", step_names)
        self.assertIn("ion.job.execute_live", step_names)

    def test_client_profiles_are_local_stdio_and_dry_run_bounded(self) -> None:
        profiles = build_profiles(self.ion_root, python_executable="python")
        names = {profile.profile_name for profile in profiles}
        self.assertIn("generic-local-stdio", names)
        self.assertIn("cursor-local-stdio", names)
        self.assertIn("vscode-local-stdio", names)
        self.assertIn("codex-local-stdio", names)
        joined = json.dumps([profile.to_dict() for profile in profiles], sort_keys=True)
        self.assertIn("kernel.ion_mcp_local_bridge", joined)
        self.assertIn("--stdio", joined)
        # Live tools may appear only as explicit forbidden examples, never as executable modules/args.
        for profile in profiles:
            command_surface = json.dumps(profile.config if not isinstance(profile.config, str) else {"toml": profile.config})
            self.assertIn("kernel.ion_mcp_local_bridge", command_surface)
            self.assertNotIn("kernel.ion_live", command_surface)
            self.assertNotIn("kernel.shell", command_surface)

    def test_write_profiles_creates_config_and_metadata_files(self) -> None:
        out = Path(self.tempdir.name) / "profiles"
        written = write_profiles(out, self.ion_root, python_executable="python")
        names = {path.name for path in written}
        self.assertIn("generic-stdio.json", names)
        self.assertIn("cursor.mcp.json", names)
        self.assertIn("vscode.mcp.json", names)
        self.assertIn("codex.config.toml", names)
        cursor_config = json.loads((out / "cursor.mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(cursor_config["mcpServers"]["ion-local"]["command"], "python")
        self.assertIn("--stdio", cursor_config["mcpServers"]["ion-local"]["args"])


if __name__ == "__main__":
    unittest.main()
