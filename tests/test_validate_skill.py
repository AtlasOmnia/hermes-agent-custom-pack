import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_skill import SKILL, validate


class SkillValidationTests(unittest.TestCase):
    def test_repository_skill_passes(self):
        self.assertEqual(validate(SKILL), [])

    def test_rejects_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text("# No frontmatter\n", encoding="utf-8")
            self.assertTrue(validate(path))

    def test_rejects_invalid_name_and_missing_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                "---\nname: Invalid Name\ndescription: test\n---\n# Body\n",
                encoding="utf-8",
            )
            errors = validate(path)
            self.assertTrue(any("name must" in error for error in errors))
            self.assertTrue(any("missing recommended heading" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
