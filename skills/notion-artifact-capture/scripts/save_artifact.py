#!/usr/bin/env python3
"""Save an artifact to a bootstrapped Notion AI Output Library."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

from bootstrap_library import NotionAPI, REQUIRED_SCHEMA, default_config_path, verify_schema

MAX_RICH_TEXT_CHUNK = 2000


class CreatedPageVerificationError(RuntimeError):
    """A page was created, but its read-back could not be confirmed."""

    def __init__(self, created_page: dict[str, Any], message: str) -> None:
        super().__init__(message)
        self.page_id = created_page.get("id", "")
        self.page_url = created_page.get("url", "")


def rich_text(value: str) -> dict[str, list[dict[str, Any]]]:
    chunks = [value[index : index + MAX_RICH_TEXT_CHUNK] for index in range(0, len(value), MAX_RICH_TEXT_CHUNK)]
    return {"rich_text": [{"type": "text", "text": {"content": chunk}} for chunk in chunks]}


def title(value: str) -> dict[str, list[dict[str, Any]]]:
    return {"title": [{"type": "text", "text": {"content": value[:MAX_RICH_TEXT_CHUNK]}}]}


def load_config(path: Path) -> dict[str, Any]:
    try:
        config = json.loads(path.expanduser().read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Config not found: {path.expanduser()}. Run bootstrap_library.py first.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Config is not valid JSON: {path.expanduser()}") from exc
    data_source_id = config.get("data_source_id")
    if not isinstance(data_source_id, str) or not data_source_id:
        raise RuntimeError("Config does not contain a valid data_source_id")
    return config


def normalize_tags(values: list[str]) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for value in values:
        for candidate in value.split(","):
            cleaned = candidate.strip()
            key = cleaned.casefold()
            if cleaned and key not in seen:
                tags.append(cleaned[:100])
                seen.add(key)
    return tags


def assert_select_option(schema: dict[str, Any], property_name: str, value: str) -> None:
    prop = schema["properties"].get(property_name, {})
    options = prop.get(prop.get("type"), {}).get("options", [])
    names = {item.get("name") for item in options if isinstance(item, dict)}
    if value not in names:
        choices = ", ".join(sorted(name for name in names if isinstance(name, str)))
        raise RuntimeError(f"Unknown {property_name} option {value!r}. Available: {choices}")


def build_page_payload(
    *,
    data_source_id: str,
    schema: dict[str, Any],
    name: str,
    artifact_type: str,
    status: str,
    topic: str = "",
    summary: str = "",
    source_url: str = "",
    file_path: str = "",
    tags: list[str] | None = None,
    notes: str = "",
    markdown: str = "",
    today: str | None = None,
) -> dict[str, Any]:
    verify_schema(schema)
    assert_select_option(schema, "Type", artifact_type)
    assert_select_option(schema, "Status", status)
    current_date = today or date.today().isoformat()
    properties: dict[str, Any] = {
        "Name": title(name),
        "Type": {"select": {"name": artifact_type}},
        "Status": {"select": {"name": status}},
        "Created": {"date": {"start": current_date}},
        "Updated": {"date": {"start": current_date}},
    }
    optional_values = {
        "Topic": topic,
        "Summary": summary,
        "File Path": file_path,
        "Notes": notes,
    }
    for property_name, value in optional_values.items():
        if value:
            properties[property_name] = rich_text(value)
    if source_url:
        properties["Source URL"] = {"url": source_url}
    normalized_tags = normalize_tags(tags or [])
    if normalized_tags:
        properties["Tags"] = {"multi_select": [{"name": item} for item in normalized_tags]}
    payload: dict[str, Any] = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "properties": properties,
    }
    if markdown:
        payload["markdown"] = markdown
    return payload


def extract_page_title(page: dict[str, Any]) -> str:
    title_items = page.get("properties", {}).get("Name", {}).get("title", [])
    return "".join(item.get("plain_text", "") for item in title_items if isinstance(item, dict))


def save_artifact(api: NotionAPI, config: dict[str, Any], **artifact: Any) -> dict[str, Any]:
    data_source_id = config["data_source_id"]
    schema = api.request("GET", f"/data_sources/{data_source_id}")
    payload = build_page_payload(data_source_id=data_source_id, schema=schema, **artifact)
    created = api.request("POST", "/pages", payload)
    page_id = created.get("id")
    if not isinstance(page_id, str) or not page_id:
        raise RuntimeError("Notion returned no page ID")
    try:
        verified = api.request("GET", f"/pages/{page_id}")
    except RuntimeError as exc:
        raise CreatedPageVerificationError(
            created,
            "Notion created the page, but read-back failed. Inspect the reported page before retrying.",
        ) from exc
    expected_name = artifact["name"][:MAX_RICH_TEXT_CHUNK]
    if extract_page_title(verified) != expected_name:
        raise CreatedPageVerificationError(
            created,
            "Notion created the page, but its read-back title did not match. Inspect the reported page before retrying.",
        )
    return verified


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument(
        "--type",
        dest="artifact_type",
        default="Other",
        choices=["Research", "Report", "Draft", "Reference", "Project Artifact", "Other"],
    )
    parser.add_argument(
        "--status",
        default="Saved",
        choices=["Saved", "Draft", "Needs Review", "Published", "Archived"],
    )
    parser.add_argument("--topic", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--file-path", default="")
    parser.add_argument("--tag", action="append", default=[], help="Repeat or pass comma-separated tags")
    parser.add_argument("--notes", default="")
    parser.add_argument("--markdown-file", type=Path, help="UTF-8 Markdown to use as the Notion page body")
    parser.add_argument("--config", type=Path, default=default_config_path())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        token = os.environ.get("NOTION_API_KEY", "")
        if not token:
            raise RuntimeError("NOTION_API_KEY is not set")
        config = load_config(args.config)
        markdown = ""
        file_path = args.file_path
        if args.markdown_file:
            markdown_path = args.markdown_file.expanduser().resolve()
            markdown = markdown_path.read_text(encoding="utf-8")
            if not file_path:
                file_path = str(markdown_path)
        page = save_artifact(
            NotionAPI(token),
            config,
            name=args.name,
            artifact_type=args.artifact_type,
            status=args.status,
            topic=args.topic,
            summary=args.summary,
            source_url=args.source_url,
            file_path=file_path,
            tags=args.tag,
            notes=args.notes,
            markdown=markdown,
        )
        print(f"NOTION_ARTIFACT_SAVE=PASS name={args.name}")
        print(f"page_id={page['id']}")
        if page.get("url"):
            print(f"url={page['url']}")
        return 0
    except CreatedPageVerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("NOTION_ARTIFACT_SAVE=CREATED_UNVERIFIED", file=sys.stderr)
        if exc.page_id:
            print(f"page_id={exc.page_id}", file=sys.stderr)
        if exc.page_url:
            print(f"url={exc.page_url}", file=sys.stderr)
        return 2
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
