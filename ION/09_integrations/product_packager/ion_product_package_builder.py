"""Build the first productized ION package scaffold.

This builder creates a sidecar product projection. It does not move live ION
authority into the generated package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import textwrap
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRODUCT_VERSION = "0.1.0"
DEFAULT_OUTPUT = Path("/home/sev/ION_PRODUCT_PACKAGE")
SEEDED_DOMAIN_IDS = [
    "USER_INTENT",
    "PROJECT_STATE",
    "DECISIONS",
    "OPEN_LOOPS",
    "ARTIFACTS",
    "CONTEXT_GRAPH",
    "RISK_REVIEW",
    "PERSONA_INTERFACE",
]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_value(repo_root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=repo_root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_reference_doc(repo_root: Path, source_rel: str, dest: Path, title: str) -> None:
    source = repo_root / source_rel
    body = source.read_text(encoding="utf-8")
    write_text(
        dest,
        f"""
        <!-- generated_product_projection: true -->
        <!-- source_path: {source_rel} -->

        # {title}

        This file is a generated product-package reference copy. The live ION
        repo remains source truth. Use `SOURCE_PROVENANCE.json` and
        `PRODUCT_SOURCE_MAP.json` to trace generation.

        ---

        {body}
        """,
    )


def touch_keep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def schema(schema_id: str, title: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
        "title": title,
        "type": "object",
        "additionalProperties": True,
        "required": required,
        "properties": properties,
    }


def build_starter_zip(output_root: Path) -> dict[str, Any]:
    starter_root = output_root / "ION_STARTER_DATA"
    dist_root = output_root / "dist"
    dist_root.mkdir(parents=True, exist_ok=True)
    zip_path = dist_root / "ION_CONTINUITY_DATA_BLANK_v1.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(starter_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(starter_root).as_posix())
    manifest = {
        "artifact": zip_path.name,
        "artifact_type": "starter_continuity_data_zip",
        "release_status": "non_release_scaffold",
        "zip_root": "data_package_root",
        "sha256": sha256_file(zip_path),
        "size_bytes": zip_path.stat().st_size,
    }
    write_json(dist_root / "ION_CONTINUITY_DATA_BLANK_v1.manifest.json", manifest)
    return manifest


def product_source_map() -> dict[str, Any]:
    return {
        "README.md": {
            "source": "curated_product_projection",
            "source_paths": ["README.md", "ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "productized_projection",
        },
        "PRODUCT_PACKAGE_SPEC.md": {
            "source": "generated_from_user_codex_settlement",
            "source_paths": [
                "ION/docs/ION_PROJECT_INGESTION.md",
                "ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md",
                "ION/docs/ION_PARALLEL_SETTLEMENT.md",
            ],
            "curation_status": "first_scaffold_spec",
        },
        "ION_ENGINE/doctrine/ION_CORE.md": {
            "source": "curated_product_projection",
            "source_paths": ["README.md", "ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "engine_law_projection",
        },
        "ION_ENGINE/context_graph/DOMAIN_GRAPH_AND_FISSION.md": {
            "source": "curated_product_projection",
            "source_paths": ["ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md"],
            "curation_status": "engine_law_projection",
        },
        "ION_ENGINE/ingestion/PROJECT_INGESTION.md": {
            "source": "curated_product_projection",
            "source_paths": ["ION/docs/ION_PROJECT_INGESTION.md"],
            "curation_status": "engine_law_projection",
        },
        "ION_ENGINE/settlement/PARALLEL_SETTLEMENT.md": {
            "source": "curated_product_projection",
            "source_paths": ["ION/docs/ION_PARALLEL_SETTLEMENT.md"],
            "curation_status": "engine_law_projection",
        },
        "ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md": {
            "source": "generated_adapter_projection",
            "source_paths": ["ION/06_intelligence/orchestration/custom_gpt/", "ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "adapter_draft",
        },
        "ION_CUSTOM_GPT_ADAPTER/FIRST_RUN_BEHAVIOR.md": {
            "source": "generated_adapter_projection",
            "source_paths": ["ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "first_run_ux_projection",
        },
        "ION_CUSTOM_GPT_ADAPTER/PERSONA_INTERFACE_RULES.md": {
            "source": "generated_adapter_projection",
            "source_paths": ["ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "persona_interface_projection",
        },
        "ION_STARTER_DATA/ION_DATA_MANIFEST.json": {
            "source": "generated_seeded_state",
            "source_paths": [],
            "curation_status": "starter_data_v1_draft",
        },
        "ION_STARTER_DATA/PERSONA/persona_state.json": {
            "source": "generated_seeded_state",
            "source_paths": [],
            "curation_status": "persona_interface_seed",
        },
        "ION_ENGINE/reference/ION_FUNDAMENTALS.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/ION_FUNDAMENTALS.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/ION_DOMAIN_GRAPH_AND_FISSION.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/ION_PARALLEL_SETTLEMENT.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/ION_PARALLEL_SETTLEMENT.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/ION_PROJECT_INGESTION.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/ION_PROJECT_INGESTION.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/TEMPLATE_LAW.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/TEMPLATE_LAW.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/CONTEXT_SYSTEM.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/CONTEXT_SYSTEM.md"],
            "curation_status": "full_reference_projection",
        },
        "ION_ENGINE/reference/AGENTS_ROLES_CARRIERS.md": {
            "source": "copied_reference_projection",
            "source_paths": ["ION/docs/AGENTS_ROLES_CARRIERS.md"],
            "curation_status": "full_reference_projection",
        },
    }


def build_package(output_root: Path = DEFAULT_OUTPUT, repo_root: Path | None = None) -> dict[str, Any]:
    repo_root = repo_root or repo_root_from_script()
    output_root = output_root.resolve()
    generated_at = utc_now()
    source_commit = git_value(repo_root, "rev-parse", "HEAD")
    source_branch = git_value(repo_root, "branch", "--show-current")
    source_remote = git_value(repo_root, "config", "--get", "remote.origin.url")

    for directory in [
        "ION_ENGINE/doctrine",
        "ION_ENGINE/laws",
        "ION_ENGINE/templates",
        "ION_ENGINE/context_graph",
        "ION_ENGINE/receipts",
        "ION_ENGINE/ingestion",
        "ION_ENGINE/settlement",
        "ION_ENGINE/projections",
        "ION_ENGINE/reference",
        "ION_DATA_SCHEMA/schemas",
        "ION_DATA_SCHEMA/migrations",
        "ION_CUSTOM_GPT_ADAPTER",
        "ION_CUSTOM_GPT_ADAPTER/templates",
        "ION_STARTER_DATA/STATE",
        "ION_STARTER_DATA/DOMAINS",
        "ION_STARTER_DATA/CONTEXT",
        "ION_STARTER_DATA/TEMPLATES",
        "ION_STARTER_DATA/PACKETS",
        "ION_STARTER_DATA/RECEIPTS",
        "ION_STARTER_DATA/DECISIONS",
        "ION_STARTER_DATA/ARTIFACTS",
        "ION_STARTER_DATA/PERSONA",
        "ION_STARTER_DATA/INBOX",
        "ION_STARTER_DATA/OUTBOX",
        "ION_STARTER_DATA/ARCHIVE",
        "ION_PRODUCT_DOCS",
        "examples/blank_project",
        "examples/ingested_project_fixture",
        "examples/receipt_examples",
        "tools",
        "tests",
        "dist",
    ]:
        (output_root / directory).mkdir(parents=True, exist_ok=True)

    for empty_dir in [
        "ION_STARTER_DATA/PACKETS",
        "ION_STARTER_DATA/ARTIFACTS",
        "ION_STARTER_DATA/INBOX",
        "ION_STARTER_DATA/OUTBOX",
        "ION_STARTER_DATA/ARCHIVE",
        "ION_STARTER_DATA/DECISIONS",
        "ION_DATA_SCHEMA/migrations",
        "examples/ingested_project_fixture",
    ]:
        touch_keep(output_root / empty_dir)

    write_text(
        output_root / "README.md",
        """
        # ION Product Package

        This folder is a clean distributable projection of ION for Custom GPT
        and browser-sandbox operation.

        It is not the live ION source of truth.

        ```text
        live ION repo = source truth / laboratory / evolving organism
        ION_PRODUCT_PACKAGE = generated distributable projection
        ```

        ## Product Law

        ```text
        ION should not be compressed into a Custom GPT.
        ION should be packaged so a Custom GPT can operate it.

        The engine stays stable.
        The data travels with the user.
        The adapter teaches the carrier how to operate the package.
        Receipts preserve continuity.
        ```

        ## Top-Level Parts

        - `ION_ENGINE/` - stable law and method projection.
        - `ION_DATA_SCHEMA/` - compatibility contract for portable data zips.
        - `ION_CUSTOM_GPT_ADAPTER/` - Custom GPT operating instructions.
        - `ION_STARTER_DATA/` - seeded portable continuity state.
        - `ION_PRODUCT_DOCS/` - operator-facing product docs.
        - `tools/` - package validation and starter zip helpers.
        - `dist/` - generated artifacts only.

        ## First Use

        ```bash
        python3 tools/validate_data_package.py ION_STARTER_DATA
        python3 tools/build_starter_zip.py
        ```

        The generated starter zip is a non-release scaffold until the product
        package receives a formal release receipt.
        """,
    )

    write_text(
        output_root / "PRODUCT_PACKAGE_SPEC.md",
        """
        # ION Product Package Specification

        Status: `FIRST_SCAFFOLD_NON_RELEASE`

        ## Objective

        Create a productized ION projection for Custom GPT and browser-sandbox
        operation without creating a second ION source of truth.

        ## Engine / Data / Adapter Separation

        ```text
        engine != data
        adapter != engine
        runtime != state
        receipt != source truth
        ```

        `ION_ENGINE/` contains law and method. `ION_STARTER_DATA/` contains
        portable state. `ION_CUSTOM_GPT_ADAPTER/` teaches a browser AI carrier
        how to operate the package. `ION_DATA_SCHEMA/` defines compatibility.

        ## Lifecycle

        1. No data zip is mounted.
        2. Adapter quietly initializes seeded starter continuity and asks what
           the user is working on.
        3. Data package is initialized from `ION_STARTER_DATA/`.
        4. Meaningful work appends a receipt and updates current state.
        5. Adapter exports a new continuity data zip.
        6. The user carries the data zip forward.

        ## Acceptance Boundary

        AI output is proposal until it has context, proof, approval, and
        receipt. A Custom GPT may draft state updates, but the data package is
        the carried continuity body.

        ## Non-Release Boundary

        This first scaffold is not a polished release. It establishes folder
        law, provenance, starter state, draft schemas, and validation tooling.

        ## Product Package Invariants

        - The package must name its live source commit.
        - The engine layer must not contain user state.
        - The data layer must not rewrite engine law.
        - The adapter must treat model output as proposal.
        - A state update must append a receipt.
        - An exported data zip must preserve the manifest, state, graph,
          packets, receipt ledger, decisions, and artifacts custody.
        - Migration between schema versions requires a migration receipt.
        - First-run UX should expose continuity benefits, not ION internals.
        - User-facing language should say `project memory pack` where possible.
        """,
    )

    write_text(output_root / "CHANGELOG.md", "# Changelog\n\n## 0.1.0\n\n- First non-release scaffold of the ION product package.\n")
    write_text(output_root / "LICENSE_OR_NOTICE.md", "# Notice\n\nThis scaffold is an ION product projection. License terms are not finalized in this first slice.\n")

    provenance = {
        "authority": "generated_projection_not_source_truth",
        "generated_at": generated_at,
        "generated_from_repo": source_remote or "ION-operations/ION",
        "generator": "ION_PRODUCT_PACKAGE_BUILDER",
        "product_package_version": PRODUCT_VERSION,
        "source_branch": source_branch,
        "source_commit": source_commit,
        "source_root": str(repo_root),
    }
    write_json(output_root / "SOURCE_PROVENANCE.json", provenance)
    write_json(output_root / "PRODUCT_SOURCE_MAP.json", product_source_map())

    write_text(
        output_root / "ION_ENGINE/README.md",
        """
        # ION Engine

        This directory contains the productized engine law projection. It is
        method and governance, not user/project state.

        Use `ION_STARTER_DATA/` or a mounted continuity zip for state.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/doctrine/ION_CORE.md",
        """
        # ION Core

        AI output is not state.

        ION is the law by which AI work becomes state.

        A meaningful act follows:

        ```text
        intent -> packet -> domain -> template -> context package -> proof
        -> Steward decision -> receipt -> next state
        ```

        No proof means no landing. No receipt means no inheritance.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/laws/SIX_LAWS.md",
        """
        # Six Laws

        1. Meaningful AI work is a candidate state transition.
        2. Every state-bearing act must be governed by a template.
        3. Every template execution must be situated by a bounded context package.
        4. Every return is proposal until proof gates and Steward integration accept it.
        5. Every accepted delta must leave a receipt.
        6. Every receipt must improve the next context or the system has not continued.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/templates/TEMPLATE_LAW.md",
        """
        # Template Law

        Templates are cognitive I/O. They define the kind of act being
        attempted, the context required, the authority ceiling, the proof owed,
        the output class, and the receipt shape.

        A template is not a form. It is the action type of the work.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/context_graph/DOMAIN_GRAPH_AND_FISSION.md",
        """
        # Domain Graph And Fission

        A domain is a governed graph region, not a topic folder.

        ION scales because the graph holds continuity while agents hold bounded
        graph regions. When a domain becomes too relationally dense for one
        lawful context package family, it should be audited for fission.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/receipts/RECEIPT_LAW.md",
        """
        # Receipt Law

        A receipt records what happened, under which authority, from which
        context, through which template, with which proof, and what future work
        may inherit.

        Logs say something happened. Receipts make continuity auditable.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/ingestion/PROJECT_INGESTION.md",
        """
        # Project Ingestion

        ION does not ingest a project by reading all files. ION ingests a
        project by converting it into a governed context graph.

        ```text
        external project -> quarantine -> manifest -> cartography
        -> graph genesis -> domain partition -> template binding
        -> risk classification -> first context packages -> receipts
        ```
        """,
    )
    write_text(
        output_root / "ION_ENGINE/settlement/PARALLEL_SETTLEMENT.md",
        """
        # Parallel Settlement

        Fan-out is easy. Fan-in is where agent systems usually fail.

        Every branch return is proposal. Settlement is the parent-scope act
        that decides how branch returns rejoin the canonical workflow.
        """,
    )
    write_text(
        output_root / "ION_ENGINE/projections/PROJECTION_LADDER.md",
        """
        # Projection Ladder

        Full engine law should not be pasted into every prompt. It should be
        projected:

        ```text
        full engine law -> system atlas -> domain docs -> role capsule
        -> task context package -> receipt
        ```
        """,
    )
    write_text(
        output_root / "ION_ENGINE/reference/README.md",
        """
        # Engine Reference Layer

        These are generated reference copies of public ION docs. They make the
        package substantial enough for Custom GPT knowledge upload while still
        preserving the source-truth boundary.

        Use `ION_ENGINE/projections/PROJECTION_LADDER.md` to decide what to
        load into a carrier turn. Do not paste the whole reference layer into
        every response.
        """,
    )
    reference_docs = [
        ("ION/docs/ION_FUNDAMENTALS.md", "ION_ENGINE/reference/ION_FUNDAMENTALS.md", "ION Fundamentals"),
        (
            "ION/docs/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md",
            "ION_ENGINE/reference/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md",
            "ION Continuity Substrate Explainer",
        ),
        ("ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md", "ION_ENGINE/reference/ION_DOMAIN_GRAPH_AND_FISSION.md", "ION Domain Graph And Fission"),
        ("ION/docs/ION_PARALLEL_SETTLEMENT.md", "ION_ENGINE/reference/ION_PARALLEL_SETTLEMENT.md", "ION Parallel Settlement"),
        ("ION/docs/ION_PROJECT_INGESTION.md", "ION_ENGINE/reference/ION_PROJECT_INGESTION.md", "ION Project Ingestion"),
        ("ION/docs/TEMPLATE_LAW.md", "ION_ENGINE/reference/TEMPLATE_LAW.md", "ION Template Law"),
        ("ION/docs/CONTEXT_SYSTEM.md", "ION_ENGINE/reference/CONTEXT_SYSTEM.md", "ION Context System"),
        ("ION/docs/AGENTS_ROLES_CARRIERS.md", "ION_ENGINE/reference/AGENTS_ROLES_CARRIERS.md", "ION Agents Roles Carriers"),
    ]
    for source_rel, dest_rel, title in reference_docs:
        copy_reference_doc(repo_root, source_rel, output_root / dest_rel, title)

    schemas = {
        "ion_data_manifest.schema.json": schema(
            "https://ion.local/schemas/ion_data_manifest.v1.json",
            "ION Data Manifest",
            {
                "schema_id": {"const": "ion.data_manifest.v1"},
                "data_schema_version": {"type": "integer"},
                "engine_version": {"type": "string"},
                "package_id": {"type": "string"},
                "project_id": {"type": "string"},
                "created_at": {"type": "string"},
                "authority": {"type": "string"},
            },
            ["schema_id", "data_schema_version", "engine_version", "package_id", "project_id", "created_at", "authority"],
        ),
        "current_state.schema.json": schema(
            "https://ion.local/schemas/current_state.v1.json",
            "ION Current State",
            {
                "schema_id": {"const": "ion.current_state.v1"},
                "project_id": {"type": "string"},
                "current_objective": {"type": "string"},
                "open_packets": {"type": "array"},
                "warnings": {"type": "array"},
            },
            ["schema_id", "project_id", "current_objective", "open_packets", "warnings"],
        ),
        "domain_registry.schema.json": schema(
            "https://ion.local/schemas/domain_registry.v1.json",
            "ION Domain Registry",
            {
                "schema_id": {"const": "ion.domain_registry.v1"},
                "domains": {"type": "array"},
            },
            ["schema_id", "domains"],
        ),
        "context_graph.schema.json": schema(
            "https://ion.local/schemas/context_graph.v1.json",
            "ION Context Graph",
            {
                "schema_id": {"const": "ion.context_graph.v1"},
                "nodes": {"type": "array"},
                "edges": {"type": "array"},
            },
            ["schema_id", "nodes", "edges"],
        ),
        "work_packet.schema.json": schema(
            "https://ion.local/schemas/work_packet.v1.json",
            "ION Work Packet",
            {
                "schema_id": {"const": "ion.work_packet.v1"},
                "packet_id": {"type": "string"},
                "objective": {"type": "string"},
                "authority": {"type": "object"},
            },
            ["schema_id", "packet_id", "objective", "authority"],
        ),
        "receipt.schema.json": schema(
            "https://ion.local/schemas/receipt.v1.json",
            "ION Receipt",
            {
                "schema_id": {"const": "ion.receipt.v1"},
                "receipt_id": {"type": "string"},
                "receipt_type": {"type": "string"},
                "created_at": {"type": "string"},
                "accepted_as_state": {"type": "boolean"},
            },
            ["schema_id", "receipt_id", "receipt_type", "created_at", "accepted_as_state"],
        ),
        "artifact_manifest.schema.json": schema(
            "https://ion.local/schemas/artifact_manifest.v1.json",
            "ION Artifact Manifest",
            {
                "schema_id": {"const": "ion.artifact_manifest.v1"},
                "artifacts": {"type": "array"},
            },
            ["schema_id", "artifacts"],
        ),
        "open_packets.schema.json": schema(
            "https://ion.local/schemas/open_packets.v1.json",
            "ION Open Packets",
            {
                "schema_id": {"const": "ion.open_packets.v1"},
                "packets": {"type": "array"},
                "queue_status": {"type": "string"},
            },
            ["schema_id", "packets"],
        ),
        "template_registry.schema.json": schema(
            "https://ion.local/schemas/template_registry.v1.json",
            "ION Template Registry",
            {
                "schema_id": {"const": "ion.template_registry.v1"},
                "templates": {"type": "array"},
            },
            ["schema_id", "templates"],
        ),
        "decision_ledger.schema.json": schema(
            "https://ion.local/schemas/decision_ledger.v1.json",
            "ION Decision Ledger",
            {
                "schema_id": {"const": "ion.decision_ledger.v1"},
                "decisions": {"type": "array"},
            },
            ["schema_id", "decisions"],
        ),
        "persona_interface.schema.json": schema(
            "https://ion.local/schemas/persona_interface.v1.json",
            "ION Persona Interface",
            {
                "schema_id": {"const": "ion.persona_interface.v1"},
                "user_facing_default": {"type": "string"},
                "translation_map": {"type": "object"},
                "hidden_domain_ids": {"type": "array"},
            },
            ["schema_id", "user_facing_default", "translation_map", "hidden_domain_ids"],
        ),
    }
    for name, payload in schemas.items():
        write_json(output_root / "ION_DATA_SCHEMA/schemas" / name, payload)
    write_text(output_root / "ION_DATA_SCHEMA/README.md", "# ION Data Schema\n\nDraft v1 compatibility schemas for portable ION continuity packages.\n")
    write_text(output_root / "ION_DATA_SCHEMA/migrations/README.md", "# Migrations\n\nNo migrations exist in schema v1. Future migrations require migration receipts.\n")

    starter_manifest = {
        "schema_id": "ion.data_manifest.v1",
        "authority": "portable_data_candidate_not_engine_truth",
        "created_at": generated_at,
        "data_schema_version": 1,
        "engine_version": "ion_engine_v1",
        "migration_required": False,
        "package_id": "ion-continuity-data-blank-v1",
        "project_id": "blank_project",
        "project_name": "Blank ION Project",
        "source_product_package_version": PRODUCT_VERSION,
    }
    write_json(output_root / "ION_STARTER_DATA/ION_DATA_MANIFEST.json", starter_manifest)
    write_text(
        output_root / "ION_STARTER_DATA/README_FOR_AI.md",
        """
        # ION Starter Data

        This is seeded portable continuity state.

        It is not the engine. It is not source truth. It is the continuity body
        that a compatible AI carrier may inspect, update by receipt, and export.

        The user does not need to see these internals during first run. The AI
        carrier uses them to make continuity feel natural.
        """,
    )
    write_json(
        output_root / "ION_STARTER_DATA/STATE/current_state.json",
        {
            "schema_id": "ion.current_state.v1",
            "project_id": "blank_project",
            "current_objective": "Discover what the user wants to work on and form the first useful project memory.",
            "open_packets": [],
            "warnings": ["seeded_starter_state_non_release_scaffold"],
        },
    )
    write_text(
        output_root / "ION_STARTER_DATA/STATE/current_state.md",
        """
        # Current State

        No accepted project objective exists yet, but the starter package is
        seeded for natural first-run continuity.

        The first user-facing move is simply:

        ```text
        What are we working on?
        ```

        Behind the scenes, the carrier should capture user intent, project
        state, decisions, open loops, artifacts, risks, and useful context as
        receipt-backed project memory.
        """,
    )
    write_json(
        output_root / "ION_STARTER_DATA/DOMAINS/domain_registry.json",
        {
            "schema_id": "ion.domain_registry.v1",
            "domains": [
                {
                    "domain_id": "USER_INTENT",
                    "name": "User Intent",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Captures what the user is trying to accomplish in plain language.",
                    "user_visible_label": "goal",
                },
                {
                    "domain_id": "PROJECT_STATE",
                    "name": "Project State",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Tracks accepted project facts and current work posture.",
                    "user_visible_label": "project memory",
                },
                {
                    "domain_id": "DECISIONS",
                    "name": "Decisions",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Stores accepted choices, rejected options, and rationale.",
                    "user_visible_label": "saved decisions",
                },
                {
                    "domain_id": "OPEN_LOOPS",
                    "name": "Open Loops",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Tracks unresolved questions, next steps, and pending commitments.",
                    "user_visible_label": "open items",
                },
                {
                    "domain_id": "ARTIFACTS",
                    "name": "Artifacts",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Tracks files, links, uploads, generated outputs, and custody status.",
                    "user_visible_label": "files and notes",
                },
                {
                    "domain_id": "CONTEXT_GRAPH",
                    "name": "Context Graph",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Maintains relationships between goals, decisions, sources, artifacts, and work areas.",
                    "user_visible_label": "project memory",
                },
                {
                    "domain_id": "RISK_REVIEW",
                    "name": "Risk Review",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Captures uncertainty, safety boundaries, stale information, and review needs.",
                    "user_visible_label": "cautions",
                },
                {
                    "domain_id": "PERSONA_INTERFACE",
                    "name": "Persona Interface",
                    "status": "provisional",
                    "authority_ceiling": "no_live_execution",
                    "description": "Translates ION machinery into natural assistant language.",
                    "user_visible_label": "assistant style",
                },
            ],
            "seeded_domain_ids": SEEDED_DOMAIN_IDS,
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/CONTEXT/context_graph.json",
        {
            "schema_id": "ion.context_graph.v1",
            "nodes": [
                {
                    "node_id": f"domain:{domain_id}",
                    "node_type": "seeded_domain",
                    "domain_id": domain_id,
                    "context_status": "PROVISIONAL_CONTEXT",
                }
                for domain_id in SEEDED_DOMAIN_IDS
            ],
            "edges": [
                {"from": "domain:USER_INTENT", "to": "domain:PROJECT_STATE", "edge_type": "shapes"},
                {"from": "domain:DECISIONS", "to": "domain:PROJECT_STATE", "edge_type": "updates"},
                {"from": "domain:OPEN_LOOPS", "to": "domain:PROJECT_STATE", "edge_type": "pressures"},
                {"from": "domain:ARTIFACTS", "to": "domain:CONTEXT_GRAPH", "edge_type": "supplies"},
                {"from": "domain:RISK_REVIEW", "to": "domain:DECISIONS", "edge_type": "guards"},
                {"from": "domain:PERSONA_INTERFACE", "to": "domain:USER_INTENT", "edge_type": "translates"},
            ],
            "graph_status": "seeded_project_graph",
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/TEMPLATES/template_registry.json",
        {
            "schema_id": "ion.template_registry.v1",
            "templates": [
                "project_ingestion",
                "first_run_intent_capture",
                "persona_translation",
                "state_update_proposal",
                "receipt_append",
                "continuity_export",
            ],
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/PACKETS/open_packets.json",
        {
            "schema_id": "ion.open_packets.v1",
            "packets": [],
            "queue_status": "empty",
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/DECISIONS/decision_ledger.json",
        {
            "schema_id": "ion.decision_ledger.v1",
            "decisions": [],
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/ARTIFACTS/artifact_manifest.json",
        {
            "schema_id": "ion.artifact_manifest.v1",
            "artifacts": [],
            "custody": "empty_starter_package",
        },
    )
    write_json(
        output_root / "ION_STARTER_DATA/PERSONA/persona_state.json",
        {
            "schema_id": "ion.persona_interface.v1",
            "user_facing_default": "natural_assistant_with_invisible_continuity",
            "first_prompt": "What are we working on?",
            "save_language": "I can package this project memory so we can continue from here later.",
            "hidden_domain_ids": SEEDED_DOMAIN_IDS,
            "translation_map": {
                "packet": "plan / next step",
                "receipt": "saved decision / project note",
                "context_graph": "project memory",
                "domain": "work area",
                "template": "workflow",
                "data_zip": "project memory pack",
            },
        },
    )
    bootstrap_receipt = {
        "schema_id": "ion.receipt.v1",
        "accepted_as_state": True,
        "created_at": generated_at,
        "receipt_id": "receipt-bootstrap-blank-project-v1",
        "receipt_type": "starter_data_bootstrap",
        "summary": "Initialized seeded portable ION continuity state.",
        "seeded_domains": SEEDED_DOMAIN_IDS,
    }
    write_json(output_root / "ION_STARTER_DATA/RECEIPTS/bootstrap_receipt.json", bootstrap_receipt)
    write_text(output_root / "ION_STARTER_DATA/RECEIPTS/receipt_ledger.jsonl", json.dumps(bootstrap_receipt, sort_keys=True))
    for leaf in ["INBOX", "OUTBOX", "ARCHIVE"]:
        write_text(output_root / f"ION_STARTER_DATA/{leaf}/README.md", f"# {leaf}\n\nReserved for portable ION data package flow.\n")

    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/README.md",
        """
        # ION Custom GPT Adapter

        This adapter teaches a Custom GPT how to operate ION engine law and a
        mounted continuity data zip inside a browser sandbox.

        The Custom GPT is not persistent. The data zip is persistent.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md",
        """
        # GPT Instructions

        You are an ION-compatible browser AI carrier.

        Your job is to operate the mounted ION data package under ION engine
        law while giving the user a natural assistant experience. Do not claim
        source truth from memory. Inspect the mounted data package, work from
        accepted state, perform bounded work, append receipts, and export
        updated continuity data.

        If no data package is mounted, do not begin with an ION protocol
        lecture. Quietly use the seeded starter posture and ask:

        ```text
        What are we working on?
        ```

        Mention the continuity package only when saving, exporting, or
        resuming:

        ```text
        I can package this project memory so we can continue from here later.
        ```

        Never treat your output as accepted state until the package has a
        corresponding receipt.

        ## Required Mount Report

        When a data zip is provided, report:

        - package id
        - project id/name
        - schema version
        - current objective
        - open packet count
        - latest receipt id
        - warnings
        - whether migration is required

        ## State Update Rule

        You may draft updates to state files, but an update is incomplete until
        you append a receipt to `RECEIPTS/receipt_ledger.jsonl` and include a
        clear export instruction for the updated data package.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/STARTUP_BEHAVIOR.md",
        """
        # Startup Behavior

        ## No Data Zip Mounted

        Do not say `No continuity package is mounted` as the first user-facing
        move.

        Quietly initialize seeded starter state from `ION_STARTER_DATA/` in
        the working sandbox. Proceed naturally:

        ```text
        What are we working on?
        ```

        Do not explain packets, receipts, domains, templates, or data zips
        unless the user asks or the workflow reaches save/export/resume.

        Good user-facing language:

        ```text
        I can keep this organized as we go and give you a project memory pack
        when you want to continue later.
        ```

        Internal posture:

        ```text
        seeded starter continuity active
        accepted state not yet exported
        first receipt required before durable continuation claim
        ```

        ## Data Zip Mounted

        Inspect the manifest, current state, domains, context graph, open
        packets, decisions, artifacts, and receipt ledger. Produce a mount
        report before doing substantive work.

        ## Multiple Data Zips Mounted

        Ask which one should be canonical for this turn. Do not merge them
        informally.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/FIRST_RUN_BEHAVIOR.md",
        """
        # First-Run Behavior

        ION is for the AI. The user should experience improved continuity, not
        system machinery.

        On first run, start from the seeded starter domains and ask what the
        user is working on. Capture intent, decisions, open loops, artifacts,
        risks, and useful context internally.

        Do not open with:

        ```text
        No continuity package is mounted.
        ```

        Prefer:

        ```text
        What are we working on?
        ```

        When the work has meaningful continuity value, offer:

        ```text
        I can package this project memory so we can continue from here later.
        ```

        The first export should include the starter state plus any accepted
        project identity, decisions, open loops, artifacts, and receipts.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/PERSONA_INTERFACE_RULES.md",
        """
        # Persona Interface Rules

        Translate ION machinery into user-facing language unless the user asks
        for internals.

        | ION term | User-facing term |
        | --- | --- |
        | packet | plan / next step |
        | receipt | saved decision / project note |
        | context graph | project memory |
        | domain | work area |
        | template | workflow |
        | data zip | project memory pack |

        The assistant may use ION internally to preserve continuity. It should
        not make the user manage protocol language during ordinary work.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/DATA_ZIP_OPERATING_PROTOCOL.md",
        """
        # Data Zip Operating Protocol

        ## Mount

        Inspect `ION_DATA_MANIFEST.json`, `STATE/current_state.json`,
        `DOMAINS/domain_registry.json`, `CONTEXT/context_graph.json`,
        `PACKETS/open_packets.json`, `DECISIONS/decision_ledger.json`,
        `ARTIFACTS/artifact_manifest.json`,
        `PERSONA/persona_state.json`, and `RECEIPTS/receipt_ledger.jsonl`.

        ## Work

        Produce proposals, not unreceipted state. Meaningful updates require a
        receipt append and an updated export.

        ## Export

        Export a new data zip after state changes. The user carries that zip
        forward as continuity.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/STATE_UPDATE_PROTOCOL.md",
        """
        # State Update Protocol

        A state update must include:

        1. the file or object being changed;
        2. the reason the change is allowed;
        3. the prior state considered;
        4. the proposed delta;
        5. the receipt appended;
        6. the export package name.

        Do not update `ION_ENGINE/` from a user data package. Engine evolution
        belongs to the live ION source repo and product packager.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/EXPORT_PROTOCOL.md",
        """
        # Export Protocol

        Any exported data package must preserve:

        - manifest
        - current state
        - domain registry
        - context graph
        - packet records
        - receipt ledger
        - artifacts/inbox/outbox/archive custody

        Exported packages should include a new receipt for the export itself.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/refusal_and_boundary_rules.md",
        """
        # Refusal And Boundary Rules

        Refuse to claim accepted state without a receipt.

        Refuse to mutate engine law from a user data package.

        Refuse to treat platform memory as stronger than the mounted data
        package.

        Refuse to merge multiple continuity packages without an explicit
        settlement packet.

        Refuse to call a generated product package source truth.
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/templates/MOUNT_REPORT_TEMPLATE.md",
        """
        # Mount Report Template

        ```text
        Mounted ION package:
        package_id:
        project_id:
        project_name:
        data_schema_version:
        engine_version:
        migration_required:
        current_objective:
        open_packets:
        latest_receipt:
        warnings:
        ```
        """,
    )
    write_text(
        output_root / "ION_CUSTOM_GPT_ADAPTER/templates/RECEIPT_APPEND_TEMPLATE.md",
        """
        # Receipt Append Template

        ```json
        {
          "schema_id": "ion.receipt.v1",
          "receipt_id": "<receipt-id>",
          "receipt_type": "<type>",
          "created_at": "<iso8601>",
          "accepted_as_state": true,
          "summary": "<what changed>",
          "context_used": [],
          "files_changed": [],
          "next_context_delta": []
        }
        ```
        """,
    )
    write_json(
        output_root / "ION_CUSTOM_GPT_ADAPTER/knowledge_manifest.json",
        {
            "schema_id": "ion.custom_gpt_knowledge_manifest.v1",
            "engine_docs": [
                "ION_ENGINE/doctrine/ION_CORE.md",
                "ION_ENGINE/laws/SIX_LAWS.md",
                "ION_ENGINE/templates/TEMPLATE_LAW.md",
                "ION_ENGINE/context_graph/DOMAIN_GRAPH_AND_FISSION.md",
                "ION_ENGINE/ingestion/PROJECT_INGESTION.md",
                "ION_ENGINE/settlement/PARALLEL_SETTLEMENT.md",
                "ION_ENGINE/projections/PROJECTION_LADDER.md",
                "ION_ENGINE/reference/README.md",
                "ION_ENGINE/reference/ION_FUNDAMENTALS.md",
                "ION_ENGINE/reference/ION_CONTINUITY_SUBSTRATE_EXPLAINER.md",
                "ION_ENGINE/reference/ION_DOMAIN_GRAPH_AND_FISSION.md",
                "ION_ENGINE/reference/ION_PARALLEL_SETTLEMENT.md",
                "ION_ENGINE/reference/ION_PROJECT_INGESTION.md",
                "ION_ENGINE/reference/TEMPLATE_LAW.md",
                "ION_ENGINE/reference/CONTEXT_SYSTEM.md",
                "ION_ENGINE/reference/AGENTS_ROLES_CARRIERS.md",
            ],
            "adapter_docs": [
                "ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md",
                "ION_CUSTOM_GPT_ADAPTER/STARTUP_BEHAVIOR.md",
                "ION_CUSTOM_GPT_ADAPTER/FIRST_RUN_BEHAVIOR.md",
                "ION_CUSTOM_GPT_ADAPTER/PERSONA_INTERFACE_RULES.md",
                "ION_CUSTOM_GPT_ADAPTER/DATA_ZIP_OPERATING_PROTOCOL.md",
                "ION_CUSTOM_GPT_ADAPTER/STATE_UPDATE_PROTOCOL.md",
                "ION_CUSTOM_GPT_ADAPTER/EXPORT_PROTOCOL.md",
                "ION_CUSTOM_GPT_ADAPTER/refusal_and_boundary_rules.md",
            ],
        },
    )

    write_text(
        output_root / "ION_PRODUCT_DOCS/GETTING_STARTED.md",
        """
        # Getting Started

        Start naturally. If no continuity data package exists, the adapter uses
        seeded starter state behind the scenes and asks:

        ```text
        What are we working on?
        ```

        The user does not need to manage ION internals during ordinary work.
        They should feel continuity through clearer plans, remembered
        decisions, open loops, artifacts, and project memory.

        Basic loop:

        ```text
        work naturally -> save decisions and open loops -> append receipt
        -> export project memory pack when useful
        ```
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/CUSTOM_GPT_SETUP.md",
        """
        # Custom GPT Setup

        Use `ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md` as the instruction
        base. Upload adapter docs and selected engine docs from
        `ION_CUSTOM_GPT_ADAPTER/knowledge_manifest.json`.

        Do not upload user data zips as permanent knowledge. User data zips are
        mounted per session and exported after updates.

        Include `FIRST_RUN_BEHAVIOR.md` and `PERSONA_INTERFACE_RULES.md` so the
        GPT does not expose protocol machinery as its default user experience.
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/CONTINUING_FROM_A_DATA_ZIP.md",
        """
        # Continuing From A Data Zip

        Mount the zip, inspect manifest/state/receipts, then continue from
        accepted state. If the latest work is not receipted, treat it as
        proposal or witness material.
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/STARTING_A_NEW_PROJECT.md",
        """
        # Starting A New Project

        Initialize a blank package, define project identity, create the first
        project memory, then emit the first project receipt.

        The starter package is not empty. It includes seeded internal work
        areas for user intent, project state, decisions, open loops, artifacts,
        context graph, risk review, and persona interface.
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/PROJECT_INGESTION.md",
        """
        # Project Ingestion

        Treat uploaded projects as untrusted graphs until manifest,
        cartography, domains, risk, and receipts exist.

        Use the ingestion ladder:

        ```text
        quarantine -> manifest -> cartography -> context graph genesis
        -> domain partition -> template binding -> risk classification
        -> first context packages -> receipts
        ```
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/RECEIPTS_AND_STATE.md",
        """
        # Receipts And State

        Output is candidate. Receipts make accepted deltas inheritable.

        A receipt should name what changed, under what authority, with what
        context and proof, and what the next worker may inherit.
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/DOMAINS_AND_CONTEXT_GRAPH.md",
        """
        # Domains And Context Graph

        Domains are governed graph regions. Split them when context
        manageability fails.

        A file is not context because it exists. It becomes context when its
        identity, authority, status, lineage, and retrieval role are known.
        """,
    )
    write_text(
        output_root / "ION_PRODUCT_DOCS/TROUBLESHOOTING.md",
        """
        # Troubleshooting

        If state is unclear, inspect the latest receipt ledger before
        continuing.

        Common blocks:

        - no mounted data package;
        - multiple data packages with no settlement;
        - migration required;
        - latest output has no receipt;
        - engine docs and user state are being confused.
        """,
    )

    write_text(output_root / "examples/blank_project/README.md", "# Blank Project Example\n\nUse `ION_STARTER_DATA/` as the example blank project state.\n")
    write_json(output_root / "examples/receipt_examples/state_update_receipt.example.json", bootstrap_receipt | {"receipt_id": "receipt-example-state-update"})

    write_text(
        output_root / "tools/validate_data_package.py",
        r'''
        #!/usr/bin/env python3
        """Validate a minimal ION portable data package without external deps."""

        from __future__ import annotations

        import json
        import sys
        from pathlib import Path


        REQUIRED = [
            "ION_DATA_MANIFEST.json",
            "README_FOR_AI.md",
            "STATE/current_state.json",
            "STATE/current_state.md",
            "DOMAINS/domain_registry.json",
            "CONTEXT/context_graph.json",
            "TEMPLATES/template_registry.json",
            "PACKETS/open_packets.json",
            "DECISIONS/decision_ledger.json",
            "ARTIFACTS/artifact_manifest.json",
            "PERSONA/persona_state.json",
            "RECEIPTS/receipt_ledger.jsonl",
        ]


        def load_json(path: Path) -> dict:
            with path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            if not isinstance(payload, dict):
                raise ValueError(f"{path} is not a JSON object")
            return payload


        def validate(root: Path) -> list[str]:
            findings: list[str] = []
            for rel in REQUIRED:
                if not (root / rel).exists():
                    findings.append(f"missing:{rel}")
            if findings:
                return findings
            manifest = load_json(root / "ION_DATA_MANIFEST.json")
            state = load_json(root / "STATE/current_state.json")
            domains = load_json(root / "DOMAINS/domain_registry.json")
            graph = load_json(root / "CONTEXT/context_graph.json")
            templates = load_json(root / "TEMPLATES/template_registry.json")
            packets = load_json(root / "PACKETS/open_packets.json")
            decisions = load_json(root / "DECISIONS/decision_ledger.json")
            artifacts = load_json(root / "ARTIFACTS/artifact_manifest.json")
            persona = load_json(root / "PERSONA/persona_state.json")
            if manifest.get("schema_id") != "ion.data_manifest.v1":
                findings.append("manifest_schema_id_invalid")
            if state.get("schema_id") != "ion.current_state.v1":
                findings.append("current_state_schema_id_invalid")
            if domains.get("schema_id") != "ion.domain_registry.v1":
                findings.append("domain_registry_schema_id_invalid")
            if graph.get("schema_id") != "ion.context_graph.v1":
                findings.append("context_graph_schema_id_invalid")
            if templates.get("schema_id") != "ion.template_registry.v1":
                findings.append("template_registry_schema_id_invalid")
            if packets.get("schema_id") != "ion.open_packets.v1":
                findings.append("open_packets_schema_id_invalid")
            if decisions.get("schema_id") != "ion.decision_ledger.v1":
                findings.append("decision_ledger_schema_id_invalid")
            if artifacts.get("schema_id") != "ion.artifact_manifest.v1":
                findings.append("artifact_manifest_schema_id_invalid")
            if persona.get("schema_id") != "ion.persona_interface.v1":
                findings.append("persona_interface_schema_id_invalid")
            ledger_lines = [line for line in (root / "RECEIPTS/receipt_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            if not ledger_lines:
                findings.append("receipt_ledger_empty")
            else:
                for index, line in enumerate(ledger_lines, start=1):
                    try:
                        json.loads(line)
                    except json.JSONDecodeError:
                        findings.append(f"receipt_ledger_line_{index}_invalid_json")
            return findings


        def main() -> int:
            root = Path(sys.argv[1] if len(sys.argv) > 1 else "ION_STARTER_DATA").resolve()
            findings = validate(root)
            if findings:
                print(json.dumps({"ok": False, "root": str(root), "findings": findings}, indent=2))
                return 1
            print(json.dumps({"ok": True, "root": str(root), "findings": []}, indent=2))
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        ''',
    )
    write_text(
        output_root / "tools/build_starter_zip.py",
        r'''
        #!/usr/bin/env python3
        """Build the non-release blank ION continuity data zip."""

        from __future__ import annotations

        import hashlib
        import json
        import zipfile
        from pathlib import Path


        ROOT = Path(__file__).resolve().parents[1]
        STARTER = ROOT / "ION_STARTER_DATA"
        DIST = ROOT / "dist"
        ZIP_PATH = DIST / "ION_CONTINUITY_DATA_BLANK_v1.zip"


        def sha256_file(path: Path) -> str:
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            return digest.hexdigest()


        def main() -> int:
            DIST.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(STARTER.rglob("*")):
                    if path.is_file():
                        archive.write(path, path.relative_to(STARTER).as_posix())
            manifest = {
                "artifact": ZIP_PATH.name,
                "artifact_type": "starter_continuity_data_zip",
                "release_status": "non_release_scaffold",
                "zip_root": "data_package_root",
                "sha256": sha256_file(ZIP_PATH),
                "size_bytes": ZIP_PATH.stat().st_size,
            }
            (DIST / "ION_CONTINUITY_DATA_BLANK_v1.manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(json.dumps({"ok": True, "zip": str(ZIP_PATH), **manifest}, indent=2))
            return 0


        if __name__ == "__main__":
            raise SystemExit(main())
        ''',
    )
    write_text(
        output_root / "tests/test_starter_data_shape.py",
        r'''
        import json
        import zipfile
        from pathlib import Path


        ROOT = Path(__file__).resolve().parents[1]
        STARTER = ROOT / "ION_STARTER_DATA"
        STARTER_ZIP = ROOT / "dist/ION_CONTINUITY_DATA_BLANK_v1.zip"


        def test_starter_manifest_shape():
            payload = json.loads((STARTER / "ION_DATA_MANIFEST.json").read_text(encoding="utf-8"))
            assert payload["schema_id"] == "ion.data_manifest.v1"
            assert payload["data_schema_version"] == 1
            assert payload["authority"] == "portable_data_candidate_not_engine_truth"


        def test_receipt_ledger_has_bootstrap_receipt():
            lines = (STARTER / "RECEIPTS/receipt_ledger.jsonl").read_text(encoding="utf-8").splitlines()
            receipts = [json.loads(line) for line in lines if line.strip()]
            assert receipts
            assert receipts[0]["receipt_type"] == "starter_data_bootstrap"


        def test_portable_state_indexes_exist():
            checks = {
                "PACKETS/open_packets.json": "ion.open_packets.v1",
                "DECISIONS/decision_ledger.json": "ion.decision_ledger.v1",
                "ARTIFACTS/artifact_manifest.json": "ion.artifact_manifest.v1",
                "PERSONA/persona_state.json": "ion.persona_interface.v1",
            }
            for rel, schema_id in checks.items():
                payload = json.loads((STARTER / rel).read_text(encoding="utf-8"))
                assert payload["schema_id"] == schema_id


        def test_seeded_domains_exist():
            payload = json.loads((STARTER / "DOMAINS/domain_registry.json").read_text(encoding="utf-8"))
            domain_ids = {domain["domain_id"] for domain in payload["domains"]}
            assert {
                "USER_INTENT",
                "PROJECT_STATE",
                "DECISIONS",
                "OPEN_LOOPS",
                "ARTIFACTS",
                "CONTEXT_GRAPH",
                "RISK_REVIEW",
                "PERSONA_INTERFACE",
            } <= domain_ids


        def test_starter_zip_manifest_is_at_root():
            with zipfile.ZipFile(STARTER_ZIP) as archive:
                names = set(archive.namelist())
            assert "ION_DATA_MANIFEST.json" in names
            assert "ION_STARTER_DATA/ION_DATA_MANIFEST.json" not in names
        ''',
    )

    zip_manifest = build_starter_zip(output_root)
    build_receipt = {
        "accepted_as_source_truth": False,
        "generated_at": generated_at,
        "outputs": [
            "ION_PRODUCT_PACKAGE/",
            "dist/ION_CONTINUITY_DATA_BLANK_v1.zip",
        ],
        "product_package_version": PRODUCT_VERSION,
        "receipt_type": "ion_product_package_build_receipt",
        "source_branch": source_branch,
        "source_commit": source_commit,
        "validation": {
            "starter_data_shape": "prepared",
            "schema_examples": "draft",
            "zip_roundtrip": "prepared",
        },
        "zip_manifest": zip_manifest,
    }
    write_json(output_root / "BUILD_RECEIPT.json", build_receipt)
    return {
        "output_root": str(output_root),
        "source_commit": source_commit,
        "source_branch": source_branch,
        "generated_at": generated_at,
        "zip_manifest": zip_manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--repo-root", type=Path, default=repo_root_from_script())
    args = parser.parse_args()
    result = build_package(args.output, args.repo_root)
    print(json.dumps({"ok": True, **result}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
