#!/usr/bin/env python3
"""Validate the structure and safety declarations of a browser harness skill."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

REQUIRED_SECTIONS = (
    "## Overview",
    "## When to Use",
    "## Prerequisites",
    "## Execution Contract",
    "## Flow",
    "## Recovery and Abort Rules",
    "## Verification Evidence",
    "## Common Pitfalls",
    "## Verification Checklist",
)

OVERVIEW_FIELDS = (
    "Domain",
    "Start URL",
    "Success boundary",
    "Browser lane",
    "Last verified",
    "Expires",
    "Tested",
    "Risk class",
)

STEP_FIELDS = (
    "Precondition",
    "Action",
    "Primary target",
    "Stable fallback",
    "Visual fallback",
    "Wait for",
    "Expected checkpoint",
    "Failure signals",
    "Recovery",
    "Decision gate",
    "External side effect",
    "Skip allowed",
)

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
LOCAL_REF_RE = re.compile(r"(?<![A-Za-z0-9])@e\d+\b")
SECRET_RE = re.compile(
    r"AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{20,}|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{20,}"
)
PRIVATE_PATH_RE = re.compile(
    r"(?:/Users/[^/\s]+|/home/[^/\s]+|[A-Za-z]:[\\/]Users[\\/][^\\/\s]+)"
)
STEP_RE = re.compile(r"(?m)^### Step (\d+):\s+.+$")


def _frontmatter(content: str) -> tuple[str, str] | None:
    if not content.startswith("---\n"):
        return None
    marker = content.find("\n---\n", 4)
    if marker < 0:
        return None
    return content[4:marker], content[marker + 5 :]


def _field(body: str, name: str) -> str | None:
    match = re.search(rf"(?m)^- {re.escape(name)}:\s*(.+?)\s*$", body)
    return match.group(1).strip().strip("`") if match else None


def _parse_iso(value: str, label: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} must be an ISO date (YYYY-MM-DD)")
        return None


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read harness: {exc}"]

    parsed = _frontmatter(content)
    if parsed is None:
        return ["SKILL.md must start with closed YAML frontmatter at byte zero"]
    frontmatter, body = parsed

    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", frontmatter)
    desc_match = re.search(r"(?m)^description:\s*([^\n]+)$", frontmatter)
    name = name_match.group(1).strip().strip("\"'") if name_match else ""
    description = desc_match.group(1).strip().strip("\"'") if desc_match else ""
    if not NAME_RE.fullmatch(name):
        errors.append("name must be 1-64 lowercase letters, digits, or hyphens")
    if not description:
        errors.append("description is required")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"missing section: {section}")

    values: dict[str, str] = {}
    for field in OVERVIEW_FIELDS:
        value = _field(body, field)
        if value is None:
            errors.append(f"missing overview field: {field}")
        else:
            values[field] = value

    if "Domain" in values and not re.fullmatch(r"(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}", values["Domain"]):
        errors.append("Domain must be a hostname without scheme or path")
    if "Start URL" in values:
        start = values["Start URL"]
        if not re.match(r"^https://", start):
            errors.append("Start URL must use https://")
        elif "Domain" in values:
            host = re.match(r"^https://([^/:?#]+)", start)
            domain = values["Domain"].lower()
            if host and host.group(1).lower() not in {domain, f"www.{domain}"} and not host.group(1).lower().endswith(f".{domain}"):
                errors.append("Start URL host does not match Domain")

    verified = _parse_iso(values["Last verified"], "Last verified", errors) if "Last verified" in values else None
    expires = _parse_iso(values["Expires"], "Expires", errors) if "Expires" in values else None
    if verified and expires and expires < verified:
        errors.append("Expires cannot be earlier than Last verified")
    if values.get("Tested", "").lower() not in {"true", "false"}:
        errors.append("Tested must be true or false")
    if values.get("Risk class", "").lower() not in {"read-only", "reversible", "consequential"}:
        errors.append("Risk class must be read-only, reversible, or consequential")

    steps = list(STEP_RE.finditer(body))
    if not steps:
        errors.append("Flow must contain at least one '### Step N:' heading")
    else:
        numbers = [int(match.group(1)) for match in steps]
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append("step numbers must be consecutive starting at 1")
        for index, match in enumerate(steps):
            end = steps[index + 1].start() if index + 1 < len(steps) else body.find("\n## ", match.end())
            if end < 0:
                end = len(body)
            block = body[match.end() : end]
            for field in STEP_FIELDS:
                if _field(block, field) is None:
                    errors.append(f"Step {numbers[index]} missing field: {field}")
            decision = (_field(block, "Decision gate") or "").lower()
            side_effect = (_field(block, "External side effect") or "").lower()
            if decision not in {"true", "false"}:
                errors.append(f"Step {numbers[index]} Decision gate must be true or false")
            if side_effect not in {"true", "false"}:
                errors.append(f"Step {numbers[index]} External side effect must be true or false")
            if side_effect == "true" and decision != "true":
                errors.append(f"Step {numbers[index]} with an external side effect must be a decision gate")

    if LOCAL_REF_RE.search(content):
        errors.append("harness contains a session-local browser ref such as @e12")
    if SECRET_RE.search(content):
        errors.append("harness contains a credential-like value")
    if PRIVATE_PATH_RE.search(content):
        errors.append("harness contains a user-specific local path")
    if not re.search(r"(?im)^- Final side effect crossed:\s*(?:`)?false(?:`)?\s*$", body):
        errors.append("Verification Evidence must state 'Final side effect crossed: false'")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("harness", type=Path, help="Path to a generated harness SKILL.md")
    args = parser.parse_args(argv)
    errors = validate(args.harness)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"HARNESS_VALIDATION=PASS path={args.harness}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
