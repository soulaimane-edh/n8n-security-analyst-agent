#!/usr/bin/env python3
"""Build an Agensi-style text-only skill ZIP from this repository."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "email-threat-triage"
DEFAULT_OUTPUT = ROOT / "dist" / "email-threat-triage-skill.zip"


def build(output: Path) -> Path:
    validator = ROOT / "scripts" / "validate_workflow.py"
    subprocess.run([sys.executable, str(validator)], cwd=ROOT, check=True, capture_output=True, text=True)
    workflow = ROOT / "security-analyst-workflow.json"
    json.loads(workflow.read_text(encoding="utf-8"))
    paths = {
        "SKILL.md": SKILL / "SKILL.md",
        "workflow.json": workflow,
        "references/usage.md": SKILL / "references" / "usage.md",
        "references/setup.md": ROOT / "docs" / "SETUP.md",
        "references/security.md": ROOT / "docs" / "SECURITY.md",
        "references/architecture.md": ROOT / "docs" / "ARCHITECTURE.md",
    }
    for arc, path in paths.items():
        if not path.is_file():
            raise FileNotFoundError(f"Required package file missing: {arc} from {path}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for arc, path in paths.items():
            archive.write(path, arcname=arc)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        path = build(args.output)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"Failed to package skill: {exc}", file=sys.stderr)
        return 1
    print(f"Built: {path}")
    print("Prototype package only; review licensing, privacy and external integration tests before selling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
