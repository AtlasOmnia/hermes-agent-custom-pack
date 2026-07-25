#!/usr/bin/env python3
"""Create and verify a generic Notion artifact library for Hermes Agent."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE = "https://api.notion.com/v1"
API_VERSION = "2026-03-11"
DEFAULT_TITLE = "AI Output Library"
REQUIRED_SCHEMA = {
    "Name": "title",
    "Type": "select",
    "Status": "select",
    "Topic": "rich_text",
    "Summary": "rich_text",
    "Source URL": "url",
    "File Path": "rich_text",
    "Created": "date",
    "Updated": "date",
    "Tags": "multi_select",
    "Notes": "rich_text",
}


class CreatedDatabaseVerificationError(RuntimeError):
    """A database was created, but bootstrap could not verify or record it."""

    def __init__(self, database_id: str, data_source_id: str, message: str) -> None:
        super().__init__(message)
        self.database_id = database_id
        self.data_source_id = data_source_id


def default_config_path() -> Path:
    hermes_home = Path(os.environ.get("HERMES_HOME", "~/.hermes")).expanduser()
    return hermes_home / "notion-artifact-capture.json"


def normalize_notion_id(value: str) -> str:
    """Extract a UUID from a raw ID or Notion URL and return dashed form."""
    compact_matches = re.findall(r"(?i)(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])", value)
    dashed_matches = re.findall(
        r"(?i)(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])",
        value,
    )
    matches = dashed_matches or compact_matches
    if not matches:
        raise ValueError("No Notion page ID was found in the supplied value")
    return str(uuid.UUID(matches[-1]))


def option(name: str, color: str = "default") -> dict[str, str]:
    return {"name": name, "color": color}


def initial_properties() -> dict[str, Any]:
    return {
        "Name": {"title": {}},
        "Type": {
            "select": {
                "options": [
                    option("Research", "blue"),
                    option("Report", "purple"),
                    option("Draft", "yellow"),
                    option("Reference", "green"),
                    option("Project Artifact", "orange"),
                    option("Other", "gray"),
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    option("Saved", "green"),
                    option("Draft", "yellow"),
                    option("Needs Review", "orange"),
                    option("Published", "blue"),
                    option("Archived", "gray"),
                ]
            }
        },
        "Topic": {"rich_text": {}},
        "Summary": {"rich_text": {}},
        "Source URL": {"url": {}},
        "File Path": {"rich_text": {}},
        "Created": {"date": {}},
        "Updated": {"date": {}},
        "Tags": {"multi_select": {}},
        "Notes": {"rich_text": {}},
    }


def build_create_payload(parent_page_id: str, title: str) -> dict[str, Any]:
    return {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "description": [
            {
                "type": "text",
                "text": {
                    "content": "Research, reports, drafts, references, and generated artifacts saved by Hermes Agent."
                },
            }
        ],
        "is_inline": True,
        "initial_data_source": {"properties": initial_properties()},
    }


class NotionAPI:
    def __init__(self, token: str) -> None:
        if not token.strip():
            raise ValueError("NOTION_API_KEY is empty")
        self.token = token.strip()

    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            f"{API_BASE}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": API_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            try:
                message = json.loads(detail).get("message", detail)
            except json.JSONDecodeError:
                message = detail
            raise RuntimeError(f"Notion API {exc.code}: {message}") from exc
        except URLError as exc:
            raise RuntimeError(f"Notion API connection failed: {exc.reason}") from exc


def extract_data_source_id(database: dict[str, Any]) -> str:
    sources = database.get("data_sources")
    if not isinstance(sources, list) or not sources or not isinstance(sources[0], dict):
        raise RuntimeError("Notion created a database but returned no initial data source ID")
    data_source_id = sources[0].get("id")
    if not isinstance(data_source_id, str) or not data_source_id:
        raise RuntimeError("Notion returned an invalid initial data source ID")
    return data_source_id


def verify_schema(data_source: dict[str, Any]) -> None:
    properties = data_source.get("properties")
    if not isinstance(properties, dict):
        raise RuntimeError("Notion data source response did not contain a property schema")
    errors: list[str] = []
    for name, expected_type in REQUIRED_SCHEMA.items():
        actual = properties.get(name, {}).get("type") if isinstance(properties.get(name), dict) else None
        if actual != expected_type:
            errors.append(f"{name}: expected {expected_type}, got {actual or 'missing'}")
    if errors:
        raise RuntimeError("Notion schema verification failed: " + "; ".join(errors))


def write_config(path: Path, config: dict[str, Any], *, force: bool = False) -> None:
    path = path.expanduser()
    if path.exists() and not force:
        raise FileExistsError(f"Config already exists: {path}. Use --force to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    if os.name != "nt":
        temporary.chmod(stat.S_IRUSR | stat.S_IWUSR)
    temporary.replace(path)


def bootstrap(
    api: NotionAPI,
    parent_page_id: str,
    title: str,
    config_path: Path,
    *,
    force: bool = False,
) -> dict[str, Any]:
    expanded_config_path = config_path.expanduser()
    if expanded_config_path.exists() and not force:
        raise FileExistsError(f"Config already exists: {expanded_config_path}. Use --force to replace it.")
    database = api.request("POST", "/databases", build_create_payload(parent_page_id, title))
    database_id = database.get("id")
    if not isinstance(database_id, str) or not database_id:
        raise RuntimeError("Notion returned no database ID")
    data_source_id = ""
    try:
        try:
            data_source_id = extract_data_source_id(database)
        except RuntimeError:
            # Some response projections omit the expanded data_sources list.
            # Retrieve the database once before treating the successful create as unusable.
            database = api.request("GET", f"/databases/{database_id}")
            data_source_id = extract_data_source_id(database)
        verified = api.request("GET", f"/data_sources/{data_source_id}")
        verify_schema(verified)
        config = {
            "version": 1,
            "api_version": API_VERSION,
            "database_title": title,
            "database_id": database_id,
            "data_source_id": data_source_id,
            "parent_page_id": parent_page_id,
        }
        write_config(expanded_config_path, config, force=force)
        return config
    except (RuntimeError, OSError) as exc:
        raise CreatedDatabaseVerificationError(
            database_id,
            data_source_id,
            "Notion created the database, but bootstrap could not verify or record it. Inspect the reported IDs before retrying.",
        ) from exc


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-page", required=True, help="Shared Notion parent page URL or page ID")
    parser.add_argument("--title", default=DEFAULT_TITLE, help=f"Database title (default: {DEFAULT_TITLE})")
    parser.add_argument("--config", type=Path, default=default_config_path(), help="Local destination config path")
    parser.add_argument("--force", action="store_true", help="Replace an existing local config file")
    parser.add_argument("--dry-run", action="store_true", help="Print the create payload without calling Notion")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        parent_page_id = normalize_notion_id(args.parent_page)
        if args.dry_run:
            print(json.dumps(build_create_payload(parent_page_id, args.title), indent=2))
            return 0
        token = os.environ.get("NOTION_API_KEY", "")
        if not token:
            raise RuntimeError("NOTION_API_KEY is not set")
        config = bootstrap(NotionAPI(token), parent_page_id, args.title, args.config, force=args.force)
        print(f"NOTION_LIBRARY_BOOTSTRAP=PASS title={config['database_title']}")
        print(f"database_id={config['database_id']}")
        print(f"data_source_id={config['data_source_id']}")
        print(f"config={args.config.expanduser()}")
        return 0
    except CreatedDatabaseVerificationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("NOTION_LIBRARY_BOOTSTRAP=CREATED_UNVERIFIED", file=sys.stderr)
        print(f"database_id={exc.database_id}", file=sys.stderr)
        if exc.data_source_id:
            print(f"data_source_id={exc.data_source_id}", file=sys.stderr)
        return 2
    except (FileExistsError, RuntimeError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
