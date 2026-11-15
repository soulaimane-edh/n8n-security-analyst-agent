"""Static regression checks; not real-time security scan tests."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_workflow import REQUIRED_NODES, validate  # noqa: E402


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = json.loads((ROOT / "security-analyst-workflow.json").read_text(encoding="utf-8"))

    def test_export_validation(self) -> None:
        self.assertEqual(validate(self.workflow), [])

    def test_expected_components(self) -> None:
        names = {n["name"] for n in self.workflow["nodes"]}
        self.assertEqual(len(names), 24)
        self.assertTrue(REQUIRED_NODES.issubset(names))

    def test_secrets_are_not_embedded(self) -> None:
        src = json.dumps(self.workflow)
        self.assertNotIn("YOUR_VIRUSTOTAL_API_KEY", src)
        self.assertNotIn("admin@example.com", src)
        self.assertIn("$env.VIRUSTOTAL_API_KEY", src)
        self.assertIn("$env.SECURITY_REPORT_EMAIL", src)

    def test_unsafe_cert_bypass_rejected(self) -> None:
        cloned = copy.deepcopy(self.workflow)
        for node in cloned["nodes"]:
            if node["name"] == "Check File Hash in VirusTotal":
                node["parameters"].setdefault("options", {})["allowUnauthorizedCerts"] = True
                break
        self.assertTrue(any("TLS" in issue for issue in validate(cloned)))

    def test_broken_connection_rejected(self) -> None:
        cloned = copy.deepcopy(self.workflow)
        cloned["connections"]["On New Email"]["main"][0][0]["node"] = "Missing Node"
        self.assertTrue(any("Broken connection" in issue for issue in validate(cloned)))

    def test_no_saved_execution_data(self) -> None:
        self.assertFalse(self.workflow.get("pinData"))

    def test_analyst_is_connected_to_gemini(self) -> None:
        entries = self.workflow["connections"]["Google Gemini"]["ai_languageModel"][0]
        self.assertTrue(any(link["node"] == "Security Analyst Agent" for link in entries))

    def test_no_indicators_not_claimed_clean(self) -> None:
        node = next(n for n in self.workflow["nodes"] if n["name"] == "No Threats Found")
        assignments = node["parameters"]["assignments"]["assignments"]
        status = next(x["value"] for x in assignments if x["name"] == "securityStatus")
        self.assertEqual(status, "NOT_SCANNED")


if __name__ == "__main__":
    unittest.main()
