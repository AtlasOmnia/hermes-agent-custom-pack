# Browser Harness Schema

A harness is a site-specific Hermes skill, not executable code and not a recording of one browser session.

## Required identity fields

The standard Hermes skill frontmatter must contain `name` and `description`. Keep the name lowercase and hyphenated. Put browser-harness metadata in the body so standard skill parsers remain portable.

The Overview section must declare:

| Field | Meaning |
|---|---|
| Domain | Exact allowed website domain |
| Start URL | Known entry point for the flow |
| Success boundary | Objective final verified state |
| Browser lane | Backend observed working during verification |
| Last verified | ISO date of full safe replay |
| Expires | ISO date after which the harness is unverified |
| Tested | `true` only after full dummy-data replay |
| Risk class | `read-only`, `reversible`, or `consequential` |

## Required step fields

Each numbered step must include:

- `Precondition`
- `Action`
- `Primary target`
- `Stable fallback`
- `Visual fallback`
- `Wait for`
- `Expected checkpoint`
- `Failure signals`
- `Recovery`
- `Decision gate`
- `External side effect`
- `Skip allowed`

Use `None` explicitly when a field is not applicable.

## Target stability

Preferred order:

1. accessibility role and accessible name;
2. associated label, stable attribute, or unique nearby text;
3. stable structural selector;
4. visual anchor;
5. coordinates only as a last resort.

Never persist browser snapshot refs such as `@e12`; they are regenerated. Treat hashed/generated classes, transient IDs, and positional selectors as brittle.

## Checkpoints

A tool reporting that it clicked or typed successfully is not a checkpoint. Checkpoints are observable page states: a heading appeared, URL changed to an allowed route, review values match expected inputs, or an explicit confirmation banner is present.

## Decision and side-effect gates

`Decision gate: true` means the executor must stop for a user choice or confirmation.

`External side effect: true` means the action can change the outside world, including purchases, bookings, transfers, claims, messages, publication, account changes, cancellations, or submissions. Authoring and verification must stop before activating such a control.

## Verification status

- `verified`: directly replayed from start to safe boundary in a fresh session.
- `observed-once`: seen during survey but not independently replayed.
- `untested`: inferred or documented but not observed.

`Tested: true` requires every mandatory step to be verified, at least one safe recovery path to be exercised, and the final side effect to remain uncrossed.

## Expiry

Default to 30 days. Use 7 days when the flow depends on vision, coordinates, brittle selectors, or frequently changing UI. High-consequence flows must be rechecked before every run.

## Prohibited content

Do not include passwords, cookies, session tokens, MFA seeds, payment details, government identifiers, medical information, customer records, real form values, private infrastructure, or personal file paths.
