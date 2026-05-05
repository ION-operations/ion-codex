#!/usr/bin/env python3
"""Wrapper for the ION ChatGPT browser Cloudflare Tunnel bridge."""
from __future__ import annotations

from pathlib import Path
import sys


def _ensure_kernel_path() -> None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "ION/04_packages"
        if candidate.exists():
            sys.path.insert(0, str(candidate))
            return


_ensure_kernel_path()

from kernel.ion_chatgpt_browser_cloudflare_tunnel import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
