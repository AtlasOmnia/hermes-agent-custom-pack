import tempfile
import unittest
from pathlib import Path
import sys
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from scaffold_vault import FILES, ROOT_DIRS, canonical_vault_path, is_link_or_reparse, main, scaffold


class ScaffoldTests(unittest.TestCase):
    def test_creates_expected_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "Vault"
            result = scaffold(vault)
            self.assertTrue((vault / "Daily").is_dir())
            self.assertTrue((vault / "System/Assistant/README.md").is_file())
            self.assertEqual(len(result["created"]), len(FILES))
            for rel in ROOT_DIRS:
                self.assertTrue((vault / rel).is_dir())

    def test_is_idempotent_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "Vault"
            scaffold(vault)
            target = vault / "System/Assistant/environment.md"
            target.write_text("custom content\n", encoding="utf-8")
            result = scaffold(vault)
            self.assertEqual(target.read_text(encoding="utf-8"), "custom content\n")
            expected = canonical_vault_path(vault) / "System/Assistant/environment.md"
            self.assertIn(str(expected), result["skipped"])

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "Vault"
            result = scaffold(vault, dry_run=True)
            self.assertFalse(vault.exists())
            self.assertEqual(len(result["would-create"]), len(FILES))

    def test_force_overwrites_managed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "Vault"
            scaffold(vault)
            target = vault / "Templates/Daily.md"
            target.write_text("changed\n", encoding="utf-8")
            result = scaffold(vault, force=True)
            self.assertEqual(target.read_text(encoding="utf-8"), FILES["Templates/Daily.md"])
            expected = canonical_vault_path(vault) / "Templates/Daily.md"
            self.assertIn(str(expected), result["overwritten"])

    @unittest.skipIf(sys.platform == "win32", "symlink creation may require Windows developer mode")
    def test_rejects_symlink_inside_managed_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vault = root / "Vault"
            outside = root / "outside"
            vault.mkdir()
            outside.mkdir()
            (vault / "Templates").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                scaffold(vault)
            self.assertEqual(list(outside.iterdir()), [])

    def test_main_empty_argv_does_not_consume_process_arguments(self):
        with mock.patch.object(sys, "argv", ["scaffold_vault.py", "--vault", "/unexpected"]):
            with self.assertRaises(SystemExit):
                main([])

    def test_regular_directory_is_not_a_link_or_reparse_point(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(is_link_or_reparse(Path(tmp)))


if __name__ == "__main__":
    unittest.main()
