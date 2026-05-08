"""Sequential kernel router for the active IDE-native ION root.

This module does not attempt to "be the LLM." It encodes the current operating law:
which role surfaces should load first, which projections are optional, and which
sequential pass chains make sense when one high-capability operator is acting as the
practical kernel router for the whole field.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
import argparse
import re
from typing import Iterable, Mapping, Sequence


ROOT_PROJECTION_PATHS = (
    "ION/MINI.md",
    "ION/STATUS.md",
    "ION/CAPSULE.md",
)
SIGNALS_DIR = "ION/05_context/signals"
DEFAULT_ATLAS_REFERENCE_PATH = "ATLAS/README.md"


def default_repo_root(start: str | Path | None = None) -> Path:
    """Discover the active repo root from local filesystem structure."""

    candidate = Path(start) if start is not None else Path(__file__).resolve()
    candidate = candidate.resolve()
    search_roots = candidate.parents if candidate.is_file() else (candidate, *candidate.parents)

    for root in search_roots:
        ion_root = root / "ION"
        if (
            (ion_root / "03_registry" / "boots").is_dir()
            and (ion_root / "04_packages" / "kernel").is_dir()
        ):
            return root

    raise FileNotFoundError(
        f"Could not discover an ION repo root from {candidate}. Expected a parent containing ION/03_registry/boots and ION/04_packages/kernel."
    )


@dataclass(frozen=True)
class LoadTarget:
    """One ordered load surface for a role session."""

    label: str
    path: str
    kind: str = "file"  # file, dir, glob
    required: bool = True
    note: str = ""

    def resolved(self, repo_root: Path) -> Path:
        candidate = Path(self.path)
        if candidate.is_absolute():
            return candidate
        return repo_root / self.path

    def exists(self, repo_root: Path) -> bool:
        if self.kind == "glob":
            return any(repo_root.glob(self.path))
        return self.resolved(repo_root).exists()


@dataclass(frozen=True)
class RoleConfig:
    """Current role topology for one ION role."""

    name: str
    continuity_class: str
    boot_path: str
    continuity_targets: tuple[LoadTarget, ...]
    inbox_glob: str | None = None
    default_extra_reads: tuple[LoadTarget, ...] = ()
    projection_paths: tuple[str, ...] = ROOT_PROJECTION_PATHS

    def build_load_targets(
        self,
        directive_paths: Sequence[str] = (),
        extra_reads: Sequence[str] = (),
        include_projections: bool = True,
    ) -> tuple[LoadTarget, ...]:
        targets: list[LoadTarget] = [
            LoadTarget(label=f"{self.name}.boot", path=self.boot_path),
            *self.continuity_targets,
        ]

        for index, directive_path in enumerate(directive_paths, start=1):
            targets.append(
                LoadTarget(
                    label=f"{self.name}.directive.{index}",
                    path=directive_path,
                )
            )

        if self.inbox_glob:
            targets.append(
                LoadTarget(
                    label=f"{self.name}.inbox",
                    path=self.inbox_glob,
                    kind="glob",
                    required=False,
                )
            )

        targets.append(
            LoadTarget(
                label=f"{self.name}.signals",
                path=SIGNALS_DIR,
                kind="dir",
            )
        )

        targets.extend(self.default_extra_reads)

        if include_projections:
            for projection_path in self.projection_paths:
                targets.append(
                    LoadTarget(
                        label=f"{self.name}.projection.{Path(projection_path).name}",
                        path=projection_path,
                        required=False,
                        note="shared projection only",
                    )
                )

        for index, extra_read in enumerate(extra_reads, start=1):
            targets.append(
                LoadTarget(
                    label=f"{self.name}.extra.{index}",
                    path=extra_read,
                    required=False,
                )
            )

        return tuple(targets)


class Workstream(str, Enum):
    """High-level sequential routing classes for the current low-burn runtime."""

    GOVERNANCE = "governance"
    IMPLEMENTATION = "implementation"
    RESEARCH = "research"
    ARCHAEOLOGY = "archaeology"
    RELAY = "relay"


@dataclass(frozen=True)
class RolePass:
    """One deliberate role pass inside a sequential end-to-end trace."""

    role_name: str
    purpose: str
    required: bool = True


@dataclass(frozen=True)
class RoleSession:
    """Resolved ordered load set for one role pass."""

    role_name: str
    objective: str
    load_targets: tuple[LoadTarget, ...]

    def ordered_labels(self) -> tuple[str, ...]:
        return tuple(target.label for target in self.load_targets)

    def missing_required(self, repo_root: Path) -> tuple[LoadTarget, ...]:
        return tuple(
            target
            for target in self.load_targets
            if target.required and not target.exists(repo_root)
        )


@dataclass(frozen=True)
class SequentialTrace:
    """A whole multi-role sequential pass chain for one bounded objective."""

    workstream: Workstream
    objective: str
    passes: tuple[RolePass, ...]
    sessions: tuple[RoleSession, ...]

    def role_names(self) -> tuple[str, ...]:
        return tuple(role_pass.role_name for role_pass in self.passes)

    def missing_required(self, repo_root: Path) -> dict[str, tuple[LoadTarget, ...]]:
        missing: dict[str, tuple[LoadTarget, ...]] = {}
        for session in self.sessions:
            session_missing = session.missing_required(repo_root)
            if session_missing:
                missing[session.role_name] = session_missing
        return missing


@dataclass(frozen=True)
class ExecutionBundle:
    """Generated packet set for one planned sequential execution run."""

    run_root: Path
    trace_path: Path
    session_paths: tuple[Path, ...]
    handoff_paths: tuple[Path, ...]


@dataclass(frozen=True)
class TaskRetirement:
    """Outcome of retiring one task packet from the active inbox."""

    source_path: Path
    destination_path: Path
    status: str


def _file(label: str, path: str, *, required: bool = True, note: str = "") -> LoadTarget:
    return LoadTarget(label=label, path=path, required=required, note=note)


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "run"


def _relative_display(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("Expected leading frontmatter block.")
    marker = "\n---\n"
    boundary = text.find(marker, 4)
    if boundary == -1:
        raise ValueError("Could not find closing frontmatter delimiter.")
    frontmatter = text[4:boundary]
    body = text[boundary + len(marker) :]
    return frontmatter, body


def _replace_frontmatter_field(frontmatter: str, key: str, value: str) -> str:
    lines = frontmatter.splitlines()
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


class SequentialKernelRouter:
    """The current low-burn sequential router for the active ION root."""

    def __init__(self, repo_root: Path, roles: Mapping[str, RoleConfig] | None = None) -> None:
        self.repo_root = Path(repo_root)
        self.roles = dict(roles or self._default_roles())

    @classmethod
    def default(cls, repo_root: str | Path) -> "SequentialKernelRouter":
        return cls(Path(repo_root))

    def role(self, role_name: str) -> RoleConfig:
        try:
            return self.roles[role_name]
        except KeyError as exc:
            raise KeyError(f"Unknown role: {role_name}") from exc

    def build_role_session(
        self,
        role_name: str,
        objective: str,
        directive_paths: Sequence[str] = (),
        extra_reads: Sequence[str] = (),
        include_projections: bool = True,
    ) -> RoleSession:
        role = self.role(role_name)
        return RoleSession(
            role_name=role_name,
            objective=objective,
            load_targets=role.build_load_targets(
                directive_paths=directive_paths,
                extra_reads=extra_reads,
                include_projections=include_projections,
            ),
        )

    def plan_workstream(self, workstream: Workstream) -> tuple[RolePass, ...]:
        if workstream is Workstream.GOVERNANCE:
            return (
                RolePass("steward", "classify the problem and prepare the bounded convergence object"),
                RolePass("vizier", "perform the primary architecture or governance pass"),
                RolePass("vice", "apply conjugate daimon pressure to preserve future answerability"),
                RolePass("nemesis", "audit the consolidated set before closure"),
                RolePass("relay", "package the result for the Sovereign or wider field", required=False),
            )
        if workstream is Workstream.IMPLEMENTATION:
            return (
                RolePass("steward", "classify the task and prepare the scoped implementation route"),
                RolePass("vizier", "define scope, dependencies, and required review posture"),
                RolePass("mason", "execute the bounded implementation slice"),
                RolePass("vice", "apply risk pressure if the slice affects continuity or governance", required=False),
                RolePass("nemesis", "audit or verify when the slice becomes release-sensitive", required=False),
            )
        if workstream is Workstream.RESEARCH:
            return (
                RolePass("steward", "frame the question and keep provenance visible"),
                RolePass("thoth", "perform the focused research or evidence sweep", required=False),
                RolePass("atlas", "supply comparative reference pressure when external lineage matters", required=False),
                RolePass("vestige", "surface stale lineage or buried contradictions", required=False),
            )
        if workstream is Workstream.ARCHAEOLOGY:
            return (
                RolePass("steward", "frame the archaeology target and desired output"),
                RolePass("vestige", "excavate lineage, stale authority, and unresolved contradictions"),
                RolePass("vice", "translate archaeological risk into future-answerability pressure", required=False),
                RolePass("nemesis", "audit admissibility if the finding becomes load-bearing", required=False),
            )
        if workstream is Workstream.RELAY:
            return (
                RolePass("steward", "frame the communication need and bound the packet"),
                RolePass("relay", "perform the courier pass"),
                RolePass("vizier", "absorb strategic implications when the packet changes governance", required=False),
            )
        raise ValueError(f"Unsupported workstream: {workstream}")

    def build_trace(
        self,
        workstream: Workstream,
        objective: str,
        directive_paths: Sequence[str] = (),
        extra_reads_by_role: Mapping[str, Sequence[str]] | None = None,
        include_projections: bool = True,
    ) -> SequentialTrace:
        passes = self.plan_workstream(workstream)
        extra_reads_by_role = dict(extra_reads_by_role or {})
        sessions = tuple(
            self.build_role_session(
                role_pass.role_name,
                objective=objective,
                directive_paths=directive_paths,
                extra_reads=extra_reads_by_role.get(role_pass.role_name, ()),
                include_projections=include_projections,
            )
            for role_pass in passes
        )
        return SequentialTrace(
            workstream=workstream,
            objective=objective,
            passes=passes,
            sessions=sessions,
        )

    def validate_current_runtime(self) -> dict[str, tuple[LoadTarget, ...]]:
        missing: dict[str, tuple[LoadTarget, ...]] = {}
        for role_name in self.roles:
            session = self.build_role_session(
                role_name=role_name,
                objective="validate current runtime surfaces",
            )
            session_missing = session.missing_required(self.repo_root)
            if session_missing:
                missing[role_name] = session_missing
        return missing

    def _default_roles(self) -> dict[str, RoleConfig]:
        return {
            "vizier": RoleConfig(
                name="vizier",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/VIZIER.boot.md",
                continuity_targets=(
                    _file("vizier.private_mini", "ION/agents/vizier/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("vizier.private_capsule", "ION/agents/vizier/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                inbox_glob="ION/05_context/inbox/vizier*",
            ),
            "vice": RoleConfig(
                name="vice",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/VICE.boot.md",
                continuity_targets=(
                    _file("vice.private_mini", "ION/agents/vice/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("vice.private_capsule", "ION/agents/vice/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
            ),
            "nemesis": RoleConfig(
                name="nemesis",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/NEMESIS.boot.md",
                continuity_targets=(
                    _file("nemesis.private_mini", "ION/agents/nemesis/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file(
                        "nemesis.private_capsule",
                        "ION/agents/nemesis/CAPSULE.md",
                        required=False,
                        note="capsule not yet present in the active root",
                    ),
                ),
            ),
            "mason": RoleConfig(
                name="mason",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/MASON.boot.md",
                continuity_targets=(
                    _file("mason.private_mini", "ION/agents/mason/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("mason.private_capsule", "ION/agents/mason/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                inbox_glob="ION/05_context/inbox/mason_*",
            ),
            "scribe": RoleConfig(
                name="scribe",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/SCRIBE.boot.md",
                continuity_targets=(
                    _file("scribe.private_mini", "ION/agents/scribe/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("scribe.private_capsule", "ION/agents/scribe/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                inbox_glob="ION/05_context/inbox/scribe_*",
            ),
            "thoth": RoleConfig(
                name="thoth",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/THOTH.boot.md",
                continuity_targets=(
                    _file("thoth.private_mini", "ION/agents/thoth/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("thoth.private_capsule", "ION/agents/thoth/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                inbox_glob="ION/05_context/inbox/thoth_*",
            ),
            "atlas": RoleConfig(
                name="atlas",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/ATLAS.boot.md",
                continuity_targets=(
                    _file("atlas.private_mini", "ION/agents/atlas/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("atlas.private_capsule", "ION/agents/atlas/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                default_extra_reads=(
                    _file(
                        "atlas.reference_root",
                        DEFAULT_ATLAS_REFERENCE_PATH,
                        required=False,
                    ),
                ),
            ),
            "steward": RoleConfig(
                name="steward",
                continuity_class="agent-private",
                boot_path="ION/03_registry/boots/STEWARD.boot.md",
                continuity_targets=(
                    _file("steward.private_mini", "ION/agents/steward/MINI.md", required=False, note="legacy private mini; live context arrives through boot/context-system package"),
                    _file("steward.private_capsule", "ION/agents/steward/CAPSULE.md", required=False, note="legacy private capsule; live context arrives through boot/context-system package"),
                ),
                inbox_glob="ION/05_context/inbox/steward_*",
            ),
            "relay": RoleConfig(
                name="relay",
                continuity_class="lane-native",
                boot_path="ION/03_registry/boots/RELAY.boot.md",
                continuity_targets=(
                    _file("relay.continuity", "ION/06_intelligence/relay/relay/continuity.md"),
                    _file("relay.profile", "ION/06_intelligence/relay/relay/sovereign_profile.md"),
                    _file("relay.digest", "ION/06_intelligence/relay/relay/interaction_digest.md"),
                    _file("relay.persona", "ION/06_intelligence/relay/relay/persona_state.md"),
                ),
            ),
            "vestige": RoleConfig(
                name="vestige",
                continuity_class="lane-native",
                boot_path="ION/03_registry/boots/VESTIGE.boot.md",
                continuity_targets=(
                    _file("vestige.continuity", "ION/06_intelligence/archaeology/vestige/continuity.md"),
                    _file("vestige.watchlist", "ION/06_intelligence/archaeology/vestige/watchlist.md"),
                ),
            ),
        }


def render_trace(trace: SequentialTrace, repo_root: Path) -> str:
    """Render a human-readable view of one sequential trace."""

    lines = [
        f"workstream: {trace.workstream.value}",
        f"objective: {trace.objective}",
    ]
    missing = trace.missing_required(repo_root)
    lines.append(f"required_surfaces_ok: {not bool(missing)}")
    lines.append("")

    for index, (role_pass, session) in enumerate(zip(trace.passes, trace.sessions), start=1):
        lines.append(f"{index}. {role_pass.role_name} — {role_pass.purpose}")
        for target in session.load_targets:
            suffix = ""
            if not target.required:
                suffix = " [optional]"
            elif not target.exists(repo_root):
                suffix = " [missing]"
            lines.append(f"   - {target.label}: {target.path}{suffix}")
        lines.append("")

    return "\n".join(lines).rstrip()


def write_trace_artifact(
    trace: SequentialTrace,
    repo_root: Path,
    output_path: str | Path,
) -> Path:
    """Persist one rendered sequential trace to disk for later inspection."""

    resolved_output = Path(output_path)
    if not resolved_output.is_absolute():
        resolved_output = repo_root / resolved_output

    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(f"{render_trace(trace, repo_root)}\n", encoding="utf-8")
    return resolved_output


def write_execution_bundle(
    trace: SequentialTrace,
    repo_root: Path,
    run_root: str | Path,
    *,
    source_task: str | None = None,
) -> ExecutionBundle:
    """Generate a filesystem-visible per-pass execution scaffold for one trace."""

    resolved_run_root = Path(run_root)
    if not resolved_run_root.is_absolute():
        resolved_run_root = repo_root / resolved_run_root
    resolved_run_root.mkdir(parents=True, exist_ok=True)

    trace_path = write_trace_artifact(trace, repo_root, resolved_run_root / "00_trace.md")
    session_paths: list[Path] = []
    handoff_paths: list[Path] = []

    for index, (role_pass, session) in enumerate(zip(trace.passes, trace.sessions), start=1):
        next_role = trace.passes[index].role_name if index < len(trace.passes) else None
        session_path = resolved_run_root / f"{index:02d}_{role_pass.role_name}_session.md"
        session_text = _render_role_session(
            trace=trace,
            role_pass=role_pass,
            session=session,
            repo_root=repo_root,
            source_task=source_task,
            next_role=next_role,
        )
        session_path.write_text(session_text, encoding="utf-8")
        session_paths.append(session_path)

        if next_role:
            next_session_path = resolved_run_root / f"{index + 1:02d}_{next_role}_session.md"
            handoff_path = resolved_run_root / f"{index:02d}_{role_pass.role_name}_to_{next_role}_handoff.md"
            handoff_text = _render_handoff(
                trace=trace,
                role_pass=role_pass,
                session=session,
                repo_root=repo_root,
                source_task=source_task,
                session_path=session_path,
                next_session_path=next_session_path,
                next_role=next_role,
            )
            handoff_path.write_text(handoff_text, encoding="utf-8")
            handoff_paths.append(handoff_path)

    return ExecutionBundle(
        run_root=resolved_run_root,
        trace_path=trace_path,
        session_paths=tuple(session_paths),
        handoff_paths=tuple(handoff_paths),
    )


def find_session_path(run_root: str | Path, role_name: str) -> Path:
    """Locate one generated role-session packet inside a run bundle."""

    resolved_run_root = Path(run_root)
    matches = sorted(resolved_run_root.glob(f"*_{role_name}_session.md"))
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected exactly one session for role {role_name!r} in {resolved_run_root}, found {len(matches)}"
        )
    return matches[0]


def record_session_update(
    session_path: str | Path,
    *,
    status: str,
    operator: str,
    summary: str,
    artifacts: Sequence[str] = (),
    next_action: str | None = None,
    note: str | None = None,
) -> Path:
    """Transition one role-session packet and append an explicit status delta."""

    resolved_session_path = Path(session_path)
    original = resolved_session_path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(original)
    updated_frontmatter = _replace_frontmatter_field(frontmatter, "status", status)
    updated_frontmatter = _replace_frontmatter_field(updated_frontmatter, "updated", _iso_now())

    lines = [
        body.rstrip(),
        "",
        f"## Status Update — {_iso_now()}",
        "",
        f"- status: {status}",
        f"- operator: {operator}",
        f"- summary: {summary}",
    ]
    if artifacts:
        lines.append("- artifacts:")
        lines.extend(f"  - {artifact}" for artifact in artifacts)
    if next_action:
        lines.append(f"- next_action: {next_action}")
    if note:
        lines.append(f"- note: {note}")

    updated = f"---\n{updated_frontmatter}\n---\n" + "\n".join(lines).rstrip() + "\n"
    resolved_session_path.write_text(updated, encoding="utf-8")
    return resolved_session_path


def record_bundle_session_update(
    run_root: str | Path,
    role_name: str,
    *,
    status: str,
    operator: str,
    summary: str,
    artifacts: Sequence[str] = (),
    next_action: str | None = None,
    note: str | None = None,
) -> Path:
    """Convenience wrapper to update one role inside a generated execution bundle."""

    session_path = find_session_path(run_root, role_name)
    return record_session_update(
        session_path,
        status=status,
        operator=operator,
        summary=summary,
        artifacts=artifacts,
        next_action=next_action,
        note=note,
    )


def retire_task_packet(
    task_path: str | Path,
    *,
    status: str,
    operator: str,
    summary: str,
    artifacts: Sequence[str] = (),
    next_action: str | None = None,
    note: str | None = None,
    destination_dir: str | Path | None = None,
) -> TaskRetirement:
    """Update one task packet with a completion record and move it to the completed lane."""

    resolved_task_path = Path(task_path)
    if not resolved_task_path.exists():
        raise FileNotFoundError(f"Task path does not exist: {resolved_task_path}")

    timestamp = _iso_now()
    original = resolved_task_path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(original)
    updated_frontmatter = _replace_frontmatter_field(frontmatter, "status", status)
    updated_frontmatter = _replace_frontmatter_field(updated_frontmatter, "updated", timestamp)
    updated_frontmatter = _replace_frontmatter_field(updated_frontmatter, "completed_by", operator)

    lines = [
        body.rstrip(),
        "",
        f"## Completion Record — {timestamp}",
        "",
        f"- status: {status}",
        f"- operator: {operator}",
        f"- summary: {summary}",
    ]
    if artifacts:
        lines.append("- artifacts:")
        lines.extend(f"  - {artifact}" for artifact in artifacts)
    if next_action:
        lines.append(f"- next_action: {next_action}")
    if note:
        lines.append(f"- note: {note}")

    updated = f"---\n{updated_frontmatter}\n---\n" + "\n".join(lines).rstrip() + "\n"

    if destination_dir is None:
        if resolved_task_path.parent.name == "completed":
            resolved_destination_dir = resolved_task_path.parent
        else:
            resolved_destination_dir = resolved_task_path.parent / "completed"
    else:
        resolved_destination_dir = Path(destination_dir)
    resolved_destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = resolved_destination_dir / resolved_task_path.name

    if destination_path != resolved_task_path and destination_path.exists():
        raise FileExistsError(f"Destination task already exists: {destination_path}")

    resolved_task_path.write_text(updated, encoding="utf-8")
    if destination_path != resolved_task_path:
        resolved_task_path.replace(destination_path)

    return TaskRetirement(
        source_path=resolved_task_path,
        destination_path=destination_path,
        status=status,
    )


def _render_role_session(
    *,
    trace: SequentialTrace,
    role_pass: RolePass,
    session: RoleSession,
    repo_root: Path,
    source_task: str | None,
    next_role: str | None,
) -> str:
    created = _iso_now()
    lines = [
        "---",
        "type: role_session",
        "template: ROLE_SESSION",
        f"created: {created}",
        "status: PLANNED",
        f"workstream: {trace.workstream.value}",
        f"role: {role_pass.role_name}",
        f"objective: {trace.objective}",
    ]
    if source_task:
        lines.append(f"source_task: {source_task}")
    if next_role:
        lines.append(f"next_role: {next_role}")
    lines.extend(
        [
            "---",
            "",
            f"# Role Session: {role_pass.role_name}",
            "",
            "## Role",
            "",
            role_pass.role_name,
            "",
            "## Purpose",
            "",
            role_pass.purpose,
            "",
            "## Source Task / Objective",
            "",
            f"- objective: {trace.objective}",
        ]
    )
    if source_task:
        lines.append(f"- source_task: {source_task}")
    lines.extend(
        [
            "",
            "## Required Reads",
            "",
        ]
    )
    for target in session.load_targets:
        suffix = ""
        if not target.required:
            suffix = " [optional]"
        elif not target.exists(repo_root):
            suffix = " [missing]"
        lines.append(f"- {target.label}: {target.path}{suffix}")
    lines.extend(
        [
            "",
            "## Expected Output",
            "",
            f"- Produce the {role_pass.role_name} pass for the bounded `{trace.workstream.value}` objective.",
            "- Preserve provenance explicitly if any cross-role judgment is made.",
            "- Update only the artifacts that the governing task or lane actually permits.",
            "",
            "## Next Target",
            "",
            f"- next_role: {next_role or 'none'}",
            "",
            "## Notes",
            "",
            "- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_handoff(
    *,
    trace: SequentialTrace,
    role_pass: RolePass,
    session: RoleSession,
    repo_root: Path,
    source_task: str | None,
    session_path: Path,
    next_session_path: Path,
    next_role: str,
) -> str:
    created = _iso_now()
    lines = [
        "---",
        "type: handoff",
        "template: HANDOFF",
        f"created: {created}",
        "status: PLANNED",
        f"from: {role_pass.role_name}",
        f"to: {next_role}",
        f"objective: {trace.objective}",
        "---",
        "",
        f"# Handoff: {role_pass.role_name} to {next_role}",
        "",
        "## From",
        "",
        role_pass.role_name,
        "",
        "## To",
        "",
        next_role,
        "",
        "## What was completed",
        "",
        f"- A planned `{trace.workstream.value}` session scaffold was generated for `{role_pass.role_name}`.",
        f"- Session artifact: {_relative_display(session_path, repo_root)}",
        "",
        "## What remains",
        "",
        f"- Perform the actual `{next_role}` pass for `{trace.objective}`.",
        "- Decide whether any generated scaffold must be tightened before real execution.",
        "",
        "## Exact artifacts to read",
        "",
        f"- {_relative_display(session_path, repo_root)}",
        f"- {_relative_display(next_session_path, repo_root)}",
    ]
    if source_task:
        lines.append(f"- {source_task}")
    for target in session.load_targets:
        lines.append(f"- {target.path}")
    lines.extend(
        [
            "",
            "## Risks / warnings",
            "",
            "- This is a machine-generated handoff packet; it does not replace independent role judgment.",
            "- Shared root projections remain optional context, not source continuity.",
            "",
            "## Requested next action",
            "",
            f"- Execute the `{next_role}` role pass or refine its packet before execution.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect the active ION sequential kernel router.")
    parser.add_argument(
        "workstream",
        choices=[workstream.value for workstream in Workstream],
        help="Which sequential workstream to render.",
    )
    parser.add_argument("objective", help="Bounded objective for the rendered trace.")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root containing the active ION root.",
    )
    parser.add_argument(
        "--directive",
        action="append",
        default=[],
        help="Directive or artifact paths to inject into every role pass.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path for a durable rendered trace artifact.",
    )
    parser.add_argument(
        "--source-task",
        help="Optional task packet or inbox artifact that the trace is replaying or executing.",
    )
    parser.add_argument(
        "--execution-root",
        help="Optional directory for a generated per-pass execution scaffold bundle.",
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root) if args.repo_root else default_repo_root()
    router = SequentialKernelRouter.default(repo_root)
    trace = router.build_trace(
        Workstream(args.workstream),
        objective=args.objective,
        directive_paths=tuple(args.directive),
    )
    print(render_trace(trace, repo_root))
    if args.output:
        output_path = write_trace_artifact(trace, repo_root, args.output)
        print(f"\ntrace_written: {output_path}")
    if args.execution_root:
        bundle = write_execution_bundle(
            trace,
            repo_root,
            args.execution_root,
            source_task=args.source_task,
        )
        print(f"\nexecution_bundle_written: {bundle.run_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
