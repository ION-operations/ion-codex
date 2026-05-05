"""V79 — ION Context Authority Team audit.

This module intentionally avoids external YAML dependencies. It performs a
structural/literal audit that the live root contains the minimum context-authority
surfaces and rejects obvious stale primary-context claims.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

REQUIRED_FILES = (
    "ION/02_architecture/ION_CONTEXT_AUTHORITY_TEAM_PROTOCOL.md",
    "ION/03_registry/ion_context_authority_team_registry.yaml",
    "ION/07_templates/README.md",
    "ION/07_templates/_MASTER.md",
    "ION/07_templates/context/AGENT_CONTEXT_PACKAGE.md",
    "ION/07_templates/context/ION_CONTEXT_DELTA_RECEIPT.md",
    "ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md",
    "ION/07_templates/agents/ION_CONTEXT_SPECIALIST_RETURN.md",
    "ION/03_registry/boots/IONOLOGIST.boot.md",
    "ION/03_registry/boots/CONTEXT_CARTOGRAPHER.boot.md",
    "ION/03_registry/boots/RUNTIME_CARTOGRAPHER.boot.md",
    "ION/03_registry/boots/CANON_LIBRARIAN.boot.md",
    "ION/03_registry/boots/TEMPLATE_CURATOR.boot.md",
)

REQUIRED_ROLE_NAMES = (
    "IONOLOGIST",
    "CONTEXT_CARTOGRAPHER",
    "RUNTIME_CARTOGRAPHER",
    "CANON_LIBRARIAN",
    "TEMPLATE_CURATOR",
)

REQUIRED_PHRASES = (
    "High-Detail Agent Context Package",
    "MINI/CAPSULE are not primary context authority",
    "### CONTEXT PROOF",
    "ION_CONTEXT_DELTA_RECEIPT",
)

STALE_PRIMARY_PATTERNS = (
    (re.compile(r"(?i)MINI/CAPSULE\s+are\s+primary"), "MINI_CAPSULE_PRIMARY_CLAIM"),
    (re.compile(r"(?i)root\s+`?ION/MINI\.md`?.{0,80}primary\s+context"), "ROOT_MINI_PRIMARY_CLAIM"),
    (re.compile(r"(?i)boot\s+file\s+alone\s+is\s+context"), "BOOT_FILE_ALONE_CONTEXT_CLAIM"),
    (re.compile(r"(?i)path\s+list\s+is\s+onboarded\s+context"), "PATH_LIST_CONTEXT_CLAIM"),
)


def lint_stale_primary_context_claims(text: str) -> list[str]:
    hits: list[str] = []
    for rx, code in STALE_PRIMARY_PATTERNS:
        if rx.search(text):
            hits.append(code)
    return sorted(set(hits))


def audit_ion_context_authority_team(root: Path) -> dict[str, Any]:
    root = root.resolve()
    missing = [path for path in REQUIRED_FILES if not (root / path).is_file()]

    corpus_parts: list[str] = []
    for path in REQUIRED_FILES:
        p = root / path
        if p.is_file():
            corpus_parts.append(p.read_text(encoding="utf-8", errors="replace"))
    corpus = "\n".join(corpus_parts)

    missing_roles = [role for role in REQUIRED_ROLE_NAMES if role not in corpus]
    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in corpus]
    stale_hits = lint_stale_primary_context_claims(corpus)

    accepted = not missing and not missing_roles and not missing_phrases and not stale_hits
    return {
        "audit_id": "v79_ion_context_authority_team",
        "root": str(root),
        "accepted": accepted,
        "missing_required_files": missing,
        "missing_required_roles": missing_roles,
        "missing_required_phrases": missing_phrases,
        "stale_primary_context_claims": stale_hits,
        "required_files": list(REQUIRED_FILES),
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    print(json.dumps(audit_ion_context_authority_team(Path(args.root)), indent=2))
