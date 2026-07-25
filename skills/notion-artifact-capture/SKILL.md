---
name: notion-artifact-capture
description: Use when a user says “save to Notion” for research, reports, drafts, references, or generated artifacts and wants a reusable default destination. Bootstraps a generic Notion AI Output Library under a user-created shared parent page, saves typed metadata and optional Markdown, verifies every write through the live API, and keeps workspace IDs and credentials out of the published skill.
version: 1.0.0
author: AtlasOmnia
license: MIT
platforms:
  - linux
  - macos
  - windows
prerequisites:
  env_vars:
    - NOTION_API_KEY
metadata:
  hermes:
    tags:
      - notion
      - artifacts
      - research
      - knowledge-capture
      - productivity
      - hermes-agent
    related_skills:
      - notion
---
# Notion Artifact Capture

## Overview

Turn “save to Notion” into a reliable reusable workflow. On first use, the user creates one blank Notion parent page and shares it with a Notion integration. Hermes then creates a child database named **AI Output Library**, stores its destination IDs in a local non-secret config file, and uses that database for later research, reports, drafts, references, and project artifacts.

This skill extends the general `notion` skill:

- `notion` owns API mechanics and current Notion behavior;
- this skill owns the artifact schema, first-run bootstrap, destination convention, save defaults, and verification contract.

The published skill contains no workspace IDs, personal paths, credentials, private hosts, or business-specific schema. Each installation discovers and stores its own destination.

## When to Use

Use when:

- the user says “save to Notion” without naming a destination;
- research, reports, substantial drafts, source collections, or generated project artifacts should be easy to find later;
- a user wants one standard Notion table rather than deciding where every output belongs;
- a new installation needs to create and configure its output library;
- an existing save must be verified by reading the created page back through the API.

Do not use when:

- the user names another Notion page or database—honor the explicit destination;
- the content belongs in Hermes memory, session history, source control, or a task manager instead;
- the artifact contains secrets that should not be stored in Notion;
- the user asks only to edit an ordinary Notion page—use the general `notion` skill;
- a final external publish, payment, deletion, or irreversible action is involved without explicit authorization.

## Architecture

```text
User creates blank parent page
             │
             ▼
Shares page with Notion integration
             │
             ▼
bootstrap_library.py
  ├─ creates AI Output Library database
  ├─ creates typed property schema
  ├─ reads schema back from Notion
  └─ writes local destination config
             │
             ▼
“Save to Notion”
             │
             ▼
save_artifact.py
  ├─ loads local destination
  ├─ fetches live schema
  ├─ creates typed page + optional Markdown
  └─ reads page back and verifies title
```

The integration token stays in `NOTION_API_KEY`. The local config contains only Notion object IDs and the API version; it is not a credential and must never contain the token.

## Prerequisites

1. A Notion account and workspace.
2. A Notion integration created at https://www.notion.so/my-integrations.
3. The integration token stored as `NOTION_API_KEY` in the environment used to launch Hermes.
4. A blank parent page created by the user and connected/shared with the integration.
5. The bundled or installed `notion` skill available for current API guidance.

The one-time human step is deliberate: a user-created parent keeps placement and sharing explicit across Notion connection types, even where workspace-level creation is available. Everything beneath it can then be automated.

Never ask the user to paste an integration token into chat. Ask them to store it through their normal Hermes environment or credential workflow.

## Installation

A direct `SKILL.md` install provides the agent instructions:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/notion-artifact-capture/SKILL.md
```

For the bootstrap/save scripts and tests, clone the collection and copy the full package:

macOS/Linux:

```bash
git clone https://github.com/AtlasOmnia/hermes-agent-custom-pack.git
mkdir -p ~/.hermes/skills/productivity/notion-artifact-capture
cp -R hermes-agent-custom-pack/skills/notion-artifact-capture/. \
  ~/.hermes/skills/productivity/notion-artifact-capture/
```

Windows PowerShell:

```powershell
git clone https://github.com/AtlasOmnia/hermes-agent-custom-pack.git
$dest = Join-Path $HOME ".hermes\skills\productivity\notion-artifact-capture"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force ".\hermes-agent-custom-pack\skills\notion-artifact-capture\*" $dest
```

Start a new Hermes session or run `/reload-skills` after installation.

## First-Run Bootstrap

### 1. User creates the parent page

Ask the user to:

1. Create a blank Notion page, such as **AI Output Library** or **Hermes Outputs**.
2. Open the page’s sharing/connections controls.
3. Connect the Notion integration that owns `NOTION_API_KEY`.
4. Provide the page URL or page ID—not the token.

### 2. Preview the database payload

From the installed skill directory:

```bash
python3 scripts/bootstrap_library.py \
  --parent-page "https://www.notion.so/your-parent-page-id" \
  --dry-run
```

Dry-run mode does not call Notion and does not require the token.

### 3. Create and verify the library

```bash
python3 scripts/bootstrap_library.py \
  --parent-page "https://www.notion.so/your-parent-page-id"
```

By default, this writes destination metadata to:

```text
${HERMES_HOME:-~/.hermes}/notion-artifact-capture.json
```

The script refuses to replace an existing local config unless `--force` is supplied. Do not use `--force` until the user intends to change the default destination; creating another database accidentally is annoyingly easy and impressively unhelpful.

If Notion creates the database but verification or config writing fails, the script reports `CREATED_UNVERIFIED` with every available database/data-source ID and exits with code `2`. Inspect that object before retrying; do not create a second database blindly.

### Created schema

| Property | Type | Purpose |
|---|---|---|
| `Name` | title | Concise artifact title |
| `Type` | select | Research, Report, Draft, Reference, Project Artifact, Other |
| `Status` | select | Saved, Draft, Needs Review, Published, Archived |
| `Topic` | rich text | Short subject area |
| `Summary` | rich text | One-to-three-sentence overview |
| `Source URL` | URL | Primary canonical source |
| `File Path` | rich text | Local path when a file exists |
| `Created` | date | Initial save date |
| `Updated` | date | Last material update date |
| `Tags` | multi-select | Searchable labels |
| `Notes` | rich text | Provenance, caveats, extra links, or operational notes |

## Saving Artifacts

### Default classification

Choose defaults from the artifact’s actual state:

| Artifact | Type | Status |
|---|---|---|
| Completed research | Research | Saved |
| Formal analysis or briefing | Report | Saved |
| Work still being edited | Draft | Draft |
| Durable source/reference note | Reference | Saved |
| Build output, generated package, or project handoff | Project Artifact | Saved |
| Anything else | Other | Saved |
| Publicly released item | Best matching type | Published |

Do not label an unpublished draft as `Published`. Status is evidence, not aspiration.

### Save metadata only

```bash
python3 scripts/save_artifact.py \
  --name "Local model comparison" \
  --type Research \
  --status Saved \
  --topic "Local LLMs" \
  --summary "Evidence-backed comparison of three local models." \
  --source-url "https://example.com/primary-source" \
  --tag "AI" \
  --tag "Research" \
  --notes "Verified against vendor model cards."
```

### Save a Markdown artifact as the page body

```bash
python3 scripts/save_artifact.py \
  --name "Quarterly research brief" \
  --type Report \
  --status Saved \
  --topic "Market research" \
  --summary "Current findings and recommendations." \
  --markdown-file "/absolute/path/to/report.md" \
  --tag "Research,Briefing"
```

When `--markdown-file` is supplied, its resolved absolute path is also written to `File Path` unless `--file-path` explicitly overrides it.

### Multiple source links

`Source URL` accepts one URL. Put the primary canonical source there. Put additional URLs in the Markdown body or `Notes`; do not concatenate several URLs into one invalid URL property.

## Agent Operating Procedure

When the user says “save to Notion”:

1. Load the general `notion` skill for current API behavior.
2. Resolve the artifact:
   - confirm the final title and body;
   - use an existing local file when one is canonical;
   - preserve primary source and publication URLs;
   - do not invent metadata.
3. Locate the installed package scripts and local config.
4. If config is absent:
   - explain the one-time parent-page/share requirement;
   - bootstrap after the user supplies the page URL or ID;
   - never request the integration token in chat.
5. Fetch the live data-source schema before writing.
6. Map only properties that exist with the expected types.
7. If database creation omits the expanded data-source list, retrieve the new database once to resolve its initial data-source ID.
8. Create the page with `parent.data_source_id` under the current Notion API.
9. Read the created page back by ID and confirm its title.
10. Report the Notion page URL and row title.

If creation succeeds but read-back fails or the title differs, do not hide the successful side effect. Report `CREATED_UNVERIFIED` with the returned page ID/URL, tell the user to inspect that page, and do not retry automatically.

If the scripts are not installed, perform the same sequence using the API mechanics in the general `notion` skill. Never fall back to somebody else’s hardcoded database ID.

## Destination Changes and Schema Drift

The local config is a pointer, not proof that the destination still exists. Every save must fetch the live data source first.

If the live schema is missing or has changed types:

1. Stop before page creation.
2. Report the exact missing or mismatched properties.
3. Do not silently write to a different database found by title search.
4. Repair the schema only with the user’s approval, or bootstrap a new destination if requested.
5. Verify the repaired/new schema before retrying the save.

If the user intentionally wants another default destination, run bootstrap with a new shared parent and a separate `--config` path first. Replace the active config with `--force` only after the new destination is verified.

## Privacy and Security

- Never store `NOTION_API_KEY` in `SKILL.md`, destination config, command history, page properties, test fixtures, or Git.
- Do not print request headers or the token when diagnosing API failures.
- Treat Notion object IDs as local configuration, not portable defaults.
- Confirm that health, financial, employer, customer, family, or credential-adjacent material belongs in the selected workspace before saving.
- Do not upload local files automatically. `File Path` records a path; `--markdown-file` reads text into the page body. Binary/file upload is a separate explicit action.
- Before publishing a derivative skill, scan the tracked tree and reachable Git history for credentials, personal paths, private hosts, real workspace IDs, and PII.

## Common Pitfalls

1. **Publishing a personal database ID.** IDs belong in each user’s local config, never in the shared skill.
2. **Assuming an integration can create a root page.** Have the user create and share one parent page first.
3. **Installing only `SKILL.md` and expecting companion scripts.** Direct installation provides instructions; copy or clone the full package for scripts and tests.
4. **Using `database_id` to create rows on the current API.** Pages in a data source use `parent.data_source_id`.
5. **Trusting stale schema.** Fetch and validate the live data source before every write.
6. **Calling a create response verification.** Read the page back by its returned ID and compare the title.
7. **Putting several links into one URL property.** Use the primary link in `Source URL`; put extras in Notes/body.
8. **Overwriting destination config casually.** Bootstrap refuses replacement by default because a second “default” is not much of a default.
9. **Leaking the token in diagnostics.** Surface status and Notion’s message, never authorization headers.
10. **Saving everything.** Session chatter, tiny preferences, reusable procedures, and source-controlled files already have better homes.

## Verification Checklist

- [ ] The user created the parent page and shared it with the intended integration.
- [ ] `NOTION_API_KEY` is available to Hermes without being pasted into chat.
- [ ] Bootstrap dry-run produces a generic schema with no personal IDs.
- [ ] Bootstrap creates one child database and returns both database and data-source IDs.
- [ ] The data source is fetched and every required property/type is verified.
- [ ] Destination config is local, contains no token, and is not committed.
- [ ] Save fetches the live schema before creating the page.
- [ ] Artifact metadata matches the actual type and publication state.
- [ ] Optional Markdown remains complete and UTF-8 readable.
- [ ] The created page is fetched by ID and its title matches.
- [ ] The final response includes the Notion page URL or a precise blocker.

## Package Validation

From this package directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/bootstrap_library.py \
  --parent-page 11111111-1111-1111-1111-111111111111 \
  --dry-run
```

From the repository root:

```bash
python3 scripts/validate_collection.py
python3 scripts/test_collection.py
```

## References

- Notion API: Create a database: https://developers.notion.com/reference/create-a-database
- Notion API: Create a page: https://developers.notion.com/reference/post-page
- Notion API: Retrieve a data source: https://developers.notion.com/reference/retrieve-a-data-source
- Notion API versioning: https://developers.notion.com/reference/versioning
- Hermes skills documentation: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Hermes environment variables: https://hermes-agent.nousresearch.com/docs/reference/environment-variables
