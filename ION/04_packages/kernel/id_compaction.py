"""Stable bounded identifier helpers for filesystem-backed kernel records."""

from __future__ import annotations

import hashlib
import re


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


def slugify_identifier(value: str, *, empty: str = "value") -> str:
    """Normalize one identifier component into the kernel's lowercase slug form."""

    safe = _SAFE_ID_RE.sub("-", value.lower()).strip("-")
    return safe or empty


def compact_identifier(value: str, *, empty: str = "value", max_length: int = 48) -> str:
    """Return a stable slug that stays within a bounded length budget."""

    if max_length < 17:
        raise ValueError("max_length must leave room for a readable prefix and digest.")

    safe = slugify_identifier(value, empty=empty)
    if len(safe) <= max_length:
        return safe

    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    prefix_budget = max_length - len(digest) - 1
    prefix = safe[:prefix_budget].rstrip("-")
    if not prefix:
        return digest[:max_length]
    return f"{prefix}-{digest}"
