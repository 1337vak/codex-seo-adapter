#!/usr/bin/env python3
"""Generated bootstrap: execute the port tool at the repository's locked commit."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / "port.json").read_text())["tool"]
local = os.environ.get("PLUGIN_PORT_TOOL")  # Explicit development override only.
with tempfile.TemporaryDirectory(prefix="plugin-port-tool-") as folder:
    tool = Path(local).resolve() if local else Path(folder)
    if not local:
        subprocess.run(["git", "init", "--quiet", str(tool)], check=True)
        subprocess.run(["git", "-C", str(tool), "fetch", "--quiet", "--depth=1", lock["repository"], lock["commit"]], check=True)
        subprocess.run(["git", "-C", str(tool), "checkout", "--quiet", "--detach", "FETCH_HEAD"], check=True)
        actual = subprocess.check_output(["git", "-C", str(tool), "rev-parse", "HEAD"], text=True).strip()
        if actual != lock["commit"]:
            raise SystemExit("Tool checkout does not match lock")
    env = {**os.environ, "PYTHONPATH": str(tool)}
    subprocess.run([sys.executable, "-m", "plugin_port", *sys.argv[1:], "--adapter", str(root)], env=env, check=True)
