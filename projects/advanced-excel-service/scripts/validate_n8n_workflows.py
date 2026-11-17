#!/usr/bin/env python3
"""Validate saved n8n workflow JSON and JavaScript Code-node syntax."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "n8n" / "workflows"


def main() -> int:
    files = sorted(WORKFLOWS.glob("*.json"))
    if not files:
        raise SystemExit("No n8n workflow JSON files found.")

    checked = 0
    for path in files:
        workflow = json.loads(path.read_text(encoding="utf-8"))
        if workflow.get("active") is not False:
            raise SystemExit(f"{path.name}: workflow must remain inactive in source control.")
        for node in workflow.get("nodes", []):
            if node.get("type") != "n8n-nodes-base.code":
                continue
            code = node.get("parameters", {}).get("jsCode")
            if not isinstance(code, str) or not code.strip():
                raise SystemExit(f"{path.name}: empty Code node: {node.get('name')}")
            with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tmp:
                tmp.write(code)
                temp_path = Path(tmp.name)
            try:
                result = subprocess.run(
                    ["node", "--check", str(temp_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            finally:
                temp_path.unlink(missing_ok=True)
            if result.returncode:
                raise SystemExit(f"{path.name} / {node.get('name')}: JavaScript syntax error\n{result.stderr}")
            checked += 1
        print(f"PASS {path.relative_to(ROOT)}")
    print(f"Validated {len(files)} workflow JSON file(s) and {checked} Code node(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
