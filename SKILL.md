---
name: obsidian-memory-architecture
description: Use when designing, setting up, or maintaining an Obsidian vault as Hermes Agent's durable knowledge layer. Routes facts, conversation history, documents, procedures, and daily logs to the correct Hermes or vault system without duplicating everything into the prompt.
version: 1.0.0
author: AtlasOmnia
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags:
      - obsidian
      - memory
      - knowledge-management
      - daily-notes
      - hermes-agent
    related_skills:
      - obsidian
---
# Obsidian Memory Architecture for Hermes Agent

## Overview

Use Obsidian as Hermes Agent's human-readable, durable knowledge layer—not as a replacement for every native memory system. Modern Hermes already has bounded built-in memory, searchable session history, optional external memory providers, reusable skills, and scheduled jobs. The vault complements those systems by holding documents, decisions, project state, daily notes, and material that should remain useful even when Hermes is offline.

The central rule is simple:

> Store information according to how it must be retrieved and maintained, not according to where there happens to be room.

This skill extends the bundled `obsidian` skill. The bundled skill covers filesystem operations; this one defines architecture, routing, ownership, maintenance, and automation.

## When to Use

Use when:

- setting up an Obsidian vault for Hermes;
- deciding whether information belongs in memory, session history, a skill, or the vault;
- creating daily-note, project, decision, or troubleshooting workflows;
- coordinating multiple Hermes profiles through one vault;
- migrating an older `MEMORY.md`-heavy setup to current Hermes capabilities;
- reducing prompt bloat without losing durable knowledge.

Do not use for:

- ordinary note editing only—load the bundled `obsidian` skill;
- storing a single durable preference—use the active memory provider;
- recalling a past conversation—use `session_search` first;
- documenting a repeatable command sequence—create or update a skill;
- storing secrets, access tokens, or credentials—the vault is not a secret manager.

## Current Hermes Storage Model

Treat these as separate layers with different jobs:

| Layer | Best use | Retrieval | Avoid |
|---|---|---|---|
| Built-in `USER.md` / `MEMORY.md` | Tiny universal identity, preferences, and environment facts | Injected at session start | Project diaries, long procedures, raw logs |
| Optional memory provider | Durable facts, entities, preferences, and semantic recall | Automatically or through provider tools | Canonical documents and large artifacts |
| `session_search` | Exact prior conversation history and task outcomes | On-demand FTS search | Facts that must always be available |
| Obsidian vault | Canonical documents, decisions, project state, daily timeline, research | Filesystem search/read | Secrets and duplicated chat transcripts |
| Hermes skills | Reusable procedures, commands, pitfalls, verification | Loaded when relevant | One-time outcomes and personal diary entries |
| Cron output/cache | Scheduled collection and transient machine state | Job history or cache files | Permanent knowledge unless deliberately promoted |

Built-in memory is a bootstrap layer, not a database. Its configured limits can vary by installation, so inspect the live memory header or `hermes memory status`; never hardcode a migration percentage.

## Routing Decision

When new information appears, classify it in this order:

1. **Is it a reusable procedure?**
   - Put it in a Hermes skill.
2. **Is it an exact conversation outcome or something already captured in chat?**
   - Leave it in session history; use `session_search` later.
3. **Is it a compact fact or preference that should follow the user across sessions?**
   - Store it through the active memory provider.
4. **Is it a canonical document, decision, project status, research note, or human-readable timeline?**
   - Write it to Obsidian.
5. **Is it temporary scheduler state or fetched data?**
   - Keep it in a cache or cron output; promote only meaningful results.

Do not write the same content into all layers. A compact memory may point to a vault location, but it should not duplicate the full note.

## Recommended Vault Structure

Use a small generic scaffold and let real use create additional folders:

```text
Vault/
├── Daily/                  # YYYY-MM-DD.md
├── Decisions/              # durable decision records
├── Projects/               # canonical project state and documentation
├── People/                 # optional relationship/contact notes
├── Profiles/               # profile-owned context for multi-profile setups
├── Shared/                 # intentionally cross-profile references
├── System/
│   └── Assistant/
│       ├── README.md       # routing and ownership map
│       ├── environment.md  # stable, non-secret environment reference
│       └── issues-fixes.md # durable troubleshooting history
├── Inbox/                  # unclassified notes awaiting review
└── Templates/
    ├── Daily.md
    ├── Decision.md
    └── Project.md
```

Do not create dozens of speculative folders. Empty taxonomy is not knowledge.

## Vault Discovery and File Operations

Use `OBSIDIAN_VAULT_PATH` as the documented path convention. Resolve it before calling file tools; file tools do not expand shell variables.

```bash
python3 - <<'PY'
import os
from pathlib import Path
path = Path(os.environ.get("OBSIDIAN_VAULT_PATH", "~/Documents/Obsidian Vault")).expanduser()
print(path.resolve())
print("exists:", path.is_dir())
PY
```

After resolving the absolute path:

- `read_file` reads notes;
- `search_files(target="files")` lists notes;
- `search_files(target="content", file_glob="*.md")` searches note text;
- `patch` performs anchored edits;
- `write_file` creates or deliberately rewrites a complete note.

Read before editing. Read back after editing. For files that another app or sync service may modify, re-read after a short delay before declaring success.

## Daily Notes

Daily notes are a timeline, not a replacement for project documentation or session history.

Recommended sections:

```markdown
---
date: YYYY-MM-DD
type: daily
tags: [daily]
---

# YYYY-MM-DD

## Priorities

## Schedule

## Log

## Decisions

## Wins

## Carry Forward
```

Rules:

- Append timestamped operational events under `## Log`.
- Link durable decisions to a dedicated note under `Decisions/`.
- Move project detail to `Projects/<project>/`; leave a short link in the daily note.
- Record corrections transparently rather than silently rewriting history.
- Do not paste full conversations into daily notes when `session_search` already retains them.
- Do not let automation overwrite human edits. Prefer anchored patches or an atomic whole-file rewrite after reading the current file.

## Canonical Living Files

A living file is the source of truth for a topic whose current state matters more than its chronological history.

Good examples:

- project status and next actions;
- architecture and operating decisions;
- stable environment documentation without secrets;
- recovery notes for recurring failures;
- ownership and profile boundaries.

Every living file should answer:

1. What is this?
2. Who owns it?
3. What is current?
4. What evidence or source supports it?
5. When was it last verified?
6. Where is the historical detail?

Prefer updating one canonical note over creating `final-v2-really-final.md`—a venerable tradition best left in the past.

## Multi-Profile Vaults

Use one vault when profiles need shared people, decisions, and project links. Give each profile an owned directory and explicit read/write boundaries:

```text
Profiles/
├── coordinator/
├── developer/
└── researcher/
Shared/
Projects/
People/
Daily/
```

Put an ownership map in `System/Assistant/README.md`:

```markdown
| Area | Owner | Other profiles |
|---|---|---|
| Profiles/developer/ | developer | read only unless delegated |
| Profiles/researcher/ | researcher | read only unless delegated |
| Shared/ | coordinator | read/write by explicit convention |
| Daily/ | coordinator | append links; avoid competing rewrites |
```

Profiles should keep their native Hermes memories isolated unless the selected memory provider explicitly supports safe shared identities. The vault is a coordination surface, not permission enforcement; operating instructions must still define boundaries.

## Automation and Cron

Cron sessions start fresh. A scheduled job must have a self-contained prompt or an attached skill and should use an absolute `workdir` when project context matters.

Use deterministic scripts for deterministic collection:

- calendar/task API fetches;
- JSON diffs and ETag checks;
- daily-note scaffolding;
- cache rotation;
- health checks.

Use an agent only when interpretation or writing is required:

- summarizing changes;
- extracting decisions;
- drafting a briefing;
- reconciling ambiguous project state.

Prefer a two-stage pattern:

1. A script collects and normalizes data without an LLM.
2. An agent wakes only when a delta requires interpretation.

Never assume a cron session sees the current interactive conversation or its recalled memory. Attach this skill, set an appropriate `workdir`, and make the prompt self-contained. Verify jobs through `hermes cron list`, run history, output files, and the resulting vault note.

## Promotion and Maintenance

### Promote into the vault when

- a decision must be auditable;
- a project needs a canonical current-state document;
- information is too large for compact memory;
- a human should be able to browse it without Hermes;
- repeated troubleshooting events reveal a durable pattern.

### Promote into a skill when

- the same multi-step workflow succeeds more than once;
- commands, ordering, pitfalls, or verification matter;
- future agents should execute rather than merely remember.

### Keep only in session history when

- the detail is an exact conversation;
- it is a completed one-off task;
- it may be useful later but does not deserve permanent prompt or vault space.

### Weekly maintenance

- Process `Inbox/`.
- Review stale project status and unresolved decisions.
- Check for duplicate canonical notes.
- Convert recurring fixes into skills.
- Verify links from profile indexes and major project notes.

### Monthly maintenance

- Review living files for stale claims.
- Archive generated artifacts that do not belong in the knowledge vault.
- Check sync conflicts and backup health.
- Review permissions before sharing or publishing any vault content.

## Privacy, Security, and Backups

- Never store API keys, passwords, tokens, private keys, session cookies, or recovery codes in the vault.
- Treat synced vaults as data shared with the sync provider.
- Keep health, financial, employer, and family material in clearly separated private areas.
- Before putting a vault under Git, inspect the entire tracked tree and reachable history for secrets and PII.
- Exclude volatile Obsidian workspace state such as `.obsidian/workspace*.json` when appropriate.
- Maintain an independent backup. Sync is not backup; it is synchronized optimism.
- Test restoration, not merely backup creation.

## Migration from Older Three-Tier Setups

Older setups often treated large `MEMORY.md` and `USER.md` files as the primary memory database and promoted entries to Obsidian when a fixed percentage was reached. Modernize them as follows:

1. Run `hermes memory status` and identify the active built-in and optional provider layers.
2. Keep only universal bootstrap facts in built-in memory.
3. Move reusable procedures into skills, not vault memory files.
4. Use `session_search` for past conversations instead of copying transcripts into daily notes.
5. Put canonical documents and project state in Obsidian.
6. Keep timeline notes concise and link outward to decisions and projects.
7. Replace percentage-based migration with semantic routing and periodic review.
8. Use current Hermes cron features—attached skills, `workdir`, no-agent scripts, run history, and explicit delivery—instead of hand-editing job storage.

## Common Pitfalls

1. **Calling Obsidian “the memory system.”** It is one durable layer. Hermes memory and session search solve different retrieval problems.
2. **Duplicating everything.** Copies drift. Use a canonical note and compact pointers.
3. **Injecting the whole vault.** Search and read only relevant files on demand.
4. **Using daily notes as a dumping ground.** Link project and decision notes instead.
5. **Writing procedures into memory.** Procedures belong in skills with commands and verification.
6. **Assuming cron sees your session.** It starts fresh; prompts must be self-contained.
7. **Blind whole-file rewrites.** Read first, patch stable anchors, and verify after sync.
8. **Hardcoding one user's paths or profile names.** Resolve `OBSIDIAN_VAULT_PATH` and document local ownership separately.
9. **Committing a private vault casually.** Scan tracked files, history, metadata, and attachments before publication.
10. **Confusing sync with backup.** Test recovery from an independent copy.

## Verification Checklist

- [ ] `hermes memory status` identifies the actual active memory layers.
- [ ] `OBSIDIAN_VAULT_PATH` resolves to an existing directory.
- [ ] The vault has an ownership/routing map.
- [ ] Built-in memory contains only compact universal facts.
- [ ] Procedures live in skills rather than memory or daily notes.
- [ ] Prior conversations are retrieved through `session_search` before being duplicated.
- [ ] Daily-note automation preserves human edits.
- [ ] A created or edited note is read back from disk.
- [ ] Scheduled jobs are visible in `hermes cron list` and their output is verified.
- [ ] The vault contains no credentials or secret-bearing files.
- [ ] Backup restoration has been tested.

## References

- Hermes memory documentation: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory/
- Hermes memory providers: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers/
- Hermes cron documentation: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- Bundled Obsidian skill: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/note-taking/note-taking-obsidian
- Original field guide: https://www.reddit.com/r/hermesagent/comments/1stz6gd/how_i_use_obsidian_as_the_longterm_memory/
