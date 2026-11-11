#!/usr/bin/env python3
"""Exercise generated SEO helpers and Codex hook events using local fixtures."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile


PLUGIN = Path(sys.argv[1]).resolve()
FIXTURES = Path(__file__).parent / "fixtures"


def call(script, *arguments, event=None, env=None):
    return subprocess.run(
        [sys.executable, str(PLUGIN / script), *map(str, arguments)],
        input=json.dumps(event) if event is not None else "",
        capture_output=True, text=True, env=env, timeout=20,
    )


def successful_json(result):
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def hook(event):
    return call("hooks/codex-schema.py", event=event)


catalog = json.loads((PLUGIN / "skills/seo/catalog.json").read_text())
assert len(catalog["roles"]) == 19
assert len(list((PLUGIN / "skills").glob("*/SKILL.md"))) == 26
for role in catalog["roles"]:
    assert (PLUGIN / "skills/seo" / role["path"]).is_file(), role
assert "Copyright (c) 2026 agricidaniel" in (PLUGIN / "LICENSE").read_text()
flow = PLUGIN / "skills/seo-flow/references/prompts/README.md"
assert "CC BY 4.0" in flow.read_text() and "AgriciDaniel/flow" in flow.read_text()
assert (PLUGIN / "skills/seo-flow/references/flow-prompts.lock").is_file()
assert (PLUGIN / "scripts/claude-seo").stat().st_mode & 0o111

with tempfile.TemporaryDirectory(prefix="codex-seo-verify-") as directory:
    work = Path(directory)
    env = {key: value for key, value in os.environ.items() if not key.startswith("CLAUDE_SEO_")}
    env.update(PLUGIN_ROOT=str(PLUGIN), PLUGIN_DATA=str(work / "runtime"),
               CLAUDE_SEO_CONFIG_DIR=str(work / "budget"))
    # Diagnosis must report missing setup instead of installing dependencies.
    doctor = call("scripts/runtime.py", "doctor", "--json", env=env)
    assert doctor.returncode == 3, doctor.stderr
    status = json.loads(doctor.stdout)
    assert status["mode"] == "plugin" and status["ready"] is False
    assert not (work / "runtime").exists()
    fixture = call("hooks/validate-schema.py", FIXTURES / "page.html")
    assert fixture.returncode == 0 and not fixture.stdout and not fixture.stderr, fixture

    profile = successful_json(call(
        "scripts/schema_generate.py", "profile", "--name", "Ada Lovelace",
        "--url", "https://example.com/ada", env=env,
    ))
    assert profile["@type"] == "ProfilePage"
    assert profile["mainEntity"]["name"] == "Ada Lovelace"
    page = work / "profile.html"
    page.write_text('<script type="application/ld+json">' + json.dumps(profile) + '</script>')
    patch = "*** Begin Patch\n*** Add File: profile.html\n+fixture\n*** End Patch"
    event = {"hook_event_name": "PostToolUse", "tool_name": "functions.apply_patch",
             "cwd": str(work), "tool_input": {"input": patch}}
    clean = hook(event)
    assert clean.returncode == 0 and not clean.stdout and not clean.stderr, clean

    page.write_text('<script type="application/ld+json">{broken}</script>')
    warning = hook(event)
    assert warning.returncode == 0, warning.stderr
    context = json.loads(warning.stdout)["hookSpecificOutput"]
    assert context["hookEventName"] == "PostToolUse" and "Invalid JSON" in context["additionalContext"]
    actual_event = {**event, "tool_name": "apply_patch", "tool_input": {"command": patch}}
    actual_warning = hook(actual_event)
    assert actual_warning.returncode == 0, actual_warning.stderr
    assert "Invalid JSON" in json.loads(actual_warning.stdout)["hookSpecificOutput"]["additionalContext"]

    page.write_text('<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Organization", "name": "[Business Name]",
    }) + '</script>')
    critical = hook(event)
    assert critical.returncode == 2 and "placeholder" in critical.stderr.lower(), critical
    ignored = hook({**event, "tool_name": "Read", "tool_input": {"file_path": str(page)}})
    assert ignored.returncode == 0 and not ignored.stdout and not ignored.stderr
    event["tool_name"] = "Write"
    event["tool_input"] = {"file_path": str(page)}
    assert hook(event).returncode == 2

    # A second preserved SEO helper detects templated metadata without a model,
    # crawl, browser, API key, or dependency installation.
    title = "Professional bicycle maintenance services"
    metadata = successful_json(call(
        "scripts/metadata_template.py", "--title", title,
        "--description", title + ". Try it free now.", "--json", env=env,
    ))
    assert metadata["templated_count"] == 1, metadata
    budget = successful_json(call(
        "scripts/dataforseo_costs.py", "check", "serp_organic_live_advanced", "--count", "10000", env=env,
    ))
    assert budget["status"] == "blocked" and budget["reason"] == "daily_limit_exceeded", budget
    unknown = successful_json(call("scripts/dataforseo_costs.py", "check", "unknown_test_endpoint", env=env))
    assert unknown["status"] == "needs_approval", unknown

manifest = json.loads((PLUGIN / "hooks/hooks.json").read_text())
handler = manifest["hooks"]["PostToolUse"][0]["hooks"][0]
assert "codex-schema.py" in handler["command"] and "args" not in handler
for skill in (PLUGIN / "skills").glob("*/SKILL.md"):
    body = skill.parent / "WORKFLOW.md"
    text = (body if body.is_file() else skill).read_text()
    assert "CLAUDE_PLUGIN_ROOT" not in text and "$ARGUMENTS" not in text, skill
    assert "./extensions/" not in text, skill
assert not (PLUGIN / "extensions/banana/scripts/setup_mcp.py").exists()
print(json.dumps({"status": "passed", "layer": "offline-behavior", "checks": [
    "26 skills and 19 role resources", "MIT and FLOW attribution", "non-mutating runtime doctor",
    "profile JSON-LD generation", "Codex patch and Write hook dispatch", "schema diagnostic feedback",
    "read events ignored", "templated metadata detection", "API budget safeguards",
], "not_exercised": ["live SEO crawling", "browser setup", "API authentication", "paid MCP calls"]}))
