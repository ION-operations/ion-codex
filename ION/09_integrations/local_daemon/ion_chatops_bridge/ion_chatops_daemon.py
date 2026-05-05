#!/usr/bin/env python3
"""Local wrapper for the ION ChatOps Bridge daemon."""

from __future__ import annotations

from kernel.ion_chatops_bridge import main


if __name__ == "__main__":
    raise SystemExit(main())
