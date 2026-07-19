# Hermes Agent Custom Pack

An independent pack of practical skills, plugins, integrations, scripts, and utilities created by AtlasOmnia for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

These projects come from workflows that have been used, revised, and tested in real Hermes installations. Each package should be installable on its own, documented with explicit verification steps, and safe to inspect before use.

This repository is unofficial and is not affiliated with or endorsed by Nous Research.

## Collection

### Skills

| Package | Purpose | Status |
|---|---|---|
| [Obsidian Memory Architecture](skills/obsidian-memory-architecture/) | Use Obsidian as Hermes's durable knowledge and coordination layer without duplicating native memory, session history, or skills | Ready |
| [Browser Harness Authoring](skills/browser-harness-authoring/) | Survey a repeatable website flow, save stable semantic targets and recovery paths, and verify a no-submit harness for later execution | Ready |

Additional packages will be added only after they are generalized, tested, and cleared of private configuration.

## Install a skill

Inspect a skill before installing it. For Browser Harness Authoring:

```bash
hermes skills inspect https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/browser-harness-authoring/SKILL.md
```

Install it directly:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/browser-harness-authoring/SKILL.md
```

Start a new Hermes session after installation so the skill registry is refreshed.

## Repository layout

```text
hermes-agent-custom-pack/
├── skills/          # installable Hermes SKILL.md packages
├── plugins/         # Hermes plugins when added
├── integrations/    # external-service and application integrations
├── scripts/         # standalone utilities shared across packages
└── .github/         # validation and release workflows
```

A package may include its own templates, scripts, references, tests, and documentation inside its directory.

## Quality standard

Every published package should include:

- a clear trigger and scope;
- exact commands or tool guidance;
- pitfalls and recovery paths;
- verification steps;
- tests for executable code;
- no credentials, personal paths, private hosts, or internal business data;
- attribution and licensing appropriate to its sources.

Pull requests must pass the repository validation workflow. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

Run all collection checks locally:

```bash
python3 scripts/validate_collection.py
python3 scripts/test_collection.py
```

## Compatibility

The collection targets current Hermes Agent releases. Hermes evolves quickly, so each package should link to the authoritative documentation it depends on and avoid hardcoding behavior that can be discovered from the live installation.

Authoritative Hermes documentation: https://hermes-agent.nousresearch.com/docs/

## License

Unless a package directory states otherwise, original work in this repository is licensed under the MIT License. See [LICENSE](LICENSE).
