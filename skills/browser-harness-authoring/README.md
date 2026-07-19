# Browser Harness Authoring for Hermes Agent

Turn a known website workflow into a verified, site-specific Hermes skill.

The package updates the builder/executor idea from the Reddit workshop [Teach Hermes to Drive Any Website — Zero Config](https://www.reddit.com/r/hermesagent/comments/1tmpq0n/workshop_teach_hermes_to_drive_any_website_zero/) for current Hermes browser tools, profiles, skills, and cron behavior.

## What it produces

A browser harness is a `SKILL.md` for one narrow site flow. It records:

- the verified browser lane;
- semantic targets and stable fallbacks;
- expected checkpoints after every action;
- failure and recovery paths;
- decision and side-effect gates;
- verification status and expiry.

The skill never treats saved browser refs, CAPTCHA bypass, or unattended checkout as reliable automation.

## Install

Inspect first:

```bash
hermes skills inspect https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/browser-harness-authoring/SKILL.md
```

Install:

```bash
hermes skills install https://raw.githubusercontent.com/AtlasOmnia/hermes-agent-custom-pack/main/skills/browser-harness-authoring/SKILL.md
```

A direct `SKILL.md` install provides the procedure. Clone the repository when you also want the template, schema reference, validator, and tests:

```bash
git clone https://github.com/AtlasOmnia/hermes-agent-custom-pack.git
cd hermes-agent-custom-pack/skills/browser-harness-authoring
```

## Use

In a new Hermes session:

```text
/browser-harness-authoring Map the order-status flow on https://example.com. Use dummy data and stop before any side effect.
```

Or ask naturally for Hermes to survey a repeatable website flow and save a verified harness.

## Validate a generated harness

```bash
python3 scripts/validate_harness.py /path/to/generated/SKILL.md
```

Run this package's tests:

```bash
python3 -m unittest discover -s tests -v
```

## Safety boundary

Authoring and verification use dummy data and stop before purchases, bookings, transfers, claims, account creation, publication, messages, cancellations, or other irreversible actions. CAPTCHA, MFA, access controls, and bot protections are human or suitability gates—not obstacles to bypass.

## Contents

- `SKILL.md` — authoring and execution procedure
- `templates/harness-template.md` — generated harness starter
- `templates/survey-log.md` — evidence log for mapping sessions
- `references/harness-schema.md` — field semantics and stability rules
- `scripts/validate_harness.py` — dependency-free structural validator
- `tests/test_validate_harness.py` — validator tests
