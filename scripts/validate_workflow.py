#!/usr/bin/env python3
"""Offline integrity and security-lint checks for an n8n JSON export.

This is not a runtime integration test, malware scanner, or formal security audit.
Requires only Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_WORKFLOW = Path(__file__).resolve().parents[1] / "security-analyst-workflow.json"
REQUIRED_NODES = {
    "On New Email", "Extract URLs and Attachments", "Route by Content Type",
    "Submit URL to VirusTotal", "Download Attachment", "Calculate File Hash",
    "Check File Hash in VirusTotal", "Upload File to VirusTotal",
    "Merge All Results", "Aggregate Scan Results", "Security Analyst Agent",
    "Google Gemini", "Send Security Report Email",
}


def validate(workflow: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(workflow, dict):
        return ["Workflow root must be a JSON object"]

    nodes = workflow.get("nodes")
    connections = workflow.get("connections")
    if not isinstance(nodes, list) or not nodes:
        return ["Workflow requires a non-empty nodes array"]
    if not isinstance(connections, dict):
        return ["Workflow requires a connections object"]

    names: list[str] = []
    node_ids: list[str] = []
    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node #{idx} must be an object")
            continue
        name = node.get("name")
        node_id = node.get("id")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"Node #{idx} has no valid name")
        else:
            names.append(name)
        if node_id is not None:
            node_ids.append(str(node_id))
        if not isinstance(node.get("type"), str):
            errors.append(f"Node #{idx} has no type")
    if len(names) != len(set(names)):
        errors.append("Node names are not unique")
    if len(node_ids) != len(set(node_ids)):
        errors.append("Node IDs are not unique")

    unknown_required = REQUIRED_NODES - set(names)
    if unknown_required:
        errors.append("Missing required nodes: " + ", ".join(sorted(unknown_required)))

    for source_name, outputs in connections.items():
        if source_name not in names:
            errors.append(f"Connection source not found: {source_name}")
            continue
        if not isinstance(outputs, dict):
            errors.append(f"Connection outputs malformed for {source_name}")
            continue
        for conntype, branches in outputs.items():
            if not isinstance(branches, list):
                errors.append(f"Malformed {conntype} connection list for {source_name}")
                continue
            for links in branches:
                if not isinstance(links, list):
                    errors.append(f"Malformed {conntype} branch for {source_name}")
                    continue
                for link in links:
                    if not isinstance(link, dict) or link.get("node") not in names:
                        errors.append(f"Broken connection from {source_name}: {link!r}")

    for node in nodes:
        if not isinstance(node, dict):
            continue
        params = node.get("parameters") or {}
        if not isinstance(params, dict):
            errors.append(f"Non-object parameters for {node.get('name')}")
            continue
        options = params.get("options") or {}
        if isinstance(options, dict) and options.get("allowUnauthorizedCerts") is True:
            errors.append(f"TLS verification bypass in node {node.get('name')}")
        for k, v in params.items():
            if k == "jsCode" and not isinstance(v, str):
                errors.append(f"Unexpected code field in {node.get('name')}")

    text = json.dumps(workflow, ensure_ascii=False)
    if "YOUR_VIRUSTOTAL_API_KEY" in text:
        errors.append("Legacy inline VirusTotal API key placeholder detected")
    if "admin@example.com" in text:
        errors.append("Legacy hard-coded reporting email detected")
    if "$env.VIRUSTOTAL_API_KEY" not in text:
        errors.append("Missing VirusTotal environment expression")
    if "$env.SECURITY_REPORT_EMAIL" not in text:
        errors.append("Missing report recipient environment expression")
    if workflow.get("pinData") not in ({}, None):
        errors.append("Pinned data must be removed before publication")
    if re.search(r"(?i)(sk-[a-z0-9]{20,}|AIza[a-z0-9_-]{25,})", text):
        errors.append("Potential credential-like secret in workflow")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_WORKFLOW)
    args = parser.parse_args()
    try:
        workflow = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: unable to load {args.path}: {exc}", file=sys.stderr)
        return 1
    errors = validate(workflow)
    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {args.path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(workflow['nodes'])} nodes, connected references valid, no configured TLS bypass or known key placeholders")
    print("Note: this is static validation only; external integrations remain untested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
