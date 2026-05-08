"""V65 client configuration profiles for the local ION MCP bridge.

The generated profiles are examples for local/founder use. They intentionally
point at the dry-run local bridge and never expose live execution tools.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import sys
from typing import Any, Mapping

VERSION = "V65_LOCAL_MCP_CLIENT_CONFIG_AND_SMOKE_HARNESS"


@dataclass(frozen=True)
class IonMcpClientConfigProfile:
    profile_name: str
    client: str
    filename: str
    config: Mapping[str, Any] | str
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _resolve_ion_root(ion_root: str | Path) -> Path:
    root = Path(ion_root).resolve()
    if root.name != "ION" and (root / "ION").exists():
        root = (root / "ION").resolve()
    return root


def _stdio_command(ion_root: str | Path, python_executable: str = "python") -> tuple[str, list[str], dict[str, str]]:
    root = _resolve_ion_root(ion_root)
    package_root = root / "04_packages"
    args = ["-m", "kernel.ion_mcp_local_bridge", "--ion-root", str(root), "--stdio"]
    env = {"PYTHONPATH": str(package_root)}
    return python_executable, args, env


def cursor_profile(ion_root: str | Path, python_executable: str = "python") -> IonMcpClientConfigProfile:
    command, args, env = _stdio_command(ion_root, python_executable)
    config = {
        "mcpServers": {
            "ion-local": {
                "command": command,
                "args": args,
                "env": env,
            }
        }
    }
    return IonMcpClientConfigProfile(
        profile_name="cursor-local-stdio",
        client="Cursor",
        filename="cursor.mcp.json",
        config=config,
        notes=(
            "Example local stdio MCP profile for Cursor-style clients.",
            "V65 exposes read-only and dry-run bridge tools only.",
            "Do not add shell/provider/browser live tools to this profile.",
        ),
    )


def vscode_profile(ion_root: str | Path, python_executable: str = "python") -> IonMcpClientConfigProfile:
    command, args, env = _stdio_command(ion_root, python_executable)
    config = {
        "servers": {
            "ion-local": {
                "type": "stdio",
                "command": command,
                "args": args,
                "env": env,
            }
        }
    }
    return IonMcpClientConfigProfile(
        profile_name="vscode-local-stdio",
        client="VS Code",
        filename="vscode.mcp.json",
        config=config,
        notes=(
            "Example VS Code MCP profile. Place/adapt according to the target VS Code MCP configuration surface.",
            "The bridge is local and dry-run bounded.",
        ),
    )


def codex_profile(ion_root: str | Path, python_executable: str = "python") -> IonMcpClientConfigProfile:
    command, args, env = _stdio_command(ion_root, python_executable)
    args_toml = ", ".join(json.dumps(arg) for arg in args)
    env_toml = ", ".join(f"{key} = {json.dumps(value)}" for key, value in env.items())
    config = (
        "[mcp_servers.ion-local]\n"
        f"command = {json.dumps(command)}\n"
        f"args = [{args_toml}]\n"
        f"env = {{ {env_toml} }}\n"
    )
    return IonMcpClientConfigProfile(
        profile_name="codex-local-stdio",
        client="Codex",
        filename="codex.config.toml",
        config=config,
        notes=(
            "Example Codex-style local MCP server profile.",
            "Use this only for dry-run bridge testing until a client-specific certification pass is performed.",
        ),
    )


def generic_stdio_profile(ion_root: str | Path, python_executable: str = "python") -> IonMcpClientConfigProfile:
    command, args, env = _stdio_command(ion_root, python_executable)
    config = {
        "name": "ion-local",
        "transport": "stdio",
        "command": command,
        "args": args,
        "env": env,
        "first_calls": ["initialize", "tools/list", "tools/call ion.mount", "tools/call ion.status"],
        "forbidden": ["ion.job.execute_live", "ion.shell.run", "ion.provider.dispatch", "ion.browser.mutate"],
    }
    return IonMcpClientConfigProfile(
        profile_name="generic-local-stdio",
        client="Generic MCP-compatible host",
        filename="generic-stdio.json",
        config=config,
        notes=(
            "Canonical local stdio bridge command profile.",
            "This is the source profile from which client-specific profiles should be derived.",
        ),
    )


def build_profiles(ion_root: str | Path, python_executable: str = "python") -> tuple[IonMcpClientConfigProfile, ...]:
    return (
        generic_stdio_profile(ion_root, python_executable),
        cursor_profile(ion_root, python_executable),
        vscode_profile(ion_root, python_executable),
        codex_profile(ion_root, python_executable),
    )


def write_profiles(output_dir: str | Path, ion_root: str | Path, python_executable: str = "python") -> tuple[Path, ...]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for profile in build_profiles(ion_root, python_executable):
        path = out / profile.filename
        if isinstance(profile.config, str):
            path.write_text(profile.config, encoding="utf-8")
        else:
            path.write_text(json.dumps(profile.config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        meta_path = out / f"{profile.filename}.meta.json"
        meta_path.write_text(json.dumps(profile.to_dict(), indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        written.extend([path, meta_path])
    return tuple(written)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate V65 local ION MCP bridge client config examples.")
    parser.add_argument("--ion-root", default=".", help="Path to ION/ or snapshot root containing ION/")
    parser.add_argument("--output-dir", default="ION/examples/mcp/generated", help="Directory for generated profile examples")
    parser.add_argument("--python", default=sys.executable, help="Python executable to place in generated profiles")
    args = parser.parse_args(argv)
    written = write_profiles(args.output_dir, args.ion_root, args.python)
    print(json.dumps({"version": VERSION, "written": [str(path) for path in written]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
