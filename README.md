# Hermes Agent Custom Pack

An independent pack of practical skills, plugins, integrations, scripts, and utilities created by AtlasOmnia for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

These projects come from workflows that have been used, revised, and tested in real Hermes installations. Each package should be installable on its own, documented with explicit verification steps, and safe to inspect before use.

This repository is unofficial and is not affiliated with or endorsed by Nous Research.

## Collection

### Skills

| Package | Purpose | Status |
|---|---|---|
| [apple-reminders](skills/apple-reminders/) | Apple Reminders via remindctl: add, list, complete | Ready |
| [application-security-review](skills/application-security-review/) | Review application repos for concrete security issues, especially trust-boundary failures, prompt-injection paths, auth/proxy mistakes, validation gaps, and risky dependencies | Ready |
| [browser-harness-authoring](skills/browser-harness-authoring/) | Survey a repeatable website flow, save stable semantic targets and recovery paths, and verify a no-submit harness for later execution | Ready |
| [claude-design](skills/claude-design/) | Design one-off HTML artifacts (landing, deck, prototype) | Ready |
| [codebase-inspection](skills/codebase-inspection/) | Inspect codebases w/ pygount: LOC, languages, ratios | Ready |
| [coding-worktree-recovery](skills/coding-worktree-recovery/) | Safely recover and continue interrupted or overlapping coding-agent work in a dirty Git checkout, including concurrent-writer arbitration, macOS cloud-synced/dataless checkout recovery, bounded handoff, and verified closeout | Ready |
| [computer-use](skills/computer-use/) | Drive the user''s desktop in the background — clicking, typing, | Ready |
| [content-style](skills/content-style/) | Writing content for r/hermesagent and similar communities — workshop posts, definitive model-variant guides, research-heavy megathreads, and community update posts | Ready |
| [cross-browser-typography-qa](skills/cross-browser-typography-qa/) | Diagnose and verify web typography rendering defects across Chromium, WebKit, and native Safari, including clipped glyphs, broken descenders, wrapping, font metrics, gradient text, and live-cache mismatches | Ready |
| [daily-news-digests](skills/daily-news-digests/) | Build and maintain local scheduled news/research digest scripts that collect fresh items from multiple public sources and save Markdown locally | Ready |
| [daily-note-wrapup](skills/daily-note-wrapup/) | Create, verify, and index daily wrap-up notes in an Obsidian vault | Ready |
| [destination-trip-planning](skills/destination-trip-planning/) | Research a specific destination/attraction, gather pricing/logistics, and build a themed trip itinerary tailored to the traveler's profile | Ready |
| [discord-connect](skills/discord-connect/) | Connect and configure Hermes on Discord — bot setup, intents, OAuth2 scopes, permissions, and gateway configuration | Ready |
| [dogfood](skills/dogfood/) | Exploratory QA of web apps: find bugs, evidence, reports | Ready |
| [domestic-trip-planning](skills/domestic-trip-planning/) | Research and plan a multi-day domestic trip — hotels, attraction tickets, itineraries, driving distances, local tips, and budget estimates. Covers the ground-level logistics that air-travel-planning and short-term-rental-search don't touch | Ready |
| [dynamic-content-extraction](skills/dynamic-content-extraction/) | Extract structured data from JavaScript-heavy sites where prices, text, or key fields don't appear in the standard accessibility tree. Covers browser_snapshot(full=true), TreeWalker text-node extraction, lazy-load handling, and React split-text recovery | Ready |
| [evidence-based-replies](skills/evidence-based-replies/) | Compare a person's claim to a cited paper or source, isolate what the evidence actually supports, and draft concise replies that correct overreach without sounding evasive | Ready |
| [external-model-review](skills/external-model-review/) | Run reproducible independent reviews of plans, architectures, major content, and release candidates through named external models; preserve provenance, verify findings against source, and amend artifacts safely | Ready |
| [github-auth](skills/github-auth/) | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login | Ready |
| [github-code-review](skills/github-code-review/) | Review PRs: diffs, inline comments via gh or REST | Ready |
| [github-issues](skills/github-issues/) | Create, triage, label, assign GitHub issues via gh or REST | Ready |
| [github-pr-workflow](skills/github-pr-workflow/) | GitHub PR lifecycle: branch, commit, open, CI, merge | Ready |
| [github-pre-push-gates](skills/github-pre-push-gates/) | Pre-push quality gates: immutable verification, privacy scanning, independent closeout review, and clean publication from divergent local history | Ready |
| [github-readme-maintenance](skills/github-readme-maintenance/) | Maintain GitHub repository docs (README, wiki-like community guides, contributor-facing indexes) with deterministic, low-noise workflows | Ready |
| [github-repo-management](skills/github-repo-management/) | Clone/create/fork repos; manage remotes, releases | Ready |
| [github-workflows](skills/github-workflows/) | Consolidate GitHub auth, repository management, PR lifecycle, issues, and code review workflows | Ready |
| [google-workspace](skills/google-workspace/) | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python | Ready |
| [hermes-agent](skills/hermes-agent/) | Configure, extend, or contribute to Hermes Agent | Ready |
| [hermes-agent-skill-authoring](skills/hermes-agent-skill-authoring/) | Author in-repo SKILL.md: frontmatter, validator, structure | Ready |
| [hermes-autoresearch-loops](skills/hermes-autoresearch-loops/) | Karpathy-style autoresearch loops for Hermes: autonomous propose→test→keep/revert cycles for config tuning, infra hardening, skill improvement, and post-update safety checks | Ready |
| [hermes-config-editing](skills/hermes-config-editing/) | Edit Hermes Agent configuration values — settings, compression, model config — with reliable patterns that work around security guards and CLI quirks | Ready |
| [hermes-context-optimization](skills/hermes-context-optimization/) | Optimize Hermes startup/context payloads, compression, tool-schema loading, memory/skill injection, and visual-context experiments | Ready |
| [hermes-desktop-plugins](skills/hermes-desktop-plugins/) | Write desktop app plugins that add UI panes and commands | Ready |
| [hermes-mnemosyne](skills/hermes-mnemosyne/) | Configure, troubleshoot, and operate the Mnemosyne memory provider for Hermes Agent | Ready |
| [hermes-nightly-self-check-decisions](skills/hermes-nightly-self-check-decisions/) | Record decisions from nightly self-check findings so behavior is consistent | Ready |
| [hermes-overnight-autonomy](skills/hermes-overnight-autonomy/) | Use for unattended Hermes continuity and watchdogs | Ready |
| [hermes-plugin-development](skills/hermes-plugin-development/) | Design, register, and debug Hermes plugins — hooks, YAML wiring, profile detection, token routing patterns | Ready |
| [hermes-plugin-evaluation](skills/hermes-plugin-evaluation/) | Evaluate third-party Hermes Agent plugins before installation: cost, licensing, required services, data flow, dependencies, and setup risk | Ready |
| [hermes-self-evaluation](skills/hermes-self-evaluation/) | Use when the user asks to evaluate, audit, or optimize Hermes itself — analyzing session history, skill library, costs, and architecture to identify improvements, automation opportunities, and system optimizations. Covers generating structured analyst prompts for external (stronger) models to review Hermes's own performance | Ready |
| [hermes-session-maintenance](skills/hermes-session-maintenance/) | Maintain Hermes Agent session history: inspect size, export backups, prune old ended sessions, and configure safe auto-prune retention | Ready |
| [hermes-starter-onboarding](skills/hermes-starter-onboarding/) | Use when a new Hermes profile needs guided first-run setup, identity choices, memory preferences, optional integrations, a step-by-step toolset walkthrough, web-search backend setup, or recurring daily briefing, wellness check-in, and stock-quote jobs. Plan the setup conversationally, obtain approval, apply only the selected changes, and verify every result | Ready |
| [hermes-themes](skills/hermes-themes/) | Author a Hermes color theme that skins every surface | Ready |
| [hf-model-card-research](skills/hf-model-card-research/) | Pull structured benchmark metadata, download stats, and quality claims from HuggingFace model cards for comparison across model variants | Ready |
| [imessage](skills/imessage/) | Send and receive iMessages/SMS via the imsg CLI on macOS | Ready |
| [inspecting-hermes-desktop-dom](skills/inspecting-hermes-desktop-dom/) | Read the live Hermes desktop DOM/CSS over CDP | Ready |
| [local-app-github-publishing](skills/local-app-github-publishing/) | Safely publish local apps, prototypes, and substantial local branches to GitHub for the first time | Ready |
| [local-discovery](skills/local-discovery/) | Find local events, venues, and activities — ad-hoc web discovery when the user asks 'what's happening' or 'what should I do this weekend' | Ready |
| [local-model-selection](skills/local-model-selection/) | Choose and recommend local LLM models for Hermes Agent — VRAM-tier recommendations, uncensored/abliterated variants, quant selection, model family naming conventions, dual-GPU setups, and auxiliary model selection | Ready |
| [macos-app-automation](skills/macos-app-automation/) | Automate native macOS apps with AppleScript, URL schemes, System Events, and Hermes computer-use fallbacks; includes TCC/Automation permission troubleshooting | Ready |
| [macos-storage-management](skills/macos-storage-management/) | Use when freeing Mac storage or moving files to SSDs | Ready |
| [maps](skills/maps/) | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM | Ready |
| [marketing-collateral-design](skills/marketing-collateral-design/) | Use when designing, recreating, critiquing, or exporting static marketing collateral such as flyers, social graphics, postcards, brochures, business cards, print ads, and promotional one-sheets. Covers reference decomposition, original art direction, deterministic HTML/CSS/SVG typesetting, separate AI imagery, print/social production, and rendered visual QA | Ready |
| [marketplace-purchase-vetting](skills/marketplace-purchase-vetting/) | Search/discover AND vet Facebook Marketplace/Craigslist/private-party purchases. Two modes: find the best live options in the area within a budget, then vet promising candidates for too-good-to-be-true risk. Covers vehicles, boats, trailers, equipment, and other high-dollar local listings | Ready |
| [meal-tracker](skills/meal-tracker/) | Track meals and calories from a photo or text description. Vision-based portion estimates, daily calorie/macro budget, markdown food log | Ready |
| [messaging-gateway-troubleshooting](skills/messaging-gateway-troubleshooting/) | Troubleshoot Hermes messaging gateway platform adapters, webhooks, authorization, delivery, and loop-prevention behavior | Ready |
| [meta-business-posting](skills/meta-business-posting/) | Publish posts to a Facebook Page through the agent's own logged-in browser session or the Meta Graph API. Account-agnostic; no credentials in the skill | Ready |
| [mnemosyne-maintenance](skills/mnemosyne-maintenance/) | Upgrade, troubleshoot, and maintain Mnemosyne memory provider — version mismatches, slow/hung consolidation, missing embeddings, import shadowing | Ready |
| [notes-automation-workflows](skills/notes-automation-workflows/) | Automate bulk Apple Notes workflows: discovery, filtering, and scripted enrichment for links/photos | Ready |
| [notion](skills/notion/) | Notion API + ntn CLI: pages, databases, markdown, Workers | Ready |
| [notion-artifact-capture](skills/notion-artifact-capture/) | Save and organize AI-generated content in a user-owned Notion library | Ready |
| [obsidian](skills/obsidian/) | Read, search, create, and edit notes in the Obsidian vault | Ready |
| [obsidian-memory-architecture](skills/obsidian-memory-architecture/) | Use Obsidian as Hermes's durable knowledge and coordination layer without duplicating native memory, session history, or skills | Ready |
| [office-document-review](skills/office-document-review/) | Review and proofread office documents in OneDrive or local file trees, including batch folder discovery, document text extraction, and spelling/grammar cleanup workflows | Ready |
| [opencode](skills/opencode/) | Delegate coding to OpenCode CLI (features, PR review) | Ready |
| [product-competitor-analysis](skills/product-competitor-analysis/) | Conduct codebase-grounded competitive assessments for iOS/macOS apps by inventorying implemented behavior, mapping user needs, extracting differentiators, identifying blockers, and producing a positioning summary with line-grounded evidence | Ready |
| [publication-link-audit](skills/publication-link-audit/) | Verify every outbound URL in a Reddit post, megathread, guide, wiki page, or README before publication. Detects transcribed IDs, GitHub filename drift, and HuggingFace repo naming mismatches that HTTP status codes alone miss | Ready |
| [reddit-browse-and-post](skills/reddit-browse-and-post/) | Browse Reddit, search, read threads and comments, and create posts through the agent's own authenticated session or OAuth app. Account-agnostic; no credentials in the skill | Ready |
| [session-artifact-indexing](skills/session-artifact-indexing/) | Create a durable index of documents, links, and files produced during multi-step sessions so the user can find them later | Ready |
| [site-mapping](skills/site-mapping/) | Map out a website's full structure — sitemaps, navigation, URL taxonomy, content inventory | Ready |
| [skill-auditor](skills/skill-auditor/) | Use when auditing, reviewing, or grading Hermes skills for quality. Checks trigger phrases, exact commands, pitfalls, verification steps, tool guidance, and shareability. Assigns A-F grade with specific fix suggestions. Run this before publishing a skill or when troubleshooting unreliable skills | Ready |
| [source-verification](skills/source-verification/) | Verify articles, claims, and web sources by separating what is directly supported, what is partially supported, and what is unverified or misleading | Ready |
| [specification-compliance-review](skills/specification-compliance-review/) | Audit partial or passing implementations against an explicit task specification, proving each requirement with code, tests, and execution evidence | Ready |
| [stale-patch-reconciliation](skills/stale-patch-reconciliation/) | Reconcile a stale patch/diff against a current checkout | Ready |
| [subagent-driven-development](skills/subagent-driven-development/) | Execute plans via delegate_task subagents (2-stage review) | Ready |
| [vault-organization](skills/vault-organization/) | Structure a new Obsidian vault (PARA taxonomy, MOCs, starter folder tree) and audit/clean up/reorganize an existing one — identify bloat, consolidate duplicates, remove empty shells, update MOCs and stale references | Ready |
| [xurl](skills/xurl/) | X/Twitter via xurl CLI: post, search, DM, media, v2 API | Ready |
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
