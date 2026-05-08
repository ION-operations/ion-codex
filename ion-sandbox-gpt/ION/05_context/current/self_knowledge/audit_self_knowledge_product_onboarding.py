#!/usr/bin/env python3
"""Audit product/front-door surfaces for ION self-knowledge mount-first wiring.

This script is sandbox-local evidence only. It does not mutate product files,
Custom GPT instructions, PRODUCT_MANIFEST.json, or ION/03_registry.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
from pathlib import Path


FRONTDOOR_SURFACES = [
    "START_HERE.md",
    "README.md",
    "PRODUCT_MANIFEST.json",
    "product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md",
    "product/custom_gpt_adapter/GPT_INSTRUCTIONS.md",
    "product/custom_gpt_adapter/STARTUP_BEHAVIOR.md",
    "product/custom_gpt_adapter/FIRST_RUN_BEHAVIOR.md",
    "product/custom_gpt_adapter/knowledge_manifest.json",
    "product/custom_gpt_adapter/README.md",
    "product/package_guides/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE.md",
    "product/package_guides/CUSTOM_GPT_PRODUCT_USE.md",
    "product/starter_data/README_FOR_AI.md",
    "product/starter_data/ION_DATA_MANIFEST.json",
]


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_surface(root: Path, rel: str) -> dict:
    path = root / rel
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    return {
        "path": rel,
        "exists": path.exists(),
        "sha256": sha256_path(path) if path.exists() else None,
        "bytes": path.stat().st_size if path.exists() else 0,
        "contains_self_knowledge_keyword": bool(re.search(r"self[- ]knowledge", text, re.I)),
        "contains_active_self_knowledge_mount_packet": "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md" in text,
        "contains_ion_about_ion_phrase": "ION-about-ION" in text or "ION about ION" in text,
        "contains_route_registry_reference": "route_registry" in text and "self_knowledge" in text,
    }


def build_patchset(root: Path, generated_at: str) -> dict:
    active_packet = root / "ION/05_context/current/ACTIVE_WORK_PACKET.json"
    allowed_paths = []
    if active_packet.exists():
        allowed_paths = json.loads(active_packet.read_text(encoding="utf-8")).get("allowed_paths", [])

    common = """## ION Self-Knowledge Route

When the user's request is about ION itself—identity, architecture, runtime bodies, agents/roles, packages, templates, workpackets, authority, receipts, recovery, or implementation—the carrier must route through the mounted self-knowledge system before answering or acting.

Required order:

```text
normal ION mount
→ active state load
→ classify whether the task is ION-about-ION
→ mount ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md
→ load self-knowledge route registry
→ load required self-knowledge domain packets
→ answer or act with explicit non-claims
```

Anti-drift guards:

- Single-carrier sequential mode is a host-limited fallback, not ION's intended center.
- The GPT sandbox package is not reduced ION; it is full ION adapted to sandbox constraints.
- Historical/donor material may inform recovery but may not become active authority without settlement.
- Do not invent replacement ION law before checking existing domains, registries, templates, protocols, receipts, and package surfaces.
"""

    return {
        "schema_id": "ion.self_knowledge.product_onboarding_patchset.v0_2",
        "generated_at": generated_at,
        "status": "candidate_overlay_pending_explicit_acceptance",
        "authority_boundary": {
            "mutates_product_surfaces": False,
            "mutates_custom_gpt_instructions": False,
            "mutates_product_manifest": False,
            "requires_explicit_acceptance_to_land": True,
            "active_packet_allowed_paths": allowed_paths,
        },
        "intent": "Make product/front-door GPT package surfaces inherit self-knowledge mount-first behavior for ION-about-ION tasks after acceptance.",
        "non_claims": [
            "This patchset is not accepted product law.",
            "This patchset has not mutated product/custom_gpt_adapter, START_HERE.md, README.md, PRODUCT_MANIFEST.json, or package guides.",
            "This patchset does not grant production authority, live execution authority, external Codex/MCP execution, or registry landing.",
        ],
        "patch_operations": [
            {
                "target_path": "START_HERE.md",
                "operation": "insert_section_after",
                "anchor": "## Mount order",
                "section_title": "ION Self-Knowledge Route",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md", "single-carrier", "not reduced ION"],
                "text": common.strip(),
            },
            {
                "target_path": "README.md",
                "operation": "insert_section_before",
                "anchor": "See:",
                "section_title": "ION Self-Knowledge Route",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md", "not reduced ION"],
                "text": common.strip(),
            },
            {
                "target_path": "product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md",
                "operation": "insert_section_after",
                "anchor": "## Full ION Package Mounting",
                "section_title": "ION Self-Knowledge Mount-First Rule",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md", "Single-carrier sequential execution is a sandbox fallback"],
                "text": "When the user asks about ION itself or asks to build, repair, explain, package, resume, or audit ION, do not free-answer from memory. After the normal package mount and active-state check, mount `ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md`, then select the matching self-knowledge route and load required domain packets.",
            },
            {
                "target_path": "product/custom_gpt_adapter/GPT_INSTRUCTIONS.md",
                "operation": "insert_section_after",
                "anchor": "# GPT Instructions",
                "section_title": "ION-About-ION Questions",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md", "Full local/API-style ION"],
                "text": "For ION-about-ION questions, mount the self-knowledge route selector before answering. Use `ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md` when present; if an accepted `ION/03_registry/self_knowledge/` namespace later exists, prefer accepted registry law over candidate current-context mirrors.",
            },
            {
                "target_path": "product/custom_gpt_adapter/STARTUP_BEHAVIOR.md",
                "operation": "insert_section_after",
                "anchor": "# Startup Behavior",
                "section_title": "ION-About-ION Startup Route",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md"],
                "text": "For ION-about-ION startup or resume requests, quietly mount the self-knowledge route selector after normal package mount and before explaining or changing ION. Use `ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md` when present. Preserve normal first-run user language for unrelated projects.",
            },
            {
                "target_path": "product/package_guides/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE.md",
                "operation": "insert_section_after",
                "anchor": "## Package Contents",
                "section_title": "Self-Knowledge Product Route",
                "required_phrases": ["ION-about-ION", "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md", "GPT sandbox package is full ION adapted to sandbox constraints"],
                "text": "The package may carry a candidate or accepted self-knowledge domain state for ION-about-ION work. When present, carriers should mount `ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md` before answering ION identity, architecture, runtime, package, role, template, receipt, recovery, or implementation questions. The GPT sandbox package is full ION adapted to sandbox constraints, not reduced ION.",
            },
            {
                "target_path": "product/custom_gpt_adapter/knowledge_manifest.json",
                "operation": "add_paths",
                "anchor": "added_surfaces",
                "paths_to_add": [
                    "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md",
                    "ION/05_context/current/self_knowledge/SELF_KNOWLEDGE_DOMAIN_STATE_INDEX_V0_2.json",
                    "ION/05_context/current/self_knowledge/candidate_registries/domain_registry.candidate.yaml",
                    "ION/05_context/current/self_knowledge/candidate_registries/route_registry.candidate.yaml",
                    "ION/05_context/current/self_knowledge/domains/",
                ],
            },
            {
                "target_path": "PRODUCT_MANIFEST.json",
                "operation": "add_object",
                "anchor": "root",
                "object_key": "self_knowledge_product_onboarding_candidate",
                "object_value": {
                    "status": "candidate_overlay_pending_explicit_acceptance",
                    "mount_packet": "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md",
                    "domain_state_index": "ION/05_context/current/self_knowledge/SELF_KNOWLEDGE_DOMAIN_STATE_INDEX_V0_2.json",
                    "route_registry_candidate": "ION/05_context/current/self_knowledge/candidate_registries/route_registry.candidate.yaml",
                    "acceptance_required_before_product_landing": True,
                },
            },
        ],
    }


def build_report(root: Path, generated_at: str, patchset_path: str | None = None, proposal_path: str | None = None) -> dict:
    surfaces = [inspect_surface(root, rel) for rel in FRONTDOOR_SURFACES]
    explicit_count = sum(
        1
        for surface in surfaces
        if surface["contains_active_self_knowledge_mount_packet"]
        or (surface["contains_self_knowledge_keyword"] and surface["contains_route_registry_reference"])
    )
    sk = root / "ION/05_context/current/self_knowledge"
    inclusion = {
        "active_self_knowledge_mount_packet_exists": (root / "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md").exists(),
        "self_knowledge_current_dir_exists": sk.exists(),
        "candidate_domain_dir_exists": (sk / "domains").exists(),
        "candidate_domain_count": len(list((sk / "domains").glob("*.domain_packet.yaml"))) if (sk / "domains").exists() else 0,
        "candidate_route_registry_exists": (sk / "candidate_registries/route_registry.candidate.yaml").exists(),
        "promotion_apply_tree_exists": (sk / "promotion_candidate/apply_tree").exists(),
    }
    return {
        "schema_id": "ion.self_knowledge.product_onboarding_audit_report.v0_2",
        "generated_at": generated_at,
        "status": "accepted_candidate_evidence_product_overlay_prepared",
        "accepted": True,
        "simulation_mode": "sandbox_local_product_frontdoor_audit_not_product_mutation",
        "package_inclusion": inclusion,
        "frontdoor_surfaces": surfaces,
        "frontdoor_explicit_self_knowledge_surface_count": explicit_count,
        "candidate_patchset_path": patchset_path,
        "candidate_proposal_path": proposal_path,
        "authority_boundary": {
            "mutated_product_surfaces": False,
            "mutated_custom_gpt_instructions": False,
            "mutated_product_manifest": False,
            "mutated_ION_03_registry": False,
            "production_authority": False,
            "live_execution_authority": False,
            "explicit_acceptance_observed": False,
        },
        "coverage": {
            "frontdoor_surface_count": len(surfaces),
            "existing_frontdoor_explicit_self_knowledge_surface_count": explicit_count,
            "required_package_surfaces_present": bool(
                inclusion["active_self_knowledge_mount_packet_exists"]
                and inclusion["self_knowledge_current_dir_exists"]
                and inclusion["candidate_domain_count"] >= 14
                and inclusion["candidate_route_registry_exists"]
            ),
        },
        "non_claims": [
            "This audit does not apply the candidate patchset to product/front-door surfaces.",
            "This audit does not change Custom GPT instructions.",
            "This audit does not accept self-knowledge registry or onboarding law.",
            "This audit is sandbox-local evidence, not external Codex/MCP/daemon execution.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ion-root", default=".", help="Shell package root containing pyproject.toml and ION/")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.ion_root).resolve()
    generated_at = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()
    patchset = build_patchset(root, generated_at)
    report = build_report(root, generated_at)
    payload = {"report": report, "patchset": patchset}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"status={report['status']}")
        print(f"frontdoor_explicit_self_knowledge_surface_count={report['frontdoor_explicit_self_knowledge_surface_count']}")
        print("mutated_product_surfaces=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
