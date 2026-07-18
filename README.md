# Hermes Agent Tools

An independent collection of practical skills, plugins, integrations, and utilities created by AtlasOmnia for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

These projects come from workflows that have been used, revised, and tested in real Hermes installations. Each tool should be installable on its own, documented with explicit verification steps, and safe to inspect before use.

This repository is unofficial and is not affiliated with or endorsed by Nous Research.

## Collection

### Skills

| Tool | Purpose | Status |
|---|---|---|
| [Obsidian Memory Architecture](skills/obsidian-memory-architecture/) | Use Obsidian as Hermes's durable knowledge and coordination layer without duplicating native memory, session history, or skills | Ready |

Additional skills and tools will be added only after they are generalized, tested, and cleared of private configuration.

## Install a skill

Inspect the skill before installing:

```bash
hermes skills inspect https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-tools/main/skills/obsidian-memory-architecture/SKILL.md
```

Install it directly:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-tools/main/skills/obsidian-memory-architecture/SKILL.md
```

Start a new Hermes session after installation so the skill registry is refreshed.

## Repository layout

```text
hermes-agent-tools/
├── skills/          # installable Hermes SKILL.md packages
├── plugins/         # Hermes plugins when added
├── integrations/    # external-service and application integrations
├── scripts/         # standalone utilities shared across tools
└── .github/         # validation and release workflows
```

A tool may include its own templates, scripts, references, tests, and documentation inside its directory.

## Quality standard

Every published tool should include:

- a clear trigger and scope;
- exact commands or tool guidance;
- pitfalls and recovery paths;
- verification steps;
- tests for executable code;
- no credentials, personal paths, private hosts, or internal business data;
- attribution and licensing appropriate to its sources.

Pull requests must pass the repository validation workflow. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Compatibility

The collection targets current Hermes Agent releases. Hermes evolves quickly, so each tool should link to the authoritative documentation it depends on and avoid hardcoding behavior that can be discovered from the live installation.

Authoritative Hermes documentation: https://hermes-agent.nousresearch.com/docs/

## License

Unless a tool directory states otherwise, original work in this repository is licensed under the MIT License. See [LICENSE](LICENSE).
