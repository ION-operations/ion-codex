"""Dependency-free template contract registry projection loader.

The governance registry source is YAML. This module reads a generated JSON
projection that is safe under ``python -S`` and does not require external
packages.

The projection is not canon by itself. It is a runtime-readable derivative.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


DEFAULT_PROJECTION_RELATIVE_PATH = "ION/03_registry/template_metadata_contract_registry.projection.json"


class TemplateContractRegistryProjectionError(Exception):
    """Raised when the runtime projection cannot be read or validated."""


def contract_projection_path(workspace_root: Path) -> Path:
    return Path(workspace_root) / DEFAULT_PROJECTION_RELATIVE_PATH


def load_template_contract_registry_projection(
    workspace_root: Path,
    *,
    strict: bool = False,
) -> dict[str, dict[str, Any]]:
    """Load template metadata contracts keyed by template_id.

    Args:
        workspace_root: Project/workspace root containing the ION directory.
        strict: If true, missing or malformed projections raise. If false,
            missing projection returns an empty mapping while malformed
            projection still raises because partial contract data is unsafe.

    Returns:
        Dict keyed by template_id.
    """

    path = contract_projection_path(workspace_root)
    if not path.exists():
        if strict:
            raise TemplateContractRegistryProjectionError(
                f"template contract projection does not exist: {path}"
            )
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise TemplateContractRegistryProjectionError(
            f"failed to read template contract projection: {path}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise TemplateContractRegistryProjectionError("projection root must be an object")

    contracts_raw = data.get("contracts")
    if not isinstance(contracts_raw, list):
        raise TemplateContractRegistryProjectionError("projection must contain contracts list")

    contracts: dict[str, dict[str, Any]] = {}
    for index, contract in enumerate(contracts_raw):
        if not isinstance(contract, dict):
            raise TemplateContractRegistryProjectionError(
                f"contract at index {index} must be an object"
            )
        template_id = contract.get("template_id")
        if not template_id:
            raise TemplateContractRegistryProjectionError(
                f"contract at index {index} missing template_id"
            )
        contracts[str(template_id)] = dict(contract)
    return contracts


def load_contracts_if_projection_exists(workspace_root: Path) -> dict[str, dict[str, Any]] | None:
    """Return contracts if projection exists, else None.

    ``None`` signals backward-compatible mode for callers. An empty dict signals
    contract-bound mode with no contracts, which should fail closed.
    """

    path = contract_projection_path(workspace_root)
    if not path.exists():
        return None
    return load_template_contract_registry_projection(workspace_root, strict=True)
