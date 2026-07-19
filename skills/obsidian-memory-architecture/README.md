# Obsidian Memory Architecture for Hermes Agent

A modern, filesystem-first architecture for using Obsidian as Hermes Agent's durable knowledge layer.

![Obsidian Memory Architecture routes compact facts, session history, canonical documents, reusable procedures, and scheduled collection to the right system](https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/assets/obsidian-memory-architecture.png)

This project grew from the Reddit guide [How I use Obsidian as the long-term memory backbone for my AI assistant](https://www.reddit.com/r/hermesagent/comments/1stz6gd/how_i_use_obsidian_as_the_longterm_memory/). The original three-tier idea remains useful, but Hermes has evolved: it now has bounded built-in memory, searchable session history, optional memory-provider plugins, skill lifecycle tooling, and substantially richer cron jobs.

The updated design gives each system one job:

- Hermes memory: compact facts and preferences
- Optional memory providers: deeper fact/entity recall
- `session_search`: exact prior conversations and task outcomes
- Obsidian: canonical documents, project state, decisions, and daily timelines
- Skills: reusable procedures
- Cron/scripts: scheduled collection and transient state

The result is less duplication, less prompt bloat, and a vault that remains useful without the agent.

## Contents

- `SKILL.md` — installable Hermes skill
- `scripts/scaffold_vault.py` — non-destructive cross-platform scaffold
- `templates/` — daily, decision, project, and ownership-map templates
- `tests/test_scaffold.py` — smoke tests for idempotence and overwrite safety

## Install the skill

After this repository is published, install it from its raw GitHub URL:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/obsidian-memory-architecture/SKILL.md
```

That installs the core skill definition. Clone the repository when you also want the scaffold script, templates, and tests:

```bash
git clone https://github.com/AtlasOmnia/hermes-agent-custom-pack.git
cd hermes-agent-custom-pack/skills/obsidian-memory-architecture
```

Or copy this repository into your local skill library:

```bash
mkdir -p ~/.hermes/skills/note-taking/obsidian-memory-architecture
cp -R SKILL.md scripts templates ~/.hermes/skills/note-taking/obsidian-memory-architecture/
```

Start a new Hermes session, then load it explicitly if needed:

```text
/skill obsidian-memory-architecture
```

## Scaffold a vault

Preview first:

```bash
python3 scripts/scaffold_vault.py --vault "$HOME/Documents/Obsidian Vault" --dry-run
```

Create missing folders and starter files:

```bash
python3 scripts/scaffold_vault.py --vault "$HOME/Documents/Obsidian Vault"
```

The script never overwrites existing files unless `--force` is supplied. Set the path for Hermes in the environment used to launch it:

```bash
export OBSIDIAN_VAULT_PATH="$HOME/Documents/Obsidian Vault"
```

If you persist that value in a Hermes `.env`, edit the file deliberately; do not paste secrets into prompts or commit the `.env` file.

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 scripts/scaffold_vault.py --vault /tmp/hermes-obsidian-demo --dry-run
```

Validate the skill before publication:

```bash
python3 scripts/validate_skill.py
```

After installation, Hermes can also audit the registered copy:

```bash
hermes skills audit obsidian-memory-architecture --deep
```

`hermes skills inspect` resolves registry identifiers and remote sources; current releases do not accept `./SKILL.md` as a local source.

## Design notes

### Why not inject the whole vault?

Large static context increases cost and decreases relevance. Hermes should search the vault and read the smallest useful set of notes on demand.

### Why keep session history separate?

Hermes already stores sessions in its searchable session database. Copying conversations into Obsidian creates duplicates that drift and wastes space. Promote only decisions, canonical state, or human-readable summaries.

### Why keep procedures in skills?

A procedure needs triggers, exact actions, pitfalls, and verification. Skills are designed for that. A note saying “we fixed it once” is not an executable workflow.

### Does this require a specific memory provider?

No. The architecture works with built-in Hermes memory alone or with any supported optional memory provider. Provider capabilities differ, so use `hermes memory status` and the current Hermes documentation rather than assuming a particular backend.

## Privacy

The sample files contain no personal data. Before publishing your own vault or derivative templates:

- remove names, addresses, internal hosts, and account identifiers;
- scan tracked files and Git history for secrets and PII;
- exclude `.env`, credentials, private attachments, and volatile workspace state;
- verify author/commit metadata;
- review every file from a clean clone.

## License

MIT. See `LICENSE`.
