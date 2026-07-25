import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from bootstrap_library import (
    API_VERSION,
    CreatedDatabaseVerificationError,
    REQUIRED_SCHEMA,
    bootstrap,
    build_create_payload,
    normalize_notion_id,
    verify_schema,
)
from save_artifact import CreatedPageVerificationError, build_page_payload, normalize_tags, save_artifact


class FakeAPI:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if not self.responses:
            raise AssertionError(f"Unexpected API call: {method} {path}")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def schema_response():
    return {
        "object": "data_source",
        "id": "22222222-2222-2222-2222-222222222222",
        "properties": {
            name: {"id": name, "name": name, "type": kind, kind: option_schema(name, kind)}
            for name, kind in REQUIRED_SCHEMA.items()
        },
    }


def option_schema(name, kind):
    if name == "Type":
        return {"options": [{"name": value} for value in ["Research", "Report", "Draft", "Reference", "Project Artifact", "Other"]]}
    if name == "Status":
        return {"options": [{"name": value} for value in ["Saved", "Draft", "Needs Review", "Published", "Archived"]]}
    return {}


class BootstrapTests(unittest.TestCase):
    def test_normalizes_raw_id_and_notion_url(self):
        expected = "11111111-1111-1111-1111-111111111111"
        self.assertEqual(normalize_notion_id(expected), expected)
        url = "https://www.notion.so/Workspace-11111111111111111111111111111111?pvs=4"
        self.assertEqual(normalize_notion_id(url), expected)

    def test_payload_uses_current_database_contract_and_generic_schema(self):
        payload = build_create_payload("11111111-1111-1111-1111-111111111111", "AI Output Library")
        self.assertEqual(payload["parent"]["type"], "page_id")
        self.assertTrue(payload["is_inline"])
        self.assertEqual(
            set(payload["initial_data_source"]["properties"]),
            set(REQUIRED_SCHEMA),
        )
        serialized = json.dumps(payload)
        self.assertNotIn("Atlas", serialized)
        self.assertNotIn("Hermes Megathreads", serialized)

    def test_bootstrap_creates_verifies_and_writes_config(self):
        created = {
            "object": "database",
            "id": "33333333-3333-3333-3333-333333333333",
            "data_sources": [{"id": "22222222-2222-2222-2222-222222222222"}],
        }
        api = FakeAPI([created, schema_response()])
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "capture.json"
            config = bootstrap(
                api,
                "11111111-1111-1111-1111-111111111111",
                "AI Output Library",
                config_path,
            )
            on_disk = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config, on_disk)
        self.assertEqual(config["api_version"], API_VERSION)
        self.assertEqual(api.calls[0][0:2], ("POST", "/databases"))
        self.assertEqual(api.calls[1][0:2], ("GET", "/data_sources/22222222-2222-2222-2222-222222222222"))

    def test_bootstrap_retrieves_database_when_create_response_omits_data_sources(self):
        created = {
            "object": "database",
            "id": "33333333-3333-3333-3333-333333333333",
        }
        retrieved = {
            **created,
            "data_sources": [{"id": "22222222-2222-2222-2222-222222222222"}],
        }
        api = FakeAPI([created, retrieved, schema_response()])
        with tempfile.TemporaryDirectory() as tmp:
            bootstrap(
                api,
                "11111111-1111-1111-1111-111111111111",
                "AI Output Library",
                Path(tmp) / "capture.json",
            )
        self.assertEqual(
            [call[0:2] for call in api.calls],
            [
                ("POST", "/databases"),
                ("GET", "/databases/33333333-3333-3333-3333-333333333333"),
                ("GET", "/data_sources/22222222-2222-2222-2222-222222222222"),
            ],
        )

    def test_bootstrap_refuses_to_replace_config_without_force(self):
        created = {
            "id": "33333333-3333-3333-3333-333333333333",
            "data_sources": [{"id": "22222222-2222-2222-2222-222222222222"}],
        }
        api = FakeAPI([created, schema_response()])
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "capture.json"
            config_path.write_text("{}", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                bootstrap(api, "11111111-1111-1111-1111-111111111111", "Library", config_path)
        self.assertEqual(api.calls, [])

    def test_schema_verification_rejects_missing_property(self):
        schema = schema_response()
        del schema["properties"]["Notes"]
        with self.assertRaisesRegex(RuntimeError, "Notes"):
            verify_schema(schema)

    def test_bootstrap_preserves_created_ids_when_schema_readback_fails(self):
        created = {
            "id": "33333333-3333-3333-3333-333333333333",
            "data_sources": [{"id": "22222222-2222-2222-2222-222222222222"}],
        }
        api = FakeAPI([created, RuntimeError("temporary timeout")])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(CreatedDatabaseVerificationError) as caught:
                bootstrap(
                    api,
                    "11111111-1111-1111-1111-111111111111",
                    "AI Output Library",
                    Path(tmp) / "capture.json",
                )
        self.assertEqual(caught.exception.database_id, created["id"])
        self.assertEqual(caught.exception.data_source_id, created["data_sources"][0]["id"])
        self.assertIn("before retrying", str(caught.exception))


class SaveTests(unittest.TestCase):
    def test_builds_typed_page_payload_and_omits_empty_fields(self):
        payload = build_page_payload(
            data_source_id="22222222-2222-2222-2222-222222222222",
            schema=schema_response(),
            name="Model research",
            artifact_type="Research",
            status="Saved",
            summary="Evidence-backed comparison",
            source_url="https://example.com/source",
            tags=["AI, Research", "research"],
            today="2026-07-25",
        )
        self.assertEqual(payload["parent"]["type"], "data_source_id")
        properties = payload["properties"]
        self.assertNotIn("Topic", properties)
        self.assertEqual(properties["Tags"]["multi_select"], [{"name": "AI"}, {"name": "Research"}])
        self.assertEqual(properties["Created"]["date"]["start"], "2026-07-25")

    def test_rich_text_is_chunked_without_data_loss(self):
        long_summary = "x" * 4500
        payload = build_page_payload(
            data_source_id="22222222-2222-2222-2222-222222222222",
            schema=schema_response(),
            name="Long report",
            artifact_type="Report",
            status="Saved",
            summary=long_summary,
            today="2026-07-25",
        )
        chunks = payload["properties"]["Summary"]["rich_text"]
        self.assertEqual("".join(item["text"]["content"] for item in chunks), long_summary)
        self.assertEqual([len(item["text"]["content"]) for item in chunks], [2000, 2000, 500])

    def test_rejects_unknown_live_select_option(self):
        with self.assertRaisesRegex(RuntimeError, "Unknown Type option"):
            build_page_payload(
                data_source_id="22222222-2222-2222-2222-222222222222",
                schema=schema_response(),
                name="Artifact",
                artifact_type="Invalid",
                status="Saved",
                today="2026-07-25",
            )

    def test_save_reads_schema_creates_page_and_verifies_title(self):
        created = {"id": "44444444-4444-4444-4444-444444444444"}
        verified = {
            "id": created["id"],
            "url": "https://www.notion.so/44444444444444444444444444444444",
            "properties": {"Name": {"title": [{"plain_text": "Artifact"}]}},
        }
        api = FakeAPI([schema_response(), created, verified])
        result = save_artifact(
            api,
            {"data_source_id": "22222222-2222-2222-2222-222222222222"},
            name="Artifact",
            artifact_type="Other",
            status="Saved",
            topic="",
            summary="",
            source_url="",
            file_path="",
            tags=[],
            notes="",
            markdown="# Artifact\n\nBody",
            today="2026-07-25",
        )
        self.assertEqual(result["id"], created["id"])
        self.assertEqual([call[0:2] for call in api.calls], [
            ("GET", "/data_sources/22222222-2222-2222-2222-222222222222"),
            ("POST", "/pages"),
            ("GET", "/pages/44444444-4444-4444-4444-444444444444"),
        ])
        self.assertEqual(api.calls[1][2]["markdown"], "# Artifact\n\nBody")

    def test_save_preserves_created_page_identity_when_readback_fails(self):
        created = {
            "id": "44444444-4444-4444-4444-444444444444",
            "url": "https://www.notion.so/44444444444444444444444444444444",
        }
        api = FakeAPI([schema_response(), created, RuntimeError("temporary timeout")])
        with self.assertRaises(CreatedPageVerificationError) as caught:
            save_artifact(
                api,
                {"data_source_id": "22222222-2222-2222-2222-222222222222"},
                name="Artifact",
                artifact_type="Other",
                status="Saved",
                topic="",
                summary="",
                source_url="",
                file_path="",
                tags=[],
                notes="",
                markdown="",
                today="2026-07-25",
            )
        self.assertEqual(caught.exception.page_id, created["id"])
        self.assertEqual(caught.exception.page_url, created["url"])
        self.assertIn("before retrying", str(caught.exception))

    def test_normalize_tags_is_ordered_and_case_insensitive(self):
        self.assertEqual(normalize_tags(["AI, Research", "research", "  Models  "]), ["AI", "Research", "Models"])


if __name__ == "__main__":
    unittest.main()
