#!/usr/bin/env python3
"""Write ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md — on-disk proof the gate ran."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _resolve_shell_root(start: Path) -> Path | None:
    for p in (start, *start.parents):
        if (p / "ION" / "REPO_AUTHORITY.md").is_file() and (p / "pyproject.toml").is_file():
            return p
    return None


def main() -> int:
    objective = " ".join(sys.argv[1:]).strip() or "operator gate stamp"
    root = _resolve_shell_root(Path.cwd().resolve())
    if root is None:
        sys.stderr.write(
            "ion_stamp_operator_gate: no shell root (need pyproject.toml + ION/REPO_AUTHORITY.md). cd to shell root first.\n"
        )
        return 2

    env = {**os.environ, "PYTHONPATH": str(root / "ION" / "04_packages")}
    blocks: list[str] = [
        "# ION — operator-visible last gate run",
        "",
        f"- **stamped_at_utc:** {datetime.now(timezone.utc).isoformat()}",
        f"- **shell_root:** `{root}`",
        f"- **objective:** {objective}",
        "",
        "Open this file in the IDE to verify the carrier actually ran commands — not chat claims.",
        "",
    ]

    steps: list[tuple[str, list[str]]] = [
        (
            "two_file_gate",
            ["bash", "-lc", "test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md && echo TWO_FILE_GATE_OK"],
        ),
        (
            "ion_carrier_onboard",
            [
                sys.executable,
                "-m",
                "kernel.ion_carrier_onboard",
                "--ion-root",
                "ION",
                "--carrier",
                "cursor",
                "--objective",
                objective,
                "--write-current",
                "--json",
            ],
        ),
        (
            "kernel_implementation",
            [sys.executable, "-m", "kernel", "implementation", objective],
        ),
    ]

    for label, cmd in steps:
        proc = subprocess.run(cmd, cwd=str(root), env=env, capture_output=True, text=True)
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        blocks.append(f"## `{label}`")
        blocks.append("")
        blocks.append("```text")
        blocks.append(out or "(no stdout)")
        if err:
            blocks.append("stderr:")
            blocks.append(err)
        blocks.append(f"exit_code: {proc.returncode}")
        blocks.append("```")
        blocks.append("")

    dest = root / "ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(blocks) + "\n", encoding="utf-8")
    print(dest.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
