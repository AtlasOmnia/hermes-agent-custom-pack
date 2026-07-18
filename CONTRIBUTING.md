# Contributing

Contributions that improve portability, verification, safety, or current Hermes compatibility are welcome.

## Adding a tool

Use the appropriate directory:

- `skills/<name>/` for installable Hermes skills;
- `plugins/<name>/` for Hermes plugins;
- `integrations/<name>/` for external-service or application bridges;
- `scripts/` for genuinely shared standalone utilities.

A skill should contain a valid `SKILL.md` with:

- lowercase hyphenated `name`;
- discovery-focused `description`;
- version, author, license, tags, and related skills where relevant;
- overview and trigger/counter-trigger guidance;
- exact operations;
- common pitfalls;
- verification checklist.

Keep the main skill concise. Move large supporting material into `references/`, `templates/`, or `scripts/`.

## Required checks

Run the tool's own tests and validator from its directory. For the Obsidian skill:

```bash
cd skills/obsidian-memory-architecture
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
```

Before opening a pull request:

1. Scan the complete change for credentials, personal paths, private IPs, account identifiers, logs, databases, screenshots, and generated artifacts.
2. Verify every command against a current Hermes installation or authoritative documentation.
3. Confirm the working tree remains unchanged after tests.
4. Describe provenance and adaptations clearly; do not relicense work you do not own.
5. Use placeholders in examples and keep secrets in environment files that are excluded from Git.

## Commit style

Use concise conventional commits when practical:

```text
feat: add a new Hermes skill
fix: correct vault path validation
docs: update installation instructions
```

## Publication boundary

Examples must be generic. Do not submit private vault content, employer data, customer records, personal medical/financial information, real credentials, private infrastructure, or internal profile configuration.
