# Codex SEO Adapter

An unofficial Codex adaptation of [Claude SEO by AgriciDaniel](https://github.com/AgriciDaniel/claude-seo), pinned to upstream commit [`734998e5fdbb16cd96dbaafe2da24eee6fb0d291`](https://github.com/AgriciDaniel/claude-seo/tree/734998e5fdbb16cd96dbaafe2da24eee6fb0d291) (version 2.6.0). The upstream author supplies the SEO expertise and tools; this repository maintains the adapter recipe, a Codex event bridge, tests, and release automation.

The generated plugin includes 26 SEO skills, supporting references and templates, 19 specialist briefs loaded as needed, and the upstream Python tools. Workflows cover technical SEO, content and E-E-A-T, structured data, sitemaps, AI search, local SEO, commerce, international SEO, and planning. Live-data and image-generation workflows retain their separate credentials and MCP prerequisites.

## Install

Register the generated release branch, then install its plugin:

```sh
codex plugin marketplace add 1337vak/codex-seo-adapter --ref release
codex plugin add codex-seo@codex-seo-adapter
```

Start a new Codex session. Invoke `$codex-seo:seo` with a command, or invoke a specific skill:

```text
Use $codex-seo:seo-schema to review the JSON-LD in this local HTML file.
Use $codex-seo:seo-content to assess this page and prioritize improvements.
Use $codex-seo:seo to plan an evidence-led technical audit of https://example.com.
```

The GitHub marketplace release contains a schema quality hook. Review and trust the installed hook in Codex's `/hooks` interface before expecting automatic checks. Its diagnostics run after edits; they do not undo a write.

## Runtime and optional services

The hook and several deterministic helpers use Python's standard library. Broader analysis, crawling, browser rendering, and reports require the upstream isolated runtime. Resolve the absolute installed plugin directory as `PLUGIN_ROOT`, then diagnose it:

```sh
"${PLUGIN_ROOT}/scripts/claude-seo" doctor --json
```

When you choose to install the runtime, run:

```sh
"${PLUGIN_ROOT}/scripts/claude-seo" setup
```

The upstream launcher name and `CLAUDE_SEO_*` application override variables remain for compatibility. Default runtime, configuration, and cache paths are adapted to Codex SEO; existing Claude configuration is not migrated. Dependencies use the upstream bounded requirements rather than a complete dependency lock. Python 3.11–3.14 is supported by the pinned runtime; Chromium availability is reported separately.

Google, backlinks, Matomo, DataForSEO, and image generation need their relevant credentials or connected MCP tools. Configure those through Codex and the service's supported setup. The Claude extension installers are omitted. Additional optional extensions beyond the two bundled skill mirrors need separate Codex adaptation. No paid calls are made during adapter verification.

## Rebuild and verify

```sh
python3 scripts/port.py build
python3 scripts/port.py verify
```

The bootstrap fetches the exact converter/tool revisions in [port.json](port.json). The build fetches the exact upstream commit, transforms instructions, preserves resource bytes and executable modes, applies reviewed patches, and creates a self-contained plugin under `build/plugin/`. Long instruction bodies are loaded from adjacent workflow files. Generated upstream code is not maintained on the source branch.

Verification covers package integrity and offline behavior: schema generation, Codex-shaped edit events, malformed/placeholder JSON-LD feedback, templated-metadata detection, cost safeguards, and non-mutating runtime diagnosis. Native installation/discovery and runtime testing are reported separately by the shared tool. Successful offline tests do not establish live API access, browser readiness, or identical model behavior.

The native hook fixture drives an actual Codex `apply_patch` call through a deterministic loopback responder, then checks that the installed schema hook returns `Invalid JSON` as model-visible feedback. It uses a temporary profile and a one-invocation hook-trust bypass for the reviewed fixture; it does not call a hosted model or change persistent user trust. This verifies native event dispatch, while model judgment remains untested.

The release workflow publishes the generated installable tree to the `release` branch. For a release, rebuild, verify, review compatibility changes and provenance, then use the repository release workflow. Public OpenAI directory submission is a separate process; its package must omit lifecycle hooks and document manual schema validation.

## Attribution and licenses

- **Origin:** [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo), Copyright (c) 2026 agricidaniel, MIT. Generated artifacts retain the upstream license and per-skill notices.
- **FLOW prompt library:** [AgriciDaniel/flow](https://github.com/AgriciDaniel/flow), CC BY 4.0. Its attribution headers, prompt index, and revision lock are retained within `skills/seo-flow/references/`.
- **Conversion:** the reviewed, pinned [Compound Engineering converter](https://github.com/EveryInc/compound-engineering-plugin) performs the format conversion; [claude-to-codex-plugin-port](https://github.com/1337vak/claude-to-codex-plugin-port) supplies the shared build and distribution flow.

This is an independent adaptation, not affiliated with the upstream author or OpenAI. Upstream SEO guidance is a pinned snapshot; verify time-sensitive recommendations against current primary sources.
