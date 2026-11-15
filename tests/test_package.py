"""Offline packaging smoke test."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_skill import build  # noqa: E402


class PackageTests(unittest.TestCase):
    def test_build_agensi_style_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            archive_path = build(Path(temp) / "test-skill.zip")
            self.assertTrue(archive_path.exists())
            with ZipFile(archive_path) as archive:
                names = set(archive.namelist())
                self.assertIn("SKILL.md", names)
                self.assertIn("workflow.json", names)
                self.assertIn("references/security.md", names)
                content = archive.read("SKILL.md").decode("utf-8")
                self.assertTrue(content.startswith("---\n"))
                self.assertIn("name: n8n-email-threat-triage", content)
                self.assertTrue(all(name.endswith((".md", ".json")) for name in names))
                self.assertEqual(len(json.loads(archive.read("workflow.json"))["nodes"]), 24)


if __name__ == "__main__":
    unittest.main()
