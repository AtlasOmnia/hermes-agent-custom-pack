from __future__ import annotations

from pathlib import Path
import importlib.util
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_harness.py"
SPEC = importlib.util.spec_from_file_location("validate_harness", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate = MODULE.validate


VALID = """---
name: example-order-status
description: Use when checking a known order-status flow on example.com.
version: 1.0.0
---
# Example Order Status

## Overview
- Domain: `example.com`
- Start URL: `https://example.com/orders`
- Success boundary: Order status is visible
- Browser lane: `configured-default`
- Last verified: `2026-07-18`
- Expires: `2026-08-17`
- Tested: `true`
- Risk class: `read-only`

## When to Use
Use for this exact flow.

## Prerequisites
- Authenticated session

## Execution Contract
- Stop on divergence.

## Flow

### Step 1: Open orders
- Precondition: Authenticated session
- Action: Navigate to the orders page
- Primary target: URL navigation
- Stable fallback: None
- Visual fallback: None
- Wait for: Heading `Orders`
- Expected checkpoint: Order list is visible
- Failure signals: Login redirect
- Recovery: Pause for user login
- Decision gate: false
- External side effect: false
- Skip allowed: false

### Step 2: Stop at final boundary
- Precondition: Order list visible
- Action: Read the status only
- Primary target: Role `status`
- Stable fallback: `[data-testid="order-status"]`
- Visual fallback: Status beside the order number
- Wait for: Status text
- Expected checkpoint: Status is captured
- Failure signals: Order not found
- Recovery: Stop and report
- Decision gate: true
- External side effect: true
- Skip allowed: false

## Recovery and Abort Rules
- Stop on an unexpected domain.

## Verification Evidence
- Verified browser lane: `configured-default`
- Replay date: `2026-07-18`
- Dummy dataset: Generic test order
- Steps passed: `2/2`
- Recovery path tested: Login redirect
- Final side effect crossed: `false`
- Known limitations: None

## Common Pitfalls
- Session expiry

## Verification Checklist
- [x] Domain verified
"""


class HarnessValidatorTests(unittest.TestCase):
    def validate_text(self, text: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(text, encoding="utf-8")
            return validate(path)

    def test_valid_harness_passes(self) -> None:
        self.assertEqual(self.validate_text(VALID), [])

    def test_rejects_missing_frontmatter(self) -> None:
        errors = self.validate_text(VALID.removeprefix("---\n"))
        self.assertIn("SKILL.md must start with closed YAML frontmatter at byte zero", errors)

    def test_rejects_session_local_refs(self) -> None:
        errors = self.validate_text(VALID.replace("Role `status`", "Browser ref @e42"))
        self.assertTrue(any("session-local" in error for error in errors))

    def test_rejects_side_effect_without_decision_gate(self) -> None:
        errors = self.validate_text(VALID.replace(
            "- Decision gate: true\n- External side effect: true",
            "- Decision gate: false\n- External side effect: true",
        ))
        self.assertTrue(any("must be a decision gate" in error for error in errors))

    def test_rejects_expiry_before_verification(self) -> None:
        errors = self.validate_text(VALID.replace("Expires: `2026-08-17`", "Expires: `2026-07-01`"))
        self.assertIn("Expires cannot be earlier than Last verified", errors)

    def test_rejects_domain_mismatch(self) -> None:
        errors = self.validate_text(VALID.replace("https://example.com/orders", "https://wrong.example.net/orders"))
        self.assertIn("Start URL host does not match Domain", errors)

    def test_rejects_private_path(self) -> None:
        errors = self.validate_text(VALID.replace("Generic test order", "/Users/alice/private/order.json"))
        self.assertTrue(any("user-specific local path" in error for error in errors))

    def test_rejects_linux_home_path(self) -> None:
        errors = self.validate_text(VALID.replace("Generic test order", "/home/alice/private/order.json"))
        self.assertTrue(any("user-specific local path" in error for error in errors))

    def test_rejects_windows_user_path(self) -> None:
        errors = self.validate_text(VALID.replace("Generic test order", "C:/Users/alice/private/order.json"))
        self.assertTrue(any("user-specific local path" in error for error in errors))

    def test_rejects_missing_final_boundary_declaration(self) -> None:
        errors = self.validate_text(VALID.replace("- Final side effect crossed: `false`\n", ""))
        self.assertTrue(any("Final side effect crossed" in error for error in errors))

    def test_rejects_nonconsecutive_steps(self) -> None:
        errors = self.validate_text(VALID.replace("### Step 2:", "### Step 3:"))
        self.assertIn("step numbers must be consecutive starting at 1", errors)


if __name__ == "__main__":
    unittest.main()
