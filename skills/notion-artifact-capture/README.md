# Notion Artifact Capture for Hermes Agent

Give “save to Notion” a dependable default destination without publishing anyone’s workspace IDs or credentials.

![Notion Artifact Capture setup and verified save workflow](https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/assets/notion-artifact-capture.svg)

This package creates a generic **AI Output Library** database beneath a Notion page the user owns and shares with their integration. Later saves fetch the live schema, create typed metadata plus optional Markdown, and read the page back before reporting success.

## What it includes

- `SKILL.md` — installable Hermes workflow
- `scripts/bootstrap_library.py` — creates and verifies the Notion database/schema
- `scripts/save_artifact.py` — saves and verifies artifacts
- `tests/test_notion_artifact_capture.py` — mocked API and payload tests

No third-party Python packages are required.

## One-time setup

1. Create a Notion integration at https://www.notion.so/my-integrations.
2. Store its token as `NOTION_API_KEY` in the environment used to launch Hermes. Never paste it into chat.
3. Create a blank Notion parent page.
4. Connect/share that page with the integration.
5. Give Hermes the page URL or ID.

The user-created parent keeps placement and sharing explicit across Notion connection types, even where workspace-level creation is available.

## Install

Install the agent instructions only:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/notion-artifact-capture/SKILL.md
```

For the scripts and tests, copy the full package:

```bash
git clone https://github.com/AtlasOmnia/hermes-agent-custom-pack.git
mkdir -p ~/.hermes/skills/productivity/notion-artifact-capture
cp -R hermes-agent-custom-pack/skills/notion-artifact-capture/. \
  ~/.hermes/skills/productivity/notion-artifact-capture/
```

Start a fresh session or run `/reload-skills`.

## Preview and bootstrap

```bash
cd ~/.hermes/skills/productivity/notion-artifact-capture

python3 scripts/bootstrap_library.py \
  --parent-page "https://www.notion.so/your-parent-page-id" \
  --dry-run

python3 scripts/bootstrap_library.py \
  --parent-page "https://www.notion.so/your-parent-page-id"
```

The verified destination is stored locally at:

```text
${HERMES_HOME:-~/.hermes}/notion-artifact-capture.json
```

That file contains object IDs, not the integration token. Bootstrap refuses to replace it unless `--force` is explicitly supplied.

## Save an artifact

```bash
python3 scripts/save_artifact.py \
  --name "Local model comparison" \
  --type Research \
  --status Saved \
  --topic "Local LLMs" \
  --summary "Evidence-backed comparison of three local models." \
  --source-url "https://example.com/primary-source" \
  --markdown-file "/absolute/path/to/report.md" \
  --tag "AI,Research"
```

The save script:

1. loads the local destination;
2. retrieves and validates the live data-source schema;
3. creates a typed Notion page using the current `data_source_id` parent contract;
4. fetches the created page by ID;
5. confirms the title and returns its URL.

## Schema

| Property | Type |
|---|---|
| Name | title |
| Type | select |
| Status | select |
| Topic | rich text |
| Summary | rich text |
| Source URL | URL |
| File Path | rich text |
| Created | date |
| Updated | date |
| Tags | multi-select |
| Notes | rich text |

Types: `Research`, `Report`, `Draft`, `Reference`, `Project Artifact`, `Other`.

Statuses: `Saved`, `Draft`, `Needs Review`, `Published`, `Archived`.

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 scripts/bootstrap_library.py \
  --parent-page 11111111-1111-1111-1111-111111111111 \
  --dry-run
```

Repository-wide:

```bash
python3 scripts/validate_collection.py
python3 scripts/test_collection.py
```

The tests mock Notion’s HTTP boundary; they do not create content in a real workspace.

## Privacy

The package contains no real Notion IDs, credentials, user paths, private hosts, or business-specific fallback destinations. Keep `NOTION_API_KEY` in the user’s local environment and never commit the generated destination config.

## License

MIT. See the repository `LICENSE`.
