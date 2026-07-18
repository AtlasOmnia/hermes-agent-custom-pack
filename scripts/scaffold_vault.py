#!/usr/bin/env python3
"""Create a minimal Hermes-friendly Obsidian vault scaffold safely."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT_DIRS = (
    "Daily",
    "Decisions",
    "Projects",
    "People",
    "Profiles",
    "Shared",
    "System/Assistant",
    "Inbox",
    "Templates",
)

FILES = {
    "System/Assistant/README.md": """# Assistant Knowledge Map

This note defines where durable information belongs and who owns each area.

## Routing

| Information | Destination |
|---|---|
| Compact universal facts and preferences | Hermes memory |
| Exact prior conversations and task outcomes | Hermes session search |
| Canonical documents and project state | Obsidian vault |
| Reusable procedures | Hermes skills |
| Temporary scheduled data | Cache or cron output |

## Ownership

| Area | Owner | Other profiles |
|---|---|---|
| Shared/ | coordinator | Read/write by explicit convention |
| Profiles/<name>/ | named profile | Read only unless delegated |
| Projects/ | project owner | Read; write by project convention |
| Daily/ | coordinator | Append links; avoid competing rewrites |

## Safety

- Do not store credentials or secret-bearing files in the vault.
- Read before editing and verify after writing.
- Keep private and work domains separated when required.
""",
    "System/Assistant/environment.md": """# Environment

Stable, non-secret environment documentation.

## Systems

- Add operating systems, tools, and service roles here.

## Known Constraints

- Add durable constraints, not temporary incidents.

## Verification

- Last verified: YYYY-MM-DD
- Verification method: describe the live check
""",
    "System/Assistant/issues-fixes.md": """# Issues and Fixes

Record durable troubleshooting lessons. Convert recurring executable workflows into Hermes skills.

## Entry Template

### YYYY-MM-DD — Short issue name

- Symptom:
- Root cause:
- Fix:
- Verification:
- Related skill or project:
""",
    "Templates/Daily.md": """---
date: {{date}}
type: daily
tags: [daily]
---

# {{date}}

## Priorities

## Schedule

## Log

## Decisions

## Wins

## Carry Forward
""",
    "Templates/Decision.md": """---
date: {{date}}
type: decision
status: proposed
---

# Decision: {{title}}

## Context

## Options Considered

## Decision

## Evidence

## Consequences

## Owner

## Review Date
""",
    "Templates/Project.md": """---
type: project
status: active
owner: {{owner}}
last_verified: {{date}}
---

# {{project}}

## Objective

## Current State

## Decisions

## Next Actions

## Risks and Blockers

## Sources and Artifacts

## History
""",
    ".gitignore": """# Secrets and local environment
.env
*.pem
*.key

# Obsidian volatile workspace state
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/workspaces.json

# Operating-system noise
.DS_Store
Thumbs.db
""",
}


def is_link_or_reparse(path: Path) -> bool:
    """Detect POSIX symlinks and Windows reparse points such as junctions."""
    if path.is_symlink():
        return True
    if os.name != "nt" or not path.exists():
        return False
    attributes = getattr(os.lstat(path), "st_file_attributes", 0)
    return bool(attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT


def canonical_vault_path(vault: Path) -> Path:
    """Canonicalize ancestor aliases while rejecting a linked vault root."""
    raw = Path(os.path.abspath(vault.expanduser()))
    expected = Path(os.path.realpath(raw.parent)) / raw.name
    actual = Path(os.path.realpath(raw))
    if raw.exists() and actual != expected:
        raise ValueError(f"Vault root must not redirect through a link or junction: {raw}")
    return expected


def reject_managed_symlink(vault: Path, target: Path) -> None:
    """Refuse writes through symlinks or junction-like path redirection."""
    target_real = Path(os.path.realpath(target))
    try:
        inside = os.path.commonpath((str(vault), str(target_real))) == str(vault)
    except ValueError:
        inside = False
    if not inside:
        raise ValueError(f"Managed path escapes vault through a symlink or junction: {target}")

    current = vault
    for part in target.relative_to(vault).parts:
        current = current / part
        if is_link_or_reparse(current):
            raise ValueError(f"Managed path must not contain a symlink or junction: {current}")


def scaffold(vault: Path, *, dry_run: bool = False, force: bool = False) -> dict[str, list[str]]:
    vault = canonical_vault_path(vault)
    result: dict[str, list[str]] = {
        "directories": [],
        "created": [],
        "overwritten": [],
        "skipped": [],
        "would-create": [],
        "would-overwrite": [],
    }

    for rel in ROOT_DIRS:
        target = vault / rel
        reject_managed_symlink(vault, target)
        if dry_run:
            if not target.exists():
                result["directories"].append(str(target))
        else:
            target.mkdir(parents=True, exist_ok=True)
            result["directories"].append(str(target))

    for rel, content in FILES.items():
        target = vault / rel
        reject_managed_symlink(vault, target)
        existed = target.exists()
        if existed and not force:
            status = "skip"
        elif dry_run:
            status = "would-overwrite" if existed else "would-create"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            status = "overwritten" if existed else "created"
        result["skipped" if status == "skip" else status].append(str(target))

    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path, help="Obsidian vault root")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite managed starter files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = scaffold(args.vault, dry_run=args.dry_run, force=args.force)
    print(f"Vault: {args.vault.expanduser().resolve()}")
    for key in ("directories", "created", "overwritten", "skipped", "would-create", "would-overwrite"):
        values = result[key]
        if values:
            print(f"{key}: {len(values)}")
            for value in values:
                print(f"  - {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
