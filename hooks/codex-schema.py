#!/usr/bin/env python3
"""Translate Codex edit events into calls to the preserved upstream schema check."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys


def changed_paths(event: dict) -> list[Path]:
    tool = str(event.get("tool_name", "")).rsplit("__", 1)[-1].rsplit(".", 1)[-1].lower()
    if tool not in {"write", "edit", "multiedit", "apply_patch", "write_file", "edit_file"}:
        return []
    value = event.get("tool_input", {})
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            value = {"patch": value}
    if not isinstance(value, dict):
        return []
    names: list[str] = []
    for key in ("file_path", "path"):
        if isinstance(value.get(key), str):
            names.append(value[key])
    # apply_patch uses a freeform patch; a post-edit hook must check every
    # surviving added, updated or moved file, rather than silently ignoring it.
    for key in ("patch", "input", "command"):
        patch = value.get(key)
        if isinstance(patch, str) and patch.lstrip().startswith("*** Begin Patch\n"):
            names.extend(re.findall(r"^\*\*\* (?:Add File|Update File|Move to): (.+)$", patch, re.M))
    base = Path(event.get("cwd") or os.getcwd())
    result: list[Path] = []
    for name in names:
        path = Path(name)
        if not path.is_absolute():
            path = base / path
        path = path.resolve()
        if path not in result and path.is_file():
            result.append(path)
    return result


def main() -> int:
    # Match all post-tool events and cheaply ignore everything without an edit
    # path. This also works when a host exposes a qualified apply_patch name.
    try:
        raw = sys.stdin.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            print("Schema check skipped: hook event exceeds 2 MiB.", file=sys.stderr)
            return 1
        event = json.loads(raw or "{}")
        if not isinstance(event, dict):
            return 0
        paths = changed_paths(event)
    except (OSError, ValueError, TypeError):
        return 0
    validator = Path(__file__).with_name("validate-schema.py")
    contexts: list[str] = []
    critical = False
    for path in paths:
        try:
            result = subprocess.run(
                [sys.executable, str(validator), str(path)],
                input="", capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            print(f"Schema validation unavailable: {error}", file=sys.stderr)
            return 1
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        if result.returncode == 2:
            critical = True
        elif result.returncode:
            return result.returncode
        if result.stdout.strip():
            try:
                context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
            except (ValueError, KeyError, TypeError):
                print("Schema validator returned an unexpected response.", file=sys.stderr)
                return 1
            contexts.append(context)
    if contexts and critical:
        print("\n\n".join(contexts), file=sys.stderr)
    elif contexts:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse", "additionalContext": "\n\n".join(contexts),
        }}))
    return 2 if critical else 0


if __name__ == "__main__":
    raise SystemExit(main())
