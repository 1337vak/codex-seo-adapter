---
name: seo-agentic
description: >
  Audit and fix agent readiness: the Lighthouse Agentic Browsing fraction,
  accessibility tree for agents, robots.txt and Content-Signal for AI agents,
  WAF treatment of agent traffic, llms.txt, Markdown delivery, ai-catalog.json,
  /.well-known discovery files, and WebMCP tools. Use when the user asks
  whether AI agents can use or browse the site, or about llms.txt or WebMCP.
  Exclude AI citability and brand signals (seo-geo) and commerce protocol
  depth (seo-ecommerce).
user-invocable: true
argument-hint: "[audit|fix|lighthouse|refresh] [url]"
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.6.0"
  category: seo
---

Read [Codex compatibility](../../COMPATIBILITY.md) before following this workflow.

Read [the SEO Codex contract](../../CODEX-COMPATIBILITY.md). Resolve PLUGIN_ROOT to this installed plugin before running bundled commands. Use native capabilities within the actual host limits; source role/model/tool metadata is advisory. Do not run Claude extension installers.

Read [the complete workflow](WORKFLOW.md) and only the supporting references relevant to this request.
