---
name: example-site-example-flow
description: Use when replaying the verified example flow on example.com. Follows known semantic targets, stops on divergence, and requires confirmation before any consequential action.
version: 1.0.0
author: Your Name
license: MIT
metadata:
  hermes:
    tags:
      - browser-automation
      - website-harness
---
# Example Site — Example Flow

## Overview

One-sentence scope of the mapped workflow.

- Domain: `example.com`
- Start URL: `https://example.com/start`
- Success boundary: Describe the last verified page state before any final side effect.
- Browser lane: `configured-default`
- Last verified: `YYYY-MM-DD`
- Expires: `YYYY-MM-DD`
- Tested: `false`
- Risk class: `read-only | reversible | consequential`

## When to Use

Use only for the exact flow and domain above.

Do not use when the harness is expired, the domain differs, authentication state is unclear, or the page diverges from an expected checkpoint.

## Prerequisites

- Required authenticated state, without credentials
- Required records/cart/reservation state
- Inputs to request from the user at runtime

## Execution Contract

- Follow steps in order.
- Take a fresh snapshot after each state change.
- Never reuse saved `@e` refs.
- Stop on domain, content, total, permission, or checkpoint divergence.
- Pause at every decision gate.
- Obtain explicit confirmation immediately before a consequential action.
- Record completed checkpoints and observed side effects.

## Flow

### Step 1: Open the start page

- Precondition: None
- Action: Navigate to `https://example.com/start`
- Primary target: URL navigation
- Stable fallback: None
- Visual fallback: None
- Wait for: Heading “Example” is visible
- Expected checkpoint: Correct domain and heading are present
- Failure signals: Redirect to login; challenge page; unexpected domain
- Recovery: Stop and request the required authenticated state
- Decision gate: false
- External side effect: false
- Skip allowed: false

### Step 2: Choose an example option

- Precondition: Step 1 checkpoint passed
- Action: Click the button named “Continue”
- Primary target: Role `button`, accessible name `Continue`
- Stable fallback: `[aria-label="Continue"]`
- Visual fallback: Labeled button below the form heading
- Wait for: Heading “Review” is visible
- Expected checkpoint: Review page shows the supplied dummy values
- Failure signals: Validation message; overlay blocks control
- Recovery: Correct dummy fields or dismiss the documented overlay, then retry once
- Decision gate: true
- External side effect: false
- Skip allowed: false

### Step 3: Stop at the side-effect boundary

- Precondition: Review checkpoint passed
- Action: Do not activate the final submit control during authoring or verification
- Primary target: Role `button`, accessible name `Submit example`
- Stable fallback: `[name="submit"]`
- Visual fallback: Final primary button beneath the review summary
- Wait for: Not applicable
- Expected checkpoint: Final values, totals, recipient, and date are visible for user review
- Failure signals: Final action occurs without confirmation
- Recovery: Stop immediately and report any observed side effect
- Decision gate: true
- External side effect: true
- Skip allowed: false

## Recovery and Abort Rules

- Authentication challenge: pause for the user; never store credentials.
- CAPTCHA or MFA: pause for the user; never bypass.
- Unexpected domain or redirect: stop.
- Missing semantic target: try only documented stable fallback, then stop.
- Changed total, date, recipient, permissions, or terms: stop and re-confirm.
- Expired harness: use as an unverified map only; re-author before consequential execution.

## Verification Evidence

- Verified browser lane: `configured-default`
- Replay date: `YYYY-MM-DD`
- Dummy dataset: Describe generically; do not include personal data
- Steps passed: `0/3`
- Recovery path tested: None yet
- Final side effect crossed: `false`
- Known limitations: List observed limitations

## Common Pitfalls

- Record observed site-specific traps here.
- Do not save session-local refs, generated class names, credentials, or cookies.

## Verification Checklist

- [ ] Domain and start URL verified
- [ ] Semantic targets found without saved refs
- [ ] Expected checkpoint passed after every state change
- [ ] Decision and side-effect gates stopped correctly
- [ ] One safe recovery path tested
- [ ] No secret or personal data stored
- [ ] Final side effect was not crossed
- [ ] Dates and tested status updated accurately
