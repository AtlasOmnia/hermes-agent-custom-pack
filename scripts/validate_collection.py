#!/usr/bin/env python3
"""Validate every Hermes skill package in this collection."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
RECOMMENDED_HEADINGS = (
    "## Overview",
    "## When to Use",
    "## Common Pitfalls",
    "## Verification Checklist",
)


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return ["must start with YAML frontmatter at byte zero"]
    marker = content.find("\n---\n", 4)
    if marker < 0:
        return ["frontmatter is not closed"]
    frontmatter = content[4:marker]
    body = content[marker + 5 :]
    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    description_match = re.search(r"(?m)^description:\s*([^\n]+)$", frontmatter)
    name = name_match.group(1).strip().strip("\"'") if name_match else ""
    description = description_match.group(1).strip().strip("\"'") if description_match else ""
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append("name must be 1-64 lowercase letters, digits, or hyphens")
    if name and path.parent.name != name:
        errors.append(f"directory name {path.parent.name!r} does not match skill name {name!r}")
    if not description:
        errors.append("description is required")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")
    if not body.strip():
        errors.append("skill body is empty")
    if len(content) > 100_000:
        errors.append("SKILL.md exceeds 100,000 characters")
    for heading in RECOMMENDED_HEADINGS:
        if heading not in body:
            errors.append(f"missing recommended heading: {heading}")
    return errors


def main() -> int:
    paths = sorted(SKILLS.glob("*/SKILL.md"))
    if not paths:
        print("ERROR: no skill packages found")
        return 1
    failures = 0
    for path in paths:
        errors = validate_skill(path)
        if errors:
            failures += 1
            for error in errors:
                print(f"ERROR: {path.relative_to(ROOT)}: {error}")
        else:
            print(f"SKILL_VALIDATION=PASS path={path.relative_to(ROOT)} chars={len(path.read_text(encoding='utf-8'))}")
    if failures:
        return 1
    print(f"COLLECTION_VALIDATION=PASS skills={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
