#!/usr/bin/env python3
"""Validate this repository's Hermes SKILL.md without installing it."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def validate(path: Path = SKILL) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return ["SKILL.md must start with YAML frontmatter at byte zero"]
    parts = content.split("---", 2)
    if len(parts) != 3:
        return ["SKILL.md frontmatter is not closed"]
    frontmatter = parts[1]
    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*([^\n]+)$", frontmatter)
    name = name_match.group(1).strip().strip("\"'") if name_match else ""
    description = description_match.group(1).strip().strip("\"'") if description_match else ""
    if not re.fullmatch(r"[a-z0-9-]{1,64}", str(name)):
        errors.append("name must be 1-64 lowercase letters, digits, or hyphens")
    if not description:
        errors.append("description is required")
    elif len(str(description)) > 1024:
        errors.append("description exceeds 1024 characters")
    if not parts[2].strip():
        errors.append("skill body is empty")
    if len(content) > 100_000:
        errors.append("SKILL.md exceeds 100,000 characters")

    for heading in ("## Overview", "## When to Use", "## Common Pitfalls", "## Verification Checklist"):
        if heading not in parts[2]:
            errors.append(f"missing recommended heading: {heading}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"SKILL_VALIDATION=PASS path={SKILL} chars={len(SKILL.read_text(encoding='utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())